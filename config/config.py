import configparser
class Config:
    @staticmethod
    def get_db_config(filename='config.ini'):
        config = configparser.ConfigParser()
        config.read(filename)
        return {
            'host': config['database']['host'],
            'user': config['database']['user'],
            'password': config['database']['password'],
            'database': config['database']['database']
        }
