import plotly.graph_objects as go

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
    
    fig.show()