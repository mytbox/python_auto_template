"""
Android 元素定位工具类
提供便捷的方法来获取元素定位信息
"""
import json
import os
import logging
from typing import Dict, Any, Tuple, Optional
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)


class ElementLocator:
    """元素定位工具类"""

    def __init__(self, config_path: str = None):
        """
        初始化元素定位工具

        Args:
            config_path: 元素配置文件路径,默认为 config/android_elements.json
        """
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'config',
                'android_elements.json'
            )

        self.config_path = config_path
        self.elements_config = self._load_config(config_path)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载元素配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"加载元素配置文件成功: {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"元素配置文件不存在: {config_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"元素配置文件解析失败: {e}")
            raise

    def reload_config(self):
        """重新加载配置文件"""
        self.elements_config = self._load_config(self.config_path)
        logger.info("元素配置已重新加载")

    def get_locator(self, element_name: str, page_name: str = None) -> Tuple[AppiumBy, str]:
        """
        获取元素定位信息

        Args:
            element_name: 元素名称
            page_name: 页面名称,如果为 None 则在所有页面中查找

        Returns:
            (AppiumBy, value) 元组

        Raises:
            ValueError: 元素未找到
        """
        if page_name:
            if page_name not in self.elements_config:
                raise ValueError(f"页面不存在: {page_name}")

            page_elements = self.elements_config[page_name]
            if element_name not in page_elements:
                raise ValueError(f"元素不存在: {page_name}.{element_name}")

            element_info = page_elements[element_name]
        else:
            element_info = None
            for page_elements in self.elements_config.values():
                if element_name in page_elements:
                    element_info = page_elements[element_name]
                    break

            if element_info is None:
                raise ValueError(f"元素不存在: {element_name}")

        locator_type = element_info.get('type', 'id')
        locator_value = element_info.get('value', element_info.get('id', ''))

        return self._parse_locator(locator_type, locator_value)

    def get_locator_by_xpath(self, xpath: str) -> Tuple[AppiumBy, str]:
        """
        通过 XPath 获取定位信息

        Args:
            xpath: XPath 表达式

        Returns:
            (AppiumBy.XPATH, xpath) 元组
        """
        return (AppiumBy.XPATH, xpath)

    def get_locator_by_id(self, element_id: str) -> Tuple[AppiumBy, str]:
        """
        通过 ID 获取定位信息

        Args:
            element_id: 元素 ID

        Returns:
            (AppiumBy.ID, element_id) 元组
        """
        return (AppiumBy.ID, element_id)

    def get_locator_by_class_name(self, class_name: str) -> Tuple[AppiumBy, str]:
        """
        通过类名获取定位信息

        Args:
            class_name: 类名

        Returns:
            (AppiumBy.CLASS_NAME, class_name) 元组
        """
        return (AppiumBy.CLASS_NAME, class_name)

    def get_locator_by_accessibility_id(self, accessibility_id: str) -> Tuple[AppiumBy, str]:
        """
        通过 Accessibility ID 获取定位信息

        Args:
            accessibility_id: Accessibility ID

        Returns:
            (AppiumBy.ACCESSIBILITY_ID, accessibility_id) 元组
        """
        return (AppiumBy.ACCESSIBILITY_ID, accessibility_id)

    def get_locator_by_android_uiautomator(self, uiautomator: str) -> Tuple[AppiumBy, str]:
        """
        通过 Android UIAutomator 获取定位信息

        Args:
            uiautomator: UIAutomator 表达式

        Returns:
            (AppiumBy.ANDROID_UIAUTOMATOR, uiautomator) 元组
        """
        return (AppiumBy.ANDROID_UIAUTOMATOR, uiautomator)

    def _parse_locator(self, locator_type: str, locator_value: str) -> Tuple[AppiumBy, str]:
        """
        解析定位方式

        Args:
            locator_type: 定位方式字符串
            locator_value: 定位值

        Returns:
            (AppiumBy, value) 元组

        Raises:
            ValueError: 不支持的定位方式
        """
        locator_map = {
            'id': AppiumBy.ID,
            'xpath': AppiumBy.XPATH,
            'class_name': AppiumBy.CLASS_NAME,
            'accessibility_id': AppiumBy.ACCESSIBILITY_ID,
            'android_uiautomator': AppiumBy.ANDROID_UIAUTOMATOR,
        }

        locator_type_lower = locator_type.lower()
        if locator_type_lower not in locator_map:
            raise ValueError(f"不支持的定位方式: {locator_type}, 支持的定位方式: {list(locator_map.keys())}")

        return (locator_map[locator_type_lower], locator_value)

    def get_all_elements(self, page_name: str = None) -> Dict[str, Any]:
        """
        获取所有元素配置

        Args:
            page_name: 页面名称,如果为 None 则返回所有页面的元素

        Returns:
            元素配置字典
        """
        if page_name:
            if page_name not in self.elements_config:
                raise ValueError(f"页面不存在: {page_name}")
            return self.elements_config[page_name]
        else:
            return self.elements_config

    def get_page_names(self) -> list:
        """
        获取所有页面名称

        Returns:
            页面名称列表
        """
        return list(self.elements_config.keys())

    def get_element_names(self, page_name: str) -> list:
        """
        获取指定页面的所有元素名称

        Args:
            page_name: 页面名称

        Returns:
            元素名称列表
        """
        if page_name not in self.elements_config:
            raise ValueError(f"页面不存在: {page_name}")
        return list(self.elements_config[page_name].keys())

    def element_exists(self, element_name: str, page_name: str = None) -> bool:
        """
        检查元素是否存在

        Args:
            element_name: 元素名称
            page_name: 页面名称

        Returns:
            元素是否存在
        """
        try:
            self.get_locator(element_name, page_name)
            return True
        except ValueError:
            return False

    def add_element(self, page_name: str, element_name: str, locator_type: str, locator_value: str):
        """
        添加元素配置

        Args:
            page_name: 页面名称
            element_name: 元素名称
            locator_type: 定位方式
            locator_value: 定位值
        """
        if page_name not in self.elements_config:
            self.elements_config[page_name] = {}

        self.elements_config[page_name][element_name] = {
            'type': locator_type,
            'value': locator_value
        }

        logger.info(f"已添加元素: {page_name}.{element_name}")

    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.elements_config, f, ensure_ascii=False, indent=2)
            logger.info(f"元素配置已保存到: {self.config_path}")
        except Exception as e:
            logger.error(f"保存元素配置失败: {e}")
            raise


# 创建全局实例
_global_locator = None


def get_element_locator(config_path: str = None) -> ElementLocator:
    """
    获取全局元素定位器实例

    Args:
        config_path: 配置文件路径

    Returns:
        ElementLocator 实例
    """
    global _global_locator

    if _global_locator is None or config_path is not None:
        _global_locator = ElementLocator(config_path)

    return _global_locator
