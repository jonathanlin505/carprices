import pymysql
import pandas as pd

def clearDatabase():
    host = "dsci551-project.comwn5fvz9ca.us-east-2.rds.amazonaws.com"
    port = 3306
    user = "dsci551"
    passw = "Dsci-551"
    database = "cars_db"

    cnx = pymysql.connect(host = host, port = port, user = user, password = passw, database = database)

    cur = cnx.cursor()

    query = "DROP TABLE IF EXISTS raw_data"
    cur.execute(query)
    query = "DROP TABLE IF EXISTS features"
    cur.execute(query)
    query = "DROP TABLE IF EXISTS recommendations"
    cur.execute(query)
    query = "DROP TABLE IF EXISTS predictions"
    cur.execute(query)

    return