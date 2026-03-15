import allure
import logging
import requests
from behave import given, when, then
from common.dto.scenario_context import ScenarioContext

logger = logging.getLogger(__name__)


@then('获取邮箱验证码{email}')
def get_email_verify_code(context, email):
    """Get email verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/send-verify-code"
    
    payload = {"loginType": "email", "number": email}
    
    logger.info(f"Sending email verification code request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    scenario_context.email = email
    context.scenario_context = scenario_context
    
    # Extract verification code from response
    response_data = response.json()
    if response_data.get('code') == 200 and 'data' in response_data:
        verify_code = response_data['data'].get('code')
        scenario_context.step_data['verify_code'] = verify_code
        logger.info(f"Email verification code: {verify_code}")
        context.scenario_context = scenario_context


@then('用邮箱验证码获取token')
def login_with_email_code(context):
    """Login with email verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": scenario_context.email,
        "authCode": scenario_context.step_data.get('verify_code', ''),
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "email"
    }
    
    logger.info(f"Sending login request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context
    
    # Extract token from response
    response_data = response.json()
    if response_data.get('code') == 200 and 'data' in response_data:
        scenario_context.apiToken = response_data['data'].get('token', '')
        scenario_context.accountId = response_data['data'].get('accountId', '')
        logger.info(f"Login successful, got token: {scenario_context.apiToken[:20]}...")
        context.scenario_context = scenario_context


@then('发送短信验证码到"{phone_number}"')
def send_sms_verify_code(context, phone_number):
    """Send SMS verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/send-verify-code"
    
    payload = {"loginType": "sms", "number": phone_number, "countryCode": "86"}
    
    logger.info(f"Sending SMS verification code request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    scenario_context.phone = phone_number
    context.scenario_context = scenario_context
    
    # Extract verification code from response
    response_data = response.json()
    if response_data.get('code') == 200 and 'data' in response_data:
        verify_code = response_data['data'].get('code')
        scenario_context.step_data['verify_code'] = verify_code
        logger.info(f"SMS verification code: {verify_code}")
        context.scenario_context = scenario_context


@then('从Redis获取短信验证码')
def get_sms_code_from_redis(context):
    """Get SMS verification code from Redis (mock: use response code)"""
    scenario_context: ScenarioContext = context.scenario_context
    # In mock mode, verification code is already in step_data
    if 'verify_code' not in scenario_context.step_data:
        logger.warning("Verification code not found in step_data")
    else:
        logger.info(f"Using verification code from step_data: {scenario_context.step_data.get('verify_code')}")


@then('使用短信验证码登录')
def login_with_sms_code(context):
    """Login with SMS verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": scenario_context.phone,
        "authCode": scenario_context.step_data.get('verify_code', ''),
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "sms"
    }
    
    logger.info(f"Sending SMS login request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context
    
    # Extract token from response
    response_data = response.json()
    if response_data.get('code') == 200 and 'data' in response_data:
        scenario_context.apiToken = response_data['data'].get('token', '')
        scenario_context.accountId = response_data['data'].get('accountId', '')
        logger.info(f"Login successful, got token: {scenario_context.apiToken[:20]}...")
        context.scenario_context = scenario_context


@then('验证短信验证码')
def verify_sms_code(context):
    """Verify SMS verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/verify-code"
    
    payload = {
        "number": scenario_context.phone,
        "verifyCode": scenario_context.step_data.get('verify_code', ''),
        "countryCode": "86"
    }
    
    logger.info(f"Sending verification request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用指定验证码"{code}"登录')
def login_with_specific_code(context, code):
    """Login with specific verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": scenario_context.email,
        "authCode": code,
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "email"
    }
    
    logger.info(f"Sending login request with specific code: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用邮箱验证码登录邮箱为空')
def login_with_empty_email(context):
    """Login with empty email"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": "",
        "authCode": scenario_context.step_data.get('verify_code', ''),
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "email"
    }
    
    logger.info(f"Sending login request with empty email: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用邮箱验证码登录验证码为空')
def login_with_empty_code(context):
    """Login with empty verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": scenario_context.email,
        "authCode": "",
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "email"
    }
    
    logger.info(f"Sending login request with empty code: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用短信验证码登录手机号为空')
def login_with_empty_phone(context):
    """Login with empty phone number"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": "",
        "authCode": scenario_context.step_data.get('verify_code', ''),
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "sms"
    }
    
    logger.info(f"Sending login request with empty phone: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用短信验证码登录，验证码为空')
def login_with_empty_sms_code(context):
    """Login with empty SMS verification code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/reg-ai-login"
    
    payload = {
        "number": scenario_context.phone,
        "authCode": "",
        "deviceToken": "",
        "deviceType": "android",
        "language": "zh_CN",
        "loginType": "sms"
    }
    
    logger.info(f"Sending login request with empty SMS code: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context


@then('使用指定验证码"{code}"验证')
def verify_with_code(context, code):
    """Verify with specific code"""
    scenario_context: ScenarioContext = context.scenario_context
    url = f"{scenario_context.base_url}/account/verify-code"
    
    payload = {
        "number": scenario_context.phone,
        "verifyCode": code,
        "countryCode": "86"
    }
    
    logger.info(f"Sending verification request: {url}")
    logger.info(f"Request body: {payload}")
    
    response = requests.post(url, json=payload)
    
    logger.info(f"Response status code: {response.status_code}")
    logger.info(f"Response body: {response.text}")
    
    scenario_context.last_response = response
    context.scenario_context = scenario_context
