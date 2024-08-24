import datetime
import json

import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from db.connect import DatabaseConnection
from urllib.parse import urljoin, urlparse
import tool.encry
import urllib3

# 禁用所有不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置
API_KEY = 'AIzaSyDVGWYSuDRMX3GTM6NxqAxX7AxW4vq8qNE'
SEARCH_ENGINE_ID = '45f1e3f35c4214993'
# 设置排除的国家和地区
EXCLUDED_COUNTRIES = ['中国', '马来西亚', '越南', '泰国']


def run():
    #排除地区国家：中国、马来西亚，越南，泰国、印度
    query = (
        'disposable gloves contact email phone '
        '-site:.cn -site:.my -site:.vn -site:.th -site:.in -site:tw'
    )
    num = 10  # 限制数量10条
    start_page = 1
    record = 0
    while True:

        # ': gl,  # 最终用户的地理位置，可以根据需要更改
        # 'lr': lr  # 搜索结果语言

        gl = ""
        lr = "al"
        results = get_search_results(query, num, start_page,gl,lr)
        start_page = start_page + num
        for result in results:
            title = result.get('title')
            snippet = result.get('snippet')
            url = result.get('link')
            # 提取联系信息
            # emails, phones = extract_contact_info(snippet)
            # 从结果中提取电子邮件和电话号码
            all_emails = set()
            all_phones = set()
            emails, phones = crawl_website(url)
            all_emails.update(emails)
            all_phones.update(phones)
            location_info = get_website_location(url)
            # 将字典转换为 JSON 字符串
            location_json = json.dumps(location_info)
            if location_info:
                print(f"IP Address: {location_info['ip']}")
                print(f"City: {location_info['city']}")
                print(f"Region: {location_info['region']}")
                print(f"Country: {location_info['country']}")
                print(f"Organization: {location_info['org']}")
            print(f'Title: {title}')
            print(f'url: {url}')
            print(f"找到的电子邮件: {all_emails}")
            print(f"找到的电话号码: {all_phones}")
            print('-' * 40)
            record += 1
            print(f" 条数:{record}")
            if len(all_emails) > 0:
                for email in all_emails:
                    email=convert_email_domain_to_lowercase(email)
                    save_to_database(query, url, email, ",".join(all_phones), 2,location_json,gl,lr)
            else:
                save_to_database(query, url, ",".join(all_emails), ",".join(all_phones), 2,location_json,gl,lr)
        print(f"start_page is {start_page}")
        if start_page >= 11:
            break


def get_search_results(query, num, startPage=1, gl="us", lr=""):
    # 设置请求参数
    params = {
        'q': query,
        'num': num,
        'start': startPage,
        'cx': SEARCH_ENGINE_ID,  # 你的Custom Search Engine ID
        'key': API_KEY,  # 你的API密钥
        'gl': gl,  # 最终用户的地理位置，可以根据需要更改
        'lr': lr  # 搜索结果语言

    }
    # 代理服务器的地址和端口
    proxies = {
        'http': 'socks5h://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080',  # 如果代理支持HTTPS，也请添加
    }

    # 调用API
    # api 文档：https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?hl=zh-cn#response-body
    url=f"https://www.googleapis.com/customsearch/v1"
    # 忽略InsecureRequestWarning警告
    response = requests.get(url,params=params,proxies=proxies,verify=False)

    if response.status_code == 200:
        # 将响应数据写入文件
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []


def get_website_location(url):
    # 解析域名
    domain = url.split("//")[-1].split("/")[0]

    # 获取IP地址
    ip_response = requests.get(f'https://ipinfo.io/{domain}/json')

    if ip_response.status_code == 200:
        ip_data = ip_response.json()
        return {
            "ip": ip_data.get("ip"),
            "city": ip_data.get("city"),
            "region": ip_data.get("region"),
            "country": ip_data.get("country"),
            "org": ip_data.get("org"),
        }
    else:
        return None
def extract_contact_info(text):
    # 正则表达式用于提取电子邮件和电话号码
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')

    emails = email_pattern.findall(text)
    phones = phone_pattern.findall(text)

    return emails, phones


def crawl_website(base_url, max_depth=4):
    to_visit = [(base_url, 0)]  # (url, depth)
    visited_urls = set()
    while to_visit:
        url, depth = to_visit.pop()
        if depth > max_depth or url in visited_urls:
            continue

        visited_urls.add(url)

        emails, phones, soup = extract_contact_info_from_url(url)
        if len(emails)>0 or len(phones)>0:
            print(f"Found on {url}")
            print(f"Emails: {emails}")
            print(f"Phones: {phones}\n")
            return emails,phones

        # 提取所有子页面链接
        if soup:
            for link in soup.find_all('a', href=True):
                new_url = urljoin(base_url, link['href'])
                # 只爬取同一网站的链接，避免外部链接
                if urlparse(new_url).netloc == urlparse(base_url).netloc:
                    to_visit.append((new_url, depth + 1))
    return set(), set()
def extract_contact_info_from_url(url):
    try:

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 匹配电子邮件地址
        # emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", soup.get_text()))
        emails = set(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', soup.get_text("<br>")))

        # 匹配电话号码（国际标准和常见格式）
        phones = set(re.findall(r"\+?\d[\d\s.-]{8,}\d", soup.get_text()))
        if len(phones) == 0:
            phones = match_phone(soup.get_text())
            if len(phones) == 0:
                phones=match_phone_href(soup)
        else:
            phones= format_phone(phones)

        return emails, phones,soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set(), set(),None

def format_phone(phones):
    for phone in phones:
        # 去除两端的空白字符（包括换行符）
        cleaned_text = phone.strip()
        # 按换行符分割字符串
        lines = cleaned_text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]  # 排除空行
        if len(cleaned_lines) == 1:
            return set(cleaned_lines)
    return set()

def match_phone(text):

    pattern_capture = r'\((\d{3})\) (\d{3})-(\d{4})'
    match_capture = re.search(pattern_capture, text)
    if match_capture:
        # 现在可以通过索引来访问捕获的组
        area_code, prefix, suffix = match_capture.groups()
        phone_number =f"({area_code}) {prefix}-{suffix}"

        phoneSet=set()
        if area_code:
            return phoneSet|{phone_number}
    return set()
def match_phone_href(soup):
    # 查找所有带有 href 属性的 <a> 标签
    a_tag = soup.find('a', href=True)
    phoneSet = set()
    # 检查 href 属性是否包含 'tel:'
    if a_tag is not None and 'tel:' in a_tag['href']:
        # 提取电话号码
        phone_number = a_tag['href'].split(':')[1]

        if phone_number:
            return phoneSet|{phone_number}
    return set()
"""
域名部转成小写
"""
def convert_email_domain_to_lowercase(email):
    local_part,domain_part=email.split("@")
    return f"{local_part}@{domain_part.lower()}"
def save_to_database(keyword, url, email, phone, category,location,gl,lr):
    """保存提取到的数据到 MySQL 数据库"""
    global db_connection
    try:
        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md5 = tool.encry.generate_md5(url + email)
        db_connection = DatabaseConnection()
        sql = f"select * from search_contact where md5 = :md6 limit 1"
        isExists = db_connection.execute_query(sql, {"md6":md5},False)
        if isExists:
            sql = "update search_contact set email=:email ,phone=:phone ,update_time=:update_time ,location=:location,gl=:gl,lr=:lr where md5=:md5"
            db_connection.update_record(sql, {"email":email, "phone":phone, "update_time":currentTime, "md5":md5,"location":location, "gl":gl, "lr":lr})
        else:
            sql = ("INSERT INTO search_contact (keyword,url, email, phone,category,create_time,md5,location,gl,lr) "
                   "VALUES (:keyword,:url, :email, :phone,:category,:create_time,:md5,:location,:gl,:lr)")
            insert_params={"keyword":keyword, "url":url, "email":email, "phone":phone, "category":category, "create_time":currentTime, "md5":md5,"location":location, "gl":gl, "lr":lr}
            db_connection.insert_record(sql, insert_params)

    except Error as e:
        print(f"数据库错误: {e}")
    # finally:
        # db_connection.close()
        # print(f"数据库错误: {e}")