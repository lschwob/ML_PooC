from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, SpectralClustering, DBSCAN, AgglomerativeClustering
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

def spectral_clustering(data):
    spectral = SpectralClustering(n_clusters=250)
    spectral.fit(data)
    return spectral

def agglomerative_clustering(data):
    agglomerative = AgglomerativeClustering(n_clusters=250)
    agglomerative.fit(data)
    return agglomerative