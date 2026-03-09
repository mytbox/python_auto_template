"""
Android 手势操作步骤定义
提供 Android App 手势操作的步骤,包括滑动、长按、拖拽等
"""
import logging
from behave import when
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import allure

logger = logging.getLogger(__name__)


@when('从坐标({start_x},{start_y})滑动到坐标({end_x},{end_y}),持续{duration}毫秒')
def swipe_by_coordinates(context, start_x: str, start_y: str, end_x: str, end_y: str, duration: str):
    """从坐标滑动到坐标"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        start_x = int(start_x)
        start_y = int(start_y)
        end_x = int(end_x)
        end_y = int(end_y)
        duration = int(duration)

        driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.info(f"从 ({start_x},{start_y}) 滑动到 ({end_x},{end_y}), 持续 {duration}ms")

        with allure.step(f"滑动 ({start_x},{start_y}) -> ({end_x},{end_y})"):
            allure.attach(
                f"起点: ({start_x}, {start_y})\n终点: ({end_x}, {end_y})\n持续时间: {duration}ms",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"滑动失败: {e}")
        raise


@when('从元素滑动到元素,起始元素定位方式为"{start_by}"值为"{start_value}",目标元素定位方式为"{end_by}"值为"{end_value}"')
def swipe_element_to_element(context, start_by: str, start_value: str, end_by: str, end_value: str):
    """从一个元素滑动到另一个元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        start_locator = _parse_locator(start_by, start_value)
        end_locator = _parse_locator(end_by, end_value)

        start_element = context.appium_manager.wait_for_element_visible(*start_locator)
        end_element = context.appium_manager.wait_for_element_visible(*end_locator)

        start_location = start_element.location
        end_location = end_element.location

        start_size = start_element.size
        end_size = end_element.size

        start_x = start_location['x'] + start_size['width'] / 2
        start_y = start_location['y'] + start_size['height'] / 2
        end_x = end_location['x'] + end_size['width'] / 2
        end_y = end_location['y'] + end_size['height'] / 2

        driver.swipe(start_x, start_y, end_x, end_y, 1000)
        logger.info(f"从元素滑动到元素: ({start_x},{start_y}) -> ({end_x},{end_y})")

        with allure.step(f"从元素滑动到元素"):
            allure.attach(
                f"起始元素: {start_by}={start_value}\n目标元素: {end_by}={end_value}",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"从元素滑动到元素失败: {e}")
        raise


@when('向左滑动')
def swipe_left(context):
    """向左滑动"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        start_x = width * 0.8
        end_x = width * 0.2
        y = height * 0.5

        driver.swipe(start_x, y, end_x, y, 1000)
        logger.info("向左滑动")

        with allure.step("向左滑动"):
            allure.attach(
                f"起点: ({start_x}, {y})\n终点: ({end_x}, {y})",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"向左滑动失败: {e}")
        raise


@when('向右滑动')
def swipe_right(context):
    """向右滑动"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        start_x = width * 0.2
        end_x = width * 0.8
        y = height * 0.5

        driver.swipe(start_x, y, end_x, y, 1000)
        logger.info("向右滑动")

        with allure.step("向右滑动"):
            allure.attach(
                f"起点: ({start_x}, {y})\n终点: ({end_x}, {y})",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"向右滑动失败: {e}")
        raise


@when('向上滑动')
def swipe_up(context):
    """向上滑动"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        x = width * 0.5
        start_y = height * 0.8
        end_y = height * 0.2

        driver.swipe(x, start_y, x, end_y, 1000)
        logger.info("向上滑动")

        with allure.step("向上滑动"):
            allure.attach(
                f"起点: ({x}, {start_y})\n终点: ({x}, {end_y})",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"向上滑动失败: {e}")
        raise


@when('向下滑动')
def swipe_down(context):
    """向下滑动"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        size = driver.get_window_size()
        width = size['width']
        height = size['height']

        x = width * 0.5
        start_y = height * 0.2
        end_y = height * 0.8

        driver.swipe(x, start_y, x, end_y, 1000)
        logger.info("向下滑动")

        with allure.step("向下滑动"):
            allure.attach(
                f"起点: ({x}, {start_y})\n终点: ({x}, {end_y})",
                name="滑动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"向下滑动失败: {e}")
        raise


@when('长按元素,定位方式为"{by}"值为"{value}",持续{duration}毫秒')
def long_press_element(context, by: str, value: str, duration: str):
    """长按元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to(element)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(int(duration) / 1000)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

        logger.info(f"长按元素: {by}={value}, 持续 {duration}ms")

        with allure.step(f"长按元素 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}\n持续时间: {duration}ms",
                name="长按信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"长按元素失败: {e}")
        raise


@when('拖拽元素,起始元素定位方式为"{start_by}"值为"{start_value}",目标元素定位方式为"{end_by}"值为"{end_value}"')
def drag_element_to_element(context, start_by: str, start_value: str, end_by: str, end_value: str):
    """拖拽元素到另一个元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        start_locator = _parse_locator(start_by, start_value)
        end_locator = _parse_locator(end_by, end_value)

        start_element = context.appium_manager.wait_for_element_visible(*start_locator)
        end_element = context.appium_manager.wait_for_element_visible(*end_locator)

        driver.drag_and_drop(start_element, end_element)
        logger.info(f"拖拽元素: {start_by}={start_value} -> {end_by}={end_value}")

        with allure.step(f"拖拽元素"):
            allure.attach(
                f"起始元素: {start_by}={start_value}\n目标元素: {end_by}={end_value}",
                name="拖拽信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"拖拽元素失败: {e}")
        raise


@when('双击元素,定位方式为"{by}"值为"{value}"')
def double_click_element(context, by: str, value: str):
    """双击元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)

        actions = ActionChains(driver)
        actions.double_click(element)
        actions.perform()

        logger.info(f"双击元素: {by}={value}")

        with allure.step(f"双击元素 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}",
                name="双击信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"双击元素失败: {e}")
        raise


@when('滚动到元素,定位方式为"{by}"值为"{value}"')
def scroll_to_element(context, by: str, value: str):
    """滚动到元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver

        if by.lower() == 'android_uiautomator':
            element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiScrollable(new UiSelector()).scrollIntoView({value})')
            logger.info(f"滚动到元素: {by}={value}")
        else:
            locator = _parse_locator(by, value)
            element = context.appium_manager.wait_for_element_visible(*locator)
            logger.info(f"元素已可见: {by}={value}")

        with allure.step(f"滚动到元素 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}",
                name="滚动信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"滚动到元素失败: {e}")
        raise


@when('缩放元素,定位方式为"{by}"值为"{value}",缩放比例为{scale}')
def zoom_element(context, by: str, value: str, scale: str):
    """缩放元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        driver = context.appium_manager.driver
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)

        size = driver.get_window_size()
        x = size['width'] / 2
        y = size['height'] / 2

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))

        if float(scale) > 1:
            actions.w3c_actions.pointer_action.move_to_location(x - 100, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(x - 200, y)
            actions.w3c_actions.pointer_action.pointer_up()

            actions.w3c_actions.pointer_action.move_to_location(x + 100, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(x + 200, y)
            actions.w3c_actions.pointer_action.pointer_up()
        else:
            actions.w3c_actions.pointer_action.move_to_location(x - 200, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(x - 100, y)
            actions.w3c_actions.pointer_action.pointer_up()

            actions.w3c_actions.pointer_action.move_to_location(x + 200, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(x + 100, y)
            actions.w3c_actions.pointer_action.pointer_up()

        actions.perform()
        logger.info(f"缩放元素: {by}={value}, 比例: {scale}")

        with allure.step(f"缩放元素 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}\n缩放比例: {scale}",
                name="缩放信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"缩放元素失败: {e}")
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
