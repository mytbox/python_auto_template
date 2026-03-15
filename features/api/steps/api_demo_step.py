"""
API Demo Step Definitions for Static JSON Files
适配静态 JSON 文件方式的 API 测试步骤
"""
import allure
import logging
import requests
import json
from urllib.parse import quote
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext

logger = logging.getLogger(__name__)


def _get_static_file_path(method: str, endpoint: str) -> str:
    """
    将 RESTful API 路径转换为静态文件路径

    Args:
        method: HTTP 方法 (GET, POST, PUT, DELETE)
        endpoint: API 端点，如 "/health", "/api/posts/1"

    Returns:
        静态文件路径，如 "/health/get.json"
    """
    # 移除路径前导斜杠
    path = endpoint.lstrip('/')

    # 移除 api/ 前缀（如果存在）
    if path.startswith('api/'):
        path = path[4:]

    # 构建 URL: base_url / path / method.json
    # 例如: /health -> /health/get.json
    return f"{path}/{method.lower()}.json"


@given('初始化测试环境')
def init_test_environment(context):
    """Initialize test environment"""
    logger.info("Test environment initialized")


@when('发送 GET 请求到 "{endpoint}"')
def send_get_request(context, endpoint):
    """Send GET request to static JSON file"""
    if not hasattr(context, 'scenario_context'):
        logger.error("scenario_context not initialized")
        raise AttributeError("scenario_context not initialized. Make sure environment.py is loaded.")

    scenario_context: ScenarioContext = context.scenario_context
    file_path = _get_static_file_path('get', endpoint)

    # 处理特殊字符（如路径中的参数）
    file_path = quote(file_path, safe='/')

    url = f"{scenario_context.base_url}/{file_path}"

    logger.info(f"发送 GET 请求（静态文件）: {url}")
    response = requests.get(url)

    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"响应体: {response.text}")

    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 POST 请求到 "{endpoint}"，请求体为:')
def send_post_request(context, endpoint):
    """Send POST request to static JSON file (simulated)"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    file_path = _get_static_file_path('post', endpoint)
    file_path = quote(file_path, safe='/')

    url = f"{scenario_context.base_url}/{file_path}"

    # 对于静态文件，使用 GET 模拟 POST（只返回预设的响应）
    logger.info(f"发送 POST 请求（静态文件映射）: {url}")
    response = requests.get(url)

    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"响应体: {response.text}")

    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 PUT 请求到 "{endpoint}"，请求体为:')
def send_put_request(context, endpoint):
    """Send PUT request to static JSON file (simulated)"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    file_path = _get_static_file_path('put', endpoint)
    file_path = quote(file_path, safe='/')

    url = f"{scenario_context.base_url}/{file_path}"

    logger.info(f"发送 PUT 请求（静态文件映射）: {url}")
    response = requests.get(url)

    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"响应体: {response.text}")

    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 DELETE 请求到 "{endpoint}"')
def send_delete_request(context, endpoint):
    """Send DELETE request to static JSON file (simulated)"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    file_path = _get_static_file_path('delete', endpoint)
    file_path = quote(file_path, safe='/')

    url = f"{scenario_context.base_url}/{file_path}"

    logger.info(f"发送 DELETE 请求（静态文件映射）: {url}")
    response = requests.get(url)

    logger.info(f"响应状态码: {response.status_code}")
    logger.info(f"响应体: {response.text}")

    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('检查 HTTP 状态码为 {status_code:d}')
def check_status_code(context, status_code):
    """Check HTTP status code"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response

    actual_code = response.status_code
    assert actual_code == status_code, f"期望状态码 {status_code}，实际为 {actual_code}"
    logger.info(f"状态码检查通过: {actual_code}")


@then('响应应该是一个数组')
def check_response_is_array(context):
    """Check if response is an array"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response

    data = response.json()

    # 处理包装的响应（如 {code: 200, data: [...], ok: true}）
    if isinstance(data, dict) and 'data' in data:
        data = data['data']

    assert isinstance(data, list), "响应应该是一个数组"
    logger.info(f"响应是一个数组，包含 {len(data)} 个元素")


@then('检查响应字段 "{json_path}" 等于 {expected_value}')
def check_response_field_equals(context, json_path, expected_value):
    """Check if response field equals expected value"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response

    from jsonpath_ng import parse
    data = response.json()

    # 处理包装的响应
    if isinstance(data, dict) and 'data' in data:
        data = data['data']

    jsonpath_expression = parse(json_path)
    matches = [match.value for match in jsonpath_expression.find(data)]

    assert len(matches) > 0, f"未找到匹配字段: {json_path}"
    actual_value = matches[0]

    # 类型转换
    if isinstance(actual_value, int) and isinstance(expected_value, str):
        try:
            expected_value = int(expected_value)
        except ValueError:
            pass
    elif isinstance(actual_value, str) and isinstance(expected_value, int):
        expected_value = str(expected_value)

    # 去除引号和空白
    if isinstance(actual_value, str) and isinstance(expected_value, str):
        actual_value = actual_value.strip()
        expected_value = expected_value.strip().strip('"').strip("'")

    assert actual_value == expected_value, f"期望值 {expected_value!r}，实际值 {actual_value!r}"
    logger.info(f"字段 {json_path} 检查通过: {actual_value}")


@then('检查响应字段 "{json_path}" 不为空')
def check_response_field_not_empty(context, json_path):
    """Check if response field is not empty"""
    if not hasattr(context, 'scenario_context'):
        raise AttributeError("scenario_context not initialized")

    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response

    from jsonpath_ng import parse
    data = response.json()

    # 处理包装的响应
    if isinstance(data, dict) and 'data' in data:
        data = data['data']

    jsonpath_expression = parse(json_path)
    matches = [match.value for match in jsonpath_expression.find(data)]

    assert len(matches) > 0, f"未找到匹配字段: {json_path}"
    actual_value = matches[0]

    assert actual_value is not None and actual_value != "", f"字段 {json_path} 为空"
    logger.info(f"字段 {json_path} 不为空: {actual_value}")
