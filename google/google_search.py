import datetime
import json

import requests
import re
import mysql.connector
from mysql.connector import Error
from db.connect import DatabaseConnection


import hashlib

import tool.encry

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
    results = get_search_results(query, num)

    for result in results:
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        # 提取联系信息
        emails, phones = extract_contact_info(snippet)
        print(f'Title: {title}')
        print(f'Link: {link}')
        print(f'Emails: {", ".join(emails)}')
        print(f'Phones: {", ".join(phones)}')
        print('-' * 40)
        save_to_database(query, link, ",".join(emails), ",".join(phones), 2)



def get_search_results(query, num,gl="us",lr=""):
    # 设置请求参数
    params = {
        'q': query,
        'num': num,
        'cx': SEARCH_ENGINE_ID,  # 你的Custom Search Engine ID
        'key': API_KEY,  # 你的API密钥
        'gl': gl,  # 最终用户的地理位置，可以根据需要更改
        'lr': lr # 搜索结果语言

    }

    # 调用API
    response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)

    # url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={num}'
    # response = requests.get(url)
    if response.status_code == 200:
        # 将响应数据写入文件
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=4)
        return response.json().get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []


def extract_contact_info(text):
    # 正则表达式用于提取电子邮件和电话号码
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    phone_pattern = re.compile(r'\+?\d[\d -]{8,12}\d')

    emails = email_pattern.findall(text)
    phones = phone_pattern.findall(text)

    return emails, phones
def save_to_database(keyword,url, email, phone, category):
    """保存提取到的数据到 MySQL 数据库"""
    try:
        currentTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        md5= tool.encry.generate_md5(url)
        connection = DatabaseConnection()
        sql = "select * from search_contact where md5=%s limit 1"
        isExists=connection.fetch_one(sql,(md5,))
        if isExists:
            sql="update search_contact set email=%s ,phone=%s ,update_time=%s where md5=%s"
            connection.execute_query(sql,(email,phone,currentTime,md5))
        else:
            sql = "INSERT INTO search_contact (keyword,url, email, phone,category,create_time,md5) VALUES (%s,%s, %s, %s,%s,%s,%s)"
            connection.execute_query(sql, (keyword,url, email, phone,category,currentTime,md5))

    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        connection.disconnect()


