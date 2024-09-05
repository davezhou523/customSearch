import datetime
from db.connect import DatabaseConnection
import tool.encry

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
def search_contact_query_all(email="",url="",page_size=50):
    sql = f"select * from search_contact where"
    params = {}
    if  len(email)>0:
        sql += " email = :email"
        params.update({"email": email})
    if url=="notEmpty":
        sql += " url != '' "
    sql += " order by id desc "
    sql += " limit :page_size"
    params.update({"page_size": page_size})
    res = db_connection.execute_query(sql, params)
    return res
def search_contact_save(keyword, url,domain, email, phone, category,location,gl,lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(url + email)

    sql = ("INSERT INTO search_contact (keyword,url,domain, email, phone,category,create_time,md5,location,gl,lr) "
           "VALUES (:keyword,:url,:domain, :email, :phone,:category,:create_time,:md5,:location,:gl,:lr)")
    insert_params = {"keyword": keyword, "url": url,"domain":domain, "email": email, "phone": phone, "category": category,
                     "create_time": currentTime, "md5": md5, "location": location, "gl": gl, "lr": lr}
    db_connection.insert_record(sql, insert_params)

def search_contact_update(keyword, domain, email, phone, category,location,gl,lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(domain + email)
    sql = "update search_contact set email=:email ,phone=:phone ,update_time=:update_time ,location=:location,gl=:gl,lr=:lr where email=:email"
    db_connection.update_record(sql, {"email": email, "phone": phone, "update_time": currentTime, "md5": md5,
                                      "location": location, "gl": gl, "lr": lr})