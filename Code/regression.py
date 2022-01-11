import pandas as pd
from sklearn import preprocessing
from scipy.sparse import csr_matrix
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors
from sklearn import linear_model
import pymysql
from sqlalchemy import create_engine
import numpy as np

def predict(features):
    df = features.reset_index()
    df = df.drop("index", axis=1)

    result = df.copy()
    max_odometer = df["odometer"].max()

    df["make"] = "make " + df["make"]
    df["model"] = "model " + df["model"]
    df["odometer"] = df["odometer"] / max_odometer
    df_binary_make = pd.get_dummies(df["make"])
    df_binary_model = pd.get_dummies(df["model"])
    knn_df = df[["year", "condition", "odometer"]]
    knn_df = knn_df.join(df_binary_make * 25)
    knn_df = knn_df.join(df_binary_model * 50)

    knn_matrix = csr_matrix(knn_df.values)
    knn_model = NearestNeighbors(metric="cosine", algorithm="brute")
    knn_model.fit(knn_matrix)

    year = input("Year: ")
    condition = input("Condition: ")
    odometer = input("Odometer: ")
    make = input("Make: ")
    model = input("Model: ")

    rows = knn_df.shape[0]
    num_neighbors = round(rows*0.2)
    if rows*0.2 >= 100:
        num_neighbors = round(rows*0.2)
    elif (rows*0.2 < 100) and (rows >= 100):
        num_neighbors = 100
    else:
        num_neighbors = rows

    user_dict = {
        "year": int(year),
        "condition": float(condition),
        "odometer": int(odometer) / max_odometer,
    }

    if "make " + make.upper() in knn_df.columns:
        user_dict["make " + make.upper()] = 25
    if "model " + model.upper() in knn_df.columns:
        user_dict["model " + model.upper()] = 50

    knn_df = knn_df.append(user_dict, ignore_index=True)
    user_input = knn_df.iloc[-1:]
    user_input = user_input.fillna(0)
    user_input = user_input.values

    knn_df = knn_df[:-1]

    distances, indices = knn_model.kneighbors(user_input, n_neighbors = int(num_neighbors))

    mr_df = result.iloc[indices.flatten()]

    x = mr_df[['year', 'condition', 'odometer']]
    y = mr_df['sellingprice']

    regr = linear_model.LinearRegression()
    regr.fit(x, y)

    prediction = regr.predict([[user_dict["year"], user_dict["condition"], user_dict["odometer"]]])

    prediction_list = [[int(year), make.upper(), model.upper(), float(condition), int(odometer), round(y.mean()), round(prediction[0])]]

    df = pd.DataFrame(prediction_list, columns = ["year", "make", "model", "condition", "odometer", "average_recommendation_price", "sellingprice"])
  
    host = "dsci551-project.comwn5fvz9ca.us-east-2.rds.amazonaws.com"
    port = 3306
    user = "dsci551"
    passw = "Dsci-551"
    database = "cars_db"

    mydb = create_engine('mysql+pymysql://' + user + ':' + passw + '@' + host + ':' + str(port) + '/' + database, echo=False)

    df.to_sql(name = "predictions", con = mydb, if_exists = "append", index = False)

    return df
