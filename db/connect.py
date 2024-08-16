# db_singleton.py
import mysql.connector
from mysql.connector import Error
from config.config import ConfigLoader
class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self, host=None, user=None, password=None, database=None):
        db_config = ConfigLoader().get_db_config()
        if host is not None:
            self.host = host
            self.user = user
            self.password = password
            self.database = database
            self.connection = None
        else:
            self.host = db_config.get('host')
            self.user = db_config.get('user')
            self.password = db_config.get('password')
            self.database = db_config.get('database')
            self.connection = None
        self.connect()

    def connect(self):
        if not self.connection or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )

            except Error as e:
                print(f"连接失败: {e}")

    def get_connection(self):
        return self.connection

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("连接已关闭")

    def execute_query(self, query, params=None):
        """执行 SQL 查询"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return self.connection.commit()

        except Error as e:
            print(f"查询执行失败: {e}")
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        """执行查询并获取所有结果"""
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
        except Error as e:
            print(f"查询执行失败: {e}")
        finally:
            cursor.close()
        return result

    def fetch_one(self, query, params=None):
        """执行查询并获取单条结果"""
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
        except Error as e:
            print(f"查询执行失败: {e}")
        finally:
            cursor.close()
        return result

