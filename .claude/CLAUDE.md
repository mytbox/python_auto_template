# Python BDD 测试自动化项目 - Claude 助手提示词

## 项目概述

这是一个基于 Python 的 BDD（行为驱动开发）测试自动化框架，使用 Behave 进行测试管理，Allure 生成测试报告。项目支持 API 测试、Android UI 测试和 Web UI 测试。

**Python 版本要求：3.12**

## 项目结构

```
python_auto_template/
├── config/                    # 配置文件目录
│   ├── config.py              # 配置管理模块
│   ├── test.json              # 测试环境配置
│   ├── dev.json               # 开发环境配置
│   └── android_*.json         # Android 测试配置
├── features/                  # Behave 特性文件
│   ├── environment.py         # Behave 环境钩子
│   ├── api/                   # API 测试
│   │   ├── features/          # .feature 文件
│   │   └── steps/             # 步骤定义
│   ├── android/               # Android UI 测试
│   │   ├── features/
│   │   └── steps/
│   └── web/                   # Web UI 测试
│       ├── features/
│       └── steps/
├── common/                    # 公共模块
│   ├── database/              # 数据库管理（Redis、MySQL）
│   ├── dto/                   # 数据传输对象
│   │   └── scenario_context.py # 场景上下文
│   ├── utils/                 # 工具类
│   ├── appium_manager.py      # Appium 管理器
│   ├── playwright_manager.py  # Playwright 管理器
│   └── element_locator.py     # 元素定位器
└── allure-results/            # Allure 测试结果
```

## 代码规范

### 1. 特性文件（.feature）

- 使用中文描述业务场景
- 遵循 Given-When-Then 格式
- 场景描述要具体明确

```gherkin
Feature: 功能名称
  功能描述

  Background:
    Given 初始化测试环境

  Scenario: 场景名称
    When 执行操作
    Then 验证结果
```

### 2. 步骤定义（steps/*.py）

- 步骤函数使用装饰器：`@given`、`@when`、`@then`
- 函数名使用下划线命名法
- 通过 `context.scenario_context` 传递数据
- 使用 logging 模块记录日志

```python
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext
import logging

logger = logging.getLogger(__name__)

@when('发送 GET 请求到 "{endpoint}"')
def send_get_request(context, endpoint):
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}{endpoint}"
    logger.info(f"Sending GET request: {url}")
    # ... 实现代码
```

### 3. 配置管理

- 使用 `ConfigManager` 类管理配置
- 通过 `-D profile=xxx` 切换环境
- 配置文件位于 `config/` 目录

```python
from config import init_behave_config, get_behave_config

# 在 environment.py 中初始化
config_manager = init_behave_config(context)
base_url = config_manager.get_base_url()
```

### 4. 场景上下文（ScenarioContext）

每个场景都有独立的 `ScenarioContext` 实例，用于存储：
- `base_url`: 基础 URL
- `apiClient`: requests.Session 实例
- `last_response`: 最后一次响应
- `step_data`: 步骤间传递的数据

## 测试运行命令

```bash
# 运行所有测试
behave

# 运行特定特性文件
behave features/api/features/api_demo.feature

# 指定环境配置
behave features/api/features/api_demo.feature -D profile=mock

# 运行 Android 测试
behave features/android/features/login.feature -D android_test=true

# 运行 Web 测试
behave features/web/features/home.feature -D web_test=true

# 生成 Allure 报告
behave -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report --clean
```

## 依赖管理

```bash
pip install -r requirements.txt
```

主要依赖：
- `behave`: BDD 测试框架
- `allure-behave`: Allure 报告集成
- `requests`: HTTP 请求
- `playwright`: Web UI 自动化
- `Appium-Python-Client`: Android UI 自动化
- `redis`: Redis 客户端
- `loguru`: 日志记录

## 编码规范

1. **文件编码**: 使用 UTF-8 编码
2. **导入顺序**: 标准库 -> 第三方库 -> 本地模块
3. **类型提示**: 使用类型注解提高代码可读性
4. **日志记录**: 使用 logging 模块，记录关键操作
5. **异常处理**: 合理处理异常，避免测试中断
6. **断言**: 使用 assert 语句，提供清晰的错误信息

## 测试开发流程

1. 在 `features/*/features/` 创建 .feature 文件
2. 在 `features/*/steps/` 创建对应的步骤定义
3. 运行测试验证功能
4. 生成 Allure 报告查看结果

## 注意事项

- Windows 环境需注意中文编码问题，已在 environment.py 中处理
- Android 测试需要 Appium 服务运行
- Web 测试需要安装 Playwright 浏览器：`playwright install`
- Redis 连接失败不会中断测试，但会记录错误日志