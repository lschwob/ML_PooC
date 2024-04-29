from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np

def scaler(data):
    scaler = StandardScaler()
    X = data.drop(columns=[col for col in data.columns if 'Symbol' in col or 'Date' in col])
    X = scaler.fit_transform(X)
    return X

def kmeans(data):
    kmeans = KMeans(n_clusters=250)
    kmeans.fit(data)
    return kmeans