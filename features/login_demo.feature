Feature: Login Functionality Demo
  Login functionality demo scenarios using mock API

  Background:
    Given 初始化测试环境

  Scenario: Email login success
    Then 获取邮箱验证码test@example.com
    Then 用邮箱验证码获取token
    Then 批量检查 API 响应结果
      | 检查字段             | 预期结果             | 判断类型     |
      | $.code           | 200              | equal    |
      | $.data.accountId |          | not_null |
      | $.data.token     | string           | type     |

  Scenario: SMS login success
    Then 发送短信验证码到"13800138000"
    Then 从Redis获取短信验证码
    Then 使用短信验证码登录
    Then 批量检查 API 响应结果
      | 检查字段         | 预期结果 | 判断类型 |
      | $.code           | 200      | equal    |
      | $.data.accountId |          | not_null |
      | $.data.token     |          | not_null |

  Scenario: Login with invalid verification code
    Then 获取邮箱验证码test@example.com
    Then 使用指定验证码"000000"登录
    Then 批量检查 API 响应结果
      | 检查字段 | 预期结果       | 判断类型 |
      | $.code   | 500            | equal    |
      | $.msg    | 验证码无效 | contains |

  Scenario: Login with missing email
    Then 获取邮箱验证码test@example.com
    Then 使用邮箱验证码登录邮箱为空
    Then 批量检查 API 响应结果
      | 检查字段 | 预期结果     | 判断类型 |
      | $.code   | 500          | equal    |
      | $.msg    | 邮箱不能为空 | equal    |

  Scenario: Login with missing verification code
    Then 获取邮箱验证码test@example.com
    Then 使用邮箱验证码登录验证码为空
    Then 批量检查 API 响应结果
      | 检查字段 | 预期结果       | 判断类型 |
      | $.code   | 500            | equal    |
      | $.msg    | 验证码不能为空 | equal    |
