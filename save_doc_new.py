"""
项目文档生成脚本
用于生成项目相关的文档文件
"""

import os
import json
from pathlib import Path
from datetime import datetime


def generate_project_summary():
    """生成项目概览文档"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    # 确保文档目录存在
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    # 读取项目配置
    config_path = project_root / "config" / "test.json"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    
    # 读取项目依赖
    requirements_path = project_root / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, 'r', encoding='utf-8') as f:
            requirements = f.read()
    else:
        requirements = ""
    
    # 生成项目概览
    summary = f"""# {project_root.name} 项目概览

## 项目简介

本项目是一个基于 Python 的自动化测试框架，集成了 API 测试、Android App 测试和 Web UI 测试功能。使用 Behave 作为 BDD 测试框架，支持多种测试场景和报告生成。

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
# API 测试
behave features/api/ -D profile=test

# Android 测试
behave features/android/ -D android_test=true

# Web 测试
behave features/web/ -D web_test=true

# 生成 Allure 报告
behave features/ -f allure_behave.formatter:AllureFormatter -o ./allure-results
```

## 开发指南

### 1. 添加新的 API 测试

1. 在 `features/` 目录下创建新的 `.feature` 文件
2. 在 `features/steps/` 目录下添加对应的步骤定义
3. 更新配置文件（如需要）

### 2. 添加新的 Android 测试

1. 在 `features/android/features/` 目录下创建新的 `.feature` 文件
2. 在 `features/android/steps/` 目录下添加对应的步骤定义
3. 更新 `config/android_elements.json` 添加元素定位

### 3. 添加新的 Web 测试

1. 在 `features/web/features/` 目录下创建新的 `.feature` 文件
2. 在 `features/web/steps/` 目录下添加对应的步骤定义
3. 更新 `config/web_elements.json` 添加元素定位

## 最佳实践

### 1. 测试组织

- 按功能模块组织特性文件
- 使用标签分类测试场景
- 保持步骤定义的可重用性

### 2. 数据管理

- 使用 Redis 管理测试状态
- 避免硬编码测试数据
- 实现测试数据的清理机制

### 3. 错误处理

- 添加详细的错误日志
- 实现失败场景的截图
- 提供清晰的错误信息

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    doc_path = docs_dir / "project_summary.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"项目概览文档已生成: {doc_path}")
    return doc_path


def generate_api_testing_guide():
    """生成 API 测试指南"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    api_guide = """# API 测试指南

## 概述

本文档介绍如何使用本项目进行 API 自动化测试，基于 Behave 框架和 Flask 模拟服务器。

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动模拟 API 服务器

```bash
python mock_api/server.py
```

## 配置文件

在 `config/` 目录下有多个环境配置文件：

- `test.json`: 测试环境配置
- `dev.json`: 开发环境配置
- `mock.json`: 模拟 API 环境配置

配置示例：
```json
{
  "base_url": "http://localhost:5000",
  "timeout": 30,
  "headers": {
    "Content-Type": "application/json"
  }
}
```

## 编写测试

### 1. 特性文件

```gherkin
Feature: 用户管理 API
  测试用户管理相关的 API 接口

  Scenario: 获取用户列表
    Given 设置请求头 "Content-Type" 为 "application/json"
    When 发送 GET 请求到 "/api/users"
    Then 响应状态码应为 200
    And 响应数据中 "code" 应为 0
    And 响应数据中 "data" 应包含 "users" 数组
```

### 2. 步骤定义

```python
from behave import given, when, then
import requests
import json

@given('设置请求头 "{header}" 为 "{value}"')
def set_request_header(context, header, value):
    \"\"\"设置请求头\"\"\"
    if not hasattr(context, 'headers'):
        context.headers = {}
    context.headers[header] = value

@when('发送 {method} 请求到 "{endpoint}"')
def send_request(context, method, endpoint):
    \"\"\"发送 HTTP 请求\"\"\"
    url = context.scenario_context.base_url + endpoint
    headers = getattr(context, 'headers', {})
    data = getattr(context, 'request_data', None)
    
    if method.upper() == 'GET':
        context.response = requests.get(url, headers=headers, params=data)
    elif method.upper() == 'POST':
        context.response = requests.post(url, headers=headers, json=data)
    elif method.upper() == 'PUT':
        context.response = requests.put(url, headers=headers, json=data)
    elif method.upper() == 'DELETE':
        context.response = requests.delete(url, headers=headers)
```

## 数据验证

### 1. 状态码验证

```gherkin
Then 响应状态码应为 200
```

### 2. 响应数据验证

```gherkin
And 响应数据中 "code" 应为 0
And 响应数据中 "data" 应包含 "users" 数组
And 响应数据中 "data.users[0].name" 应为 "张三"
```

### 3. JSONPath 表达式

支持使用 JSONPath 表达式验证响应数据：

- `$.data.users[0].name`: 获取第一个用户的名称
- `$.data.users[*].id`: 获取所有用户的 ID
- `$.data.users[?(@.age > 18)]`: 获取年龄大于 18 的用户

## 运行测试

### 1. 基本运行

```bash
# 运行所有 API 测试
behave features/ -D profile=test

# 运行特定特性文件
behave features/user_api.feature -D profile=test

# 运行特定场景
behave features/user_api.feature:10 -D profile=test
```

### 2. 并行测试

```bash
# 使用 4 个线程并行运行
python run_behave_parallel.py -n 4 -D profile=test
```

### 3. 生成报告

```bash
# 生成 Allure 报告
behave -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
```

## 最佳实践

### 1. 测试组织

- 按功能模块组织特性文件
- 使用标签分类测试场景
- 保持步骤定义的可重用性

生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    doc_path = docs_dir / "api_testing_guide.md"
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(api_guide)
    
    print(f"API 测试指南已生成: {doc_path}")
    return doc_path


def generate_web_testing_guide():
    """生成 Web 测试指南"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    web_guide = """# Web 测试指南

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
{
  "playwright": {
    "browser": {
      "type": "chromium",
      "headless": true,
      "slow_mo": 100,
      "timeout": 30000
    },
    "context": {
      "viewport": {
        "width": 1280,
        "height": 720
      },
      "ignore_https_errors": true,
      "accept_downloads": true
    },
    "trace": {
      "enabled": false,
      "screenshots": true,
      "snapshots": true,
      "sources": true
    },
    "video": {
      "enabled": false,
      "dir": "./test-results/videos"
    },
    "screenshot": {
      "enabled": true,
      "dir": "./test-results/screenshots",
      "full_page": true,
      "only_on_failure": true
    }
  },
  "test": {
    "base_url": "http://localhost:3000",
    "timeout": 10000,
    "retry": 2
  }
}
```

`web_elements.json`:
```json
{
  "login_page": {
    "username_input": {
      "id": "username"
    },
    "password_input": {
      "id": "password"
    },
    "login_button": {
      "css": "button[type='submit']"
    },
    "error_message": {
      "css": ".error-message"
    }
  },
  "home_page": {
    "user_menu": {
      "css": ".user-menu"
    },
    "logout_button": {
      "css": ".logout-button"
    },
    "welcome_message": {
      "css": ".welcome-message"
    }
  }
}
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
    \"\"\"启动浏览器\"\"\"
    context.is_web_test = True
    context.playwright_manager = PlaywrightManager()
    context.page = context.playwright_manager.start_browser()

@when('导航到 "{url}"')
def navigate_to_url(context, url):
    \"\"\"导航到指定 URL\"\"\"
    if not hasattr(context, 'playwright_manager') or not context.playwright_manager:
        raise RuntimeError("Playwright 管理器未初始化")
    
    context.playwright_manager.navigate_to(url)

@when('在 {page_name} 页面的 {element_name} 元素中输入 "{text}"')
def input_text(context, page_name, element_name, text):
    \"\"\"在指定元素中输入文本\"\"\"
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
context.page.evaluate(f"window.scrollBy(0, {pixels})")
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

生成时间: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
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

本文档介绍如何使用本项目进行 Android App 自动化测试，基于 Appium 和 Behave 框架。

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. Android 开发环境

- 安装 Android Studio
- 配置 ANDROID_HOME 环境变量
- 启用开发者选项和 USB 调试

### 3. Appium 服务器

```bash
# 安装 Appium
npm install -g appium

# 安装驱动
appium driver install uiautomator2

# 启动 Appium 服务器
appium
```

## 配置文件

在 `config/` 目录下创建 Android 相关配置：

`android_config.json`:
```json
{{
  "platformName": "Android",
  "platformVersion": "11",
  "deviceName": "Android Emulator",
  "automationName": "UiAutomator2",
  "appPackage": "com.example.app",
  "appActivity": ".MainActivity",
  "noReset": true,
  "fullReset": false,
  "newCommandTimeout": 300,
  "commandTimeouts": {{
    "default": 60000
  }}
}}
```

`android_elements.json`:
```json
{{
  "login_page": {{
    "username_input": {{
      "id": "com.example.app:id/username"
    }},
    "password_input": {{
      "id": "com.example.app:id/password"
    }},
    "login_button": {{
      "id": "com.example.app:id/login"
    }},
    "error_message": {{
      "id": "com.example.app:id/error"
    }}
  }},
  "home_page": {{
    "user_menu": {{
      "id": "com.example.app:id/user_menu"
    }},
    "logout_button": {{
      "id": "com.example.app:id/logout"
    }},
    "welcome_message": {{
      "id": "com.example.app:id/welcome"
    }}
  }}
}}
```

## 编写测试

### 1. 特性文件

```gherkin
Feature: 用户登录
  测试 Android App 的用户登录功能

  Background:
    Given 启动 Android App

  Scenario: 使用用户名密码登录成功
    When 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待 home_page 页面的 welcome_message 元素出现
    And 检查 home_page 页面的 welcome_message 元素包含文本 "欢迎"
```

### 2. 步骤定义

```python
from behave import given, when, then
from common.appium_manager import AppiumManager

@given('启动 Android App')
def launch_android_app(context):
    \"\"\"启动 Android App\"\"\"
    context.is_android_test = True
    context.appium_manager = AppiumManager()
    context.driver = context.appium_manager.connect()

@when('在 {page_name} 页面的 {element_name} 元素中输入 "{text}"')
def input_text(context, page_name, element_name, text):
    \"\"\"在指定元素中输入文本\"\"\"
    if not hasattr(context, 'appium_manager') or not context.appium_manager:
        raise RuntimeError("Appium 管理器未初始化")
    
    element = context.appium_manager.get_element(page_name, element_name)
    element.send_keys(text)
```

## 元素定位策略

### 1. 定位方式

- ID: `{"id": "com.example.app:id/element"}`
- XPath: `{"xpath": "//android.widget.TextView[@text='按钮']"}`
- Class Name: `{"class": "android.widget.Button"}`
- Accessibility ID: `{"accessibility_id": "login_button"}`

### 2. 元素等待

```python
def wait_for_element(driver, locator, timeout=10):
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
```

## 手势操作

### 1. 点击操作

```python
# 单击
element.click()

# 长按
from appium.webdriver.common.touch_action import TouchAction
actions = TouchAction(driver)
actions.long_press(element).release().perform()
```

### 2. 滑动操作

```python
# 滑动
driver.swipe(start_x, start_y, end_x, end_y, duration)

# 滚动
driver.scroll(origin_element, destination_element)
```

### 3. 多点触控

```python
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction

# 创建两个触摸动作
action1 = TouchAction(driver)
action2 = TouchAction(driver)

# 添加多点触控操作
multi_action = MultiAction(driver)
multi_action.add(action1).add(action2).perform()
```

## 运行测试

### 1. 基本运行

```bash
# 运行所有 Android 测试
behave features/android/ -D android_test=true

# 运行特定特性文件
behave features/android/features/login.feature -D android_test=true

# 运行特定场景
behave features/android/features/login.feature:10 -D android_test=true
```

### 2. 并行测试

```bash
# 使用 2 个线程并行运行
python run_behave_parallel.py -n 2 -D android_test=true features/android/
```

### 3. 生成报告

```bash
# 生成 Allure 报告
behave features/android/ -D android_test=true -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
```

## 最佳实践

### 1. 元素定位

- 优先使用资源 ID 定位
- 避免使用绝对 XPath
- 使用 Accessibility ID 提高可访问性

### 2. 测试数据管理

- 使用独立的测试环境
- 每次测试前清理应用数据
- 使用 Redis 管理测试状态

### 3. 设备兼容性

- 测试不同屏幕尺寸
- 测试不同 Android 版本
- 处理设备特定行为

### 4. 错误处理

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