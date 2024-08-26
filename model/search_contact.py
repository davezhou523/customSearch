import datetime
import json
import socket
import requests
import re
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from db.connect import DatabaseConnection
from urllib.parse import urljoin, urlparse
import tool.encry
import urllib3
import geoip2.database
from urllib.parse import urlparse
# global db_connection
db_connection = DatabaseConnection()

def search_contact_query(email=""):
    sql = f"select * from search_contact where"
    params = {}
    if  len(email)>0:
        sql += " email = :email"
        params = {"email": email}

    res = db_connection.execute_query(sql, params, False)
    return res

def search_contact_save(keyword, url, email, phone, category,location,gl,lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)

    sql = ("INSERT INTO search_contact (keyword,url, email, phone,category,create_time,md5,location,gl,lr) "
           "VALUES (:keyword,:url, :email, :phone,:category,:create_time,:md5,:location,:gl,:lr)")
    insert_params = {"keyword": keyword, "url": url, "email": email, "phone": phone, "category": category,
                     "create_time": currentTime, "md5": md5, "location": location, "gl": gl, "lr": lr}
    db_connection.insert_record(sql, insert_params)

def search_contact_update(keyword, url, email, phone, category,location,gl,lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)
    sql = "update search_contact set email=:email ,phone=:phone ,update_time=:update_time ,location=:location,gl=:gl,lr=:lr where md5=:md5"
    db_connection.update_record(sql, {"email": email, "phone": phone, "update_time": currentTime, "md5": md5,
                                      "location": location, "gl": gl, "lr": lr})