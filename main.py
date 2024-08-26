import requests
import re
from urllib.parse import urlparse
import google.google_search
import model.search_contact
from config.config import ConfigLoader
from db.connect import DatabaseConnection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from sqlalchemy import text

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
    print(page_source)
    # 使用正则表达式提取信息
    emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", page_source))
    phones = set(re.findall(r"\+?\d[\d\s.-]{8,}\d", page_source))

    print(f"找到的电子邮件: {emails}")
    print(f"找到的电话号码: {phones}")

    # 关闭浏览器
    driver.quit()

def main():
    # 在其他模块中使用

    # db_connection= DatabaseConnection()
    #
    # query = "SELECT * FROM search_contact WHERE md5 = :md5"
    # params = {'md5': "1afbcadf15603609815423fdad025cf8"}
    # single_record = db_connection.execute_query(query, params, fetch_all=False)
    # print(single_record)

    # sql = "update search_contact set email=:email1   where id=:id6"
    # update_params = {'email1': 'updated_example', 'id6': 19}
    # db_connection.update_record(sql, update_params)

    url = "https://shopping.medexpressgloves.com/"
    url = "https://www.cypressmed.com/contact-us/"
    # url = "https://shopping.medexpressgloves.com/Contact-Us_ep_58.html"
    # getContentByWebdriver(url)
    # emails, phones = google.google_search.crawl_website(url)
    # all_emails = set()
    # all_phones = set()
    # all_emails.update(emails)
    # all_phones.update(phones)
    # print(f"找到的电子邮件: {all_emails}")
    # print(f"找到的电话号码: {all_phones}")

    # res= model.search_contact.search_contact_query("cdsafety@cumc.columbia.edu")
    # print(res)
    google.google_search.run()
    # url = "https://pdihc.com/products/environment-of-care/super-sani-cloth-germicidal-disposable-wipe/"

    # print(google.google_search.get_ip_from_domain(url))


if __name__ == '__main__':
    main()
