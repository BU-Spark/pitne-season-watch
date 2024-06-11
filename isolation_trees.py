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

print(os.getcwd())
df = pd.read_csv("all data/citizen/kerala.csv")
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
for week in range(1):
    df_week = df_noNaN[df_noNaN['Week'] == week]
    model = IsolationForest(n_estimators = 100, verbose = 1, random_state = 42)
    model.fit(df_week)
    preds = model.predict(df_week)
    try:
        os.makedirs(f"models/kerala/2023/week{week}")
    except:
        print(f"models/kerala/2023/week{week} already exists")
    with open(f"models/kerala/2023/week{week}/mango.pkl", 'wb') as file:
        # Serialize and save the data to the file
        pkl.dump(model, file)
    print("done!")
    