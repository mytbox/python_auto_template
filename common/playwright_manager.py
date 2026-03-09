"""
Playwright 驱动管理器
用于管理 Playwright 浏览器实例和页面
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, expect
from loguru import logger


class PlaywrightManager:
    """Playwright 驱动管理器"""
    
    def __init__(self, config_path: str = None):
        """初始化 Playwright 管理器
        
        Args:
            config_path: 配置文件路径，默认为 config/web_config.json
        """
        self.project_root = Path(__file__).parent.parent.parent
        if config_path is None:
            config_path = self.project_root / "config" / "web_config.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.elements_config = self._load_elements_config()
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
    def _load_elements_config(self) -> Dict[str, Any]:
        """加载元素定位配置"""
        elements_config_path = self.project_root / "config" / "web_elements.json"
        with open(elements_config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def start_browser(self, browser_type: str = None, headless: bool = None) -> Page:
        """启动浏览器并返回页面对象
        
        Args:
            browser_type: 浏览器类型，默认从配置读取
            headless: 是否无头模式，默认从配置读取
            
        Returns:
            Page: Playwright 页面对象
        """
        if self.page is not None:
            logger.warning("浏览器已经启动，返回现有页面")
            return self.page
        
        browser_config = self.config.get("playwright", {}).get("browser", {})
        context_config = self.config.get("playwright", {}).get("context", {})
        
        if browser_type is None:
            browser_type = browser_config.get("type", "chromium")
        if headless is None:
            headless = browser_config.get("headless", True)
        
        logger.info(f"启动 {browser_type} 浏览器，无头模式: {headless}")
        
        self.playwright = sync_playwright().start()
        
        # 根据类型选择浏览器
        if browser_type.lower() == "chromium":
            self.browser = self.playwright.chromium.launch(
                headless=headless,
                slow_mo=browser_config.get("slow_mo", 100)
            )
        elif browser_type.lower() == "firefox":
            self.browser = self.playwright.firefox.launch(
                headless=headless,
                slow_mo=browser_config.get("slow_mo", 100)
            )
        elif browser_type.lower() == "webkit":
            self.browser = self.playwright.webkit.launch(
                headless=headless,
                slow_mo=browser_config.get("slow_mo", 100)
            )
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")
        
        # 创建上下文
        self.context = self.browser.new_context(
            viewport=context_config.get("viewport", {"width": 1280, "height": 720}),
            ignore_https_errors=context_config.get("ignore_https_errors", True),
            accept_downloads=context_config.get("accept_downloads", True)
        )
        
        # 设置超时
        self.context.set_default_timeout(
            self.config.get("test", {}).get("timeout", 10000)
        )
        
        # 创建页面
        self.page = self.context.new_page()
        
        # 设置截图目录
        screenshot_config = self.config.get("playwright", {}).get("screenshot", {})
        if screenshot_config.get("enabled", True):
            screenshot_dir = self.project_root / screenshot_config.get("dir", "./test-results/screenshots")
            screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        return self.page
    
    def close_browser(self):
        """关闭浏览器"""
        if self.page:
            self.page.close()
            self.page = None
            logger.info("页面已关闭")
        
        if self.context:
            self.context.close()
            self.context = None
            logger.info("浏览器上下文已关闭")
        
        if self.browser:
            self.browser.close()
            self.browser = None
            logger.info("浏览器已关闭")
        
        if self.playwright:
            self.playwright.stop()
            self.playwright = None
            logger.info("Playwright 已停止")
    
    def take_screenshot(self, filename: str = None, full_page: bool = True) -> str:
        """截图
        
        Args:
            filename: 文件名，如果为 None 则自动生成
            full_page: 是否全页截图
            
        Returns:
            str: 截图文件路径
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，无法截图")
        
        screenshot_config = self.config.get("playwright", {}).get("screenshot", {})
        if not screenshot_config.get("enabled", True):
            return ""
        
        if filename is None:
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshot_dir = self.project_root / screenshot_config.get("dir", "./test-results/screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        screenshot_path = screenshot_dir / filename
        self.page.screenshot(
            path=str(screenshot_path),
            full_page=full_page or screenshot_config.get("full_page", True)
        )
        
        logger.info(f"截图已保存: {screenshot_path}")
        return str(screenshot_path)
    
    def get_element_locator(self, page_name: str, element_name: str) -> str:
        """获取元素定位器
        
        Args:
            page_name: 页面名称
            element_name: 元素名称
            
        Returns:
            str: 定位器字符串
        """
        if page_name not in self.elements_config:
            raise ValueError(f"页面配置不存在: {page_name}")
        
        page_elements = self.elements_config[page_name]
        if element_name not in page_elements:
            raise ValueError(f"元素配置不存在: {page_name}.{element_name}")
        
        element_config = page_elements[element_name]
        
        # 根据配置生成定位器
        if "id" in element_config:
            return f"#{element_config['id']}"
        elif "css" in element_config:
            return element_config["css"]
        elif "xpath" in element_config:
            return element_config["xpath"]
        elif "text" in element_config:
            return f"text={element_config['text']}"
        else:
            raise ValueError(f"无效的元素配置: {page_name}.{element_name}")
    
    def navigate_to(self, url: str):
        """导航到指定 URL
        
        Args:
            url: 目标 URL
        """
        if not self.page:
            raise RuntimeError("浏览器未启动，无法导航")
        
        base_url = self.config.get("test", {}).get("base_url", "")
        if url.startswith("/"):
            full_url = base_url + url
        else:
            full_url = url
        
        logger.info(f"导航到: {full_url}")
        self.page.goto(full_url)
    
    def wait_for_element(self, locator: str, timeout: int = None):
        """等待元素出现
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（毫秒）
            
        Returns:
            ElementHandle: 元素句柄
        """
        if not self.page:
            raise RuntimeError("浏览器未启动")
        
        if timeout is None:
            timeout = self.config.get("test", {}).get("timeout", 10000)
        
        logger.debug(f"等待元素: {locator}")
        return self.page.wait_for_selector(locator, timeout=timeout)
    
    def is_element_visible(self, locator: str, timeout: int = 5000) -> bool:
        """检查元素是否可见
        
        Args:
            locator: 元素定位器
            timeout: 超时时间（毫秒）
            
        Returns:
            bool: 元素是否可见
        """
        if not self.page:
            return False
        
        try:
            element = self.page.wait_for_selector(locator, timeout=timeout)
            return element.is_visible()
        except:
            return False