from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import numpy as np
from sklearn.cluster import DBSCAN

def scaler(data):
    scaler = StandardScaler()
    X = data.drop(columns=[col for col in data.columns if 'Symbol' in col or 'Date' in col])
    X = scaler.fit_transform(X)
    return X

def kmeans(data):
    kmeans = KMeans(n_clusters=250)
    kmeans.fit(data)
    return kmeans

def dbscan(data):
    db = DBSCAN(eps=1, max_samples=2).fit(data)
    db.fit(data)
    return db