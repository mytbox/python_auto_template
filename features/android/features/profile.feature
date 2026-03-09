Feature: 个人中心
  测试 Android App 的个人中心功能

  Background:
    Given 启动 Android App
    And 等待元素可见,定位方式为"id"值为"com.example.app:id/main_container"
    When 点击元素,定位方式为"id"值为"com.example.app:id/profile_tab"

  Scenario: 验证个人中心信息
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/profile_container"
    And 验证元素存在,定位方式为"id"值为"com.example.app:id/user_avatar"
    And 验证元素存在,定位方式为"id"值为"com.example.app:id/user_name"
    And 验证元素存在,定位方式为"id"值为"com.example.app:id/user_phone"

  Scenario: 修改用户昵称
    When 点击元素,定位方式为"id"值为"com.example.app:id/edit_profile_button"
    And 等待元素可见,定位方式为"id"值为"com.example.app:id/edit_name_input"
    And 清空元素内容,定位方式为"id"值为"com.example.app:id/edit_name_input"
    And 在元素中输入文本"测试用户",定位方式为"id"值为"com.example.app:id/edit_name_input"
    And 点击元素,定位方式为"id"值为"com.example.app:id/save_button"
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/profile_container"
    And 验证元素文本为"测试用户",定位方式为"id"值为"com.example.app:id/user_name"

  Scenario: 退出登录
    When 点击元素,定位方式为"id"值为"com.example.app:id/logout_button"
    And 等待元素可见,定位方式为"id"值为"com.example.app:id/logout_confirm_button"
    And 点击元素,定位方式为"id"值为"com.example.app:id/logout_confirm_button"
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/login_container"
    And 验证当前 Activity 为".LoginActivity"
