import requests
import re

import google.google_search
from config.config import ConfigLoader
from db.connect import DatabaseConnection



def main():
    # 在其他模块中使用

    # mysqlconn= DatabaseConnection()
    # sql="select * from search_contact where md5=%s limit 1"
    #
    # data=mysqlconn.fetch_one(sql,("d41d8cd98f00b204e9800998ecf8427e",))
    # # data=mysqlconn.fetch_one(sql)
    # print(data[0])


    google.google_search.run()


if __name__ == '__main__':
    main()
