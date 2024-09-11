import datetime
from db.connect import DatabaseConnection
import tool.encry

# global db_connection
db_connection = DatabaseConnection()


def google_lr_query(sta=0):
    sql = f"select * from google_lr where"
    params = {}
    if sta > 0:
        sql += " sta = :sta"
        params = {"sta": sta}

    res = db_connection.execute_query(sql, params, False)
    return res


def google_lr_query_all(sta=0):
    sql = f"select * from google_lr where"
    params = {}
    if sta > 0:
        sql += " sta = :sta"
        params = {"sta": sta}
    sql += " order by id asc "
    res = db_connection.execute_query(sql, params, True)
    return res


def google_lr_save(keyword, url, email, phone, category, location, gl, lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)

    sql = ("INSERT INTO google_lr (keyword,url, email, phone,category,create_time,md5,location,gl,lr) "
           "VALUES (:keyword,:url, :email, :phone,:category,:create_time,:md5,:location,:gl,:lr)")
    insert_params = {"keyword": keyword, "url": url, "email": email, "phone": phone, "category": category,
                     "create_time": currentTime, "md5": md5, "location": location, "gl": gl, "lr": lr}
    db_connection.insert_record(sql, insert_params)


def google_lr_update(code, sta):

    sql = "update google_lr set sta=:sta where code=:code"
    db_connection.update_record(sql, {"code": code, "sta": sta})
