"""
云测试平台集成管理器
支持BrowserStack、Sauce Labs等云测试平台
"""
import json
import os
import logging
from typing import List, Dict, Any, Optional
from appium import webdriver
from common.appium_manager import AppiumManager

logger = logging.getLogger(__name__)


class CloudDeviceManager:
    """云设备管理器"""

    def __init__(self, platform: str = "browserstack", config_path: str = None):
        """
        初始化云设备管理器

        Args:
            platform: 云平台名称 (browserstack, saucelabs)
            config_path: 配置文件路径
        """
        self.platform = platform
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            f'{platform}_config.json'
        )
        self.config = self._load_config()
        self.server_url = self._build_server_url()
        self.devices = self.config.get('devices', [])
        self.available_devices = self.devices.copy()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"加载云平台配置成功: {self.platform}")
            return config
        except FileNotFoundError:
            logger.error(f"云平台配置文件不存在: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"云平台配置文件解析失败: {e}")
            raise

    def _build_server_url(self) -> str:
        """构建服务器URL"""
        if self.platform == "browserstack":
            server = self.config.get('server', 'hub-cloud.browserstack.com')
            user = self.config.get('user')
            key = self.config.get('key')
            return f"http://{user}:{key}@{server}/wd/hub"
        elif self.platform == "saucelabs":
            server = self.config.get('server', 'ondemand.saucelabs.com')
            user = self.config.get('user')
            key = self.config.get('key')
            return f"http://{user}:{key}@{server}/wd/hub'
        else:
            raise ValueError(f"不支持的云平台: {self.platform}")

    def acquire_device(self) -> Optional[Dict[str, Any]]:
        """
        获取一个可用设备

        Returns:
            设备配置字典,如果没有可用设备则返回 None
        """
        if not self.available_devices:
            logger.warning("没有可用云设备")
            return None

        device = self.available_devices.pop(0)
        logger.info(f"获取云设备: {device.get('device', 'unknown')}")
        return device

    def release_device(self, device_name: str):
        """
        释放设备

        Args:
            device_name: 设备名称
        """
        for device in self.devices:
            if device.get('device') == device_name:
                if device not in self.available_devices:
                    self.available_devices.append(device)
                    logger.info(f"释放云设备: {device_name}")
                break

    def create_driver(self, device_config: Dict[str, Any]) -> Optional[webdriver.Remote]:
        """
        创建云设备驱动

        Args:
            device_config: 设备配置

        Returns:
            WebDriver 实例
        """
        try:
            logger.info(f"正在连接到云设备: {device_config}")
            driver = webdriver.Remote(
                command_executor=self.server_url,
                desired_capabilities=device_config
            )
            logger.info(f"云设备连接成功: {device_config.get('device', 'unknown')}")
            return driver
        except Exception as e:
            logger.error(f"连接云设备失败: {e}")
            return None

    def get_available_count(self) -> int:
        """获取可用设备数量"""
        return len(self.available_devices)

    def get_total_count(self) -> int:
        """获取设备总数"""
        return len(self.devices)


class CloudParallelManager:
    """云平台并行测试管理器"""

    def __init__(self, platform: str = "browserstack", config_path: str = None):
        """
        初始化云平台并行管理器

        Args:
            platform: 云平台名称
            config_path: 配置文件路径
        """
        self.device_manager = CloudDeviceManager(platform, config_path)
        self.active_drivers = {}

    def create_manager_for_device(self) -> Optional[AppiumManager]:
        """
        为云设备创建管理器

        Returns:
            AppiumManager 实例,如果没有可用设备则返回 None
        """
        device_config = self.device_manager.acquire_device()
        if device_config is None:
            return None

        device_name = device_config.get('device', 'unknown')
        manager = AppiumManager()

        try:
            # 创建云设备驱动
            driver = self.device_manager.create_driver(device_config)
            if driver is None:
                raise Exception("创建云设备驱动失败")

            manager.driver = driver
            manager._configure_waits()

            logger.info(f"云设备 {device_name} 的 Appium 管理器创建成功")
            self.active_drivers[device_name] = manager

            return manager

        except Exception as e:
            logger.error(f"为云设备 {device_name} 创建 Appium 管理器失败: {e}")
            self.device_manager.release_device(device_name)
            return None

    def release_manager(self, device_name: str):
        """
        释放云设备管理器

        Args:
            device_name: 设备名称
        """
        if device_name in self.active_drivers:
            manager = self.active_drivers.pop(device_name)
            try:
                if manager.is_connected():
                    manager.disconnect()
                logger.info(f"云设备 {device_name} 的 Appium 管理器已释放")
            except Exception as e:
                logger.error(f"释放云设备 {device_name} 的 Appium 管理器时出错: {e}")

        self.device_manager.release_device(device_name)

    def cleanup_all(self):
        """清理所有活跃的管理器"""
        device_names = list(self.active_drivers.keys())
        for device_name in device_names:
            self.release_manager(device_name)