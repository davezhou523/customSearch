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
    url="https://www.cordovasafety.com/contact-1-2/"
    url="https://dhs.saccounty.gov/PUB/EMS/Pages/PPE-List/DisposableGloves.aspx"
    url="https://revenue.iowa.gov/taxes/tax-guidance/sales-use-excise-tax/medical-clinics-and-related-businesses-iowa-sales-and-use-tax-information"
    url="https://www.commbuys.com/bso/external/purchaseorder/poSummary.sdo?docId=PO-19-1080-OSD03-SRC3-14635&releaseNbr=0&external=true&parentUrl=close"
    # emails, phones = google.google_search.crawl_website(url)
    google.google_search.single_search_save(url)
    # email="jfaulkner@safewareinc.ac.comphone"
    # splistList = email.split(".")
    # print(splistList)
    # comReg=re.match(r"^com.*",splistList[-1])
    # if comReg is not None:
    #     splistList[-1]="com"
    # email=".".join(splistList)
    # print(email)




    # google.google_search.run()



if __name__ == '__main__':
    main()
