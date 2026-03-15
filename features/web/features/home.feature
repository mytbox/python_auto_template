Feature: Web Automation Demo Page
  Test docs/mock/html/index.html page

  Scenario: Verify Home Page
    Given 启动 chromium 浏览器（有头模式）
    # When 导航到 "file:///D:/githup_home/python_auto_template/docs/mock/html/index.html"
    # Then 页面标题应为 "Web 自动化测试演示页面"
    # And 检查 home 页面的 welcome_message 元素可见

  Scenario: Navigation Test
    Given 启动 chromium 浏览器（有头模式）
    When 导航到 "file:///D:/githup_home/python_auto_template/docs/mock/html/index.html"
    And 点击 home 页面的 nav_register 元素
    Then 检查 register 页面的 form 元素可见

  Scenario: Login Test
    Given 启动 chromium 浏览器（有头模式）
    When 导航到 "file:///D:/githup_home/python_auto_template/docs/mock/html/index.html"
    And 点击 home 页面的 login_link 元素
    Then 检查 login 页面的 modal 元素可见

  Scenario: Dropdown Test
    Given 启动 chromium 浏览器（有头模式）
    When 导航到 "file:///D:/githup_home/python_auto_template/docs/mock/html/index.html"
    And 点击 home 页面的 nav_dropdown 元素
    And 点击 dropdown 页面的 city_select_button 元素
    And 点击 dropdown 页面的 city_beijing 元素
    Then 检查 dropdown 页面的 city_select_button 元素包含文本 "北京"
