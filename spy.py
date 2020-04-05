import pandas as pd
import numpy as np
import requests
history=r=requests.get('https://api.worldtradingdata.com/api/v1/history?symbol=SPY&api_token=cif0zQNJZrTwHRktOAqNrz6JnYqPE4EmWtGlCawvjFYhMLMc1rVTPgZWLcMG').json()['history']
closing=np.array([ r for r in reversed([float(v['close']) for v in history.values()])])
spy=pd.Series(closing, index=reversed([h for h in history.keys()]))
spy_pct=spy.pct_change()
spy_pct.name='pct_spy'
spy_pct.iloc[0]=0
benchmark=1+spy_pct
for x in range(1,len(benchmark)):
    benchmark.iloc[x]*=benchmark.iloc[x-1]
    
def benchmark_start(start_date,spy_pct=spy_pct):
    benchmark=1+spy_pct[start_date:]
    benchmark.iloc[0]=1
    for x in range(1,len(benchmark)):
        benchmark.iloc[x]*=benchmark.iloc[x-1]
    return benchmark