import datetime
import json
import socket
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import certifi
import model.search_contact
import model.ggl
from db.connect import DatabaseConnection
from urllib.parse import urljoin, urlparse
import tool.encry
import urllib3
import geoip2.database
from urllib.parse import urlparse
import spider.get_web_drive
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r"\+?\d[\d\s.-]{8,}\d"
def getContentByBS(url=""):
    try:
        if url != "":
            # 设置伪装的 User-Agent 头部
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            print(url)
            # 代理服务器的地址和端口
            proxies = {
                'http': 'socks5h://127.0.0.1:1080',
                'https': 'socks5h://127.0.0.1:1080',  # 如果代理支持HTTPS，也请添加
            }
            response = requests.get(url, headers=headers, proxies=proxies,verify=None)
            # response = requests.get(url, headers=headers, verify=None)
            # 检查请求是否成功
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                # 解析HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                emails = get_email(soup)
                print(f"BeautifulSoup Emails: {emails}")
                if len(emails) > 0:
                    return emails, get_phone(soup), soup
                else:
                    emails, phones, soup = spider.get_web_drive.get_dynamic_content(url)
                    print(f"get_dynamic_content Emails: {emails}")
                    if len(emails) > 0:
                        return emails, phones, soup
            else:
                print(f"拒绝访问. Status code: {response.status_code}")
                if response.status_code == 403:
                    emails, phones, soup=spider.get_web_drive.get_dynamic_content(url)
                    if len(emails) > 0:
                        return emails,phones,soup
                    if soup == "":
                        return set(), set(), ""
                    return get_email(soup), get_phone(soup), soup

        return set(), set(), ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return set(), set(), ""

def get_email(soup):
    # 使用正则表达式查找邮箱地址
    # email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = match_email_href(soup)
    # print(f"get_email: {emails}")
    if len(emails) == 0:
        emails = re.findall(EMAIL_PATTERN, soup.text)
        return emails
    return emails
def get_phone(soup):
    # 使用正则表达式查找邮箱地址
    phones=set()
    # 匹配电话号码（国际标准和常见格式）
    phones = set(re.findall(PHONE_PATTERN, soup.get_text()))
    if len(phones) == 0:
        phones = match_phone(soup.get_text())
        if len(phones) == 0:
            phones = match_phone_href(soup)
    else:
        phones = format_phone(phones)
    return phones

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
        phone_number = f"({area_code}) {prefix}-{suffix}"

        phoneSet = set()
        if area_code:
            return phoneSet | {phone_number}
    return set()

def match_email_href(soup):
    # <a href="mailto:efa@apisource.com" data-once="ef-outbound-url">efa@apisource.com</a>
    email_tags = soup.find_all('a', href=True)

    # 提取邮箱地址
    for tag in email_tags:
        if tag['href'].startswith('mailto:'):
            email= tag['href'].split("?")[0].replace("mailto:", "")
            if len(email)>0:
                emails = re.findall(EMAIL_PATTERN, email)
                return emails

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
            return phoneSet | {phone_number}
    return set()
