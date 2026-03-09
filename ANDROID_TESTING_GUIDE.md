# Android App 测试使用指南

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 安装 Appium Server

```bash
npm install -g appium
npm install -g appium-doctor
```

### 3. 配置 Android 环境

- 安装 Android SDK
- 配置 ANDROID_HOME 环境变量
- 启动 Android 模拟器或连接真机
- 启用 USB 调试(真机测试时)

### 4. 验证环境

```bash
appium-doctor --android
```

## 配置文件

### 1. Appium 配置文件

编辑 `config/android_config.json`:

```json
{
  "appium_server": {
    "host": "127.0.0.1",
    "port": 4723,
    "base_path": "/wd/hub"
  },
  "device": {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "emulator-5554",
    "appPackage": "com.example.app",
    "appActivity": ".MainActivity",
    "noReset": true,
    "fullReset": false,
    "unicodeKeyboard": true,
    "resetKeyboard": true,
    "autoGrantPermissions": true,
    "newCommandTimeout": 300
  }
}
```

### 2. 设备能力配置文件

编辑 `config/android_capabilities.json`:

```json
{
  "devices": [
    {
      "name": "emulator-5554",
      "platformName": "Android",
      "automationName": "UiAutomator2",
      "deviceName": "emulator-5554",
      "platformVersion": "12",
      "appPackage": "com.example.app",
      "appActivity": ".MainActivity"
    }
  ]
}
```

### 3. 元素定位配置文件

编辑 `config/android_elements.json`:

```json
{
  "login_page": {
    "phone_input": {
      "type": "id",
      "value": "com.example.app:id/phone_input"
    },
    "login_button": {
      "type": "id",
      "value": "com.example.app:id/login_button"
    }
  }
}
```

## 运行测试

### 启动 Appium Server

```bash
appium
```

### 运行 Android 测试

```bash
# 运行所有 Android 测试
behave features/android/ -D android_test=true

# 运行特定特性文件
behave features/android/features/login.feature -D android_test=true

# 运行特定场景
behave features/android/features/login.feature:9 -D android_test=true

# 生成 Allure 报告
behave features/android/ -D android_test=true -f allure_behave.formatter:AllureFormatter -o ./allure-results
allure generate ./allure-results -o ./allure-report
allure open ./allure-report
```

### 并行运行测试

```bash
# 使用 4 个线程并行运行
behave-parallel -n 4 -D android_test=true features/android/
```

## 编写测试用例

### 特性文件示例

```gherkin
Feature: 用户登录
  测试 Android App 的用户登录功能

  Background:
    Given 启动 Android App

  Scenario: 使用手机号登录成功
    When 点击登录按钮
    And 输入手机号 "13800138000"
    And 点击获取验证码按钮
    And 等待 "3" 秒
    And 输入验证码 "123456"
    And 点击确认登录
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/user_avatar"
    And 验证登录成功
```

### 可用步骤

#### 通用步骤

- `启动 Android App` - 启动 Android App
- `启动 Android App 并使用设备"{device_name}"` - 使用指定设备启动 App
- `关闭 Android App` - 关闭 Android App
- `重启 Android App` - 重启 Android App
- `按返回键` - 按返回键
- `按 Home 键` - 按 Home 键
- `按 Enter 键` - 按 Enter 键
- `等待"{timeout}"秒` - 等待指定秒数
- `截图` - 截图
- `截图并保存为"{filename}"` - 截图并保存为指定文件名

#### 元素操作步骤

- `点击元素,定位方式为"{by}"值为"{value}"` - 点击元素
- `点击元素"{element_name}"` - 通过元素名称点击元素
- `在元素中输入文本"{text}",定位方式为"{by}"值为"{value}"` - 在元素中输入文本
- `在元素"{element_name}"中输入文本"{text}"` - 通过元素名称输入文本
- `清空元素内容,定位方式为"{by}"值为"{value}"` - 清空元素内容
- `验证元素文本为"{expected_text}",定位方式为"{by}"值为"{value}"` - 验证元素文本
- `验证元素存在,定位方式为"{by}"值为"{value}"` - 验证元素存在
- `验证元素可见,定位方式为"{by}"值为"{value}"` - 验证元素可见

#### 手势操作步骤

- `向左滑动` - 向左滑动
- `向右滑动` - 向右滑动
- `向上滑动` - 向上滑动
- `向下滑动` - 向下滑动
- `从坐标({start_x},{start_y})滑动到坐标({end_x},{end_y}),持续{duration}毫秒` - 从坐标滑动到坐标
- `长按元素,定位方式为"{by}"值为"{value}",持续{duration}毫秒` - 长按元素
- `双击元素,定位方式为"{by}"值为"{value}"` - 双击元素
- `滚动到元素,定位方式为"{by}"值为"{value}"` - 滚动到元素

#### 验证步骤

- `验证当前 Activity 为"{activity}"` - 验证当前 Activity
- `验证当前包名为"{package}"` - 验证当前包名
- `验证元素存在,定位方式为"{by}"值为"{value}"` - 验证元素存在
- `验证元素不存在,定位方式为"{by}"值为"{value}"` - 验证元素不存在
- `验证元素可见,定位方式为"{by}"值为"{value}"` - 验证元素可见
- `验证元素不可见,定位方式为"{by}"值为"{value}"` - 验证元素不可见

### 定位方式

支持的定位方式:
- `id` - 通过 ID 定位
- `xpath` - 通过 XPath 定位
- `class_name` - 通过类名定位
- `accessibility_id` - 通过 Accessibility ID 定位
- `android_uiautomator` - 通过 Android UIAutomator 定位

## 元素定位

### 使用元素名称

在 `config/android_elements.json` 中定义元素:

```json
{
  "login_page": {
    "phone_input": {
      "type": "id",
      "value": "com.example.app:id/phone_input"
    }
  }
}
```

然后在测试中使用:

```gherkin
When 点击元素"phone_input"
And 在元素"phone_input"中输入文本"13800138000"
```

### 直接使用定位方式

```gherkin
When 点击元素,定位方式为"id"值为"com.example.app:id/phone_input"
And 在元素中输入文本"13800138000",定位方式为"id"值为"com.example.app:id/phone_input"
```

## Allure 报告

测试完成后会自动生成 Allure 报告,包含:
- 测试执行结果
- 截图(失败时自动截图)
- 设备信息
- 步骤详情

查看报告:

```bash
allure open ./allure-report
```

## 常见问题

### 1. Appium 连接失败

检查 Appium Server 是否启动:

```bash
appium
```

检查设备是否连接:

```bash
adb devices
```

### 2. 元素定位失败

使用 Appium Inspector 查看元素信息:

```bash
appium-inspector
```

### 3. 测试超时

在 `config/android_config.json` 中调整超时时间:

```json
{
  "wait": {
    "implicit_wait": 10,
    "explicit_wait": 20,
    "page_load_timeout": 30
  }
}
```

### 4. 中文输入问题

确保配置中启用了 Unicode 键盘:

```json
{
  "unicodeKeyboard": true,
  "resetKeyboard": true
}
```

## 最佳实践

1. **使用元素名称而非直接定位** - 便于维护和重用
2. **添加适当的等待** - 避免因页面加载慢导致的失败
3. **使用显式等待** - 比隐式等待更可靠
4. **失败时自动截图** - 便于问题排查
5. **使用页面对象模式** - 提高代码可维护性
6. **定期更新元素定位** - App 更新后元素可能变化
7. **使用并行测试** - 提高测试效率
8. **保持测试独立性** - 每个测试应该可以独立运行

## 项目结构

```
features/
├── android/                    # Android App 测试目录
│   ├── features/               # Android 特性文件
│   │   ├── login.feature      # 登录功能测试
│   │   ├── home.feature       # 首页功能测试
│   │   └── profile.feature    # 个人中心测试
│   └── steps/                 # Android 步骤定义
│       ├── android_step.py    # Android 通用步骤
│       ├── element_step.py    # 元素操作步骤
│       └── gesture_step.py    # 手势操作步骤
common/
├── appium_manager.py         # Appium 驱动管理器
├── element_locator.py        # 元素定位工具类
└── device_pool.py           # 设备池管理器
config/
├── android_config.json       # Appium 配置文件
├── android_capabilities.json # 设备能力配置
└── android_elements.json    # 元素定位配置
```

## 下一步

- 根据实际 App 修改元素定位配置
- 编写更多测试用例覆盖主要功能
- 配置 CI/CD 自动运行测试
- 集成云测试平台(如 BrowserStack)
- 添加性能监控指标
