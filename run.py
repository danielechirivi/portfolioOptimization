import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alphavantage import getData
from scipy.optimize import minimize
from portfolioOptimization import optimize

products=[
    'SPY',  #USA
    #'HDV',
    #'DIA',  #USA gg
    #'SDY',  #USA
    #'SPYD',  #USA div
    #'DGRO',
    #'VIX',
    #'HDV', #High dividend prices
    #'VYM', #High dividend
    'GLD',  #Gold
    #'SHY', #1-3y USA Bonds
    #'IEI',
    #'IEF',
    'TLT',  #20y USA Bonds
    #'ACWI',
    #'BND', # Bond index
   # 'VWO',  #China, Brazil, India, ecc..
    #'INDA',  #India
    #'FXI', #China
    #'FEZ', #Europe
    #'EWA', #Australia
    #'EWG', #Germany
    #'AAXJ', #Asia
    #Top 10
    #'SAOC', #non c'è
    #'AAPL',
    #'MSFT',
    #'AMZN',
    #'GOOG',
    #'FB',
    #'TCEHY',
    #'BABA',
    #'BRK-B',
    #'V',
    
    #'TSLA'

    ]


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

prices=prices.iloc[-63:,:]

optimal_weights=optimize(prices)


portfolio_returns=prices.multiply(optimal_weights).sum(axis=1)
portfolio_norm_returns=portfolio_returns/portfolio_returns[0]
norm_returns=prices.divide(prices.iloc[0])

ax=norm_returns.plot()
portfolio_norm_returns.plot(ax=ax,color='black', linewidth=3)
plt.grid()

plt.figure()
patches,text,junk=plt.pie(optimal_weights,labels=products,autopct='%1.1f%%')
plt.legend(patches, products, loc="best")

for i in range(0,len(products)):
    print('{:10} : {:.2f}'.format(products[i],optimal_weights[i]))

plt.show()