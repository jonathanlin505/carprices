import pymysql
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Support for other file formats later
def loadData(data, table):

    if table == "raw_data":
        if data[-3:] == "csv":
            df = pd.read_csv(data, on_bad_lines="skip")
        if data[-4:] == "json":
            df = pd.read_json(data)
        _id = range(1, len(df) + 1)
        df.insert(loc = 0, column = "id", value = _id)
        df = df.replace({np.nan: None})
    else:
        df = data

    host = "dsci551-project.comwn5fvz9ca.us-east-2.rds.amazonaws.com"
    port = 3306
    user = "dsci551"
    passw = "Dsci-551"
    database = "cars_db"

    mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database, echo=False)

    df.to_sql(name = table, con = mydb, if_exists = "replace", index = False)