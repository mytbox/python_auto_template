"""
通用 API 请求步骤定义
支持 JSON 格式的 HTTP 请求，自动处理项目默认请求头和响应保存
"""
import json
import logging
from datetime import datetime
from behave import given, when, then
import requests
import allure
from common.dto.scenario_context import ScenarioContext

logger = logging.getLogger(__name__)


# 项目默认的移动端请求头
DEFAULT_HEADERS = {
    'content-type': 'application/json',
    'client-platform': 'android',
    'client-channel': 'test',
    'client-version': '2.3.0',
    'client-os': '12 31',
    'client-device': 'V1986A',
    'client-time-zone': '8',
    'client-language': 'zh_CN',
    'user-agent': 'com.qzlighter.lighteryou.ai/2 (Linux; U; Android 12; zh_CN; V1986A; Build/SP1A.210812.003; Cronet/113.0.5672.61)',
    'accept-encoding': 'gzip, deflate'
}


def _get_current_time() -> str:
    """获取当前时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def _prepare_headers(custom_headers: dict = None, token: str = None) -> dict:
    """
    准备请求头，合并默认请求头和自定义请求头

    Args:
        custom_headers: 自定义请求头，会覆盖默认请求头中的同名字段
        token: 认证 Token，会自动添加到 Authorization 头

    Returns:
        合并后的请求头字典
    """
    headers = DEFAULT_HEADERS.copy()
    headers['client-time'] = _get_current_time()

    if token:
        headers['Authorization'] = f"Bearer {token}"

    if custom_headers:
        headers.update(custom_headers)

    return headers


def _build_url(base_url: str, endpoint: str) -> str:
    """构建完整的请求 URL"""
    endpoint = endpoint.lstrip('/') if endpoint else ""
    return f"{base_url}/{endpoint}"


def _log_request_details(method: str, url: str, request_headers: dict,
                         json_data: dict = None, params: dict = None):
    """
    统一打印请求详情信息

    Args:
        method: HTTP 方法
        url: 请求 URL
        request_headers: 请求头
        json_data: JSON 请求体
        params: URL 查询参数
    """
    logger.info("=" * 60)
    logger.info(f"【请求详情】{method.upper()} {url}")
    logger.info("-" * 60)
    logger.info(f"请求头: {json.dumps(request_headers, ensure_ascii=False)}")
    if params:
        logger.info(f"查询参数: {json.dumps(params, ensure_ascii=False)}")
    if json_data:
        logger.info(f"请求体: {json.dumps(json_data, ensure_ascii=False)}")
    logger.info("=" * 60)


def _log_response_details(response: requests.Response):
    """
    统一打印响应详情信息

    Args:
        response: requests.Response 对象
    """
    logger.info("=" * 60)
    logger.info(f"【响应详情】状态码: {response.status_code}")
    logger.info("-" * 60)
    logger.info(f"Content-Type: {response.headers.get('Content-Type', '')}")
    logger.info(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False)}")

    # 尝试格式化 JSON 响应体
    try:
        response_json = response.json()
        logger.info(f"响应体: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
    except (json.JSONDecodeError, ValueError, requests.exceptions.JSONDecodeError):
        # 如果不是 JSON，直接输出文本
        body_text = response.text
        if len(body_text) > 500:
            body_preview = body_text[:500] + "..."
        else:
            body_preview = body_text if body_text else "(空响应体)"
        logger.info(f"响应体: {body_preview}")
    logger.info("=" * 60)


def _make_request(context, method: str, endpoint: str,
                  json_data: dict = None, params: dict = None,
                  headers: dict = None) -> requests.Response:
    """
    执行 HTTP 请求的核心方法

    Args:
        context: Behave context 对象
        method: HTTP 方法 (GET, POST, PUT, DELETE, PATCH)
        endpoint: API 端点路径
        json_data: JSON 格式的请求体
        params: URL 查询参数
        headers: 额外的请求头

    Returns:
        requests.Response 对象
    """
    scenario_context: ScenarioContext = context.scenario_context
    url = _build_url(scenario_context.base_url, endpoint)

    # 准备请求头（自动添加 token）
    request_headers = _prepare_headers(headers, scenario_context.apiToken)

    # 打印请求详情
    _log_request_details(method, url, request_headers, json_data, params)

    # ============ Allure 报告 - 请求信息 ============
    with allure.step(f"{method.upper()} {endpoint}"):
        allure.attach(f"{method.upper()} {url}", name="请求URL", attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(request_headers, ensure_ascii=False, indent=2),
                      name="请求头", attachment_type=allure.attachment_type.JSON)
        if params:
            allure.attach(json.dumps(params, ensure_ascii=False, indent=2),
                          name="查询参数", attachment_type=allure.attachment_type.JSON)
        if json_data:
            allure.attach(json.dumps(json_data, ensure_ascii=False, indent=2),
                          name="请求体", attachment_type=allure.attachment_type.JSON)

    # 发送请求
    response = requests.request(
        method=method,
        url=url,
        params=params,
        json=json_data,
        headers=request_headers
    )

    # 保存响应到上下文
    scenario_context.last_response = response
    scenario_context.api_request_headers = request_headers
    scenario_context.api_request_body = json_data
    scenario_context.api_response_headers = dict(response.headers)
    try:
        scenario_context.api_response_body = response.json()
    except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
        scenario_context.api_response_body = response.text

    context.scenario_context = scenario_context

    # 打印响应详情
    _log_response_details(response)

    # ============ Allure 报告 - 响应信息 ============
    with allure.step(f"响应 - 状态码 {response.status_code}"):
        allure.attach(str(response.status_code), name="状态码", attachment_type=allure.attachment_type.TEXT)
        allure.attach(json.dumps(dict(response.headers), ensure_ascii=False, indent=2),
                      name="响应头", attachment_type=allure.attachment_type.JSON)
        try:
            response_body = response.json()
            allure.attach(json.dumps(response_body, ensure_ascii=False, indent=2),
                          name="响应体", attachment_type=allure.attachment_type.JSON)
        except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
            allure.attach(response.text if response.text else "(空响应体)",
                          name="响应体", attachment_type=allure.attachment_type.TEXT)

    return response


# ========== Behave 步骤定义 ==========

@when('发送GET请求"{endpoint}"')
def send_get_request(context, endpoint: str):
    """发送 GET 请求"""
    _make_request(context, "GET", endpoint)


@when('发送带参数GET请求到"{endpoint}"参数为"{params_str}"')
def send_get_request_with_params(context, endpoint: str, params_str: str):
    """发送带查询参数的 GET 请求"""
    params = {}
    if params_str:
        for pair in params_str.split('&'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value

    _make_request(context, "GET", endpoint, params=params)


@when('发送POST请求到"{endpoint}"')
def send_post_request(context, endpoint: str):
    """发送 POST 请求（空请求体）"""
    _make_request(context, "POST", endpoint)


@when('发送POST请求到"{endpoint}"，请求体为:')
def send_post_request_with_body(context, endpoint: str):
    """发送带 JSON 请求体的 POST 请求"""
    doc_string = getattr(context, 'text', '')
    try:
        json_data = json.loads(doc_string) if doc_string else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    _make_request(context, "POST", endpoint, json_data=json_data)


@when('发送POST请求到"{endpoint}"，使用上下文变量"{key}"作为请求体')
def send_post_request_with_context_body(context, endpoint: str, key: str):
    """使用上下文中保存的变量作为 POST 请求体"""
    scenario_context: ScenarioContext = context.scenario_context

    if key not in scenario_context.step_data:
        raise ValueError(f"上下文中不存在变量: {key}")

    json_data = scenario_context.step_data[key]
    _make_request(context, "POST", endpoint, json_data=json_data)


@when('发送PUT请求到"{endpoint}"，请求体为:')
def send_put_request_with_body(context, endpoint: str):
    """发送带 JSON 请求体的 PUT 请求"""
    doc_string = getattr(context, 'text', '')
    try:
        json_data = json.loads(doc_string) if doc_string else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    _make_request(context, "PUT", endpoint, json_data=json_data)


@when('发送DELETE请求到"{endpoint}"')
def send_delete_request(context, endpoint: str):
    """发送 DELETE 请求"""
    _make_request(context, "DELETE", endpoint)


@when('发送PATCH请求到"{endpoint}"，请求体为:')
def send_patch_request_with_body(context, endpoint: str):
    """发送带 JSON 请求体的 PATCH 请求"""
    doc_string = getattr(context, 'text', '')
    try:
        json_data = json.loads(doc_string) if doc_string else {}
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON 解析失败: {e}")

    _make_request(context, "PATCH", endpoint, json_data=json_data)


@when('设置认证Token为"{token}"')
def set_auth_token(context, token: str):
    """设置认证 Token"""
    scenario_context: ScenarioContext = context.scenario_context
    scenario_context.apiToken = token
    context.scenario_context = scenario_context
    logger.info(f"已设置认证Token: {token[:20]}...")


@when('使用上下文Token"{key}"作为认证')
def use_context_token(context, key: str):
    """使用上下文中保存的 Token 作为认证"""
    scenario_context: ScenarioContext = context.scenario_context

    if key not in scenario_context.step_data:
        raise ValueError(f"上下文中不存在Token: {key}")

    token = scenario_context.step_data[key]
    scenario_context.apiToken = token
    context.scenario_context = scenario_context
    logger.info(f"已使用上下文Token作为认证: {token[:20]}...")
