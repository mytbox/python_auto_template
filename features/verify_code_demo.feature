Feature: Verification Code Functionality Demo
  Verification code functionality demo scenarios using mock API

  Background:
    Given 初始化测试环境

  Scenario: Send email verification code successfully
    Then 获取邮箱验证码test@example.com
    Then 批量检查 API 响应结果
      | 检查字段   | 预期结果      | 判断类型  |
      | $.code | 200       | equal |
      | $.msg  | 邮箱验证码发送成功 | equal |
      | $.ok   | true      | equal |

  Scenario: Send SMS verification code successfully
    Then 发送短信验证码到"13800138000"
    Then 批量检查 API 响应结果
      | 检查字段       | 预期结果 | 判断类型 |
      | $.code         | 200      | equal |
      | $.data.success | true     | equal |

  Scenario: Send verification code with missing phone number
    Then 发送短信验证码到动态手机号，国家编码为"86"
    Then 批量检查 API 响应结果
      | 检查字段 | 预期结果     | 判断类型 |
      | $.code   | 500      | equal    |
      | $.msg    |          | not_null |

  Scenario: Verify SMS code successfully
    Then 发送短信验证码到"13800138000"
    Then 从Redis获取短信验证码
    Then 验证短信验证码
    Then 批量检查 API 响应结果
      | 检查字段            | 预期结果 | 判断类型 |
      | $.code              | 200      | equal    |
      | $.data.verifyResult | PASS     | equal    |

  Scenario: Verify SMS code with invalid code
    Then 发送短信验证码到"13800138000"
    Then 从Redis获取短信验证码
    Then 使用指定验证码"000000"验证
    Then 批量检查 API 响应结果
      | 检查字段 | 预期结果       | 判断类型 |
      | $.code   | 500            | equal    |
      | $.msg    | 短信验证码无效 | contains |
