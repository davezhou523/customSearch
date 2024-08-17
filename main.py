import requests
import re

import google.google_search
from config.config import ConfigLoader
from db.connect import DatabaseConnection



def main():
    # 在其他模块中使用

    # mysqlconn= DatabaseConnection()
    # sql="select * from search_contact where md5=%s limit 1"

    # data=mysqlconn.fetch_one(sql,("8beb30f521e1c27a153ef276272fc84a",))
    # data=mysqlconn.fetch_one(sql)
    # print(data)
    url = "https://www.lifeguardgloves.com/"

    emails, phones = google.google_search.extract_emails_from_url(url)
    all_emails = set()
    all_phones = set()
    all_emails.update(emails)
    all_phones.update(phones)
    print(f"找到的电子邮件: {all_emails}")
    print(f"找到的电话号码: {all_phones}")

    # google.google_search.run()


if __name__ == '__main__':
    main()
