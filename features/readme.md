# Python BDD 测试自动化框架

这是一个基于 Python Behave 的行为驱动开发测试框架，用于测试自动化项目。

## 项目概述

本项目使用 Behave 框架，实现了行为驱动开发（BDD）的测试自动化方案。通过 Gherkin 语言编写的特性文件（Feature Files）来描述业务需求和验收标准。

## 项目结构

```
python-bdd/
├── features/                # BDD 特性文件
│   ├── readme.md            # 本说明文件
│   └── *.feature            # Gherkin 特性文件
├── features/steps/          # 步骤定义
│   └── *.py                 # Python 步骤实现
├── allure-results/          # Allure 测试结果
├── allure-report/           # Allure 生成的 HTML 报告
├── common/                  # 公共组件
│   ├── database/            # 数据库管理
│   ├── dto/                 # 数据传输对象
│   └── utils/               # 工具类
├── config/                  # 配置文件
├── requirements.txt         # 依赖包列表
```

## 环境要求

- Python 3.12 或更高版本
- pip 包管理器

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd python-bdd
```

### 2. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖包括：
- `behave==1.3.3` - BDD 测试框架
- `allure-behave==2.15.3` - Allure 报告集成
- `requests` - HTTP 客户端库
- `loguru` - 日志库
- `redis` - Redis 客户端

## 运行测试

### 1. 运行所有 Behave 测试

```bash
# 基本运行
behave

# 带详细输出
behave -v

# 运行特定特性文件
behave features/jsonplaceholder_api.feature

# 运行特定场景（通过标签）
behave --tags=@smoke
behave --tags=@regression
```

### 2. 使用 Tag Expressions

Behave 支持复杂的标签表达式，参考文档：https://behave.readthedocs.io/en/latest/tag_expressions/

```bash
# AND 运算
behave --tags="@tag1 and @tag2"

# OR 运算
behave --tags="@tag1 or @tag2"

# NOT 运算
behave --tags="not @wip"

# 复杂表达式
behave --tags="(@smoke or @regression) and not @slow"
```

## 特性文件（Feature Files）

特性文件使用 Gherkin 语法编写，位于 `features/` 目录下：

```gherkin
Feature: 登录功能
  作为一个用户
  我希望能够在应用中登录
  以便访问我的个人资料

  Scenario: 成功登录
    Given 我在登录页面
    When 我输入有效的邮箱和密码
    And 我点击登录按钮
    Then 我应该被重定向到主页
    And 我应该看到欢迎消息
```

## 步骤定义（Step Definitions）

步骤定义位于 `features/steps/` 目录下：

```python
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext


@given('我在登录页面')
def step_impl(context):
    # 初始化场景上下文
    context.scenario_context = ScenarioContext()


@when('我输入有效的邮箱和密码')
def step_impl(context):
    # 执行登录操作
    pass


@then('我应该被重定向到主页')
def step_impl(context):
    # 验证登录结果
    assert context.scenario_context.apiToken is not None
```

## Allure 报告

### 生成 Allure 报告

```bash
# 运行测试并生成 Allure 结果
behave --format=allure_behave.formatter:AllureFormatter --output-directory=./allure-results

# 生成 HTML 报告
allure generate ./allure-results -o ./allure-report

# 打开报告
allure open ./allure-report
```

## 配置说明

### Behave 配置

Behave 支持 `behave.ini`、`setup.cfg` 或 `pyproject.toml` 配置文件：

```ini
[behave]
show_timings = true
show_skipped = false
quiet = false
lang = en
format = pretty
color = true
```

### 环境配置

在 `environment.py` 文件中可以配置测试环境：

```python
def before_all(context):
    # 设置全局配置
    pass

def before_feature(context, feature):
    # 特性开始前的设置
    pass

def after_scenario(context, scenario):
    # 场景结束后的清理
    pass
```

## 数据传递

BDD 测试中，数据通过 context 对象在步骤间传递：

```python
# 在步骤A中设置数据
context.user_email = "test@example.com"

# 在后续步骤中使用数据
assert context.user_email == "test@example.com"
```

## 最佳实践

1. **清晰的特性描述**：每个特性文件应该专注于单一功能
2. **有意义的场景名称**：场景标题应该清楚描述测试目的
3. **独立的场景**：每个场景应该能够独立运行
4. **使用标签组织测试**：通过标签分类不同类型测试（@smoke, @regression, @wip）
5. **避免重复步骤**：提取公共步骤到背景部分（Background）

## 常见问题

### Q: 如何调试 Behave 测试？
A: 添加 `-D` 参数启用调试模式：
```bash
behave -D
```

### Q: 如何只运行失败的场景？
A: 使用 `--rerun` 功能或标签过滤：
```bash
behave --tags="@failed"
```

### Q: 如何设置测试数据？
A: 在 `environment.py` 中设置全局数据或在场景中使用 Given 步骤准备数据。

## 项目规则

```shell
behave 自动化测试必须要遵守的规则。
1. features 目录下是 behave 自动化测试的相关文件
2. steps 目录下是 behave 自动化测试的步骤定义文件
3. environment.py 文件是 behave 自动化测试的配置文件
4. common 这个是公共模块，behave 和其他框架都可以使用。
5. config 这个是配置文件目录。
```

## 参考资源

- [Behave 官方文档](https://behave.readthedocs.io/)
- [Gherkin 语法指南](https://cucumber.io/docs/gherkin/)
- [Allure 报告文档](https://docs.qameta.io/allure/)
- [Tag Expressions 文档](https://behave.readthedocs.io/en/latest/tag_expressions/)
