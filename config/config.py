import os
import configparser

class ConfigLoader:
    def __init__(self):
        self.env = os.getenv('APP_ENV', 'dev')  # 默认使用开发环境
        self.config = configparser.ConfigParser()
        self.load_config()

    def load_config(self):
        config_file = f"./config/config.{self.env}.ini"
        self.config.read(config_file)


    def get_db_config(self):
        return {
            'host': self.config.get('database', 'host'),
            'user': self.config.get('database', 'user'),
            'password': self.config.get('database', 'password'),
            'database': self.config.get('database', 'database')
        }

