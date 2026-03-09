# Directly define environment configuration dictionaries
import time
import uuid
import json
import os
import requests

def get_base_url():
    """Get base URL from configuration file"""
    config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config', 'test.json')
    default_url = "https://jsonplaceholder.typicode.com"
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return config_data.get('base_url', default_url)
        except Exception:
            return default_url
    return default_url


class ScenarioContext:
    """
    Scenario class for storing test scenario information
    """
    scenarioId: str
    testDateTime: int
    apiClient: requests.Session
    accountId: str
    config: dict
    base_url: str
    apiToken: str
    last_response: requests.Response

    def __init__(self):
        """
        Initialize scenario class
        """
        self.scenarioId = uuid.uuid4()
        self.testDateTime = time.time()
        self.apiClient = requests.Session()
        self.apiToken = ""
        self.email = ""
        self.accountId= ""
        self.config = {}
        self.base_url = get_base_url()
        self.step_data = {}
