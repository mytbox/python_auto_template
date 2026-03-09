"""
Android 通用步骤定义
提供 Android App 测试的通用步骤,包括启动/关闭 App、截图、等待元素等
"""
import logging
import os
from datetime import datetime
from behave import given, when, then
from common.appium_manager import AppiumManager
from appium.webdriver.common.appiumby import AppiumBy
import allure

logger = logging.getLogger(__name__)


@given('启动 Android App')
def launch_android_app(context):
    """启动 Android App"""
    if not hasattr(context, 'appium_manager'):
        context.appium_manager = AppiumManager()

    try:
        context.appium_manager.connect()
        logger.info("Android App 启动成功")

        device_info = context.appium_manager.get_device_info()
        logger.info(f"设备信息: {device_info}")

        with allure.step("启动 Android App"):
            allure.attach(
                str(device_info),
                name="设备信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"启动 Android App 失败: {e}")
        raise


@given('启动 Android App 并使用设备"{device_name}"')
def launch_android_app_with_device(context, device_name: str):
    """使用指定设备启动 Android App"""
    if not hasattr(context, 'appium_manager'):
        context.appium_manager = AppiumManager()

    try:
        context.appium_manager.connect(device_name=device_name)
        logger.info(f"Android App 启动成功,使用设备: {device_name}")

        device_info = context.appium_manager.get_device_info()
        logger.info(f"设备信息: {device_info}")

        with allure.step(f"启动 Android App (设备: {device_name})"):
            allure.attach(
                str(device_info),
                name="设备信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"启动 Android App 失败: {e}")
        raise


@when('关闭 Android App')
def close_android_app(context):
    """关闭 Android App"""
    if hasattr(context, 'appium_manager') and context.appium_manager.is_connected():
        try:
            context.appium_manager.disconnect()
            logger.info("Android App 已关闭")
        except Exception as e:
            logger.error(f"关闭 Android App 时出错: {e}")
            raise


@when('重启 Android App')
def restart_android_app(context):
    """重启 Android App"""
    if hasattr(context, 'appium_manager'):
        try:
            context.appium_manager.disconnect()
            logger.info("Android App 已关闭")

            context.appium_manager.connect()
            logger.info("Android App 已重新启动")

        except Exception as e:
            logger.error(f"重启 Android App 失败: {e}")
            raise


@when('按返回键')
def press_back_key(context):
    """按返回键"""
    if hasattr(context, 'appium_manager') and context.appium_manager.is_connected():
        try:
            context.appium_manager.press_back()
            logger.info("已按返回键")
        except Exception as e:
            logger.error(f"按返回键失败: {e}")
            raise


@when('按 Home 键')
def press_home_key(context):
    """按 Home 键"""
    if hasattr(context, 'appium_manager') and context.appium_manager.is_connected():
        try:
            context.appium_manager.press_home()
            logger.info("已按 Home 键")
        except Exception as e:
            logger.error(f"按 Home 键失败: {e}")
            raise


@when('按 Enter 键')
def press_enter_key(context):
    """按 Enter 键"""
    if hasattr(context, 'appium_manager') and context.appium_manager.is_connected():
        try:
            context.appium_manager.press_enter()
            logger.info("已按 Enter 键")
        except Exception as e:
            logger.error(f"按 Enter 键失败: {e}")
            raise


@when('等待"{timeout}"秒')
def wait_seconds(context, timeout: str):
    """等待指定秒数"""
    import time
    wait_time = int(timeout)
    logger.info(f"等待 {wait_time} 秒")
    time.sleep(wait_time)


@when('等待元素出现,定位方式为"{by}"值为"{value}"')
def wait_for_element(context, by: str, value: str):
    """等待元素出现"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.find_element(*locator)
        logger.info(f"元素已出现: {by}={value}")
    except Exception as e:
        logger.error(f"等待元素失败: {e}")
        raise


@when('等待元素可见,定位方式为"{by}"值为"{value}"')
def wait_for_element_visible(context, by: str, value: str):
    """等待元素可见"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        logger.info(f"元素已可见: {by}={value}")
    except Exception as e:
        logger.error(f"等待元素可见失败: {e}")
        raise


@when('等待元素可点击,定位方式为"{by}"值为"{value}"')
def wait_for_element_clickable(context, by: str, value: str):
    """等待元素可点击"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_clickable(*locator)
        logger.info(f"元素已可点击: {by}={value}")
    except Exception as e:
        logger.error(f"等待元素可点击失败: {e}")
        raise


@when('截图')
def take_screenshot(context):
    """截图"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        screenshot_path = context.appium_manager.take_screenshot()
        logger.info(f"截图已保存: {screenshot_path}")

        with allure.step("截图"):
            allure.attach.file(
                screenshot_path,
                name="截图",
                attachment_type=allure.attachment_type.PNG
            )

    except Exception as e:
        logger.error(f"截图失败: {e}")
        raise


@when('截图并保存为"{filename}"')
def take_screenshot_with_name(context, filename: str):
    """截图并保存为指定文件名"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        screenshot_dir = context.appium_manager.config.get('screenshot', {}).get('directory', './screenshots')
        os.makedirs(screenshot_dir, exist_ok=True)

        if not filename.endswith('.png'):
            filename += '.png'

        screenshot_path = os.path.join(screenshot_dir, filename)
        context.appium_manager.take_screenshot(screenshot_path)
        logger.info(f"截图已保存: {screenshot_path}")

        with allure.step(f"截图 ({filename})"):
            allure.attach.file(
                screenshot_path,
                name=filename,
                attachment_type=allure.attachment_type.PNG
            )

    except Exception as e:
        logger.error(f"截图失败: {e}")
        raise


@then('验证当前 Activity 为"{activity}"')
def verify_current_activity(context, activity: str):
    """验证当前 Activity"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        current_activity = context.appium_manager.get_current_activity()
        logger.info(f"当前 Activity: {current_activity}, 期望: {activity}")

        assert current_activity == activity, f"当前 Activity 不匹配: 期望 {activity}, 实际 {current_activity}"

    except Exception as e:
        logger.error(f"验证当前 Activity 失败: {e}")
        raise


@then('验证当前包名为"{package}"')
def verify_current_package(context, package: str):
    """验证当前包名"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        current_package = context.appium_manager.get_current_package()
        logger.info(f"当前包名: {current_package}, 期望: {package}")

        assert current_package == package, f"当前包名不匹配: 期望 {package}, 实际 {current_package}"

    except Exception as e:
        logger.error(f"验证当前包名失败: {e}")
        raise


@then('验证元素存在,定位方式为"{by}"值为"{value}"')
def verify_element_exists(context, by: str, value: str):
    """验证元素存在"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        exists = context.appium_manager.is_element_present(*locator)
        logger.info(f"元素存在: {by}={value}, 结果: {exists}")

        assert exists, f"元素不存在: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素存在失败: {e}")
        raise


@then('验证元素不存在,定位方式为"{by}"值为"{value}"')
def verify_element_not_exists(context, by: str, value: str):
    """验证元素不存在"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        exists = context.appium_manager.is_element_present(*locator)
        logger.info(f"元素存在: {by}={value}, 结果: {exists}")

        assert not exists, f"元素不应该存在: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素不存在失败: {e}")
        raise


@then('验证元素可见,定位方式为"{by}"值为"{value}"')
def verify_element_visible(context, by: str, value: str):
    """验证元素可见"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        visible = context.appium_manager.is_element_visible(*locator)
        logger.info(f"元素可见: {by}={value}, 结果: {visible}")

        assert visible, f"元素不可见: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素可见失败: {e}")
        raise


@then('验证元素不可见,定位方式为"{by}"值为"{value}"')
def verify_element_not_visible(context, by: str, value: str):
    """验证元素不可见"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        visible = context.appium_manager.is_element_visible(*locator)
        logger.info(f"元素可见: {by}={value}, 结果: {visible}")

        assert not visible, f"元素不应该可见: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素不可见失败: {e}")
        raise


def _parse_locator(by: str, value: str) -> tuple:
    """
    解析定位方式

    Args:
        by: 定位方式字符串 (id, xpath, class_name, accessibility_id, android_uiautomator)
        value: 定位值

    Returns:
        (AppiumBy, value) 元组
    """
    locator_map = {
        'id': AppiumBy.ID,
        'xpath': AppiumBy.XPATH,
        'class_name': AppiumBy.CLASS_NAME,
        'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
        'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
    }

    by_lower = by.lower()
    if by_lower not in locator_map:
        raise ValueError(f"不支持的定位方式: {by}, 支持的定位方式: {list(locator_map.keys())}")

    return (locator_map[by_lower], value)
