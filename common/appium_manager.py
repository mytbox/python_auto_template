"""
Appium 驱动管理器
用于管理 Appium WebDriver 实例,提供设备连接、断开和常用操作
"""
import json
import os
import logging
from typing import Optional, Dict, Any
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)


class AppiumManager:
    """Appium 驱动管理器类"""

    def __init__(self, config_path: str = None):
        """
        初始化 Appium 管理器

        Args:
            config_path: 配置文件路径,默认为 config/android_config.json
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'android_config.json'
            )

        self.config = self._load_config(config_path)
        self.driver: Optional[webdriver.Remote] = None
        self.server_url = self._build_server_url()

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"加载配置文件成功: {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"配置文件不存在: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"配置文件解析失败: {e}")
            raise

    def _build_server_url(self) -> str:
        """构建 Appium 服务器 URL"""
        server_config = self.config.get('appium_server', {})
        host = server_config.get('host', '127.0.0.1')
        port = server_config.get('port', 4723)
        base_path = server_config.get('base_path', '/wd/hub')
        return f"http://{host}:{port}{base_path}"

    def connect(self, device_name: str = None) -> webdriver.Remote:
        """
        连接到 Appium 服务器并创建驱动实例

        Args:
            device_name: 设备名称,如果为 None 则使用配置文件中的默认设备

        Returns:
            webdriver.Remote 实例
        """
        if self.driver is not None:
            logger.warning("驱动已存在,先关闭现有连接")
            self.disconnect()

        capabilities = self._get_capabilities(device_name)

        try:
            logger.info(f"正在连接到 Appium 服务器: {self.server_url}")
            logger.info(f"设备能力: {json.dumps(capabilities, ensure_ascii=False, indent=2)}")

            self.driver = webdriver.Remote(
                command_executor=self.server_url,
                desired_capabilities=capabilities
            )

            self._configure_waits()

            logger.info("Appium 驱动连接成功")
            return self.driver

        except Exception as e:
            logger.error(f"连接 Appium 服务器失败: {e}")
            raise

    def _get_capabilities(self, device_name: str = None) -> Dict[str, Any]:
        """
        获取设备能力配置

        Args:
            device_name: 设备名称

        Returns:
            设备能力字典
        """
        device_config = self.config.get('device', {})

        if device_name:
            capabilities = device_config.copy()
            capabilities['deviceName'] = device_name
        else:
            capabilities = device_config.copy()

        return capabilities

    def _configure_waits(self):
        """配置等待时间"""
        wait_config = self.config.get('wait', {})

        implicit_wait = wait_config.get('implicit_wait', 10)
        explicit_wait = wait_config.get('explicit_wait', 20)
        page_load_timeout = wait_config.get('page_load_timeout', 30)

        self.driver.implicitly_wait(implicit_wait)
        self.driver.set_page_load_timeout(page_load_timeout)

        logger.info(f"配置等待时间: implicit={implicit_wait}s, explicit={explicit_wait}s, page_load={page_load_timeout}s")

    def disconnect(self):
        """断开 Appium 驱动连接"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Appium 驱动已断开")
            except Exception as e:
                logger.error(f"断开驱动时出错: {e}")
            finally:
                self.driver = None

    def is_connected(self) -> bool:
        """检查驱动是否已连接"""
        return self.driver is not None

    def find_element(self, by: AppiumBy, value: str, timeout: int = None) -> webdriver.WebElement:
        """
        查找元素(带显式等待)

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间(秒),如果为 None 则使用配置文件中的值

        Returns:
            WebElement 实例

        Raises:
            TimeoutException: 元素未找到
        """
        if not self.driver:
            raise RuntimeError("驱动未连接,请先调用 connect() 方法")

        if timeout is None:
            timeout = self.config.get('wait', {}).get('explicit_wait', 20)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"元素查找超时: by={by}, value={value}, timeout={timeout}s")
            raise

    def find_elements(self, by: AppiumBy, value: str, timeout: int = None) -> list:
        """
        查找多个元素(带显式等待)

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间(秒)

        Returns:
            WebElement 列表
        """
        if not self.driver:
            raise RuntimeError("驱动未连接,请先调用 connect() 方法")

        if timeout is None:
            timeout = self.config.get('wait', {}).get('explicit_wait', 20)

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            logger.warning(f"未找到元素: by={by}, value={value}")
            return []

    def wait_for_element_visible(self, by: AppiumBy, value: str, timeout: int = None) -> webdriver.WebElement:
        """
        等待元素可见

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间(秒)

        Returns:
            WebElement 实例
        """
        if not self.driver:
            raise RuntimeError("驱动未连接,请先调用 connect() 方法")

        if timeout is None:
            timeout = self.config.get('wait', {}).get('explicit_wait', 20)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"等待元素可见超时: by={by}, value={value}")
            raise

    def wait_for_element_clickable(self, by: AppiumBy, value: str, timeout: int = None) -> webdriver.WebElement:
        """
        等待元素可点击

        Args:
            by: 定位方式
            value: 定位值
            timeout: 超时时间(秒)

        Returns:
            WebElement 实例
        """
        if not self.driver:
            raise RuntimeError("驱动未连接,请先调用 connect() 方法")

        if timeout is None:
            timeout = self.config.get('wait', {}).get('explicit_wait', 20)

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except TimeoutException:
            logger.error(f"等待元素可点击超时: by={by}, value={value}")
            raise

    def is_element_present(self, by: AppiumBy, value: str) -> bool:
        """
        检查元素是否存在

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            元素是否存在
        """
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, by: AppiumBy, value: str) -> bool:
        """
        检查元素是否可见

        Args:
            by: 定位方式
            value: 定位值

        Returns:
            元素是否可见
        """
        try:
            element = self.driver.find_element(by, value)
            return element.is_displayed()
        except NoSuchElementException:
            return False

    def get_current_activity(self) -> str:
        """
        获取当前 Activity

        Returns:
            当前 Activity 名称
        """
        if not self.driver:
            raise RuntimeError("驱动未连接")

        current_activity = self.driver.current_activity
        logger.info(f"当前 Activity: {current_activity}")
        return current_activity

    def get_current_package(self) -> str:
        """
        获取当前包名

        Returns:
            当前包名
        """
        if not self.driver:
            raise RuntimeError("驱动未连接")

        current_package = self.driver.current_package
        logger.info(f"当前包名: {current_package}")
        return current_package

    def take_screenshot(self, filename: str = None) -> str:
        """
        截图

        Args:
            filename: 截图文件名,如果为 None 则自动生成

        Returns:
            截图文件路径
        """
        if not self.driver:
            raise RuntimeError("驱动未连接")

        if filename is None:
            screenshot_config = self.config.get('screenshot', {})
            screenshot_dir = screenshot_config.get('directory', './screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)

            import time
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')

        self.driver.save_screenshot(filename)
        logger.info(f"截图已保存: {filename}")
        return filename

    def press_back(self):
        """按返回键"""
        if not self.driver:
            raise RuntimeError("驱动未连接")

        self.driver.press_keycode(4)
        logger.info("按返回键")

    def press_home(self):
        """按 Home 键"""
        if not self.driver:
            raise RuntimeError("驱动未连接")

        self.driver.press_keycode(3)
        logger.info("按 Home 键")

    def press_enter(self):
        """按 Enter 键"""
        if not self.driver:
            raise RuntimeError("驱动未连接")

        self.driver.press_keycode(66)
        logger.info("按 Enter 键")

    def get_device_info(self) -> Dict[str, Any]:
        """
        获取设备信息

        Returns:
            设备信息字典
        """
        if not self.driver:
            raise RuntimeError("驱动未连接")

        device_info = {
            'platform_name': self.driver.capabilities.get('platformName'),
            'platform_version': self.driver.capabilities.get('platformVersion'),
            'device_name': self.driver.capabilities.get('deviceName'),
            'automation_name': self.driver.capabilities.get('automationName'),
            'app_package': self.driver.capabilities.get('appPackage'),
            'app_activity': self.driver.capabilities.get('appActivity'),
            'current_activity': self.get_current_activity(),
            'current_package': self.get_current_package()
        }

        return device_info

    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()
