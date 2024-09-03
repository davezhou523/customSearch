import datetime
from db.connect import DatabaseConnection
import tool.encry

# global db_connection
db_connection = DatabaseConnection()


def search_config_query():
    sql = f"select * from search_config "
    params = {}
    sql += " order by id asc"
    res = db_connection.execute_query(sql, params, False)
    return res
def search_config_query_where(not_in_id):
    sql = f"select * from search_config where "
    params = {}
    if len(not_in_id)>0:
        sql += f"id not in :ids"
        params.update({'ids': not_in_id})

    sql += " order by id asc"
    print(sql)
    res = db_connection.execute_query(sql, params, False)
    return res


def search_config_query_all(sta=0):
    sql = f"select * from search_config where"
    params = {}
    if sta > 0:
        sql += " sta = :sta"
        params = {"sta": sta}

    res = db_connection.execute_query(sql, params, True)
    return res

