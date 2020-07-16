import requests as req
import pandas as pd
import matplotlib.pyplot as plt

def getData(product):
    df=pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey=BZRVQO1S7RSZV3W1&datatype=csv&outputsize=full'.format(product),index_col=0)
    df=df.reindex(index=df.index[::-1])
    return df

def quote(product):
    url='https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+product+'&apikey=BZRVQO1S7RSZV3W1'
    res=req.get(url)
    return res.json()

def search(query):
    res=req.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey=BZRVQO1S7RSZV3W1'.format(query))
    return res.json()
