Feature: 首页功能
  测试 Android App 的首页功能

  Background:
    Given 启动 Android App
    And 等待元素可见,定位方式为"id"值为"com.example.app:id/home_container"

  Scenario: 验证首页元素显示
    Then 验证元素存在,定位方式为"id"值为"com.example.app:id/home_title"
    And 验证元素存在,定位方式为"id"值为"com.example.app:id/banner_view"
    And 验证元素存在,定位方式为"id"值为"com.example.app:id/function_list"

  Scenario: 点击功能菜单
    When 点击元素,定位方式为"id"值为"com.example.app:id/menu_item_1"
    Then 等待元素可见,定位方式为"id"值为"com.example.app:id/detail_container"
    And 验证元素文本为"功能详情",定位方式为"id"值为"com.example.app:id/detail_title"

  Scenario: 滑动首页
    When 向上滑动
    And 等待 "1" 秒
    And 向下滑动
    Then 验证元素存在,定位方式为"id"值为"com.example.app:id/home_container"
