import redis
import json
import logging
from typing import Any, Optional
from redis.exceptions import ConnectionError

logger = logging.getLogger(__name__)


class RedisManager:
    """
    简化版 Redis 管理工具类
    只提供基本的键值读写功能
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0,
                 password: Optional[str] = None, decode_responses: bool = True, **kwargs):
        """
        初始化 Redis 连接

        Args:
            host: Redis 服务器主机地址
            port: Redis 服务器端口
            db: 数据库编号
            password: 连接密码
            decode_responses: 是否自动解码响应
            **kwargs: 其他 Redis 连接参数
        """
        self.logger = logging.getLogger(__name__)

        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=decode_responses,
                **kwargs
            )
            # 测试连接
            self.redis_client.ping()
            self.logger.debug(f"Redis 连接成功 (Host: {host}:{port})")
        except ConnectionError as e:
            self.logger.error(f"Redis 连接失败: {e}")
            self.redis_client = None
            raise

    def close(self):
        """
        关闭 Redis 连接
        """
        try:
            if hasattr(self, 'redis_client') and self.redis_client:
                self.redis_client.close()
                self.logger.debug("Redis 连接已关闭")
        except Exception as e:
            self.logger.error(f"关闭 Redis 连接时出错: {e}")

    def get(self, key: str) -> Optional[Any]:
        """
        获取 Redis 中的值

        Args:
            key: 键名

        Returns:
            键对应的值，如果不存在则返回 None
        """
        logger.debug(f"获取键 '{key}' 的值")
        try:
            value = self.redis_client.get(key)
            logger.debug(f"获取键 '{key}' 的值成功: {value}")
            if value is None:
                return None

            # 尝试解析 JSON
            try:
                return json.loads(value)
            except (ValueError, TypeError):
                return value
        except Exception as e:
            self.logger.error(f"获取键 '{key}' 时出错: {e}")
            return None

    def set(self, key: str, value: Any, ex: Optional[int] = None) -> bool:
        """
        设置 Redis 中的值

        Args:
            key: 键名
            value: 值
            ex: 过期时间（秒），None 表示永不过期

        Returns:
            设置是否成功
        """
        try:
            # 如果值是复杂对象，转换为 JSON 字符串
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            else:
                value = str(value)

            result = self.redis_client.set(key, value, ex=ex)
            return result is True
        except Exception as e:
            self.logger.error(f"设置键 '{key}' 时出错: {e}")
            return False

    @classmethod
    def get_connection(cls, host='localhost', port=6379, db=0, password=None):
        """
        获取 Redis 连接
        """
        try:
            redis_manager = cls(
                host=host,
                port=port,
                db=db,
                password=password
            )
            logger.debug("Redis 连接成功")
            return redis_manager
        except Exception as e:
            logger.error(f"Redis 连接失败: {e}")
            raise e


# 使用示例
if __name__ == "__main__":
    # 配置日志输出用于测试
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # 从配置文件获取 Redis 连接
    redis_conn = RedisManager()
    # user_data = redis_conn.get("VERIFY_CODE:EMAIL_gggg@qq.com")
    # logger.info(f"用户数据: {user_data}")

    # 测试连接
    try:
        # 示例：存储和获取数据
        redis_conn.set("csq:1001", {"name": "张三", "age": 30}, ex=3600)
        user_data = redis_conn.get("1000588")
        logger.info(f"用户数据: {user_data}")
    except Exception as e:
        logger.error(f"Redis 操作失败: {e}")
    finally:
        # 关闭连接
        redis_conn.close()
        logger.info("连接已关闭")
