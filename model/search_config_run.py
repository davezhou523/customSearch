import datetime
from db.connect import DatabaseConnection
import tool.encry

# global db_connection
db_connection = DatabaseConnection()

def search_config_run_query(create_time):
    sql = (f"SELECT search_config.* from search_config_run left join search_config "
           f"on search_config.id=search_config_run.config_id"
           f" where search_config_run.create_time >= '{create_time}'")
    params = {}

    sql += " order by search_config_run.id desc"
    res = db_connection.execute_query(sql, params, False)
    return res
def search_config_run_query_all(create_time):
    sql = (f"SELECT search_config_run.config_id "
           f"from search_config_run "
           f" where search_config_run.create_time >= '{create_time}'")
    params = {}

    sql += " order by search_config_run.id desc"
    res = db_connection.execute_query(sql, params)
    return res

def search_config_run_save(config_id):
    sql = ("INSERT INTO search_config_run (config_id) "
           "VALUES (:config_id)")
    insert_params = {"config_id": config_id}
    db_connection.insert_record(sql, insert_params)

def search_config_run_update(keyword, domain, email, phone, category,location,gl,lr):
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md5 = tool.encry.generate_md5(domain + email)
    sql = "update search_config_run set email=:email ,phone=:phone ,update_time=:update_time ,location=:location,gl=:gl,lr=:lr where email=:email"
    db_connection.update_record(sql, {"email": email, "phone": phone, "update_time": currentTime, "md5": md5,
                                      "location": location, "gl": gl, "lr": lr})