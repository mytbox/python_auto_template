"""
API 测试环境配置文件
简化版，不依赖 Redis
"""
import sys
import os
import io
import json
import logging
from datetime import datetime

# 修复 Windows 控制台中文乱码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from common.dto.scenario_context import ScenarioContext
from config import init_behave_config, get_behave_config

logger = logging.getLogger(__name__)


def setup_logger():
    """配置 logging 日志输出"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def before_all(context):
    """在所有测试开始前执行一次"""
    setup_logger()
    logger.info("初始化全局配置...")

    # 初始化Behave配置管理器
    config_manager = init_behave_config(context)
    logger.info(f"Base URL: {config_manager.get_base_url()}")


def after_all(context):
    """在所有测试结束后执行一次"""
    logger.info("测试结束")


def before_scenario(context, scenario):
    """在每个场景开始前执行"""
    # 为每个场景创建新的场景上下文
    context.scenario_context = ScenarioContext()

    # 从Behave配置管理器获取基础URL
    config_manager = get_behave_config()
    base_url = config_manager.get_base_url()
    context.scenario_context.base_url = base_url

    logger.info(f"场景开始: {scenario.name}")
