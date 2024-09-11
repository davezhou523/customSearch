import datetime
import json
import socket
import time

import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import certifi
import model.search_contact
import model.ggl
import model.glr
import model.search_keyword
import model.search_config
import model.search_config_run
import spider
from db.connect import DatabaseConnection
from urllib.parse import urljoin, urlparse
import tool.encry
import urllib3
import geoip2.database
from urllib.parse import urlparse
import spider.get_beautiful_soup
import spider.get_web_drive


# 禁用所有不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#搜索引擎程序化地访问每天的查询数上限为 10,000 次。
# 配置 AIzaSyBkq9s4W1xTm0LKvMryQhSxm4PZef-Fqgs
API_KEY = 'AIzaSyBkq9s4W1xTm0LKvMryQhSxm4PZef-Fqgs'
# API_KEY = 'AIzaSyDVGWYSuDRMX3GTM6NxqAxX7AxW4vq8qNE' //每天100次查询
SEARCH_ENGINE_ID = '45f1e3f35c4214993'
# SEARCH_ENGINE_ID2 = '237198be3239943fc'
# 设置排除的国家和地区
EXCLUDED_COUNTRIES = ['中国', '马来西亚', '越南', '泰国']


def run():
    #排除地区国家：中国、马来西亚，越南，泰国、印度
    query = (
        'disposable gloves contact email phone'
        '-site:.cn -site:.my -site:.vn -site:.th -site:.in -site:tw'
    )
    keywordList=model.search_keyword.search_keyword_query(1)

    exludeDomain = json.loads(keywordList.exclude)

    # 构建排除网站的查询字符串
    url="notEmpty"
    page_size = 600
    contactList= model.search_contact.search_contact_query_all("",url,page_size)
    siteSet = set()
    for contact in contactList:
        #集合去重复
        siteSet.add(f"-site:{contact.domain}")

    site = list(siteSet)
    exclusion_url = ' '.join(site)
    exclusion_query = ' '.join([f'-site:{site}' for site in exludeDomain])
    exclusion_type=" -filetype:pdf -site:www.gloves.com"

    query = f"{keywordList.keyword} {exclusion_type} {exclusion_url} {exclusion_query}"
    start_google_search(keywordList.keyword,query)


def start_google_search(keyword,query):
    res = start_google_search_by_location(keyword,query)
    if res is None:
        start_google_search_by_language(keyword, query)

def start_google_search_by_location(keyword,query):
    sta = 1  # 状态,1:启用，2：停用
    glListAll = model.ggl.google_gl_query_all(sta)
    if len(glListAll) == 0:
        print(f"按用户的地理位置搜索已经查询完成")
        return None
    for glData in glListAll:
        gl = glData.code
        num = 10  # 限制数量10条
        start_page = 0  # 免费搜索限制100页
        record = 0
        while True:
            # ': gl,  # 最终用户的地理位置，可以根据需要更改
            # 'lr': lr  # 搜索结果语言
            lr = ""
            results = get_search_results(query, num, start_page, gl, lr)
            if len(results) == 0:
                model.ggl.google_gl_update(gl, 2)
                break
            start_page = start_page + num
            # 处理搜索的结果
            handle_search_result(results, keyword, gl, lr)
            print(f"start_page is {start_page}")
    return True
def start_google_search_by_language(keyword,query):
    print(f"开始按网站语言搜索")
    sta = 1  # 状态,1:启用，2：停用
    glListAll = model.glr.google_lr_query_all(sta)
    if len(glListAll) == 0:
        print(f"按网站语言搜索已经查询完成")
        return None
    for glData in glListAll:
        lr = glData.code
        num = 10  # 限制数量10条
        start_page = 0  # 免费搜索限制100页
        record = 0
        while True:
            # ': gl,  # 最终用户的地理位置，可以根据需要更改
            # 'lr': lr  # 搜索结果语言
            gl = ""
            results = get_search_results(query, num, start_page, gl, lr)
            if len(results) == 0:
                model.glr.google_lr_update(lr, 2)
                break
            start_page = start_page + num
            #处理搜索的结果
            handle_search_result(results,keyword,gl,lr)
            print(f"start_page is {start_page}")
    return True
def handle_search_result(results,keyword,gl,lr):
    """ 处理搜索的结果"""
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

        print(f'Title: {title}')
        print(f'url: {url}')
        print(f"找到的电子邮件: {all_emails}")
        print(f"找到的电话号码: {all_phones}")
        location_info = get_website_location(get_ip_from_domain(url))
        # 将字典转换为 JSON 字符串
        location_json = json.dumps(location_info)
        if location_info:
            print(f"IP Address: {location_info['ip']}")
            print(f"City: {location_info['city']}")
            print(f"Region: {location_info['region']}")
            print(f"Country: {location_info['country']}")

        currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f" current time:{currentTime}")
        print('-' * 40)
        if len(all_emails) > 0:
            for email in all_emails:
                email = convert_email_domain_to_lowercase(email)
                save_to_database(keyword, url, email, ",".join(all_phones), 2, location_json, gl, lr)
        else:
            save_to_database(keyword, url, ",".join(all_emails), ",".join(all_phones), 2, location_json, gl, lr)
def single_search_save(url,keyword="",gl="",lr=""):
    all_emails = set()
    all_phones = set()
    emails, phones = crawl_website(url)
    all_emails.update(emails)
    all_phones.update(phones)

    print(f'url: {url}')
    print(f"找到的电子邮件: {all_emails}")
    print(f"找到的电话号码: {all_phones}")
    location_info = get_website_location(get_ip_from_domain(url))
    # 将字典转换为 JSON 字符串
    location_json = json.dumps(location_info)
    if location_info:
        print(f"IP Address: {location_info['ip']}")
        print(f"City: {location_info['city']}")
        print(f"Region: {location_info['region']}")
        print(f"Country: {location_info['country']}")
    if len(all_emails) > 0:
        for email in all_emails:
            email = convert_email_domain_to_lowercase(email)
            save_to_database(keyword, url, email, ",".join(all_phones), 2, location_json, gl, lr)
    else:
        save_to_database(keyword, url, ",".join(all_emails), ",".join(all_phones), 2, location_json, gl, lr)

"""
域名部转成小写
"""
def convert_email_domain_to_lowercase(email):
    local_part,domain_part=email.split("@")
    return f"{local_part}@{domain_part.lower()}"

def get_api_key():
    create_time=datetime.datetime.now().strftime("%Y-%m-%d")
    #获取当天最新api_key
    data= model.search_config_run.search_config_run_query(create_time)
    if data is None:
        search_config = model.search_config.search_config_query()
        if search_config is None:
            return None
        #没有则添加一条api_key
        model.search_config_run.search_config_run_save(search_config.id)
        return search_config.key
    return data.key

def get_query_params(query, num, startPage=1, gl="us", lr=""):
    api_key = get_api_key()
    params = {
        'q': query,
        'num': num,
        'start': startPage,
        'cx': SEARCH_ENGINE_ID,  # 你的Custom Search Engine ID
        'key': api_key,  # 你的API密钥
        'gl': gl,  # 最终用户的地理位置，可以根据需要更改
        'lr': lr,  # 搜索结果语言
        'siteSearch': 'gloves.com',
        'siteSearchFilter': 'e'  # "e"：排除"i"：包含
    }

    # 代理服务器的地址和端口
    proxies = {
        'http': 'socks5h://127.0.0.1:1080',
        'https': 'socks5h://127.0.0.1:1080',  # 如果代理支持HTTPS，也请添加
    }

    # 调用API
    # api 文档：https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list?hl=zh-cn#response-body
    url = f"https://www.googleapis.com/customsearch/v1"
    return  requests.get(url, params=params, proxies=proxies, verify=None)

def get_search_results(query, num, startPage=1, gl="us", lr=""):
    # 设置请求参数
    # api_key = get_api_key()
    print(f"query:{query}")
    response = get_query_params(query, num, startPage, gl, lr)
    print(f"response.status_code:{response.status_code}")
    if response.status_code == 200:
        # 将响应数据写入文件
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return response.json().get('items', [])
    if response.status_code == 429:
        #每日数额上限
        create_time = datetime.datetime.now().strftime("%Y-%m-%d")
        # 获取当天最新api_key
        dataList = model.search_config_run.search_config_run_query_all(create_time)
        config_id = list()
        for data in dataList:
            config_id.append(data.config_id)
        lastConfig = model.search_config.search_config_query_where(config_id)
        model.search_config_run.search_config_run_save(lastConfig.id)
        get_search_results(query, num, startPage, gl, lr)
        return []
    else:
        print(f"get_search_results Error: {response.json()}")
        return []

def get_ip_from_domain(url):
    try:
        parsed_uri = urlparse(url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        ip_address = socket.gethostbyname(domain)
        return ip_address
    except socket.gaierror:
        return None
def get_website_location(ip_address):
    # 需要使用MaxMind GeoLite2数据库的路径
    if ip_address is None:
        return None
    reader = geoip2.database.Reader('./tool/GeoLite2-City.mmdb')

    try:
        response = reader.city(ip_address)
        return {
            "ip": ip_address,
            "city": response.city.name,
            "region": response.subdivisions.most_specific.name,
            "country": response.country.name,
            "latitude": response.location.latitude,
            "longitude": response.location.longitude,
        }
    except geoip2.errors.AddressNotFoundError:
        return None
    finally:
        reader.close()
def extract_contact_info(text):
    # 正则表达式用于提取电子邮件和电话号码
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')

    emails = email_pattern.findall(text)
    phones = phone_pattern.findall(text)

    return emails, phones


def crawl_website(base_url, max_depth=2):
    to_visit = [(base_url, 0)]  # (url, depth)
    visited_urls = set()
    while to_visit:
        url, depth = to_visit.pop()
        if depth > max_depth or url in visited_urls:
            continue

        visited_urls.add(url)

        emails, phones, soup = spider.get_beautiful_soup.getContentByBS(url)
        if len(emails) > 0:
            print(f"Found on {url}")
            print(f"Emails: {emails}")
            print(f"Phones: {phones}\n")
            return emails,phones

        # 提取所有子页面链接
        if soup:
            to_visit =get_all_url_by_soup(soup,base_url, depth)

    return set(), set()


def get_all_url_by_soup(soup,base_url,depth):
    """获取网站a标签href网站的内容"""
    to_visit=[]
    for link in soup.find_all('a', href=True):
        new_url = urljoin(base_url, link['href'])
        # 只爬取同一网站的链接，避免外部链接
        if urlparse(new_url).netloc == urlparse(base_url).netloc:
            to_visit.append((new_url, depth + 1))
    print("to_visit")
    print(to_visit)
    return to_visit


def save_to_database(keyword, url, email, phone, category,location,gl,lr):
    """保存提取到的数据到 MySQL 数据库"""
    global db_connection
    try:
        parsed_uri = urlparse(url)
        domain=parsed_uri.netloc
        # currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # md5 = tool.encry.generate_md5(url + email)
        db_connection = DatabaseConnection()
        if  len(email) > 0:
            isExists = model.search_contact.search_contact_query(email)
            if isExists:
                print(f"{email} 更新数据")
                model.search_contact.search_contact_update(keyword, domain, email, phone, category, location, gl, lr)
            else:
                print(f"{email} 新增数据")
                model.search_contact.search_contact_save(keyword,url, domain, email, phone, category,location,gl,lr)
        else:
            isExists = model.search_contact.search_contact_query("",url)
            if isExists is None:
                print(f"{email} 新增数据")
                model.search_contact.search_contact_save(keyword, url,domain, email, phone, category,location,gl,lr)

    except Error as e:
        print(f"数据库错误: {e}")
    # finally:
        # db_connection.close()
        # print(f"数据库错误: {e}")