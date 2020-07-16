import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alphavantage import getData
from scipy.optimize import minimize
from portfolioOptimization import optimize


def generateDF(products):
    prices=pd.DataFrame(columns=products)
    n_products=len(products)
    prices=pd.DataFrame()
    for product in products:
        df=getData(product)
        df.to_csv('.\\data\\'+product+'.csv')
        df=df.adjusted_close
        prices=pd.concat([prices,df],axis=1)
    prices.columns=products
    prices=prices.fillna(method='ffill')
    prices=prices.dropna()
    return prices

if __name__=='__main__':
    products=[
        'SPY',  
        'TLT',
        'GLD']

    prices=generateDF(products)

    weights=optimize(prices.iloc[-63:,:])*1072
    text=''
    for i in range(0,len(products)):
        text=text+'\r\n'+'{:10} : {:.2f}'.format(products[i],weights[i])
    print(text)
    