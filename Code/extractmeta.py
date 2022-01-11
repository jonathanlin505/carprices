import pandas as pd
import numpy as np

def extractMeta(dataframe):
    
    df_datatypes = pd.DataFrame(dataframe.dtypes)
    df_datatypes = df_datatypes.rename({0: "Datatype"}, axis=1)
    df_datatypes.index.name = "Columns"

    df_null_count = dataframe.count()
    df_datatypes["Existing Values"] = df_null_count
    
    rows, columns = dataframe.shape

    df_datatypes["Missing Values"] = rows - df_datatypes["Existing Values"]

    memory = dataframe.memory_usage().sum()
    conversion = 1024
    n = 0
    conversion_labels = {0 : "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while memory > conversion:
        memory /= conversion
        n += 1
    memory = str(round(memory, 2)) + " " + conversion_labels[n] + "B"

    print("Metadata of currently viewed table:")
    print("There are " + str(rows) + " rows and " + str(columns) + " columns using " + memory + " of memory in total.")

    return df_datatypes