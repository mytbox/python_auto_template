"""
Web 通用步骤定义
包含浏览器启动、关闭等通用操作
"""

from behave import given, then
from common.playwright_manager import PlaywrightManager
from loguru import logger


@given('启动浏览器')
def launch_browser(context):
    """启动浏览器"""
    # 检查是否为 Web 测试模式
    context.is_web_test = True
    logger.info("检测到 Web 测试模式")
    
    # 创建 Playwright 管理器
    context.playwright_manager = PlaywrightManager()
    
    # 启动浏览器
    context.page = context.playwright_manager.start_browser()
    logger.info("浏览器启动成功")


@given('启动 {browser_type} 浏览器')
def launch_specific_browser(context, browser_type):
    """启动指定类型的浏览器"""
    # 检查是否为 Web 测试模式
    context.is_web_test = True
    logger.info(f"检测到 Web 测试模式，使用 {browser_type} 浏览器")
    
    # 创建 Playwright 管理器
    context.playwright_manager = PlaywrightManager()
    
    # 启动指定浏览器
    context.page = context.playwright_manager.start_browser(browser_type=browser_type)
    logger.info(f"{browser_type} 浏览器启动成功")


@given('启动 {browser_type} 浏览器（有头模式）')
def launch_headful_browser(context, browser_type):
    """启动有头模式的浏览器"""
    # 检查是否为 Web 测试模式
    context.is_web_test = True
    logger.info(f"检测到 Web 测试模式，使用 {browser_type} 浏览器（有头模式）")
    
    # 创建 Playwright 管理器
    context.playwright_manager = PlaywrightManager()
    
    # 启动有头模式浏览器
    context.page = context.playwright_manager.start_browser(browser_type=browser_type, headless=False)
    logger.info(f"{browser_type} 浏览器启动成功（有头模式）")


@then('关闭浏览器')
def close_browser(context):
    """关闭浏览器"""
    if hasattr(context, 'playwright_manager') and context.playwright_manager:
        context.playwright_manager.close_browser()
        logger.info("浏览器已关闭")


@then('截取当前页面')
def take_screenshot(context):
    """截取当前页面"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        logger.error("Playwright 管理器未初始化，无法截图")
        return
    
    screenshot_path = context.playwright_manager.take_screenshot()
    logger.info(f"截图已保存: {screenshot_path}")


@then('截取当前页面并命名为 "{filename}"')
def take_screenshot_with_name(context, filename):
    """截取当前页面并指定文件名"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        logger.error("Playwright 管理器未初始化，无法截图")
        return
    
    screenshot_path = context.playwright_manager.take_screenshot(filename=f"{filename}.png")
    logger.info(f"截图已保存: {screenshot_path}")


@then('等待 {seconds:d} 秒')
def wait_seconds(context, seconds):
    """等待指定秒数"""
    import time
    logger.info(f"等待 {seconds} 秒")
    time.sleep(seconds)


@then('页面标题应为 "{expected_title}"')
def check_page_title(context, expected_title):
    """检查页面标题"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    actual_title = context.page.title()
    logger.info(f"页面标题: {actual_title}")
    assert actual_title == expected_title, f"页面标题不匹配，期望: {expected_title}, 实际: {actual_title}"


@then('当前 URL 应包含 "{expected_path}"')
def check_url_contains(context, expected_path):
    """检查当前 URL 是否包含指定路径"""
    if not hasattr(context, 'page') or not context.page:
        raise RuntimeError("页面未初始化")
    
    current_url = context.page.url
    logger.info(f"当前 URL: {current_url}")
    assert expected_path in current_url, f"URL 不包含期望路径，期望包含: {expected_path}, 实际 URL: {current_url}"