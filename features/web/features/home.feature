Feature: Web 首页功能
  测试 Web 应用的首页功能

  Background:
    Given 启动浏览器
    And 导航到 "/login"
    And 在 login_page 页面的 username_input 元素中输入 "testuser"
    And 在 login_page 页面的 password_input 元素中输入 "password123"
    And 点击 login_page 页面的 login_button 元素
    Then 等待页面加载完成

  Scenario: 验证首页导航链接
    And 检查 navigation 页面的 home_link 元素存在
    And 检查 navigation 页面的 profile_link 元素存在
    And 检查 navigation 页面的 settings_link 元素存在

  Scenario: 导航到个人资料页面
    When 点击 navigation 页面的 profile_link 元素
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/profile"

  Scenario: 导航到设置页面
    When 点击 navigation 页面的 settings_link 元素
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/settings"

  Scenario: 导航回首页
    When 点击 navigation 页面的 profile_link 元素
    And 等待页面加载完成
    And 点击 navigation 页面的 home_link 元素
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/home"

  Scenario: 验证页面滚动功能
    When 滚动到页面底部
    And 等待 2 秒
    And 滚动到页面顶部
    And 等待 2 秒
    Then 检查 home_page 页面的 welcome_message 元素可见

  Scenario: 验证浏览器导航功能
    When 点击 navigation 页面的 profile_link 元素
    And 等待页面加载完成
    And 点击浏览器后退按钮
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/home"
    When 点击浏览器前进按钮
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/profile"
    And 刷新当前页面
    Then 等待页面加载完成
    And 检查当前 URL 包含 "/profile"