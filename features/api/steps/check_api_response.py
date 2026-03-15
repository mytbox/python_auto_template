"""
通用 API 响应检查步骤
用于验证 API 返回结果的各项指标
"""
import json
import os
import logging
from datetime import datetime
from behave import then, given
from jsonpath_ng import parse
from common.dto.scenario_context import ScenarioContext
import requests

logger = logging.getLogger(__name__)


def _get_batch_check_results(context):
    """从场景上下文获取批量检查结果列表"""
    scenario_context: ScenarioContext = context.scenario_context
    if not hasattr(scenario_context, 'batch_check_results'):
        scenario_context.batch_check_results = []
    return scenario_context.batch_check_results


def _append_check_result(context, result_data):
    """追加单次检查结果到场景上下文"""
    results = _get_batch_check_results(context)
    results.append(result_data)
    context.scenario_context.batch_check_results = results


@then('检查HTTP状态码为{status_code:d}')
def check_http_status_code(context, status_code: int):
    """检查 HTTP 响应状态码"""
    scenario_context: ScenarioContext = context.scenario_context

    # 从上下文获取最近一次的响应
    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    logger.info(f"检查HTTP状态码: 期望={status_code}, 实际={response.status_code}")

    assert response.status_code == status_code, f"HTTP状态码不匹配: 期望 {status_code}, 实际 {response.status_code}"


@then('检查业务code为{business_code:d}')
def check_business_code(context, business_code: int):
    """检查响应中的业务 code 字段"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    logger.info(f"检查业务code: 期望={business_code}, 实际={response_data.get('code')}")

    assert 'code' in response_data, "响应中缺少 code 字段"
    assert response_data['code'] == business_code, f"业务code不匹配: 期望 {business_code}, 实际 {response_data['code']}"


@then('检查响应消息为"{message}"')
def check_response_message(context, message: str):
    """检查响应中的 msg 字段"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    logger.info(f"检查响应消息: 期望={message}, 实际={response_data.get('msg')}")

    assert 'msg' in response_data, "响应中缺少 msg 字段"
    assert response_data['msg'] == message, f"响应消息不匹配: 期望 '{message}', 实际 '{response_data['msg']}'"


@then('检查ok字段为{expected_value}')
def check_ok_field(context, expected_value: str):
    """检查响应中的 ok 字段"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    # 转换字符串 "true"/"false" 为布尔值
    actual_value = response_data.get('ok')
    expected_bool = expected_value.lower() in ('true', 'yes', '1')

    logger.info(f"检查ok字段: 期望={expected_bool}, 实际={actual_value}")

    assert 'ok' in response_data, "响应中缺少 ok 字段"
    assert actual_value == expected_bool, f"ok字段不匹配: 期望 {expected_bool}, 实际 {actual_value}"


@then('检查响应包含字段"{field_name}"')
def check_field_exists(context, field_name: str):
    """检查响应中是否包含指定字段"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    logger.info(f"检查响应包含字段: {field_name}")

    # 支持嵌套字段，如 "data.token"
    fields = field_name.split('.')
    current_data = response_data

    for field in fields:
        assert isinstance(current_data, dict), f"字段 {field} 的父级不是字典类型"
        assert field in current_data, f"响应中缺少字段: {field_name}"
        current_data = current_data[field]

    logger.info(f"字段 {field_name} 存在，值: {current_data}")


@then('检查字段"{field_name}"的值为"{expected_value}"')
def check_field_value(context, field_name: str, expected_value: str):
    """检查响应中指定字段的值"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    # 支持嵌套字段，如 "data.token"
    fields = field_name.split('.')
    current_data = response_data

    for field in fields:
        assert isinstance(current_data, dict), f"字段 {field} 的父级不是字典类型"
        assert field in current_data, f"响应中缺少字段: {field_name}"
        current_data = current_data[field]

    logger.info(f"检查字段 {field_name}: 期望={expected_value}, 实际={current_data}")

    # 尝试将期望值转换为数字进行比较
    try:
        if isinstance(current_data, (int, float)):
            expected_value = float(expected_value) if '.' in expected_value else int(expected_value)
    except ValueError:
        pass

    assert str(current_data) == str(expected_value), f"字段 {field_name} 值不匹配: 期望 {expected_value}, 实际 {current_data}"


@then('检查响应数据不为空')
def check_response_data_not_empty(context):
    """检查响应中的 data 字段不为空"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    logger.info("检查响应数据不为空")

    assert 'data' in response_data, "响应中缺少 data 字段"
    assert response_data['data'] is not None, "响应 data 字段为 None"

    # 如果 data 是字典或列表，检查是否为空
    if isinstance(response_data['data'], dict):
        assert len(response_data['data']) > 0, "响应 data 字典为空"
    elif isinstance(response_data['data'], list):
        assert len(response_data['data']) > 0, "响应 data 列表为空"

    logger.info(f"响应数据: {response_data['data']}")


@then('打印完整响应')
def print_full_response(context):
    """打印完整的 API 响应，用于调试"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        logger.warning("未找到 API 响应")
        return

    response = scenario_context.last_response

    logger.info("=" * 50)
    logger.info(f"HTTP状态码: {response.status_code}")
    logger.info(f"响应头: {dict(response.headers)}")
    logger.info(f"响应体: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    logger.info("=" * 50)


@then('保存响应字段"{field_name}"到上下文"{key_name}"')
def save_response_field_to_context(context, field_name: str, key_name: str):
    """将响应中的字段保存到场景上下文，供后续步骤使用"""
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response
    response_data = response.json()

    # 支持嵌套字段
    fields = field_name.split('.')
    current_data = response_data

    for field in fields:
        assert isinstance(current_data, dict), f"字段 {field} 的父级不是字典类型"
        assert field in current_data, f"响应中缺少字段: {field_name}"
        current_data = current_data[field]

    scenario_context.step_data[key_name] = current_data
    context.scenario_context = scenario_context

    logger.info(f"保存字段 {field_name} 的值到上下文 {key_name}: {current_data}")


# ========== 批量检查步骤 ==========

@then('批量检查 API 响应结果')
def batch_check_api_response(context):
    """
    通过 Examples 表格批量检查 API 响应

    Examples 表格格式:
      | Json path | 预期结果 | 判断类型 |
      | $.code    | 200      | equal    |
      | $.msg     | 成功     | contains |

    支持的判断类型:
      - equal: 等于（支持类型自动转换）
      - not_null: 不为空
      - contains: 包含字符串
      - greater_than: 大于
      - less_than: 小于
      - not_equal: 不等于
      - type: 类型检查
    """
    scenario_context: ScenarioContext = context.scenario_context

    if not hasattr(scenario_context, 'last_response'):
        raise AssertionError("未找到 API 响应，请先执行 API 请求")

    response = scenario_context.last_response

    # 尝试解析 JSON 响应
    try:
        response_data = response.json()
    except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
        # 非 JSON 响应，记录日志并抛出异常
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"响应不是 JSON 格式，状态码: {response.status_code}")
        logger.info(f"响应体内容: {response.text[:500] if response.text else '(空响应体)'}")
        raise AssertionError(f"响应不是 JSON 格式，无法进行字段检查。状态码: {response.status_code}，响应体: {response.text[:200] if response.text else '(空)'}")

    # 附加响应体到 Allure 报告
    try:
        import allure
        allure.attach(
            json.dumps(response_data, ensure_ascii=False, indent=2),
            name="响应体",
            attachment_type=allure.attachment_type.JSON
        )
    except ImportError:
        pass

    # 检查是否有 Examples 表格
    if not context.table:
        raise AssertionError("未找到 Examples 表格，请在 Scenario 中定义检查规则")

    # 统计检查结果
    total_checks = 0
    passed_checks = []
    failed_checks = []

    # 遍历 Examples 表格的每一行
    for row in context.table.rows:
        total_checks += 1
        json_path = row['检查字段']
        expected = row['预期结果']
        check_type = row['判断类型']

        try:
            # 使用 JSONPath 解析字段
            jsonpath_expression = parse(json_path)
            matches = jsonpath_expression.find(response_data)

            if not matches:
                raise AssertionError(f"JSONPath '{json_path}' 未匹配到任何值")

            actual_value = matches[0].value

            # 根据判断类型执行检查
            _check_by_type(actual_value, expected, check_type, json_path)
            passed_checks.append({
                'index': total_checks,
                'path': json_path,
                'type': check_type,
                'expected': expected,
                'actual': str(actual_value) if actual_value is not None else None
            })
        except AssertionError as e:
            failed_checks.append({
                'index': total_checks,
                'path': json_path,
                'type': check_type,
                'expected': expected,
                'reason': str(e)
            })

    # 构建单次检查结果数据
    result_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'step_name': '批量检查 API 响应结果',
        'total_checks': total_checks,
        'passed_count': len(passed_checks),
        'failed_count': len(failed_checks),
        'status': 'PASSED' if not failed_checks else 'FAILED',
        'api_response': response_data,
        'passed_checks': passed_checks,
        'failed_checks': failed_checks
    }

    # 追加结果到场景上下文
    _append_check_result(context, result_data)

    # 如果有失败的检查，抛出异常
    if failed_checks:
        failure_summary = "\n".join([
            f"[{c['index']}] {c['path']} ({c['type']}): {c['reason']}"
            for c in failed_checks
        ])
        raise AssertionError(f"批量检查有 {len(failed_checks)} 项失败:\n{failure_summary}")


def _check_by_type(actual, expected, check_type, path):
    """
    根据判断类型执行检查

    Args:
        actual: 实际值
        expected: 预期值（字符串形式，需要转换）
        check_type: 判断类型
        path: JSON 路径（用于错误信息）
    """
    if check_type == 'equal':
        # 等于（支持类型自动转换）
        expected = _convert_type(expected)
        assert actual == expected, f"期望 {expected} ({type(expected).__name__}), 实际 {actual} ({type(actual).__name__})"
    elif check_type == 'not_null':
        # 不为空
        assert actual is not None, f"值不应为空"
    elif check_type == 'contains':
        # 包含字符串
        assert isinstance(actual, str), f"实际值 {actual} 不是字符串类型，无法使用 contains 检查"
        assert expected in actual, f"'{actual}' 不包含 '{expected}'"
    elif check_type == 'greater_than':
        # 大于
        expected = _convert_type(expected)
        assert actual > expected, f"{actual} 不大于 {expected}"
    elif check_type == 'less_than':
        # 小于
        expected = _convert_type(expected)
        assert actual < expected, f"{actual} 不小于 {expected}"
    elif check_type == 'not_equal':
        # 不等于
        expected = _convert_type(expected)
        assert actual != expected, f"值不应等于 {expected}"
    elif check_type == 'type':
        # 类型检查
        type_map = {
            'str': str,
            'string': str,
            'int': int,
            'integer': int,
            'float': float,
            'bool': bool,
            'boolean': bool,
            'list': list,
            'dict': dict,
        }
        expected_type = type_map.get(expected.lower())
        if expected_type:
            assert isinstance(actual, expected_type), f"值类型应为 {expected}，实际为 {type(actual).__name__}"
        else:
            raise AssertionError(f"不支持的类型检查: {expected}")
    else:
        raise AssertionError(f"不支持的判断类型: {check_type}")


def _convert_type(value):
    """
    自动转换字符串值的类型

    Args:
        value: 字符串形式的值

    Returns:
        转换后的值（int/float/bool/str）
    """
    if value is None or value == '':
        return value

    # 布尔值转换
    if isinstance(value, str):
        lower_value = value.lower()
        if lower_value in ('true', 'yes'):
            return True
        if lower_value in ('false', 'no'):
            return False

    # 数字转换
    try:
        # 尝试转换为整数
        if '.' not in str(value):
            return int(value)
        else:
            # 尝试转换为浮点数
            return float(value)
    except (ValueError, TypeError):
        # 保持字符串
        return value