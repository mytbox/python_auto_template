#!/usr/bin/env python3
"""
Android模拟器集群管理工具
用于启动、停止和管理多个模拟器实例
"""
import os
import sys
import time
import subprocess
import signal
import argparse
from typing import List, Dict, Any
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmulatorCluster:
    """模拟器集群管理器"""

    def __init__(self, config_file: str = None):
        """
        初始化模拟器集群

        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'android_cluster_capabilities.json'
        )
        self.emulator_processes = {}
        self.android_sdk_root = os.environ.get('ANDROID_HOME', '')
        self.emulator_cmd = os.path.join(self.android_sdk_root, 'emulator', 'emulator.exe')
        self.adb_cmd = os.path.join(self.android_sdk_root, 'platform-tools', 'adb.exe')

    def start_emulators(self, count: int = 5):
        """
        启动指定数量的模拟器

        Args:
            count: 要启动的模拟器数量
        """
        logger.info(f"准备启动 {count} 个模拟器实例")

        for i in range(count):
            avd_name = f"test_emulator_{i+1}"
            port = 5554 + (i * 2)
            
            # 检查AVD是否存在
            if not self._avd_exists(avd_name):
                logger.warning(f"AVD {avd_name} 不存在，跳过启动")
                continue

            # 启动模拟器
            cmd = [
                self.emulator_cmd,
                '-avd', avd_name,
                '-port', str(port),
                '-no-window',
                '-no-boot-anim',
                '-no-audio',
                '-gpu', 'host'
            ]

            try:
                logger.info(f"启动模拟器 {avd_name} 在端口 {port}")
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )
                self.emulator_processes[avd_name] = process
                time.sleep(5)  # 等待模拟器启动
            except Exception as e:
                logger.error(f"启动模拟器 {avd_name} 失败: {e}")

        # 等待所有模拟器完全启动
        self._wait_for_emulators_ready(count)

    def stop_emulators(self):
        """停止所有模拟器"""
        logger.info("停止所有模拟器实例")
        
        for avd_name, process in self.emulator_processes.items():
            try:
                if process.poll() is None:  # 进程仍在运行
                    logger.info(f"停止模拟器 {avd_name}")
                    process.terminate()
                    process.wait(timeout=10)
            except Exception as e:
                logger.error(f"停止模拟器 {avd_name} 时出错: {e}")

        self.emulator_processes.clear()

        # 强制停止所有模拟器
        try:
            subprocess.run([self.adb_cmd, 'kill-server'], check=True)
            time.sleep(2)
            subprocess.run([self.adb_cmd, 'start-server'], check=True)
        except Exception as e:
            logger.error(f"重启ADB服务时出错: {e}")

    def get_running_emulators(self) -> List[str]:
        """获取正在运行的模拟器列表"""
        try:
            result = subprocess.run(
                [self.adb_cmd, 'devices'],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split('\n')[1:]  # 跳过第一行标题
            emulators = []
            
            for line in lines:
                if line.strip() and 'emulator-' in line:
                    parts = line.split('\t')
                    if len(parts) >= 2 and parts[1] == 'device':
                        emulators.append(parts[0])
            
            return emulators
        except Exception as e:
            logger.error(f"获取运行中的模拟器列表失败: {e}")
            return []

    def _avd_exists(self, avd_name: str) -> bool:
        """检查AVD是否存在"""
        try:
            result = subprocess.run(
                ['emulator', '-list-avds'],
                capture_output=True,
                text=True,
                check=True
            )
            return avd_name in result.stdout.split()
        except Exception as e:
            logger.error(f"检查AVD {avd_name} 是否存在时出错: {e}")
            return False

    def _wait_for_emulators_ready(self, expected_count: int, timeout: int = 300):
        """
        等待模拟器完全启动

        Args:
            expected_count: 期望的模拟器数量
            timeout: 超时时间(秒)
        """
        logger.info(f"等待 {expected_count} 个模拟器完全启动...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            running_emulators = self.get_running_emulators()
            if len(running_emulators) >= expected_count:
                logger.info(f"所有模拟器已启动: {running_emulators}")
                return True
            
            logger.info(f"已启动 {len(running_emulators)}/{expected_count} 个模拟器，继续等待...")
            time.sleep(10)
        
        logger.warning(f"等待模拟器启动超时，当前已启动: {self.get_running_emulators()}")
        return False

    def create_avds(self, count: int = 5):
        """
        创建指定数量的AVD

        Args:
            count: 要创建的AVD数量
        """
        logger.info(f"准备创建 {count} 个AVD")
        
        system_image = "system-images;android-31;google_apis;x86_64"
        device = "pixel_4"
        
        for i in range(count):
            avd_name = f"test_emulator_{i+1}"
            
            cmd = [
                'avdmanager',
                'create', 'avd',
                '-n', avd_name,
                '-k', system_image,
                '-d', device,
                '--force'
            ]
            
            try:
                logger.info(f"创建AVD: {avd_name}")
                subprocess.run(cmd, check=True, input='no\n', text=True)
            except Exception as e:
                logger.error(f"创建AVD {avd_name} 失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Android模拟器集群管理工具')
    parser.add_argument(
        'action',
        choices=['start', 'stop', 'status', 'create'],
        help='要执行的操作'
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        default=5,
        help='模拟器数量，默认为5'
    )
    
    args = parser.parse_args()
    
    cluster = EmulatorCluster()
    
    if args.action == 'start':
        cluster.start_emulators(args.count)
    elif args.action == 'stop':
        cluster.stop_emulators()
    elif args.action == 'status':
        emulators = cluster.get_running_emulators()
        print(f"运行中的模拟器: {emulators}")
        print(f"总数: {len(emulators)}")
    elif args.action == 'create':
        cluster.create_avds(args.count)


if __name__ == '__main__':
    main()