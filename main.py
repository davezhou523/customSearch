import requests
import re

import google.google_search
from config.config import ConfigLoader
from db.connect import DatabaseConnection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def getContentByWebdriver(url):
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 启用无头模式
    chrome_options.add_argument("--disable-gpu")  # 如果在Windows上运行，这个可能会提高稳定性
    chrome_options.add_argument("--no-sandbox")  # 在Linux服务器上运行时可能需要
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # 获取网页源码
    page_source = driver.page_source
    # 使用正则表达式提取信息
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_source))
    phones = set(re.findall(r"\+?\d[\d\s.-]{8,}\d", page_source))

    print(f"找到的电子邮件: {emails}")
    print(f"找到的电话号码: {phones}")

    # 关闭浏览器
    driver.quit()

def main():
    # 在其他模块中使用

    # mysqlconn= DatabaseConnection()
    # sql="select * from search_contact where md5=%s limit 1"

    # data=mysqlconn.fetch_one(sql,("8beb30f521e1c27a153ef276272fc84a",))
    # data=mysqlconn.fetch_one(sql)
    # print(data)
    url = "https://shopping.medexpressgloves.com/"
    # url = "https://shopping.medexpressgloves.com/Contact-Us_ep_58.html"
    getContentByWebdriver(url)
    # emails, phones = google.google_search.crawl_website(url)
    # all_emails = set()
    # all_phones = set()
    # all_emails.update(emails)
    # all_phones.update(phones)
    # print(f"找到的电子邮件: {all_emails}")
    # print(f"找到的电话号码: {all_phones}")

    # google.google_search.run()


if __name__ == '__main__':
    main()
