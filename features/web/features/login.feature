Feature: Web 用户登录
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

  Scenario: 登录失败-密码错误
    When 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "wrongpassword"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 检查 login_page 页面的 error_message 元素存在
    And 检查 login_page 页面的 error_message 元素包含文本 "用户名或密码错误"
    And 检查当前 URL 包含 "/login"

  Scenario: 登录失败-用户名为空
    When 导航到 "/login"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 检查 login_page 页面的 error_message 元素存在
    And 检查 login_page 页面的 error_message 元素包含文本 "用户名不能为空"

  Scenario: 登录失败-密码为空
    When 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 检查 login_page 页面的 error_message 元素存在
    And 检查 login_page 页面的 error_message 元素包含文本 "密码不能为空"

  Scenario: 登录后退出
    When 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成
    And 检查 home_page 页面的 welcome_message 元素存在
    When 点击 home_page 页面的 user_menu 元素
    And 等待 home_page 页面的 logout_button 元素加载完成
    And 点击 home_page 页面的 logout_button 元素
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/login"