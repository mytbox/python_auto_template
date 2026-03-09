"""
Behave 测试环境配置文件
用于在测试执行前后进行初始化和清理工作
"""
import sys
import io
import os
import json
import shutil
import logging
from datetime import datetime

# 修复 Windows 控制台中文乱码问题
if sys.platform == 'win32':
    # 设置控制台输出编码为 UTF-8
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from common.dto.scenario_context import ScenarioContext
from common.database.redis_manager import RedisManager
from config import init_behave_config, get_behave_config

# 创建模块级别的 logger
logger = logging.getLogger(__name__)


def setup_logger():
    """配置 logging 日志输出"""
    # 配置根日志记录器
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def before_all(context):
    """
    在所有测试开始前执行一次
    用于全局初始化
    """
    # 配置日志输出
    setup_logger()
    logger.info("初始化全局配置...")

    # 初始化Behave配置管理器
    config_manager = init_behave_config(context)

    # 从配置管理器获取Redis配置
    redis_config = config_manager.get_redis_config()
    logger.info(f"Redis配置: host={redis_config['host']}, port={redis_config['port']}, db={redis_config['db']}")

    try:
        context.redis_conn = RedisManager(**redis_config)
        logger.info("Redis 连接成功")
    except Exception as e:
        logger.error(f"Redis 连接失败: {e}")
        context.redis_conn = None

    # 检查是否为 Android 测试模式
    context.is_android_test = hasattr(context.config, 'userdata') and context.config.userdata.get('android_test') == 'true'
    if context.is_android_test:
        logger.info("检测到 Android 测试模式")
        try:
            from common.appium_manager import AppiumManager
            context.appium_manager = AppiumManager()
            logger.info("Appium 管理器初始化成功")
        except Exception as e:
            logger.error(f"Appium 管理器初始化失败: {e}")
            context.appium_manager = None
    
    # 检查是否为 Web 测试模式
    context.is_web_test = hasattr(context.config, 'userdata') and context.config.userdata.get('web_test') == 'true'
    if context.is_web_test:
        logger.info("检测到 Web 测试模式")
        try:
            from common.playwright_manager import PlaywrightManager
            context.playwright_manager = PlaywrightManager()
            logger.info("Playwright 管理器初始化成功")
        except Exception as e:
            logger.error(f"Playwright 管理器初始化失败: {e}")
            context.playwright_manager = None


def after_all(context):
    """
    在所有测试结束后执行一次
    用于全局清理
    """
    if hasattr(context, 'redis_conn') and context.redis_conn:
        try:
            context.redis_conn.close()
            logger.info("Redis 连接已关闭")
        except Exception as e:
            logger.error(f"关闭 Redis 连接时出错: {e}")

    # 关闭 Appium 驱动
    if hasattr(context, 'appium_manager') and context.appium_manager and context.appium_manager.is_connected():
        try:
            context.appium_manager.disconnect()
            logger.info("Appium 驱动已关闭")
        except Exception as e:
            logger.error(f"关闭 Appium 驱动时出错: {e}")
    
    # 关闭 Playwright 浏览器
    if hasattr(context, 'playwright_manager') and context.playwright_manager:
        try:
            context.playwright_manager.close_browser()
            logger.info("Playwright 浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭 Playwright 浏览器时出错: {e}")


def before_feature(context, _feature):
    """
    在每个特性文件开始前执行
    """
    pass


def after_feature(context, _feature):
    """
    在每个特性文件结束后执行
    """
    pass


def before_scenario(context, scenario):
    """
    在每个场景开始前执行
    """
    # 为每个场景创建新的场景上下文
    context.scenario_context = ScenarioContext()

    # 从Behave配置管理器获取基础URL
    config_manager = get_behave_config()
    base_url = config_manager.get_base_url()
    context.scenario_context.base_url = base_url


def after_scenario(context, scenario):
    """
    在每个场景结束后执行
    """
    # 保存批量检查结果到文件
    if hasattr(context, 'scenario_context') and hasattr(context.scenario_context, 'batch_check_results'):
        results = context.scenario_context.batch_check_results
        if results:
            _save_batch_check_results(context, scenario, results)

    # Android 测试失败时截图
    if scenario.status == 'failed' and hasattr(context, 'appium_manager') and context.appium_manager and context.appium_manager.is_connected():
        try:
            import os
            screenshot_dir = './screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"failed_{scenario.name.replace(' ', '_')}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, filename)
            context.appium_manager.take_screenshot(screenshot_path)
            logger.info(f"场景失败,截图已保存: {screenshot_path}")

            # 附加到 Allure 报告
            try:
                import allure
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"失败截图 - {scenario.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except ImportError:
                pass
        except Exception as e:
            logger.error(f"失败截图保存出错: {e}")
    
    # Web 测试失败时截图
    if scenario.status == 'failed' and hasattr(context, 'playwright_manager') and context.playwright_manager:
        try:
            import os
            screenshot_dir = './screenshots'
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"failed_{scenario.name.replace(' ', '_')}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, filename)
            context.playwright_manager.take_screenshot(filename)
            logger.info(f"场景失败,截图已保存: {screenshot_path}")

            # 附加到 Allure 报告
            try:
                import allure
                with open(screenshot_path, 'rb') as f:
                    allure.attach(
                        f.read(),
                        name=f"失败截图 - {scenario.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except ImportError:
                pass
        except Exception as e:
            logger.error(f"失败截图保存出错: {e}")

    # 清理场景相关的数据
    if hasattr(context, 'scenario_context'):
        pass


def _save_batch_check_results(context, scenario, results):
    """
    保存批量检查结果到 JSON 文件

    Args:
        context: Behave 上下文
        scenario: 当前场景
        results: 批量检查结果列表
    """
    now = datetime.now()

    # 创建按日期和时间分类的目录结构: .test_data/YYYY/MM/DD/HH/
    test_data_dir = os.path.join(os.getcwd(), ".test_data", now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"))
    os.makedirs(test_data_dir, exist_ok=True)

    # 文件名包含时分秒
    time_filename = now.strftime("%H%M%S")
    result_file = os.path.join(test_data_dir, f"batch_check_api_result_{time_filename}.json")

    # 构建汇总数据
    summary_data = {
        'timestamp': now.strftime("%Y-%m-%d %H:%M:%S"),
        'feature': context.feature.name if hasattr(context, 'feature') else 'Unknown',
        'scenario': scenario.name,
        'total_batch_checks': len(results),
        'batch_checks': results
    }

    # 保存检查结果
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)

    logger.info(f"批量检查结果已保存到: {result_file}")


def before_step(context, _step):
    """
    在每个步骤开始前执行
    """
    pass


def after_step(context, _step):
    """
    在每个步骤结束后执行
    """
    pass
