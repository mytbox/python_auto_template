"""
Android 元素操作步骤定义
提供 Android App 元素操作的步骤,包括点击、输入、获取文本等
"""
import logging
from behave import when, then
from appium.webdriver.common.appiumby import AppiumBy
import allure

logger = logging.getLogger(__name__)


@when('点击元素,定位方式为"{by}"值为"{value}"')
def click_element(context, by: str, value: str):
    """点击元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_clickable(*locator)
        element.click()
        logger.info(f"已点击元素: {by}={value}")

        with allure.step(f"点击元素 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}",
                name="元素信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"点击元素失败: {e}")
        raise


@when('点击元素"{element_name}"')
def click_element_by_name(context, element_name: str):
    """通过元素名称点击元素(从配置文件读取)"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _get_element_locator(context, element_name)
        element = context.appium_manager.wait_for_element_clickable(*locator)
        element.click()
        logger.info(f"已点击元素: {element_name}")

        with allure.step(f"点击元素 ({element_name})"):
            allure.attach(
                f"元素名称: {element_name}\n定位方式: {locator[0]}\n定位值: {locator[1]}",
                name="元素信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"点击元素失败: {e}")
        raise


@when('在元素中输入文本"{text}",定位方式为"{by}"值为"{value}"')
def input_text(context, text: str, by: str, value: str):
    """在元素中输入文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"已在元素中输入文本: {by}={value}, 文本: {text}")

        with allure.step(f"输入文本 ({by}={value})"):
            allure.attach(
                f"定位方式: {by}\n定位值: {value}\n输入文本: {text}",
                name="元素信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"输入文本失败: {e}")
        raise


@when('在元素"{element_name}"中输入文本"{text}"')
def input_text_by_name(context, element_name: str, text: str):
    """通过元素名称在元素中输入文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _get_element_locator(context, element_name)
        element = context.appium_manager.wait_for_element_visible(*locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"已在元素中输入文本: {element_name}, 文本: {text}")

        with allure.step(f"输入文本 ({element_name})"):
            allure.attach(
                f"元素名称: {element_name}\n输入文本: {text}",
                name="元素信息",
                attachment_type=allure.attachment_type.TEXT
            )

    except Exception as e:
        logger.error(f"输入文本失败: {e}")
        raise


@when('清空元素内容,定位方式为"{by}"值为"{value}"')
def clear_element(context, by: str, value: str):
    """清空元素内容"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        element.clear()
        logger.info(f"已清空元素内容: {by}={value}")

    except Exception as e:
        logger.error(f"清空元素内容失败: {e}")
        raise


@when('清空元素"{element_name}"的内容')
def clear_element_by_name(context, element_name: str):
    """通过元素名称清空元素内容"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _get_element_locator(context, element_name)
        element = context.appium_manager.wait_for_element_visible(*locator)
        element.clear()
        logger.info(f"已清空元素内容: {element_name}")

    except Exception as e:
        logger.error(f"清空元素内容失败: {e}")
        raise


@when('追加文本"{text}"到元素,定位方式为"{by}"值为"{value}"')
def append_text(context, text: str, by: str, value: str):
    """追加文本到元素"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        element.send_keys(text)
        logger.info(f"已追加文本到元素: {by}={value}, 文本: {text}")

    except Exception as e:
        logger.error(f"追加文本失败: {e}")
        raise


@then('获取元素文本,定位方式为"{by}"值为"{value}"')
def get_element_text(context, by: str, value: str):
    """获取元素文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        text = element.text
        logger.info(f"元素文本: {by}={value}, 文本: {text}")

        with allure.step(f"获取元素文本 ({by}={value})"):
            allure.attach(
                text,
                name="元素文本",
                attachment_type=allure.attachment_type.TEXT
            )

        return text

    except Exception as e:
        logger.error(f"获取元素文本失败: {e}")
        raise


@then('验证元素文本为"{expected_text}",定位方式为"{by}"值为"{value}"')
def verify_element_text(context, expected_text: str, by: str, value: str):
    """验证元素文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        actual_text = element.text
        logger.info(f"元素文本: {by}={value}, 期望: {expected_text}, 实际: {actual_text}")

        assert actual_text == expected_text, f"元素文本不匹配: 期望 '{expected_text}', 实际 '{actual_text}'"

    except Exception as e:
        logger.error(f"验证元素文本失败: {e}")
        raise


@then('验证元素文本包含"{expected_text}",定位方式为"{by}"值为"{value}"')
def verify_element_text_contains(context, expected_text: str, by: str, value: str):
    """验证元素文本包含指定文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        actual_text = element.text
        logger.info(f"元素文本: {by}={value}, 期望包含: {expected_text}, 实际: {actual_text}")

        assert expected_text in actual_text, f"元素文本不包含 '{expected_text}', 实际文本: '{actual_text}'"

    except Exception as e:
        logger.error(f"验证元素文本包含失败: {e}")
        raise


@then('验证元素"{element_name}"的文本为"{expected_text}"')
def verify_element_text_by_name(context, element_name: str, expected_text: str):
    """通过元素名称验证元素文本"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _get_element_locator(context, element_name)
        element = context.appium_manager.wait_for_element_visible(*locator)
        actual_text = element.text
        logger.info(f"元素文本: {element_name}, 期望: {expected_text}, 实际: {actual_text}")

        assert actual_text == expected_text, f"元素文本不匹配: 期望 '{expected_text}', 实际 '{actual_text}'"

    except Exception as e:
        logger.error(f"验证元素文本失败: {e}")
        raise


@then('验证元素属性"{attribute}"为"{expected_value}",定位方式为"{by}"值为"{value}"')
def verify_element_attribute(context, attribute: str, expected_value: str, by: str, value: str):
    """验证元素属性"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        actual_value = element.get_attribute(attribute)
        logger.info(f"元素属性: {by}={value}, 属性: {attribute}, 期望: {expected_value}, 实际: {actual_value}")

        assert actual_value == expected_value, f"元素属性不匹配: 属性 '{attribute}', 期望 '{expected_value}', 实际 '{actual_value}'"

    except Exception as e:
        logger.error(f"验证元素属性失败: {e}")
        raise


@then('验证元素启用,定位方式为"{by}"值为"{value}"')
def verify_element_enabled(context, by: str, value: str):
    """验证元素启用"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        is_enabled = element.is_enabled()
        logger.info(f"元素启用状态: {by}={value}, 结果: {is_enabled}")

        assert is_enabled, f"元素未启用: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素启用失败: {e}")
        raise


@then('验证元素禁用,定位方式为"{by}"值为"{value}"')
def verify_element_disabled(context, by: str, value: str):
    """验证元素禁用"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        is_enabled = element.is_enabled()
        logger.info(f"元素启用状态: {by}={value}, 结果: {is_enabled}")

        assert not is_enabled, f"元素应该禁用: {by}={value}"

    except Exception as e:
        logger.error(f"验证元素禁用失败: {e}")
        raise


@then('保存元素文本到上下文"{key}",定位方式为"{by}"值为"{value}"')
def save_element_text_to_context(context, key: str, by: str, value: str):
    """保存元素文本到上下文"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        text = element.text

        if not hasattr(context, 'scenario_context'):
            raise RuntimeError("场景上下文未初始化")

        context.scenario_context.step_data[key] = text
        logger.info(f"已保存元素文本到上下文: {key}={text}")

    except Exception as e:
        logger.error(f"保存元素文本到上下文失败: {e}")
        raise


@then('保存元素属性"{attribute}"到上下文"{key}",定位方式为"{by}"值为"{value}"')
def save_element_attribute_to_context(context, attribute: str, key: str, by: str, value: str):
    """保存元素属性到上下文"""
    if not hasattr(context, 'appium_manager') or not context.appium_manager.is_connected():
        raise RuntimeError("Appium 驱动未连接")

    try:
        locator = _parse_locator(by, value)
        element = context.appium_manager.wait_for_element_visible(*locator)
        attr_value = element.get_attribute(attribute)

        if not hasattr(context, 'scenario_context'):
            raise RuntimeError("场景上下文未初始化")

        context.scenario_context.step_data[key] = attr_value
        logger.info(f"已保存元素属性到上下文: {key}={attr_value}")

    except Exception as e:
        logger.error(f"保存元素属性到上下文失败: {e}")
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


def _get_element_locator(context, element_name: str) -> tuple:
    """
    从配置文件获取元素定位信息

    Args:
        context: Behave 上下文
        element_name: 元素名称

    Returns:
        (AppiumBy, value) 元组
    """
    import json
    import os

    if not hasattr(context, 'android_elements_config'):
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config',
            'android_elements.json'
        )

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                context.android_elements_config = json.load(f)
        except FileNotFoundError:
            logger.warning(f"元素配置文件不存在: {config_path}")
            context.android_elements_config = {}

    elements_config = context.android_elements_config

    for page_name, page_elements in elements_config.items():
        if element_name in page_elements:
            element_info = page_elements[element_name]
            locator_type = element_info.get('type', 'id')
            locator_value = element_info.get('value', element_info.get('id', ''))

            return _parse_locator(locator_type, locator_value)

    raise ValueError(f"未找到元素配置: {element_name}")
