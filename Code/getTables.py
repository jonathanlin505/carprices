import pymysql
import pandas as pd

def getTables():
    host = "dsci551-project.comwn5fvz9ca.us-east-2.rds.amazonaws.com"
    port = 3306
    user = "dsci551"
    passw = "Dsci-551"
    database = "cars_db"

    cnx = pymysql.connect(host = host, port = port, user = user, password = passw, database = database)

    cur = cnx.cursor()
    query = "SHOW TABLES"
    cur.execute(query)
    tables = cur.fetchall()

    table_list = []

    for table in tables:
        table_list.append(table[0])

    return table_list