#!/usr/bin/env python3
"""
文档生成脚本
用于生成项目相关的文档
"""

import os
from pathlib import Path
from datetime import datetime


def generate_project_summary():
    """生成项目概览文档"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    summary_doc = f"""# 项目概览

## 项目简介

本项目是一个基于 Python + Behave 的 BDD 测试自动化框架，支持 HTTP API 测试和 Android App 测试。

## 技术栈

- **Python**: 3.12 (推荐) / 3.11 (兼容)
- **Behave**: BDD 测试框架
- **Allure**: 测试报告生成
- **Appium**: Android App 自动化测试
- **Playwright**: Web UI 自动化测试
- **Flask**: 模拟 API 服务器
- **Redis**: 数据缓存和测试数据管理

## 项目结构

```
{project_root.name}/
├── common/                  # 公共模块
│   ├── dto/                 # 数据传输对象
│   ├── database/            # 数据库模块
│   ├── utils/               # 工具类
│   ├── appium_manager.py    # Appium 驱动管理器
│   └── playwright_manager.py # Playwright 驱动管理器
├── config/                  # 配置文件
│   ├── test.json            # 测试环境配置
│   ├── dev.json             # 开发环境配置
│   ├── mock.json            # 模拟 API 环境配置
│   ├── android_config.json  # Android 测试配置
│   ├── web_config.json      # Web 测试配置
│   ├── android_elements.json # Android 元素定位配置
│   ├── web_elements.json    # Web 元素定位配置
│   └── config.py            # 配置管理器
├── features/                # Behave 特性文件和步骤定义
│   ├── android/             # Android 测试
│   │   ├── features/         # Android 特性文件
│   │   └── steps/           # Android 步骤定义
│   ├── web/                 # Web 测试
│   │   ├── features/         # Web 特性文件
│   │   └── steps/           # Web 步骤定义
│   ├── steps/               # API 测试步骤
│   ├── environment.py       # Behave 环境配置
│   └── *.feature            # 特性文件
├── mock_api/                # 模拟 API 服务器
│   └── server.py            # Flask 模拟服务器
├── requirements.txt         # 项目依赖
├── behave.ini              # Behave 配置
└── run_behave_parallel.py  # 并行测试脚本
```

## 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（仅 Web 测试需要）
playwright install

# 启动模拟 API 服务器
python mock_api/server.py
```

### 2. 运行测试

```bash
# 运行 API 测试
behave features/api_demo.feature -D profile=mock

# 运行 Android 测试
behave features/android/ -D android_test=true

# Web 测试
behave features/web/ -D web_test=true

# 生成 Allure 报告
behave features/ -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
```

## 核心功能

### 1. 多平台测试支持

- **API 测试**: 支持 RESTful API 的完整测试流程
- **Android 测试**: 基于 Appium 的 Android App 自动化测试
- **Web 测试**: 基于 Playwright 的 Web UI 自动化测试

### 2. 配置管理

- 环境配置分离（测试、开发、模拟）
- 动态配置加载和切换
- Redis 连接管理

### 3. 测试数据管理

- JSONPath 表达式支持
- 批量数据检查
- 测试数据存储和检索

### 4. 报告生成

- Allure 测试报告
- 测试结果截图
- 详细错误日志

## 开发指南

### 1. 编写测试

- 使用 Gherkin 语法编写特性文件
- 实现对应的步骤定义
- 使用场景上下文管理测试数据

### 2. 配置管理

- 使用配置文件管理环境相关设置
- 避免在代码中硬编码配置
- 使用环境变量管理敏感信息

### 3. 最佳实践

- 保持步骤定义的可重用性
- 使用适当的等待策略
- 添加详细的错误日志

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    doc_path = docs_dir / "project_summary.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(summary_doc)
    
    print(f"项目概览文档已生成: {doc_path}")
    return doc_path


def generate_api_testing_guide():
    """生成 API 测试指南"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    api_guide = f"""# API 测试指南

## 概述

本文档介绍如何使用本项目进行 API 自动化测试。

## 环境配置

### 1. 配置文件

项目支持多环境配置，配置文件位于 `config/` 目录：

- `dev.json`: 开发环境配置
- `test.json`: 测试环境配置
- `mock.json`: 模拟 API 环境配置

### 2. 启动模拟 API 服务器

```bash
# Windows
start_mock_api.bat

# Linux/Mac
./start_mock_api.sh

# 或直接运行
python mock_api/server.py
```

## 编写测试

### 1. 特性文件

特性文件使用 Gherkin 语法编写，描述测试场景：

```gherkin
Feature: 用户管理 API 测试
  测试用户管理相关的 API 功能

  Scenario: 获取用户列表
    Given 设置基础URL为 "http://127.0.0.1:48080"
    When 发送 GET 请求到 "/api/users"
    Then 检查 HTTP 状态码为 200
    And 检查响应字段 "data" 是一个列表

  Scenario: 创建新用户
    Given 设置基础URL为 "http://127.0.0.1:48080"
    When 发送 POST 请求到 "/api/users"，请求体为:
    '''
    {{
      "name": "测试用户",
      "email": "test@example.com"
    }}
    '''
    Then 检查 HTTP 状态码为 201
    And 检查响应字段 "data.name" 等于 "测试用户"
```

### 2. 步骤定义

步骤定义将 Gherkin 步骤映射到 Python 代码：

```python
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext
import requests
import json

@given('设置基础URL为 "{{base_url}}"')
def set_base_url(context, base_url):
    context.scenario_context = ScenarioContext()
    context.scenario_context.base_url = base_url

@when('发送 GET 请求到 "{{endpoint}}"')
def send_get_request(context, endpoint):
    scenario_context = context.scenario_context
    url = f"{{scenario_context.base_url}}{{endpoint}}"
    response = requests.get(url)
    scenario_context.last_response = response

@when('发送 POST 请求到 "{{endpoint}}"，请求体为:')
def send_post_request(context, endpoint):
    scenario_context = context.scenario_context
    url = f"{{scenario_context.base_url}}{{endpoint}}"
    payload = json.loads(context.text)
    response = requests.post(url, json=payload)
    scenario_context.last_response = response

@then('检查 HTTP 状态码为 {{status_code:d}}')
def check_status_code(context, status_code):
    scenario_context = context.scenario_context
    assert scenario_context.last_response.status_code == status_code

@then('检查响应字段 "{{json_path}}" 等于 {{expected_value}}')
def check_response_field_equals(context, json_path, expected_value):
    scenario_context = context.scenario_context
    response = scenario_context.last_response
    data = response.json()
    
    from jsonpath_ng import parse
    jsonpath_expression = parse(json_path)
    matches = [match.value for match in jsonpath_expression.find(data)]
    
    assert len(matches) > 0, f"No matching field found: {{json_path}}"
    actual_value = matches[0]
    assert actual_value == expected_value
```

## 运行测试

### 1. 基本运行

```bash
# 运行所有测试
behave features/

# 运行特定特性文件
behave features/api_demo.feature

# 使用特定配置环境
behave features/api_demo.feature -D profile=mock
```

### 2. 生成报告

```bash
# 生成 Allure 报告
behave features/ -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
```

### 3. 并行测试

```bash
# 使用 4 个线程并行运行
python run_behave_parallel.py -n 4 -p mock
```

## 最佳实践

### 1. 测试数据管理

- 使用场景上下文管理测试数据
- 使用配置文件管理环境相关数据
- 使用 Redis 或数据库管理持久化数据

### 2. 错误处理

- 添加详细的错误日志
- 使用断言提供清晰的错误信息
- 在失败时记录请求和响应详情

### 3. 测试组织

- 按功能模块组织特性文件
- 使用标签分类测试场景
- 保持步骤定义的可重用性

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    doc_path = docs_dir / "api_testing_guide.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(api_guide)
    
    print(f"API 测试指南已生成: {doc_path}")
    return doc_path


def generate_web_testing_guide():
    """生成 Web 测试指南"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    web_guide = f"""# Web 测试指南

## 概述

本文档介绍如何使用本项目进行 Web UI 自动化测试，基于 Playwright 和 Behave 框架。

## 环境准备

### 1. 安装依赖

```bash
pip install playwright==1.40.0
```

### 2. 安装 Playwright 浏览器

```bash
playwright install
```

### 3. 配置文件

在 `config/` 目录下创建 Web 相关配置：

`web_config.json`:
```json
{{
  "playwright": {{
    "browser": {{
      "type": "chromium",
      "headless": true,
      "slow_mo": 100,
      "timeout": 30000
    }},
    "context": {{
      "viewport": {{
        "width": 1280,
        "height": 720
      }},
      "ignore_https_errors": true,
      "accept_downloads": true
    }},
    "trace": {{
      "enabled": false,
      "screenshots": true,
      "snapshots": true,
      "sources": true
    }},
    "video": {{
      "enabled": false,
      "dir": "./test-results/videos"
    }},
    "screenshot": {{
      "enabled": true,
      "dir": "./test-results/screenshots",
      "full_page": true,
      "only_on_failure": true
    }}
  }},
  "test": {{
    "base_url": "http://localhost:3000",
    "timeout": 10000,
    "retry": 2
  }}
}}
```

`web_elements.json`:
```json
{{
  "login_page": {{
    "username_input": {{
      "id": "username"
    }},
    "password_input": {{
      "id": "password"
    }},
    "login_button": {{
      "css": "button[type='submit']"
    }},
    "error_message": {{
      "css": ".error-message"
    }}
  }},
  "home_page": {{
    "user_menu": {{
      "css": ".user-menu"
    }},
    "logout_button": {{
      "css": ".logout-button"
    }},
    "welcome_message": {{
      "css": ".welcome-message"
    }}
  }}
}}
```

## 编写测试

### 1. 特性文件

```gherkin
Feature: 用户登录
  测试 Web 应用的用户登录功能

  Background:
    Given 启动浏览器

  Scenario: 使用用户名密码登录成功
    When 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 检查 home_page 页面的 welcome_message 元素存在
    And 检查 home_page 页面的 welcome_message 元素包含文本 "欢迎"
    And 检查当前 URL 包含 "/home"
```

### 2. 步骤定义

```python
from behave import given, when, then
from common.playwright_manager import PlaywrightManager

@given('启动浏览器')
def launch_browser(context):
    """启动浏览器"""
    context.is_web_test = True
    context.playwright_manager = PlaywrightManager()
    context.page = context.playwright_manager.start_browser()

@when('导航到 "{{url}}"')
def navigate_to_url(context, url):
    """导航到指定 URL"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    context.playwright_manager.navigate_to(url)

@when('在 {{page_name}} 页面的 {{element_name}} 元素中输入 "{{text}}"')
def input_text(context, page_name, element_name, text):
    """在指定元素中输入文本"""
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    locator = context.playwright_manager.get_element_locator(page_name, element_name)
    context.page.fill(locator, text)
```

## 元素定位策略

### 1. 定位方式

- ID: `{"id": "element-id"}`
- CSS: `{"css": ".class-name"}`
- XPath: `{"xpath": "//div[@text='button']"}`
- Text: `{"text": "按钮文本"}`

### 2. 元素等待

```python
def wait_for_element(page, locator, timeout=10000):
    return page.wait_for_selector(locator, timeout=timeout)
```

## 页面操作

### 1. 导航操作

```python
# 导航到 URL
context.playwright_manager.navigate_to("/login")

# 点击浏览器后退按钮
context.page.go_back()

# 点击浏览器前进按钮
context.page.go_forward()

# 刷新当前页面
context.page.reload()
```

### 2. 滚动操作

```python
# 滚动到页面顶部
context.page.evaluate("window.scrollTo(0, 0)")

# 滚动到页面底部
context.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

# 滚动指定像素
context.page.evaluate(f"window.scrollBy(0, {{pixels}})")
```

## 运行测试

### 1. 基本运行

```bash
# 运行所有 Web 测试
behave features/web/ -D web_test=true

# 运行特定特性文件
behave features/web/features/login.feature -D web_test=true

# 使用特定浏览器
behave features/web/features/login.feature -D web_test=true -D browser=firefox
```

### 2. 生成报告

```bash
# 生成 Allure 报告
behave features/web/ -D web_test=true -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
```

### 3. 并行测试

```bash
# 使用 4 个线程并行运行
behave-parallel -n 4 -D web_test=true features/web/
```

## 最佳实践

### 1. 元素定位

- 优先使用稳定的定位器（ID、数据测试属性）
- 避免使用绝对 XPath
- 使用显式等待而非隐式等待

### 2. 测试数据管理

- 使用独立的测试环境
- 每次测试前清理数据
- 使用 Redis 管理测试状态

### 3. 浏览器兼容性

- 测试不同浏览器（Chrome、Firefox、Safari）
- 测试不同屏幕尺寸
- 处理浏览器特定行为

### 4. 错误处理

- 添加详细的错误日志
- 自动截图失败场景
- 提供清晰的错误信息

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    doc_path = docs_dir / "web_testing_guide.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(web_guide)
    
    print(f"Web 测试指南已生成: {doc_path}")
    return doc_path


def generate_android_testing_guide():
    """生成 Android 测试指南"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    android_guide = f"""# Android 测试指南

## 概述

本文档介绍如何使用本项目进行 Android App 自动化测试。

## 环境准备

### 1. 安装依赖

```bash
pip install Appium-Python-Client==2.11.1
pip install selenium==4.16.0
```

### 2. 安装 Appium Server

```bash
npm install -g appium
# 安装 UiAutomator2 驱动
appium driver install uiautomator2
```

### 3. 配置 Android 开发环境

- 安装 Android SDK
- 配置 ANDROID_HOME 环境变量
- 安装 Android 模拟器或连接真机
- 启用 USB 调试 (真机测试时)

## 编写测试

### 1. 特性文件

```gherkin
Feature: 用户登录
  测试 Android App 的用户登录功能

  Background:
    Given 启动 Android App

  Scenario: 使用手机号登录
    When 点击登录按钮
    And 输入手机号 "13800138000"
    And 输入验证码 "123456"
    And 点击确认登录
    Then 验证登录成功
    And 验证首页显示用户信息

  Scenario: 登录失败-验证码错误
    When 点击登录按钮
    And 输入手机号 "13800138000"
    And 输入验证码 "000000"
    And 点击确认登录
    Then 验证显示错误提示 "验证码错误"
```

### 2. 步骤定义

```python
from behave import given, when, then
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.appium_manager import AppiumManager

@given('启动 Android App')
def launch_android_app(context):
    context.appium_manager = AppiumManager()
    context.driver = context.appium_manager.create_driver()

@when('点击登录按钮')
def click_login_button(context):
    login_button = context.driver.find_element(AppiumBy.ID, "com.example.app:id/login_button")
    login_button.click()

@when('输入手机号 "{{phone}}"')
def input_phone(context, phone):
    phone_input = context.driver.find_element(AppiumBy.ID, "com.example.app:id/phone_input")
    phone_input.clear()
    phone_input.send_keys(phone)

@then('验证登录成功')
def verify_login_success(context):
    # 等待首页元素出现
    home_element = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((AppiumBy.ID, "com.example.app:id/home_container"))
    )
    assert home_element.is_displayed()
```

## 元素定位策略

### 1. 定位方式

- ID: `driver.find_element(AppiumBy.ID, "com.example.app:id/button")`
- XPath: `driver.find_element(AppiumBy.XPATH, "//android.widget.Button[@text='登录']")`
- Accessibility ID: `driver.find_element(AppiumBy.ACCESSIBILITY_ID, "登录按钮")`
- UIAutomator: `driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("登录")')`

### 2. 元素等待

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_for_element(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
```

## 手势操作

### 1. 滑动

```python
def swipe(driver, start_x, start_y, end_x, end_y, duration=1000):
    driver.swipe(start_x, start_y, end_x, end_y, duration)
```

### 2. 长按

```python
from appium.webdriver.common.touch_action import TouchAction

def long_press(driver, element, duration=1000):
    action = TouchAction(driver)
    action.long_press(element, duration).release().perform()
```

## 运行测试

### 1. 启动 Appium 服务器

```bash
appium
```

### 2. 运行测试

```bash
# 运行所有 Android 测试
behave features/android/ -D android_test=true

# 运行特定特性文件
behave features/android/features/login.feature -D android_test=true

# 生成 Allure 报告
behave features/android/ -D android_test=true -f allure_behave.formatter:AllureFormatter -o ./allure-results
```

## 最佳实践

### 1. 元素定位

- 优先使用 ID 定位
- 避免使用绝对 XPath
- 使用显式等待而非隐式等待

### 2. 测试数据管理

- 使用独立的测试环境
- 每次测试前清理数据
- 使用 Redis 管理测试状态

### 3. 错误处理

- 添加详细的错误日志
- 自动截图失败场景
- 提供清晰的错误信息

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    doc_path = docs_dir / "android_testing_guide.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(android_guide)
    
    print(f"Android 测试指南已生成: {doc_path}")
    return doc_path


def main():
    """主函数"""
    print("开始生成项目文档...")
    
    docs = []
    docs.append(generate_project_summary())
    docs.append(generate_api_testing_guide())
    docs.append(generate_web_testing_guide())
    docs.append(generate_android_testing_guide())
    
    print("\n所有文档生成完成:")
    for doc in docs:
        print(f"  - {doc}")


if __name__ == "__main__":
    main()