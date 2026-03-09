Feature: REST API Demo
  REST API demo scenarios using mock API

  Background:
    Given 初始化测试环境

  Scenario: Get all posts
    When 发送 GET 请求到 "/api/posts"
    Then 检查 HTTP 状态码为 200
    Then 响应应该是一个数组

  Scenario: Get specific post
    When 发送 GET 请求到 "/api/posts/1"
    Then 检查 HTTP 状态码为 200
    Then 检查响应字段 "$.id" 等于 1
    Then 检查响应字段 "$.title" 不为空

  Scenario: Create new post
    When 发送 POST 请求到 "/api/posts"，请求体为:
    """
    {
      "title": "测试文章",
      "body": "这是一篇测试文章的内容",
      "userId": 1
    }
    """
    Then 检查 HTTP 状态码为 201
    Then 检查响应字段 "$.id" 不为空
    Then 检查响应字段 "$.title" 等于 "测试文章"

  Scenario: Update post
    When 发送 PUT 请求到 "/api/posts/1"，请求体为:
    """
    {
      "id": 1,
      "title": "更新后的标题",
      "body": "更新后的内容",
      "userId": 1
    }
    """
    Then 检查 HTTP 状态码为 200
    Then 检查响应字段 "$.id" 等于 1
    Then 检查响应字段 "$.title" 等于 "更新后的标题"

  Scenario: Delete post
    When 发送 DELETE 请求到 "/api/posts/1"
    Then 检查 HTTP 状态码为 200

  Scenario: Get user posts
    When 发送 GET 请求到 "/api/users/1/posts"
    Then 检查 HTTP 状态码为 200
    Then 响应应该是一个数组

  Scenario: Get post comments
    When 发送 GET 请求到 "/api/posts/1/comments"
    Then 检查 HTTP 状态码为 200
    Then 响应应该是一个数组

  Scenario: Get all users
    When 发送 GET 请求到 "/api/users"
    Then 检查 HTTP 状态码为 200
    Then 响应应该是一个数组

  Scenario: Create user
    When 发送 POST 请求到 "/api/users"，请求体为:
    """
    {
      "name": "测试用户",
      "email": "test@example.com",
      "phone": "13800138000"
    }
    """
    Then 检查 HTTP 状态码为 201
    Then 检查响应字段 "$.id" 不为空
    Then 检查响应字段 "$.name" 不为空
