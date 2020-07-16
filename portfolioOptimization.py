import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from alphavantage import getData
from scipy.optimize import minimize



def optimize(prices):
    products=prices.columns
    n_products=len(products)

    norm_df=prices.divide(prices.iloc[0])
    log_ret = np.log(prices/prices.shift(1))

    # create constraint variable
    cons = ({'type':'eq','fun':check_sum})

    # create weight boundaries
    bounds = ((0,1),(0,1),(0,1),(0,1))
    bounds_arr = []
    for i in range(0,n_products):
        bounds_arr.append((0,1))
    bounds=tuple(bounds_arr)

    # initial guess
    init_guess = 1.0/n_products*np.ones(n_products)

    opt_results = minimize(neg_sharpe, init_guess, args=(log_ret),method='SLSQP', bounds=bounds, constraints=cons)
    optimal_weights=opt_results.x

    portfolio_returns=prices.multiply(optimal_weights).sum(axis=1)

    portfolio_norm_returns=portfolio_returns.divide(portfolio_returns.iloc[0])


    """
    num_ports = 5000
    all_weights = np.zeros((num_ports, len(prices.columns)))
    ret_arr = np.zeros(num_ports)
    vol_arr = np.zeros(num_ports)
    sharpe_arr = np.zeros(num_ports)

    for ind in range(num_ports):
        # weights
        weights = np.array(np.random.random(len(products)))
        weights = weights/np.sum(weights)

        # save the weights
        all_weights[ind,:] = weights

        # expected return
        ret_arr[ind] = np.sum((log_ret.mean()*weights)*252)

        # expected volatility
        vol_arr[ind] = np.sqrt(np.dot(weights.T,np.dot(log_ret.cov()*252, weights)))

        # Sharpe Ratio
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]

    print('Max sharpe ratio: '+str(sharpe_arr.max()))
    index=sharpe_arr.argmax()
    print('Weights')
    print(all_weights[index])
    max_sr_ret = ret_arr[index]
    max_sr_vol = vol_arr[index]

    # plot the data
    plt.figure(figsize=(12,8))
    plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
    # add a red dot for max_sr_vol & max_sr_ret
    plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50, edgecolors='black')
    plt.colorbar(label='Sharpe Ratio')
    plt.xlabel('Volatility')
    plt.ylabel('Return')
    plt.show()
    """
    return optimal_weights

def get_ret_vol_sr(weights,log_ret):
    weights = np.array(weights)
    ret = np.sum(log_ret.mean() * weights)*252
    vol = np.sqrt(np.dot(weights.T,np.dot(log_ret.cov()*252,weights)))
    sr = ret/vol
    return np.array([ret,vol,sr])

# minimize negative Sharpe Ratio
def neg_sharpe(weights,log_ret):
    return get_ret_vol_sr(weights,log_ret)[2] * -1

# check allocation sums to 1
def check_sum(weights):
    return np.sum(weights) - 1
