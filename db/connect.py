# db_singleton.py
import mysql.connector
from mysql.connector import Error
from config.config import ConfigLoader
import threading
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
class SingletonMeta(type):
    """
    单例模式元类
    """
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
class DatabaseConnection(metaclass=SingletonMeta):


    def __init__(self, db_url=None):
        db_config = ConfigLoader().get_db_config()
        if db_url is  None:
            self.host = db_config.get('host')
            self.user = db_config.get('user')
            self.password = db_config.get('password')
            self.database = db_config.get('database')
            self.connection = None
            db_url = f"mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database}"

        self.engine = create_engine(
            db_url,
            pool_size=5,  # 连接池中可用连接的最大数量
            max_overflow=10,  # 最大溢出连接数
            pool_timeout=30,  # 超时时间
            pool_recycle=1800,  # 连接超时时间
        )
        self.Session = sessionmaker(bind=self.engine)

    def close(self):
        """
        关闭数据库连接和连接池
        """
        if self.session:
            self.session.close()
        self.engine.dispose()
    def get_session(self):
        """
        获取数据库会话
        """
        return self.Session()

    def start_transaction(self):
        """
        开始一个事务，并返回会话对象
        """
        self.session = self.Session()
        return self.session

    def commit_transaction(self):
        """
        提交当前事务
        """
        if self.session:
            try:
                self.session.commit()
            except SQLAlchemyError as e:
                print(f"Commit failed: {e}")
                self.session.rollback()
            finally:
                self.session.close()
                self.session = None

    def rollback_transaction(self):
        """
        回滚当前事务
        """
        if self.session:
            try:
                self.session.rollback()
            except SQLAlchemyError as e:
                print(f"Rollback failed: {e}")
            finally:
                self.session.close()
                self.session = None

    def execute_query(self, query, params=None, fetch_all=True):
        """
        执行参数化查询

        参数:
        query (str): SQL查询语句。
        params (tuple/dict): 查询参数，可以是元组或字典。
        fetch_all (bool): 是否获取所有结果。如果为 False，只获取第一条记录。

        返回:
        list/tuple: 查询结果。如果 fetch_all 为 True，返回所有记录；否则返回单条记录。
        """
        session = self.get_session()
        try:
            # 使用session.execute()执行查询并绑定参数
            # 使用text()明确声明查询为SQL文本
            sql_query = text(query)
            if params is None:
                result = session.execute(sql_query)
            else:
                result = session.execute(sql_query, params)

            if fetch_all:
                return result.fetchall()
            else:
                return result.fetchone()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
        finally:
            session.close()

    def paginated_query(self, query, params=None, page=1, page_size=10):
        """
        执行分页查询

        参数:
        query (str): SQL查询语句。
        params (tuple/dict): 查询参数，可以是元组或字典。
        page (int): 页码，从1开始。
        page_size (int): 每页记录数。

        返回:
        list: 分页查询结果。
        """
        offset = (page - 1) * page_size
        paginated_query = f"{query} LIMIT :limit OFFSET :offset"
        params = params or {}
        params.update({'limit': page_size, 'offset': offset})

        return self.execute_query(paginated_query, params)

    def insert_record(self, query, params):
        """
        插入记录

        参数:
        query (str): SQL插入语句。
        params (dict): 插入参数。
        """
        session = self.get_session()
        try:
            sql_query = text(query)
            session.execute(sql_query, params)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def update_record(self, query, params):
        """
        更新记录

        参数:
        query (str): SQL更新语句。
        params (dict): 更新参数。
        """
        session = self.get_session()
        try:
            sql_query = text(query)
            session.execute(sql_query, params)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()

    def delete_record(self, query, params):
        """
        删除记录

        参数:
        query (str): SQL删除语句。
        params (dict): 删除参数。
        """
        session = self.get_session()
        try:
            sql_query = text(query)
            session.execute(sql_query, params)
            session.commit()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            session.rollback()
        finally:
            session.close()
