"""
多设备并行测试支持
提供设备池管理,支持在多个设备上并行运行测试
"""
import json
import os
import logging
import threading
from typing import List, Dict, Any, Optional
from common.appium_manager import AppiumManager

logger = logging.getLogger(__name__)


class DevicePool:
    """设备池管理器"""

    def __init__(self, config_path: str = None):
        """
        初始化设备池

        Args:
            config_path: 设备配置文件路径,默认为 config/android_capabilities.json
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'android_capabilities.json'
            )

        self.config_path = config_path
        self.devices = self._load_devices(config_path)
        self.available_devices = self.devices.copy()
        self.lock = threading.Lock()

    def _load_devices(self, config_path: str) -> List[Dict[str, Any]]:
        """加载设备配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            devices = config.get('devices', [])
            logger.info(f"加载设备配置成功,共 {len(devices)} 个设备")
            return devices
        except FileNotFoundError:
            logger.warning(f"设备配置文件不存在: {config_path}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"设备配置文件解析失败: {e}")
            raise

    def acquire_device(self) -> Optional[Dict[str, Any]]:
        """
        获取一个可用设备

        Returns:
            设备配置字典,如果没有可用设备则返回 None
        """
        with self.lock:
            if not self.available_devices:
                logger.warning("没有可用设备")
                return None

            device = self.available_devices.pop(0)
            logger.info(f"获取设备: {device.get('deviceName', 'unknown')}")
            return device

    def release_device(self, device_name: str):
        """
        释放设备

        Args:
            device_name: 设备名称
        """
        with self.lock:
            for device in self.devices:
                if device.get('deviceName') == device_name:
                    if device not in self.available_devices:
                        self.available_devices.append(device)
                        logger.info(f"释放设备: {device_name}")
                    break

    def get_available_count(self) -> int:
        """获取可用设备数量"""
        with self.lock:
            return len(self.available_devices)

    def get_total_count(self) -> int:
        """获取设备总数"""
        return len(self.devices)

    def reload_devices(self):
        """重新加载设备配置"""
        self.devices = self._load_devices(self.config_path)
        self.available_devices = self.devices.copy()
        logger.info("设备配置已重新加载")


class ParallelDeviceManager:
    """并行设备管理器"""

    def __init__(self, device_pool: DevicePool):
        """
        初始化并行设备管理器

        Args:
            device_pool: 设备池实例
        """
        self.device_pool = device_pool
        self.active_managers: Dict[str, AppiumManager] = {}
        self.lock = threading.Lock()

    def create_manager_for_device(self) -> Optional[AppiumManager]:
        """
        为设备创建 Appium 管理器

        Returns:
            AppiumManager 实例,如果没有可用设备则返回 None
        """
        device_config = self.device_pool.acquire_device()
        if device_config is None:
            return None

        device_name = device_config.get('deviceName', 'unknown')
        manager = AppiumManager()

        try:
            manager.connect(device_name=device_name)
            logger.info(f"设备 {device_name} 的 Appium 管理器创建成功")

            with self.lock:
                self.active_managers[device_name] = manager

            return manager

        except Exception as e:
            logger.error(f"为设备 {device_name} 创建 Appium 管理器失败: {e}")
            self.device_pool.release_device(device_name)
            return None

    def release_manager(self, device_name: str):
        """
        释放 Appium 管理器

        Args:
            device_name: 设备名称
        """
        with self.lock:
            if device_name in self.active_managers:
                manager = self.active_managers.pop(device_name)
                try:
                    if manager.is_connected():
                        manager.disconnect()
                    logger.info(f"设备 {device_name} 的 Appium 管理器已释放")
                except Exception as e:
                    logger.error(f"释放设备 {device_name} 的 Appium 管理器时出错: {e}")

        self.device_pool.release_device(device_name)

    def get_active_count(self) -> int:
        """获取活跃管理器数量"""
        with self.lock:
            return len(self.active_managers)

    def cleanup_all(self):
        """清理所有活跃的管理器"""
        with self.lock:
            device_names = list(self.active_managers.keys())

        for device_name in device_names:
            self.release_manager(device_name)


# 创建全局设备池
_global_device_pool = None


def get_device_pool(config_path: str = None) -> DevicePool:
    """
    获取全局设备池实例

    Args:
        config_path: 配置文件路径

    Returns:
        DevicePool 实例
    """
    global _global_device_pool

    if _global_device_pool is None or config_path is not None:
        _global_device_pool = DevicePool(config_path)

    return _global_device_pool


def create_parallel_manager(device_pool: DevicePool = None) -> ParallelDeviceManager:
    """
    创建并行设备管理器

    Args:
        device_pool: 设备池实例,如果为 None 则使用全局设备池

    Returns:
        ParallelDeviceManager 实例
    """
    if device_pool is None:
        device_pool = get_device_pool()

    return ParallelDeviceManager(device_pool)
