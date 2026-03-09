# Android SDK命令行工具安装与使用指南

本文档介绍如何仅安装Android SDK命令行工具，无需安装完整的Android Studio IDE，即可运行Android模拟器。

## 目录
- [1. 下载Android SDK命令行工具](#1-下载android-sdk命令行工具)
- [2. 设置环境变量](#2-设置环境变量)
- [3. 安装必要组件](#3-安装必要组件)
- [4. 创建AVD（Android虚拟设备）](#4-创建avdandroid虚拟设备)
- [5. 启动模拟器](#5-启动模拟器)
- [6. 验证安装](#6-验证安装)
- [7. 常用系统镜像版本](#7-常用系统镜像版本)
- [8. 常用设备型号](#8-常用设备型号)
- [9. 启动多个模拟器](#9-启动多个模拟器)
- [10. 常见问题](#10-常见问题)

## 1. 下载Android SDK命令行工具

### Windows系统：
1. 访问 [Android Studio下载页面](https://developer.android.com/studio#command-tools)
2. 向下滚动找到"Command line tools only"部分
3. 下载"Command line tools for Windows"
4. 解压到一个目录，例如 `C:\android-sdk`

### macOS/Linux系统：
1. 同样访问上述页面
2. 下载对应的macOS或Linux版本
3. 解压到目录，例如 `~/android-sdk`

## 2. 设置环境变量

### Windows:
```cmd
set ANDROID_HOME=C:\android-sdk
set PATH=%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin;%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\emulator
```

或者永久设置（在系统环境变量中添加）：
- `ANDROID_HOME`: `C:\android-sdk`
- `PATH`: 添加 `%ANDROID_HOME%\cmdline-tools\latest\bin`、`%ANDROID_HOME%\platform-tools`、`%ANDROID_HOME%\emulator`

### macOS/Linux:
```bash
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator
```

## 3. 安装必要组件

打开命令行，执行以下命令：

```bash
# 1. 首先接受许可协议
sdkmanager --licenses

# 2. 安装platform-tools（包含adb等工具）
sdkmanager "platform-tools"

# 3. 安装emulator（模拟器）
sdkmanager "emulator"

# 4. 安装系统镜像（选择一个你需要的版本）
sdkmanager "system-images;android-31;google_apis;x86_64"
```

## 4. 创建AVD（Android虚拟设备）

```bash
# 创建一个名为test_emulator的AVD
echo "no" | avdmanager create avd -n test_emulator -k "system-images;android-31;google_apis;x86_64" -d "pixel_4"
```

## 5. 启动模拟器

```bash
# 启动模拟器（有界面）
emulator -avd test_emulator

# 启动模拟器（无界面，适合服务器环境）
emulator -avd test_emulator -no-window -no-boot-anim -no-audio

# 启动模拟器（指定端口）
emulator -avd test_emulator -port 5554
```

## 6. 验证安装

```bash
# 检查adb版本
adb version

# 列出所有AVD
emulator -list-avds

# 检查已连接的设备
adb devices
```

## 7. 常用系统镜像版本

你可以选择不同版本的系统镜像：

```bash
# Android 12 (API 32)
sdkmanager "system-images;android-32;google_apis;x86_64"

# Android 11 (API 30)
sdkmanager "system-images;android-30;google_apis;x86_64"

# Android 10 (API 29)
sdkmanager "system-images;android-29;google_apis;x86_64"

# Android 9 (API 28)
sdkmanager "system-images;android-28;google_apis;x86_64"
```

## 8. 常用设备型号

创建AVD时可以选择不同的设备型号：

```bash
# 查看所有可用设备
avdmanager list device

# 创建不同设备的AVD
avdmanager create avd -n pixel4 -k "system-images;android-31;google_apis;x86_64" -d "pixel_4"
avdmanager create avd -n pixel6 -k "system-images;android-31;google_apis;x86_64" -d "pixel_6"
avdmanager create avd -n nexus5x -k "system-images;android-31;google_apis;x86_64" -d "Nexus 5X"
```

## 9. 启动多个模拟器

```bash
# 在不同端口启动多个模拟器
emulator -avd test_emulator1 -port 5554 &
emulator -avd test_emulator2 -port 5556 &
emulator -avd test_emulator3 -port 5558 &

# 启动无界面模式的多个模拟器（适合服务器）
emulator -avd test_emulator1 -port 5554 -no-window -no-boot-anim -no-audio &
emulator -avd test_emulator2 -port 5556 -no-window -no-boot-anim -no-audio &
emulator -avd test_emulator3 -port 5558 -no-window -no-boot-anim -no-audio &
```

## 10. 常见问题

### 问题1：sdkmanager命令找不到
**解决方案**：确保已正确设置环境变量，特别是`ANDROID_HOME`和`PATH`

### 问题2：模拟器启动慢
**解决方案**：
- 使用硬件加速：添加`-gpu host`参数
- 使用无界面模式：添加`-no-window -no-boot-anim`参数
- 分配更多内存：在AVD配置中增加RAM大小

### 问题3：模拟器无法连接网络
**解决方案**：
- 添加`-dns-server 8.8.8.8`参数
- 检查防火墙设置

### 问题4：模拟器启动后adb devices看不到
**解决方案**：
- 等待更长时间让模拟器完全启动
- 使用`adb wait-for-device`命令等待设备就绪
- 检查模拟器端口是否被占用

## 优势

使用命令行工具而非完整Android Studio的优势：

1. **轻量级**：只需约500MB，而完整Android Studio需要几个GB
2. **适合服务器环境**：无GUI，完全通过命令行操作
3. **CI/CD友好**：易于自动化和脚本化
4. **资源占用少**：不需要运行完整的IDE

## 总结

通过以上步骤，你可以完全不需要安装Android Studio，只需要Android SDK命令行工具就可以运行Android模拟器。这种方式特别适合：
- 服务器环境
- CI/CD流水线
- 自动化测试
- 资源受限的环境

只需要几百MB的空间，就可以获得完整的Android模拟器功能。