"""
配置包初始化文件
"""
from .config import (
    config_manager, 
    get_redis_config, 
    get_base_url, 
    get_config_value,
    init_behave_config,
    get_behave_config
)

__all__ = [
    'config_manager', 
    'get_redis_config', 
    'get_base_url', 
    'get_config_value',
    'init_behave_config',
    'get_behave_config'
]