import datetime

import requests
import re
import mysql.connector
from mysql.connector import Error

import hashlib

import tool.encry

# 配置
API_KEY = 'AIzaSyDVGWYSuDRMX3GTM6NxqAxX7AxW4vq8qNE'
SEARCH_ENGINE_ID = '45f1e3f35c4214993'
SEARCH_QUERY = 'disposable gloves contact email phone'
NUM_RESULTS = 10 #限制数量10条

# MySQL 数据库配置
DB_CONFIG = {
    'user': 'root',
    'password': '1234abcd',
    'host': '127.0.0.1',
    'database': 'trade'
}

def get_search_results(query, num_results):
    url = f'https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}&num={num_results}'
    response = requests.get(url)
    if response.status_code == 200:
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
        unique= tool.encry.generate_md5(url)
        print(unique)

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        insert_query = "INSERT INTO search_contact (keyword,url, email, phone,category,create_time,md5) VALUES (%s,%s, %s, %s,%s,%s,%s)"
        cursor.execute(insert_query, (keyword,url, email, phone,category,currentTime,unique))
        connection.commit()
    except Error as e:
        print(f"数据库错误: {e}")
    finally:
        if (cursor):
            cursor.close()
        if (connection.is_connected()):
            connection.close()

def run():
    results = get_search_results(SEARCH_QUERY, NUM_RESULTS)

    for result in results:
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')

        # 提取联系信息
        emails, phones = extract_contact_info(snippet)

        save_to_database(SEARCH_QUERY,link,  ",".join(emails),  ",".join(phones),"google")
        print(f'Title: {title}')
        print(f'Link: {link}')
        print(f'Emails: {", ".join(emails)}')
        print(f'Phones: {", ".join(phones)}')
        print('-' * 40)

