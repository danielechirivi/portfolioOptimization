import pandas as pd
from alphavantage import getData
from portfolioOptimization import optimize
import sys

def generateDF(products):
    prices=pd.DataFrame(columns=products)
    prices=pd.DataFrame()
    for product in products:
        df=getData(product)
        df=df.adjusted_close
        prices=pd.concat([prices,df],axis=1)
    prices.columns=products
    prices=prices.fillna(method='ffill')
    prices=prices.dropna()
    return prices

if __name__=='__main__':
    if len(sys.argv)>=2:
        c=int(sys.argv[1])
    else:
        c=1
    if len(sys.argv)>=3:
        n=int(sys.argv[2])
    else:
        n=-1
    products=[
        'BTCUSD',
        'ETHUSD',
        'XRPUSD',
        'LTCUSD',
        'BCHUSD'
        ]

    prices=generateDF(products)

    if n==-1:
        n=len(prices)
    else:
        n=min([n,len(prices)])

    weights=optimize(prices.iloc[-n:,:])
    #weights=[1/3,1/3,1/3]

    print('Historical data: '+ str(n))
    print('Capital: ' + str(c))

    text=''
    for i in range(0,len(products)):
        text=text+'\r\n'+'{:10} : {:.2f}'.format(products[i],weights[i]*c)
    print(text)

    daily_returns=prices/prices.shift(1)-1
    daily_returns=daily_returns.dropna()
    cum_returns=daily_returns.cumsum()
    portfolio_cum_returns = cum_returns.dot(weights)
    cummax = portfolio_cum_returns.cummax()
    max_drawdown = (portfolio_cum_returns - cummax).min()
    print(portfolio_cum_returns.index[0])
    print(portfolio_cum_returns.index[-1])
    portfolio_daily_returns=(portfolio_cum_returns-portfolio_cum_returns.shift(1)).mean()
    #print('Expected return: +{}%'.format(round(portfolio_cum_returns[-1]*100,2)))
    print('Expected annual return: +{}%'.format(round(portfolio_daily_returns*252*100,2)))
    print('Max Drawdown: {}%'.format(round(max_drawdown*100,2)))

