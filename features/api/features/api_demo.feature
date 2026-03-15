Feature: REST API Demo
  REST API demo scenarios using static JSON files from GitHub Pages

  Background:
    Given 初始化测试环境

  Scenario: Get health check
    When 发送 GET 请求到 "/health"
    Then 检查 HTTP 状态码为 200
    Then 检查响应字段 "$.status" 等于 "ok"
