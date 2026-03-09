# Python BDD 测试自动化项目

这是一个基于 Python 的测试自动化项目，使用 Behave 进行 BDD（行为驱动开发）测试管理和 Allure 生成测试报告。

# 项目要用 python 3.12版本

## 项目结构

```
python-bdd/
├── allure-results/          # Allure 测试结果
├── allure-report/           # Allure 生成的 HTML 报告
├── config/                  # 配置文件目录
│   ├── test.json            # 测试环境配置
│   ├── dev.json             # 开发环境配置
│   ├── mock.json            # 模拟 API 环境配置
│   └── config.py            # 配置管理模块
├── features/                # Behave 特性文件
│   ├── login_demo.feature      # 登录功能演示
│   ├── verify_code_demo.feature # 验证码功能演示
│   ├── api_demo.feature       # REST API 演示
│   ├── environment.py         # Behave 环境配置
│   └── steps/               # 步骤定义
│       ├── login_demo_step.py       # 登录步骤定义
│       ├── verify_code_demo_step.py # 验证码步骤定义
│       └── api_demo_step.py        # API 步骤定义
├── mock_api/                # 模拟 API 服务器
│   └── server.py           # Flask 模拟 API 服务器
├── common/                  # 公共模块
│   ├── database/            # 数据库管理
│   ├── dto/                 # 数据传输对象
│   └── utils/               # 工具类
└── readme.md                # 项目说明
```

## 依赖安装

```bash
pip install -r requirements.txt

# 导出依赖关系
pip freeze > requirements.txt
```

或者如果还没有 requirements.txt：

```bash
pip install behave requests allure-behave loguru redis
```

## Behave 测试运行

### 基本命令

```bash
# 运行所有特性文件
behave

# 运行特定特性文件
behave features/login_demo.feature

# 运行特定场景（按行号）
behave features/login_demo.feature:9

# 指定环境配置
behave features/account.feature -D profile=dev

# 带详细输出
behave -v

# 显示步骤定义
behave --format=pretty
```

### Allure 报告集成
# 运行测试并生成 Allure 结果
```bash
behave features/account.feature -D profile=test -f allure_behave.formatter:AllureFormatter -o ./allure-results
```

```bash
# 生成可视化报告
allure generate ./allure-results -o ./allure-report
```

```bash
# 打开报告
allure open ./allure-report
```

```bash
# 清理旧结果并重新生成报告
allure generate ./allure-results -o ./allure-report --clean
```

```bash
# 安装并运行
pip install behave-parallel
behave-parallel -n 4 -f progress2 features/

```

## 配置说明

项目使用配置文件管理不同环境的设置：
- `config/test.json` - 测试环境配置
- `config/dev.json` - 开发环境配置
- `config/mock.json` - 模拟 API 环境配置
- `config/config.py` - 配置管理模块

### 配置文件格式

```json
{
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "base_url": "https://api.example.com"
}
```

### 环境切换

通过 Behave 的 `-D profile=` 参数切换不同环境：

```bash
# 使用测试环境配置
behave features/account.feature

# 使用开发环境配置
behave features/account.feature -D profile=dev

# 使用模拟 API 环境配置
behave features/account.feature -D profile=mock
```

## 模拟 API 服务器

项目包含一个本地模拟 API 服务器，用于测试时无需依赖外部系统。

### 启动模拟 API 服务器

**Windows:**
```bash
start_mock_api.bat
```

**Linux/Mac:**
```bash
chmod +x start_mock_api.sh
./start_mock_api.sh
```

**或者直接运行:**
```bash
python mock_api/server.py
```

模拟 API 服务器将在 `http://127.0.0.1:48080` 上运行。

### 模拟 API 功能

模拟 API 服务器提供以下端点：

#### 账户相关
- `POST /account/send-verify-code` - 发送验证码（支持邮箱和手机号）
- `POST /account/reg-ai-login` - 使用验证码登录

#### 用户相关
- `GET /api/users` - 获取所有用户
- `GET /api/users/<id>` - 获取指定用户
- `POST /api/users` - 创建用户

#### 文章相关（JSONPlaceholder 兼容）
- `GET /api/posts` - 获取所有文章
- `GET /api/posts/<id>` - 获取指定文章
- `POST /api/posts` - 创建文章
- `PUT /api/posts/<id>` - 更新文章
- `DELETE /api/posts/<id>` - 删除文章
- `GET /api/users/<id>/posts` - 获取用户的文章
- `GET /api/posts/<id>/comments` - 获取文章的评论
- `GET /api/comments` - 获取所有评论

#### 健康检查
- `GET /health` - 健康检查端点

### 使用模拟 API 进行测试

1. 启动模拟 API 服务器
2. 使用 mock 配置运行测试：
   ```bash
   behave features/account.feature -D profile=mock
   ```
3. 模拟 API 会自动处理验证码生成和验证

## Demo 测试文件

项目包含三个主要的 demo 测试文件，用于演示不同类型的 API 测试：

### 1. login_demo.feature - 登录功能演示
演示邮箱和短信验证码登录功能，包括：
- 邮箱验证码登录成功
- 短信验证码登录成功
- 验证码错误场景
- 缺少必填参数场景

运行方式：
```bash
behave features/login_demo.feature -D profile=mock
```

### 2. verify_code_demo.feature - 验证码功能演示
演示验证码发送和验证功能，包括：
- 发送邮箱验证码
- 发送短信验证码
- 验证码验证成功
- 验证码验证失败

运行方式：
```bash
behave features/verify_code_demo.feature -D profile=mock
```

### 3. api_demo.feature - REST API 演示
演示标准 REST API 操作，包括：
- GET 请求（获取文章、用户、评论）
- POST 请求（创建文章、用户）
- PUT 请求（更新文章）
- DELETE 请求（删除文章）

运行方式：
```bash
behave features/api_demo.feature -D profile=mock
```

## 主要功能

- BDD 行为驱动测试（Behave）
- Allure 报告集成
- Redis 数据库集成
- 多环境配置管理
- 自动化测试流程
- 本地模拟 API 服务器

## 测试开发规范

### 特性文件（.feature）
- 使用中文描述业务场景
- 遵循 Given-When-Then 格式
- 场景描述要具体明确

### 步骤定义（steps/*.py）
- 步骤函数使用装饰器：@given, @when, @then
- 函数名要与步骤描述匹配
- 通过 context 对象传递数据

### 环境配置（environment.py）
- before_all: 全局初始化
- before_scenario: 场景初始化
- after_scenario: 场景清理
