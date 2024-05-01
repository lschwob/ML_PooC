import pandas as pd
from tqdm import tqdm
from models import kmeans
import re
import numpy as np

def dataset_preparation(file):
    data = pd.read_csv(file)
    dict_df = {}
    for symbol in tqdm(data['Symbol'].unique(), desc='Processing data'):
        dict_df[symbol] = data[data['Symbol'] == symbol][['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']]
    return dict_df

def merge_dataframes(dict_df):
    merged_df = pd.DataFrame()
    for symbol in tqdm(dict_df.keys(), desc='Merging dataframes'):
        if merged_df.empty:
            merged_df = dict_df[symbol]
        else:
            try :
                merged_df = pd.merge(merged_df, dict_df[symbol], on='Date', suffixes=('', f'_{symbol}'), how='outer')
            except:
                print(f'Error with {symbol}')
    merged_df = merged_df.dropna(thresh=0.9*len(merged_df.columns), axis=0)
    test = merged_df.fillna(method='bfill')
    return test

def adjust_scaled_df(data, X, symbols):
    new_df = pd.DataFrame(X, columns=[col for col in data.columns if 'Symbol' not in col and 'Date' not in col])
    date = data['Date'].reset_index(drop=True)
    new_df.rename(columns={'Open' : 'Open_A', 'High' : 'High_A', 'Low' : 'Low_A', 'Close' : 'Close_A', 'Volume' : 'Volume_A', 'Adj Close' : 'Adj Close_A'}, inplace=True)
    new_df['Date'] = date
    for symbol in symbols:
        try:    
            new_df[f'Volatility_{symbol}'] = abs(new_df[f'Close_{symbol}'] - new_df[f'Open_{symbol}'])
        except:
            pass
    return new_df

def reshape_process(df, variable):
    data = df[[col for col in df.columns if f'{variable}' in col]]
    data['Date'] = df['Date']
    
    data_reshape = data.transpose()
    data_reshape = data_reshape.drop('Date', axis=0)
    return data, data_reshape

def clustering(data, data_reshape, model, nb_symbols):
    ml_model = model
    data_reshape['Cluster'] = ml_model.labels_
    dict = {}
    for cluster in data_reshape['Cluster'].unique():
        index = data_reshape[data_reshape['Cluster'] == cluster].index
        result = []
        for i in index:
            result.append(re.search(r'_(.*)', i).group(1))
        dict[cluster] = result
    dict = {key: value for key, value in dict.items() if len(value) in np.arange(2, nb_symbols+1)}
    return dict