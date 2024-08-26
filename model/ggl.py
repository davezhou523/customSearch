import datetime
from db.connect import DatabaseConnection
import tool.encry

# global db_connection
db_connection = DatabaseConnection()


def google_gl_query(sta=0):
    sql = f"select * from google_gl where"
    params = {}
    if sta > 0:
        sql += " sta = :sta"
        params = {"sta": sta}

    res = db_connection.execute_query(sql, params, False)
    return res


def google_gl_query_all(sta=0):
    sql = f"select * from google_gl where"
    params = {}
    if sta > 0:
        sql += " sta = :sta"
        params = {"sta": sta}

    res = db_connection.execute_query(sql, params, True)
    return res


def google_gl_save(keyword, url, email, phone, category, location, gl, lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)

    sql = ("INSERT INTO google_gl (keyword,url, email, phone,category,create_time,md5,location,gl,lr) "
           "VALUES (:keyword,:url, :email, :phone,:category,:create_time,:md5,:location,:gl,:lr)")
    insert_params = {"keyword": keyword, "url": url, "email": email, "phone": phone, "category": category,
                     "create_time": currentTime, "md5": md5, "location": location, "gl": gl, "lr": lr}
    db_connection.insert_record(sql, insert_params)


def google_gl_update(keyword, url, email, phone, category, location, gl, lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)
    sql = "update google_gl set email=:email ,phone=:phone ,update_time=:update_time ,location=:location,gl=:gl,lr=:lr where md5=:md5"
    db_connection.update_record(sql, {"email": email, "phone": phone, "update_time": currentTime, "md5": md5,
                                      "location": location, "gl": gl, "lr": lr})
