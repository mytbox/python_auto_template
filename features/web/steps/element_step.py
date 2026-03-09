"""
元素操作步骤定义
包含点击、输入、检查等元素操作
"""

from behave import when, then
from loguru import logger


@when('导航到 "{url}"')
def navigate_to_url(context, url):
    """导航到指定 URL"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    context.playwright_manager.navigate_to(url)


@when('点击 {page_name} 页面的 {element_name} 元素')
def click_element(context, page_name, element_name):
    """点击指定页面的元素"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"点击元素: {page_name}.{element_name} ({locator})")
    
    context.page.click(locator)


@when('双击 {page_name} 页面的 {element_name} 元素')
def double_click_element(context, page_name, element_name):
    """双击指定页面的元素"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"双击元素: {page_name}.{element_name} ({locator})")
    
    context.page.dblclick(locator)


@when('在 {page_name} 页面的 {element_name} 元素中输入 "{text}"')
def input_text(context, page_name, element_name, text):
    """在指定元素中输入文本"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"在元素中输入文本: {page_name}.{element_name} ({locator}) = {text}")
    
    # 先清空再输入
    context.page.fill(locator, text)


@when('在 {page_name} 页面的 {element_name} 元素中追加 "{text}"')
def append_text(context, page_name, element_name, text):
    """在指定元素中追加文本"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"在元素中追加文本: {page_name}.{element_name} ({locator}) += {text}")
    
    context.page.fill(locator, text, append=True)


@when('清空 {page_name} 页面的 {element_name} 元素')
def clear_element(context, page_name, element_name):
    """清空指定元素的内容"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"清空元素内容: {page_name}.{element_name} ({locator})")
    
    context.page.fill(locator, "")


@when('选择 {page_name} 页面的 {element_name} 元素中的选项 "{option}"')
def select_option(context, page_name, element_name, option):
    """在下拉框中选择指定选项"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"选择选项: {page_name}.{element_name} ({locator}) = {option}")
    
    context.page.select_option(locator, option)


@when('悬停在 {page_name} 页面的 {element_name} 元素上')
def hover_over_element(context, page_name, element_name):
    """悬停在指定元素上"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"悬停在元素上: {page_name}.{element_name} ({locator})")
    
    context.page.hover(locator)


@when('滚动到 {page_name} 页面的 {element_name} 元素')
def scroll_to_element(context, page_name, element_name):
    """滚动到指定元素"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"滚动到元素: {page_name}.{element_name} ({locator})")
    
    context.page.scroll_into_viewIfNeeded(locator)


@then('检查 {page_name} 页面的 {element_name} 元素存在')
def check_element_exists(context, page_name, element_name):
    """检查元素是否存在"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素存在: {page_name}.{element_name} ({locator})")
    
    element = context.playwright_manager.wait_for_element(locator)
    assert element is not None, f"元素不存在: {page_name}.{element_name}"


@then('检查 {page_name} 页面的 {element_name} 元素可见')
def check_element_visible(context, page_name, element_name):
    """检查元素是否可见"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素可见: {page_name}.{element_name} ({locator})")
    
    is_visible = context.playwright_manager.is_element_visible(locator)
    assert is_visible, f"元素不可见: {page_name}.{element_name}"


@then('检查 {page_name} 页面的 {element_name} 元素不可见')
def check_element_not_visible(context, page_name, element_name):
    """检查元素是否不可见"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素不可见: {page_name}.{element_name} ({locator})")
    
    is_visible = context.playwright_manager.is_element_visible(locator)
    assert not is_visible, f"元素仍然可见: {page_name}.{element_name}"


@then('检查 {page_name} 页面的 {element_name} 元素文本为 "{expected_text}"')
def check_element_text(context, page_name, element_name, expected_text):
    """检查元素文本是否为期望值"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素文本: {page_name}.{element_name} ({locator}) = {expected_text}")
    
    actual_text = context.page.text_content(locator).strip()
    assert actual_text == expected_text, f"元素文本不匹配，期望: {expected_text}, 实际: {actual_text}"


@then('检查 {page_name} 页面的 {element_name} 元素包含文本 "{expected_text}"')
def check_element_contains_text(context, page_name, element_name, expected_text):
    """检查元素是否包含指定文本"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素包含文本: {page_name}.{element_name} ({locator}) 包含 {expected_text}")
    
    actual_text = context.page.text_content(locator).strip()
    assert expected_text in actual_text, f"元素不包含期望文本，期望包含: {expected_text}, 实际文本: {actual_text}"


@then('检查 {page_name} 页面的 {element_name} 元素被禁用')
def check_element_disabled(context, page_name, element_name):
    """检查元素是否被禁用"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素被禁用: {page_name}.{element_name} ({locator})")
    
    is_disabled = context.page.is_disabled(locator)
    assert is_disabled, f"元素未被禁用: {page_name}.{element_name}"


@then('检查 {page_name} 页面的 {element_name} 元素被启用')
def check_element_enabled(context, page_name, element_name):
    """检查元素是否被启用"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"检查元素被启用: {page_name}.{element_name} ({locator})")
    
    is_disabled = context.page.is_disabled(locator)
    assert not is_disabled, f"元素未被启用: {page_name}.{element_name}"