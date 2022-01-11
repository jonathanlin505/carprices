import pandas as pd
from sklearn import preprocessing
from scipy.sparse import csr_matrix
from sklearn import neighbors
from sklearn.neighbors import NearestNeighbors

def recommend(features):
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
    num_neighbors = input("Number of recommendations: ")

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

    return result.iloc[indices.flatten()]
