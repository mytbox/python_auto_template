"""
配置管理模块
用于读取和管理测试配置
"""
import json
import os
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """配置管理器类"""

    def __init__(self, config_file=None, profile=None):
        # 如果指定了profile，则使用 {profile}.json 格式
        if profile:
            self.config_file = f"config/{profile}.json"
        elif config_file:
            self.config_file = config_file
        else:
            # 默认使用test.json
            self.config_file = "config/local.json"

        self._config_data = None
        self._load_config()

    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config_data = json.load(f)
                logger.debug(f"配置文件加载成功: {self.config_file}")
            except Exception as e:
                logger.error(f"读取配置文件失败: {e}")
                raise FileNotFoundError(f"配置文件 {self.config_file} 读取失败") from e
        else:
            logger.error(f"配置文件不存在: {self.config_file}")
            raise FileNotFoundError(f"配置文件 {self.config_file} 不存在")

    def get_redis_config(self):
        """获取Redis配置"""
        return {
            "host": self._config_data["REDIS_HOST"],
            "port": self._config_data["REDIS_PORT"],
            "db": self._config_data["REDIS_DB"]
        }

    def get_base_url(self):
        """获取基础URL"""
        return self._config_data["base_url"]

    def get_config_value(self, key, default=None):
        """获取指定配置项的值"""
        return self._config_data.get(key, default)


# 全局配置管理器实例
# 注意：在Behave环境中会通过context传递配置，这里提供默认实例
config_manager = ConfigManager()

# 用于Behave环境的配置管理器
_behave_config_manager = None

# 便捷函数
def get_redis_config(profile=None):
    """获取Redis配置的便捷函数"""
    if profile:
        # 为特定profile创建临时配置管理器
        temp_manager = ConfigManager(profile=profile)
        return temp_manager.get_redis_config()
    return config_manager.get_redis_config()

def get_base_url(profile=None):
    """获取基础URL的便捷函数"""
    if profile:
        # 为特定profile创建临时配置管理器
        temp_manager = ConfigManager(profile=profile)
        return temp_manager.get_base_url()
    return config_manager.get_base_url()

def get_config_value(key, default=None, profile=None):
    """获取配置值的便捷函数"""
    if profile:
        # 为特定profile创建临时配置管理器
        temp_manager = ConfigManager(profile=profile)
        return temp_manager.get_config_value(key, default)
    return config_manager.get_config_value(key, default)

def get_ai_config(profile=None):
    """获取AI助手配置的便捷函数"""
    if profile:
        temp_manager = ConfigManager(profile=profile)
        return temp_manager.get_ai_config()
    return config_manager.get_ai_config()

def init_behave_config(context):
    """初始化Behave环境的配置管理器"""
    global _behave_config_manager
    # 从Behave context获取profile参数，默认使用dev
    profile = getattr(context.config, 'userdata', {}).get('profile', 'dev')
    logger.info(f"Loading config with profile: {profile}")
    _behave_config_manager = ConfigManager(profile=profile)
    logger.info(f"Loaded base_url: {_behave_config_manager.get_base_url()}")
    return _behave_config_manager

def get_behave_config():
    """获取Behave环境的配置管理器"""
    return _behave_config_manager


if __name__ == '__main__':
    # 配置日志输出用于测试
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # 测试配置读取
    logger.info("=== 配置信息 ===")
    logger.info(f"Redis配置: {get_redis_config()}")
    logger.info(f"基础URL: {get_base_url()}")
    logger.info(f"所有配置: {config_manager._config_data}")

    # 测试不同profile
    logger.info("=== 测试不同profile ===")
    try:
        dev_config = ConfigManager(profile="dev")
        logger.info(f"Dev环境Redis配置: {dev_config.get_redis_config()}")
        logger.info(f"Dev环境基础URL: {dev_config.get_base_url()}")
    except Exception as e:
        logger.error(f"Dev配置加载失败: {e}")
