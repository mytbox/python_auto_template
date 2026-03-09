"""
简单的 Playwright 测试脚本
用于验证 Playwright 集成是否正常工作
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from playwright.sync_api import sync_playwright
    print("✓ Playwright 模块导入成功")
except ImportError as e:
    print(f"✗ Playwright 模块导入失败: {e}")
    sys.exit(1)

try:
    from common.playwright_manager import PlaywrightManager
    print("✓ PlaywrightManager 导入成功")
except ImportError as e:
    print(f"✗ PlaywrightManager 导入失败: {e}")
    sys.exit(1)

def test_playwright_manager():
    """测试 PlaywrightManager 是否正常工作"""
    try:
        # 创建 PlaywrightManager 实例
        manager = PlaywrightManager()
        print("✓ PlaywrightManager 创建成功")
        
        # 启动浏览器
        page = manager.start_browser()
        print("✓ 浏览器启动成功")
        
        # 导航到测试页面
        manager.navigate_to("http://localhost:3000")
        print("✓ 页面导航成功")
        
        # 获取页面标题
        title = page.title()
        print(f"✓ 页面标题: {title}")
        
        # 截图
        screenshot_path = manager.take_screenshot("test_screenshot.png")
        print(f"✓ 截图成功: {screenshot_path}")
        
        # 关闭浏览器
        manager.close_browser()
        print("✓ 浏览器关闭成功")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试 Playwright 集成...")
    if test_playwright_manager():
        print("\n✓ 所有测试通过！Playwright 集成工作正常。")
    else:
        print("\n✗ 测试失败！请检查 Playwright 集成配置。")