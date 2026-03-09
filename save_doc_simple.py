"""
简化的项目文档生成脚本
用于生成项目相关的文档文件
"""

import os
import json
from pathlib import Path
from datetime import datetime


def generate_simple_docs():
    """生成简化版的项目文档"""
    project_root = Path(__file__).parent
    docs_dir = project_root / ".trae" / "documents"
    
    # 确保文档目录存在
    docs_dir.mkdir(parents=True, exist_ok=True)
    
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
    
    # 生成 Web 测试指南
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
```

## 运行测试

```bash
# 运行所有 Web 测试
behave features/web/ -D web_test=true

# 运行特定特性文件
behave features/web/features/login.feature -D web_test=true
```

## 配置文件

Web 测试使用以下配置文件：
- `config/web_config.json`: Playwright 浏览器配置
- `config/web_elements.json`: 页面元素定位配置

生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    web_doc_path = docs_dir / "web_testing_guide.md"
    with open(web_doc_path, 'w', encoding='utf-8') as f:
        f.write(web_guide)
    
    print(f"Web 测试指南已生成: {web_doc_path}")
    
    return [doc_path, web_doc_path]


def main():
    """主函数"""
    print("开始生成项目文档...")
    docs = generate_simple_docs()
    
    print("\n所有文档生成完成:")
    for doc in docs:
        print(f"  - {doc}")


if __name__ == "__main__":
    main()