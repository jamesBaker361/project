import pandas as pd
import numpy as np
import requests
history=r=requests.get('https://api.worldtradingdata.com/api/v1/history?symbol=SPY&api_token=cif0zQNJZrTwHRktOAqNrz6JnYqPE4EmWtGlCawvjFYhMLMc1rVTPgZWLcMG').json()['history']
closing=np.array([ r for r in reversed([float(v['close']) for v in history.values()])])
spy=pd.Series(closing, index=reversed([h for h in history.keys()]))
spy_pct=spy.pct_change()
spy_pct.iloc[0]=0