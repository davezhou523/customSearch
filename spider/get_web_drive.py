
from selenium.webdriver.chrome.options import Options
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cloudscraper
from bs4 import BeautifulSoup
def get_content_by_webdriver(url):
    # 配置Chrome选项
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 启用无头模式
    chrome_options.add_argument("--disable-gpu")  # 如果在Windows上运行，这个可能会提高稳定性
    chrome_options.add_argument("--no-sandbox")  # 在Linux服务器上运行时可能需要
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    try:
        # 遇到 “Verifying you are human”  使用 Selenium + WebDriver 等待页面加载 等待页面加载完成，
        # 最长等待时间为10秒
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 获取网页源码
        return driver
    finally:
    # 关闭浏览器
        driver.quit()
        return  None

def get_dynamic_content(url):
    ##动态内容
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 启用无头模式
    chrome_options.add_argument("--disable-gpu")  # 如果在Windows上运行，这个可能会提高稳定性
    chrome_options.add_argument("--no-sandbox")  # 在Linux服务器上运行时可能需要
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免内存不足问题
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    try:
        # 遇到 “Verifying you are human”  使用 Selenium + WebDriver 等待页面加载 等待页面加载完成，
        # 最长等待时间为10秒
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 执行 JavaScript 来获取动态内容
        # <a href="mailto:LMS_Helpdesk@efa.org" data-once="ef-outbound-url">LMS_Helpdesk@efa.org</a>
        emails_script = """
                      var emailElements = document.querySelectorAll('a[href^="mailto:"]');
                      var emails = [];
                      emailElements.forEach(function(element) {
                          var href = element.getAttribute('href');
                          var email = href.split('?')[0].replace('mailto:', ''); // 提取 ? 之前的部分
                          if (email) {
                            emails.push(email);
                          }
                      });
                      return emails;
                  """
        emails = driver.execute_script(emails_script)
        print("Found emails_set:", sorted(set(emails)))
        tel_script = """
                      var telElements = document.querySelectorAll('a[href^="tel:"]');
                      var phones = [];
                      telElements.forEach(function(element) {
                          phones.push(element.getAttribute('href').replace('tel:', ''));
                      });
                      return phones;
                  """
        phones = driver.execute_script(tel_script)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 将邮件去重并排序
        return sorted(set(emails)), sorted(set(phones)), soup
    except Exception  as e:
        print(f"get_dynamic_content错误: {e}")
    finally:
        # 关闭浏览器
        driver.quit()
    return set(),set(),""

def getContentBycloudScraper(url):
    #cloudscraper 是一个专门为绕过 Cloudflare 和其他防护机制设计的库。
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    response = scraper.get(url)

    if response.status_code == 200:
        return  BeautifulSoup(response.content, 'html.parser')
    else:
        print(f"cloudScraper. Status code: {response.status_code}")
        return None