#!/usr/bin/env python3.12
import os
import sys
import glob
import subprocess
import argparse
from multiprocessing import Pool
from pathlib import Path

# ===================== 配置项（可根据需要调整） =====================
# 并发进程数
PARALLEL_NUM = 5
# Behave执行参数基础模板（profile将从命令行传入）
BEHAVE_ARGS_BASE = [
    "-f", "allure_behave.formatter:AllureFormatter",
    "-o", "./allure-results"
]
# 全局Behave执行参数（将在parse_args中构建）
BEHAVE_ARGS = []
# Feature文件目录
FEATURE_DIR = "./features"
# Python解释器路径（和Jenkins中一致）
PYTHON_PATH = "/usr/local/bin/python3.12"
# Allure报告生成路径
ALLURE_RESULTS = "./allure-results"
ALLURE_REPORT = "./allure-report"
# Allure命令路径（和Jenkins中一致）
ALLURE_CMD = "/var/lib/jenkins/tools/ru.yandex.qatools.allure.jenkins.tools.AllureCommandlineInstallation/Allure/bin/allure"

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='并发执行 Behave BDD 测试')
    parser.add_argument(
        '-p', '--profile',
        type=str,
        default='local',
        help='Behave 配置环境 (dev/test/local)，默认: local'
    )
    parser.add_argument(
        '-n', '--parallel',
        type=int,
        default=PARALLEL_NUM,
        help=f'并发进程数，默认: {PARALLEL_NUM}'
    )
    return parser.parse_args()

def build_behave_args(profile):
    """构建Behave执行参数"""
    global BEHAVE_ARGS
    BEHAVE_ARGS = ["-D", f"profile={profile}"] + BEHAVE_ARGS_BASE
    return BEHAVE_ARGS

def init_worker(behave_args):
    """子进程初始化函数，设置全局变量"""
    global BEHAVE_ARGS
    BEHAVE_ARGS = behave_args

def clean_old_results():
    """清理旧的allure-results目录"""
    if Path(ALLURE_RESULTS).exists():
        import shutil
        shutil.rmtree(ALLURE_RESULTS)
    Path(ALLURE_RESULTS).mkdir(parents=True, exist_ok=True)
    print(f"✅ 已清理并重建目录: {ALLURE_RESULTS}")

def get_all_feature_files():
    """获取所有.feature文件的绝对路径"""
    feature_files = glob.glob(os.path.join(FEATURE_DIR, "**/*.feature"), recursive=True)
    # 转为绝对路径，避免进程执行时路径错误
    feature_files = [os.path.abspath(f) for f in feature_files]
    print(f"🔍 找到 {len(feature_files)} 个feature文件")
    return feature_files

def run_behave(feature_files):
    """单个进程执行behave的函数（核心）"""
    if not feature_files:
        print("⚠️  当前进程无需要执行的feature文件")
        return 0
    
    # 构造behave命令
    cmd = [
        PYTHON_PATH,
        "-m", "behave",
        *BEHAVE_ARGS,
        *feature_files
    ]
    
    try:
        print(f"🚀 进程 {os.getpid()} 开始执行: {feature_files}")
        # 执行命令并捕获输出
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        # 打印进程输出（便于调试）
        if result.stdout:
            print(f"📝 进程 {os.getpid()} 输出:\n{result.stdout}")
        if result.stderr:
            print(f"⚠️  进程 {os.getpid()} 错误输出:\n{result.stderr}")
        # 返回执行结果码
        return result.returncode
    except Exception as e:
        print(f"❌ 进程 {os.getpid()} 执行失败: {str(e)}")
        return 1

def split_files_for_processes(files, num_processes):
    """将文件列表平均拆分给多个进程"""
    split_files = []
    for i in range(num_processes):
        # 按索引拆分：第i个进程取 i, i+num_processes, i+2*num_processes... 位置的文件
        process_files = files[i::num_processes]
        split_files.append(process_files)
    return split_files

def generate_allure_report():
    """生成Allure报告"""
    if not Path(ALLURE_RESULTS).exists():
        print("❌ allure-results目录不存在，跳过报告生成")
        return 1
    
    cmd = [
        ALLURE_CMD,
        "generate",
        ALLURE_RESULTS,
        "-c",  # 清理旧报告
        "-o", ALLURE_REPORT
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Allure报告生成成功: {ALLURE_REPORT}")
        print(result.stdout)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Allure报告生成失败: {e.stderr}")
        return 1

def main():
    """主函数：控制整个并发执行流程"""
    # 解析命令行参数
    args = parse_args()
    profile = args.profile
    parallel_num = args.parallel

    # 构建Behave执行参数
    behave_args = build_behave_args(profile)
    print(f"📋 使用配置环境: {profile}")
    print(f"🔢 并发进程数: {parallel_num}")

    # 步骤1：清理旧结果
    clean_old_results()

    # 步骤2：获取所有feature文件
    feature_files = get_all_feature_files()
    if not feature_files:
        print("❌ 未找到任何feature文件，退出执行")
        sys.exit(1)

    # 步骤3：拆分文件到多个进程
    split_feature_files = split_files_for_processes(feature_files, parallel_num)

    # 步骤4：创建进程池并执行（使用initializer传递behave_args到子进程）
    print(f"\n🚀 启动 {parallel_num} 个进程并发执行...")
    with Pool(
        processes=parallel_num,
        initializer=init_worker,
        initargs=(behave_args,)
    ) as pool:
        # 异步执行所有进程
        results = pool.map(run_behave, split_feature_files)

    # 步骤5：检查执行结果
    failed_processes = [i for i, code in enumerate(results) if code != 0]
    if failed_processes:
        print(f"\n❌ 有 {len(failed_processes)} 个进程执行失败: {failed_processes}")
        exit_code = 1
    else:
        print("\n✅ 所有进程执行完成！")
        exit_code = 0

    # 步骤6：生成Allure报告（无论测试是否失败，都生成报告）
    generate_allure_report()

    # 退出脚本
    sys.exit(exit_code)

if __name__ == "__main__":
    # 修复多进程在Linux下的路径问题（避免AF_UNIX path too long）
    os.environ["TMPDIR"] = "/tmp/behave_parallel_temp"
    Path(os.environ["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    
    main()


# 添加了 argparse 命令行参数解析
# 添加了 -p/--profile 参数（默认：local）
# 添加了 -n/--parallel 参数（默认：5）
# 添加了 init_worker() 函数，将 behave_args 传递给子进程
# 使用 Pool(initializer=init_worker, initargs=(behave_args,)) 确保子进程正确获取参数
# 支持的配置环境：

# local - 本地环境（默认）
# dev - 开发环境
# test - 测试环境