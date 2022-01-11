import pandas as pd
import numpy as np
from scipy import stats
pd.options.mode.chained_assignment = None  # default='warn'

def transformData(data, type, outlier):
    features = data[["id", "year", "make", "model", "condition", "odometer", "mmr", "sellingprice"]]

    if type == "Remove missing data":
        features = features.dropna()
    elif type == "Replace missing data":
        for column in features.columns:
            features[column].fillna(features[column].mode()[0], inplace=True)

    # Common standardization
    features["make"] = features["make"].str.upper()
    features["make"] = features["make"].replace({
        "MERCEDES": "MERCEDES-BENZ",
        "MERCEDES-B": "MERCEDES-BENZ",
        "VW": "VOLKSWAGEN",
        "DODGE TK": "DODGE",
        "CHEV TRUCK": "CHEVROLET",
        "GMC TRUCK": "GMC",
        "MAZDA TK": "MAZDA",
        "HYUNDAI TK": "HYUNDAI",
        "FORD TK": "FORD",
        "FORD TRUCK": "FORD",
    })
    features["model"] = features["model"].str.upper()

    if outlier == "Yes":
        features = features[(np.abs(stats.zscore(features[["year", "condition", "odometer", "mmr", "sellingprice"]])) < 3).all(axis=1)]
    
    return features