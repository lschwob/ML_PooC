import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scraping import scrape_symbols, scrape_financial, download_data
from preprocessing import dataset_preparation, merge_dataframes, adjust_scaled_df, reshape_process, clustering
from models import scaler, kmeans, spectral_clustering, agglomerative_clustering
from viz import plot_cluster_graph
import os

##streamlit run ./notebooks/scripts/streamlit.py  --client.showErrorDetails=false

FIRST_RUN = False
cotation_url = ['https://www.slickcharts.com/sp500']

@st.cache

def plot_cluster_graph(dict, cluster, df, variable):
    fig = go.Figure()
    for symbol in dict[cluster]:
        cluster_df = df[['Date', f'{variable}_{symbol}']]
             
        fig.add_trace(go.Scatter(
            x=cluster_df['Date'],
            y=cluster_df[f'{variable}_{symbol}'],
            mode='lines', 
            name=symbol
        ))
    
    fig.update_layout(
        title=f'Cluster {cluster} Stock Prices',
        xaxis_title='Date',
        yaxis_title=variable,
        showlegend=True
    )
    
    return fig


def main():
    
    print('First run')
    pwd = os.getcwd()
    print(pwd)

    st.title('Pairs Trading Platform')

@st.cache_data
def process():
    if FIRST_RUN:
        if 'data' not in os.listdir('..'):
            os.mkdir('./data')
        if 'symbols.txt' not in os.listdir('./data'):
            with open('./data/symbols.txt', 'w') as f:
                pass
        if 'financials' not in os.listdir('..'):
            os.mkdir('./data/financials')
        if 'links.txt' not in os.listdir('./data'):
            with open('./data/links.txt', 'w') as f:
                pass
        symbols = scrape_symbols(cotation_url, './data/symbols.txt')
        links = scrape_financial(symbols, progress_file='./data/links.txt')
        download_data('./data/links.txt')
    else:
        with open('./data/symbols.txt', 'r') as f:
            symbols = f.readlines()
            symbols = [symbol.strip() for symbol in symbols]
        with open('./data/links.txt', 'r') as f:
            links = f.readlines()
            links = [link.split(':')[1] for link in links]
    dict_df = dataset_preparation('./data/financials.csv')
    test = merge_dataframes(dict_df)
    X = scaler(test)
    new_df = adjust_scaled_df(test, X, symbols)
    return new_df, symbols, dict_df
new_df, symbols, dict_df = process() 


if __name__ == "__main__":
    main()
    
    st.write('Liste des symboles du S&P500 :')
    data_df = pd.DataFrame(
        {
            "symbols" : [symbols[i:i+50] for i in range(0, len(symbols), 50)],
        }
    )

    st.data_editor(
        data_df,
        column_config={
            "symbols": st.column_config.ListColumn(
                "S&P500 Symbols",
                help="The symbols of the S&P500 companies.",
                width="large",
            ),
        },
        hide_index=True,
    )
    
    st.write('Dataframe contenant les données de chaque cotation du S&P500 :')
    st.dataframe(new_df)
    
    nb_paires = st.sidebar.slider('Nombre de paires à afficher', 1, 20, 10)
    nb_symbols = st.sidebar.slider('Nombre de symbols maximum par cluster', 2, 10, 2)
    option = st.sidebar.selectbox('Critère pour le choix des paires ?', ['Open', 'Adj Close', 'Volatility', 'Volume'])
    model = st.sidebar.selectbox('Critère pour le choix des paires ?', ['KMeans', 'Spectral Clustering', 'Agglomerative Clustering'])
    
    if st.button('Afficher les paires'):
        data, data_reshape = reshape_process(new_df, option)
        if model == 'KMeans':   
            ml_model = kmeans(data_reshape)
        elif model == 'Spectral Clustering':
            ml_model = spectral_clustering(data_reshape)
        elif model == 'Agglomerative Clustering':
            ml_model = agglomerative_clustering(data_reshape)
        dict = clustering(data, data_reshape, ml_model, nb_symbols)
        for cluster in dict.keys():
            #Si l'index de la clé dans le dictionnaire est inférieur a nb_paires alors on affiche le graphique
            if list(dict.keys()).index(cluster) < nb_paires:
                st.plotly_chart(plot_cluster_graph(dict, cluster, data, option))

    