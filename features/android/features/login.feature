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

  Scenario: 登录失败-验证码错误
    When 点击登录按钮
    And 输入手机号 "13800138000"
    And 点击获取验证码按钮
    And 等待 "3" 秒
    And 输入验证码 "000000"
    And 点击确认登录
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/error_message"
    And 验证元素文本为"验证码错误",定位方式为"id"值为"com.example.app:id/error_message"

  Scenario: 登录失败-手机号为空
    When 点击登录按钮
    And 点击确认登录
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/error_message"
    And 验证元素文本为"请输入手机号",定位方式为"id"值为"com.example.app:id/error_message"
