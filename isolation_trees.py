import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kmodes.kprototypes import KPrototypes
import seaborn as sns
from sklearn.decomposition import PCA
import numpy as np
from sklearn.ensemble import IsolationForest
import pickle as pkl
import os

# TODO:
# - extend this to work for all states and species (will be easy when data cleaning is done)
# - calculate the evaluation metrics, save those results

print(os.getcwd())
df = pd.read_csv("/rprojectnb/sparkpit/pit-seasonwatch/pitne-season-watch/all data/citizen/kerala.csv")
df = df[df["Species_name"] == "Mango (all varieties)-Mangifera indica"]
df = df.drop(["Date_of_observation", "Observation_ID", "User_id", "User_Tree_id"], axis=1)
df = df[df["Year"] == 2023]
df_noNaN = df.dropna()
df_noNaN = df_noNaN.drop(["Flowers_male", "Flowers_Female", "Fruits_open", "Species_name", "Year"], axis=1)
df_noNaN = df_noNaN[~df_noNaN.isin([-2.0, -1.0]).any(axis=1)]

try:
    os.makedirs(f"models/kerala/2023")
    print("making the directory")
except:
    print(f"models/kerala/2023 already exists")

ref_data = []
for week in range(1):
    df_week = df_noNaN[df_noNaN['Week'] == week]
    model = IsolationForest(n_estimators = 100, verbose = 1, random_state = 42)
    model.fit(df_week)
    preds = model.predict(df_week)
    try:
        os.makedirs(f"models/kerala/2023/week{week}")
    except:
        print(f"models/kerala/2023/week{week} already exists")
    with open(f"models/kerala/2023/week{week}/isolation_mango.pkl", 'wb') as file:
        # Serialize and save the data to the file
        pkl.dump(model, file)

    # get dataframe of inliers
    inlier_indices = [index for index, value in enumerate(preds) if value == 1]
    df_week_inliers = df_week.iloc[inlier_indices]
    outlier_indices  = [index for index, value in enumerate(preds) if value == -1]
    df_week_outliers = df_week.iloc[outlier_indices]
    
    print("outlier scores: {}".format(model.decision_function(df_week_outliers)))
    print("inlier scores: {}".format(model.decision_function(df_week_inliers)))
    
    # get row with max decision score
    max_idx = np.argmax(model.decision_function(df_week_inliers))
    max_row = df_week_inliers.iloc[max_idx]
    
    print("best row: {}".format(max_row))
