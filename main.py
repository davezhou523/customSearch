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
import spider.get_web_drive


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

    # url = "https://shopping.medexpressgloves.com/"
    # url = "https://order.ammex.com/s/product/gwon44100/01tf20000089sCVAAY"
    url = "https://acaai.org/allergies/allergic-conditions/latex-allergy/"

    # url = "https://shopping.medexpressgloves.com/Contact-Us_ep_58.html"
    # url = "https://www.smartandfinal.com/contact-us/"
    url = "https://www.henryschein.com/us-en/dental/contact.aspx"
    # emails, phones = google.google_search.crawl_website(url)
    # emails, phones, soup = spider.get_web_drive.get_dynamic_content(url)
    # print(emails, phones)



    google.google_search.run()



if __name__ == '__main__':
    main()
