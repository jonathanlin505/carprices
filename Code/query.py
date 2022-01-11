import pymysql
import pandas as pd

def queryData(table):
    host = "dsci551-project.comwn5fvz9ca.us-east-2.rds.amazonaws.com"
    port = 3306
    user = "dsci551"
    passw = "Dsci-551"
    database = "cars_db"

    cnx = pymysql.connect(host = host, port = port, user = user, password = passw, database = database)

    try:
        query = pd.read_sql_query("SELECT * FROM " + table, cnx)
        df = pd.DataFrame(query)
    except:
        print("invalid query")
    
    return df