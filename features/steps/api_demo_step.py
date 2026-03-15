import allure
import logging
import requests
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext

logger = logging.getLogger(__name__)


@given('初始化测试环境')
def init_test_environment(context):
    """Initialize test environment"""
    logger.info("Test environment initialized")


@when('发送 GET 请求到 "{endpoint}"')
def send_get_request(context, endpoint):
    """Send GET request"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}{endpoint}"
    
    logger.info(f"Sending GET request: {url}")
    response = requests.get(url)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 POST 请求到 "{endpoint}"，请求体为:')
def send_post_request(context, endpoint):
    """Send POST request"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}{endpoint}"
    
    import json
    payload = json.loads(context.text)
    
    logger.info(f"Sending POST request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 PUT 请求到 "{endpoint}"，请求体为:')
def send_put_request(context, endpoint):
    """Send PUT request"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}{endpoint}"
    
    import json
    payload = json.loads(context.text)
    
    logger.info(f"Sending PUT request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.put(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@when('发送 DELETE 请求到 "{endpoint}"')
def send_delete_request(context, endpoint):
    """Send DELETE request"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}{endpoint}"
    
    logger.info(f"Sending DELETE request: {url}")
    response = requests.delete(url)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('检查 HTTP 状态码为 {status_code:d}')
def check_status_code(context, status_code):
    """Check HTTP status code"""
    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response
    
    assert response.status_code == status_code, f"Expected status code {status_code}, got {response.status_code}"
    logger.info(f"Status code check passed: {response.status_code}")


@then('响应应该是一个数组')
def check_response_is_array(context):
    """Check if response is an array"""
    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response
    
    import json
    data = response.json()
    
    # Handle wrapped responses (e.g., {code: 200, data: [...], ok: true})
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    
    assert isinstance(data, list), "Response should be an array"
    logger.info(f"Response is an array with {len(data)} elements")


@then('检查响应字段 "{json_path}" 等于 {expected_value}')
def check_response_field_equals(context, json_path, expected_value):
    """Check if response field equals expected value"""
    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response
    
    from jsonpath_ng import parse
    data = response.json()
    
    # Handle wrapped responses (e.g., {code: 200, data: {...}, ok: true})
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    
    jsonpath_expression = parse(json_path)
    matches = [match.value for match in jsonpath_expression.find(data)]
    
    assert len(matches) > 0, f"No matching field found: {json_path}"
    actual_value = matches[0]
    
    # Try to convert expected_value to match actual_value type
    if isinstance(actual_value, int) and isinstance(expected_value, str):
        try:
            expected_value = int(expected_value)
        except ValueError:
            pass
    elif isinstance(actual_value, str) and isinstance(expected_value, int):
        expected_value = str(expected_value)
    
    # For string comparison, strip whitespace and quotes
    if isinstance(actual_value, str) and isinstance(expected_value, str):
        actual_value = actual_value.strip()
        expected_value = expected_value.strip().strip('"').strip("'")
    
    assert actual_value == expected_value, f"Expected value {expected_value!r} ({type(expected_value)}), got {actual_value!r} ({type(actual_value)})"
    logger.info(f"Field {json_path} check passed: {actual_value}")


@then('检查响应字段 "{json_path}" 不为空')
def check_response_field_not_empty(context, json_path):
    """Check if response field is not empty"""
    scenario_context: ScenarioContext = context.scenario_context
    response = scenario_context.last_response
    
    from jsonpath_ng import parse
    data = response.json()
    
    # Handle wrapped responses (e.g., {code: 200, data: {...}, ok: true})
    if isinstance(data, dict) and 'data' in data:
        data = data['data']
    
    jsonpath_expression = parse(json_path)
    matches = [match.value for match in jsonpath_expression.find(data)]
    
    assert len(matches) > 0, f"No matching field found: {json_path}"
    actual_value = matches[0]
    
    assert actual_value is not None and actual_value != "", f"Field {json_path} is empty"
    logger.info(f"Field {json_path} is not empty: {actual_value}")