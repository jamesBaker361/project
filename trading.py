import pandas as pd
import numpy as np
from matplotlib import cm, pyplot as plt

x=10

def time_series_chart(**series):
    colours = cm.rainbow(
        np.linspace(0, 1,len(series )))
    df=pd.DataFrame(series)
    df.fillna(0,inplace=True)
    colors = iter(cm.rainbow(np.linspace(0, 1, len(series))))
    for k in series.keys():
        plt.plot(df.index,df[k],color=next(colors),label=k)
    plt.legend()
    plt.show()
    
def generate_signals(df,func): #df is the df, func is the function that takes each row as an argument, and returns 1 if buy, 0 if cash out and -1 if short
    ret=pd.Series([0 for _ in range(len(df))],index=df.index)
    for x in range(len(df)-1):
        ret.iloc[x+1]=func(df.iloc[x])
    return ret

def test_signals(asset,signals): #asset is time series of  %change in price, signals is trade signals,1,0,-1, returns a multiplier reflecting the portfolio's change in value since yesterday
    ret=pd.Series([1 for _ in range(len(asset))],index=asset.index)
    for x in range(len(ret)):
        ret.iloc[x]+=signals.iloc[x]*asset.iloc[x]
    return ret

def eval_signals(asset,signals): #reflects change in portfolio's value since the beginning
    ret=test_signals(asset,signals)
    for x in range(1,len(ret)):
        ret.iloc[x]*=ret.iloc[x-1]
    return ret