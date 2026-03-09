"""
导航步骤定义
包含页面导航、前进后退等操作
"""

from behave import when, then
from loguru import logger


@when('点击浏览器后退按钮')
def click_browser_back(context):
    """点击浏览器后退按钮"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("点击浏览器后退按钮")
    context.page.go_back()


@when('点击浏览器前进按钮')
def click_browser_forward(context):
    """点击浏览器前进按钮"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("点击浏览器前进按钮")
    context.page.go_forward()


@when('刷新当前页面')
def refresh_page(context):
    """刷新当前页面"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("刷新当前页面")
    context.page.reload()


@when('滚动到页面顶部')
def scroll_to_top(context):
    """滚动到页面顶部"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("滚动到页面顶部")
    context.page.evaluate("window.scrollTo(0, 0)")


@when('滚动到页面底部')
def scroll_to_bottom(context):
    """滚动到页面底部"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("滚动到页面底部")
    context.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")


@when('向下滚动 {pixels:d} 像素')
def scroll_down_pixels(context, pixels):
    """向下滚动指定像素"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info(f"向下滚动 {pixels} 像素")
    context.page.evaluate(f"window.scrollBy(0, {pixels})")


@when('向上滚动 {pixels:d} 像素')
def scroll_up_pixels(context, pixels):
    """向上滚动指定像素"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info(f"向上滚动 {pixels} 像素")
    context.page.evaluate(f"window.scrollBy(0, -{pixels})")


@when('向右滚动 {pixels:d} 像素')
def scroll_right_pixels(context, pixels):
    """向右滚动指定像素"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info(f"向右滚动 {pixels} 像素")
    context.page.evaluate(f"window.scrollBy({pixels}, 0)")


@when('向左滚动 {pixels:d} 像素')
def scroll_left_pixels(context, pixels):
    """向左滚动指定像素"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info(f"向左滚动 {pixels} 像素")
    context.page.evaluate(f"window.scrollBy(-{pixels}, 0)")


@when('打开新标签页并导航到 "{url}"')
def open_new_tab_and_navigate(context, url):
    """打开新标签页并导航到指定 URL"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    logger.info(f"打开新标签页并导航到: {url}")
    
    # 创建新的页面
    new_page = context.playwright_manager.context.new_page()
    
    # 导航到指定 URL
    base_url = context.playwright_manager.config.get("test", {}).get("base_url", "")
    if url.startswith("/"):
        full_url = base_url + url
    else:
        full_url = url
    
    new_page.goto(full_url)
    
    # 保存新页面引用
    if not hasattr(context, 'additional_pages'):
        context.additional_pages = []
    context.additional_pages.append(new_page)


@when('切换到第 {tab_index:d} 个标签页')
def switch_to_tab(context, tab_index):
    """切换到指定索引的标签页"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info(f"切换到第 {tab_index} 个标签页")
    
    # 获取所有页面
    all_pages = context.playwright_manager.context.pages
    
    # 索引从 0 开始，所以减 1
    actual_index = tab_index - 1
    
    if 0 <= actual_index < len(all_pages):
        context.page = all_pages[actual_index]
        context.page.bring_to_front()
    else:
        raise IndexError(f"标签页索引超出范围: {tab_index}")


@when('关闭当前标签页')
def close_current_tab(context):
    """关闭当前标签页"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("关闭当前标签页")
    
    # 关闭当前页面
    context.page.close()
    
    # 切换到第一个可用的页面
    all_pages = context.playwright_manager.context.pages
    if all_pages:
        context.page = all_pages[0]
        context.page.bring_to_front()
    else:
        context.page = None


@then('检查当前 URL 为 "{expected_url}"')
def check_current_url(context, expected_url):
    """检查当前 URL 是否为期望值"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    current_url = context.page.url
    logger.info(f"当前 URL: {current_url}")
    
    # 处理相对 URL
    if expected_url.startswith("/"):
        base_url = context.playwright_manager.config.get("test", {}).get("base_url", "")
        expected_url = base_url + expected_url
    
    assert current_url == expected_url, f"URL 不匹配，期望: {expected_url}, 实际: {current_url}"


@then('检查当前 URL 包含 "{expected_path}"')
def check_url_contains(context, expected_path):
    """检查当前 URL 是否包含指定路径"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    current_url = context.page.url
    logger.info(f"当前 URL: {current_url}")
    assert expected_path in current_url, f"URL 不包含期望路径，期望包含: {expected_path}, 实际 URL: {current_url}"


@then('等待页面加载完成')
def wait_for_page_load(context):
    """等待页面加载完成"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    logger.info("等待页面加载完成")
    
    # 等待页面加载状态为 complete
    context.page.wait_for_load_state("networkidle")


@then('等待 {page_name} 页面的 {element_name} 元素加载完成')
def wait_for_element_load(context, page_name, element_name):
    """等待指定元素加载完成"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    logger.info(f"等待元素加载完成: {page_name}.{element_name} ({locator})")
    
    context.playwright_manager.wait_for_element(locator)