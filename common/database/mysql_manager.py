import pymysql
import logging
from sshtunnel import SSHTunnelForwarder
from typing import Optional, List, Dict, Any
from pytest_home import config

logger = logging.getLogger(__name__)


class MysqlManager:
    """
    简化版 MySQL 管理工具类
    提供基本的数据库连接和 CRUD 操作功能
    """

    def __init__(self, host: str = 'localhost', port: int = 3306, user: str = 'root',
                 password: str = '123456', database: str = '', ssh_config: Optional[dict] = None):
        """
        初始化 MySQL 连接

        Args:
            host: MySQL 服务器主机地址
            port: MySQL 服务器端口
            user: 用户名
            password: 密码
            database: 数据库名
            ssh_config: SSH 跳板配置
        """
        self.ssh_tunnel = None
        self.ssh_config = ssh_config
        self.logger = logging.getLogger(__name__)

        # 如果提供了 SSH 配置，则建立隧道
        if ssh_config:
            self._setup_ssh_tunnel(host, port)
            tunnel_host = 'localhost'
            tunnel_port = int(self.ssh_tunnel.local_bind_port)
        else:
            tunnel_host = host
            tunnel_port = int(port)

        try:
            self.connection = pymysql.connect(
                host=tunnel_host,
                port=tunnel_port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                autocommit=True
            )
            self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)
            self.logger.info(f"MySQL 连接成功 (Host: {tunnel_host}:{tunnel_port}, Database: {database})")
        except Exception as e:
            self.logger.error(f"MySQL 连接失败: {e}")
            raise

    def _setup_ssh_tunnel(self, remote_host: str, remote_port: int):
        """
        设置 SSH 隧道连接
        """
        if not self.ssh_config:
            raise ValueError("SSH 配置不能为空")

        ssh_host = self.ssh_config.get('ssh_host')
        ssh_port = self.ssh_config.get('ssh_port', 22)
        ssh_username = self.ssh_config.get('ssh_username')
        ssh_password = self.ssh_config.get('ssh_password')
        ssh_private_key = self.ssh_config.get('ssh_private_key')
        local_bind_address = self.ssh_config.get('local_bind_address', '127.0.0.1')
        local_bind_port = self.ssh_config.get('local_bind_port')

        if not ssh_host or not ssh_username:
            raise ValueError("SSH 配置必须包含 ssh_host 和 ssh_username")

        try:
            import paramiko
            if not hasattr(paramiko, 'DSSKey'):
                paramiko.DSSKey = paramiko.RSAKey

            if ssh_private_key:
                self.ssh_tunnel = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_username,
                    ssh_pkey=ssh_private_key,
                    remote_bind_address=(remote_host, remote_port),
                    local_bind_address=(local_bind_address, local_bind_port or 0)
                )
            elif ssh_password:
                self.ssh_tunnel = SSHTunnelForwarder(
                    (ssh_host, ssh_port),
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    remote_bind_address=(remote_host, remote_port),
                    local_bind_address=(local_bind_address, local_bind_port or 0)
                )
            else:
                raise ValueError("SSH 配置必须包含 ssh_password 或 ssh_private_key")

            self.ssh_tunnel.start()
            self.logger.info(f"SSH 隧道已建立: {ssh_host}:{ssh_port} -> {remote_host}:{remote_port}")
        except Exception as e:
            self.logger.error(f"SSH 隧道建立失败: {e}")
            raise

    def close(self):
        """
        关闭 MySQL 连接和 SSH 隧道
        """
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
        except Exception as e:
            self.logger.error(f"关闭游标时出错: {e}")

        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception as e:
            self.logger.error(f"关闭 MySQL 连接时出错: {e}")

        try:
            if self.ssh_tunnel:
                self.ssh_tunnel.stop()
                self.logger.info("SSH 隧道已关闭")
        except Exception as e:
            self.logger.error(f"关闭 SSH 隧道时出错: {e}")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行查询语句

        Args:
            query: SQL 查询语句
            params: 查询参数

        Returns:
            查询结果列表
        """
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            self.logger.error(f"执行查询失败: {e}")
            raise

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """
        执行更新语句（INSERT, UPDATE, DELETE）

        Args:
            query: SQL 更新语句
            params: 查询参数

        Returns:
            影响的行数
        """
        try:
            result = self.cursor.execute(query, params)
            self.connection.commit()
            return result
        except Exception as e:
            self.logger.error(f"执行更新失败: {e}")
            self.connection.rollback()
            raise

    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        批量执行更新语句

        Args:
            query: SQL 更新语句
            params_list: 参数列表

        Returns:
            影响的总行数
        """
        try:
            result = self.cursor.executemany(query, params_list)
            self.connection.commit()
            return result
        except Exception as e:
            self.logger.error(f"批量执行失败: {e}")
            self.connection.rollback()
            raise

    @classmethod
    def get_connection(cls, host='127.0.0.1', port=3306, user='root', password='123456',
                       database='', ssh_config=None):
        """
        获取 MySQL 连接，优先尝试 SSH 隧道连接，如果失败则直接连接
        """
        try:
            mysql_manager = cls(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            logger.info("直接连接 MySQL 成功")
            return mysql_manager
        except Exception as e:
            logger.warning(f"直接连接 MySQL 也失败: {e}")
            try:
                logger.info("尝试使用 SSH 隧道连接 MySQL...")
                mysql_manager = cls(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    database=database,
                    ssh_config=ssh_config
                )
                logger.info("SSH 隧道连接成功")
                return mysql_manager
            except Exception as e:
                logger.error(f"SSH 隧道连接失败: {e}")
                logger.info("尝试直接连接 MySQL...")
                raise

    @classmethod
    def get_connection_from_config(cls):
        """
        从配置文件获取 MySQL 连接
        """
        ssh_config = config.config.get('ssh_config')

        current_config = config.config
        mysql_host = current_config.get('mysql_host', '127.0.0.1')
        mysql_port = current_config.get('mysql_port', 3306)
        mysql_user = current_config.get('mysql_user', 'root')
        mysql_password = current_config.get('mysql_password', '123456')
        mysql_database = current_config.get('mysql_database', '')

        return cls.get_connection(
            host=mysql_host,
            port=mysql_port,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database,
            ssh_config=ssh_config
        )


# 使用示例
if __name__ == "__main__":
    # 配置日志输出用于测试
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    # 从配置文件获取 MySQL 连接
    mysql_conn = MysqlManager.get_connection_from_config()

    # 测试连接
    try:
        # 示例：执行查询
        result = mysql_conn.execute_query("SELECT VERSION() as version")
        logger.info(f"MySQL 版本: {result}")

        # 示例：执行更新
        # result = mysql_conn.execute_update("CREATE DATABASE IF NOT EXISTS test_db")
        # logger.info(f"创建数据库结果: {result}")
    except Exception as e:
        logger.error(f"MySQL 操作失败: {e}")
    finally:
        # 关闭连接
        mysql_conn.close()
        logger.info("连接已关闭")
