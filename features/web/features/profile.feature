Feature: Web 个人资料页面
  测试 Web 应用的个人资料页面功能

  Background:
    Given 启动浏览器
    And 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 点击 navigation 页面的 profile_link 元素
    And 等待页面加载完成

  Scenario: 验证个人资料页面元素
    Then 检查当前 URL 包含 "/profile"
    And 检查 navigation 页面的 home_link 元素存在
    And 检查 navigation 页面的 profile_link 元素存在
    And 检查 navigation 页面的 settings_link 元素存在

  Scenario: 修改个人资料信息
    When 在 profile_page 页面的 email_input 元素中输入 "newemail@example.com"
    And 在 profile_page 页面的 phone_input 元素中输入 "1234567890"
    And 点击 profile_page 页面的 save_button 元素
    Then 等待页面加载完成
    And 检查 profile_page 页面的 success_message 元素存在
    And 检查 profile_page 页面的 success_message 元素包含文本 "保存成功"

  Scenario: 修改个人资料信息-邮箱格式错误
    When 在 profile_page 页面的 email_input 元素中输入 "invalid-email"
    And 在 profile_page 页面的 phone_input 元素中输入 "1234567890"
    And 点击 profile_page 页面的 save_button 元素
    Then 等待页面加载完成
    And 检查 profile_page 页面的 error_message 元素存在
    And 检查 profile_page 页面的 error_message 元素包含文本 "邮箱格式不正确"

  Scenario: 修改个人资料信息-手机号为空
    When 在 profile_page 页面的 email_input 元素中输入 "newemail@example.com"
    And 清空 profile_page 页面的 phone_input 元素
    And 点击 profile_page 页面的 save_button 元素
    Then 等待页面加载完成
    And 检查 profile_page 页面的 error_message 元素存在
    And 检查 profile_page 页面的 error_message 元素包含文本 "手机号不能为空"

  Scenario: 取消修改个人资料
    When 在 profile_page 页面的 email_input 元素中输入 "newemail@example.com"
    And 在 profile_page 页面的 phone_input 元素中输入 "1234567890"
    And 点击 profile_page 页面的 cancel_button 元素
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/profile"
    And 检查 profile_page 页面的 email_input 元素文本不为 "newemail@example.com"