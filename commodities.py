import quandl
import pandas as pd
import numpy as np
import talib
import csv

gold=quandl.get("PERTH/GOLD_USD_D", authtoken="B5RSB-jK5vYvZKyFBm4q")
silver=quandl.get("PERTH/SLVR_USD_D", authtoken="B5RSB-jK5vYvZKyFBm4q")
oil=quandl.get("FRED/DCOILWTICO", authtoken="B5RSB-jK5vYvZKyFBm4q")
ruthenium=quandl.get("JOHNMATT/RUTH", authtoken="B5RSB-jK5vYvZKyFBm4q")
iridium=quandl.get("JOHNMATT/IRID", authtoken="B5RSB-jK5vYvZKyFBm4q")
rhodium=quandl.get("JOHNMATT/RHOD", authtoken="B5RSB-jK5vYvZKyFBm4q")
palladium=quandl.get("JOHNMATT/PALL", authtoken="B5RSB-jK5vYvZKyFBm4q")
platinum=quandl.get("JOHNMATT/PLAT", authtoken="B5RSB-jK5vYvZKyFBm4q")

oil=oil.rename(columns={"Value":'value'})
gold_value=pd.DataFrame((gold['Bid Average']+gold['Ask Average'])/2).rename(columns={0:'value'})
silver_value=pd.DataFrame((silver['Bid Average']+silver['Ask Average'])/2).rename(columns={0:'value_silver'})
ruth_value=pd.DataFrame(ruthenium['New York 9:30']).rename(columns={'New York 9:30':'value_ruth'})
irid_value=pd.DataFrame(iridium['New York 9:30']).rename(columns={'New York 9:30':'value_irid'})
rhod_value=pd.DataFrame(rhodium['New York 9:30']).rename(columns={'New York 9:30':'value_rhod'})
pall_value=pd.DataFrame(palladium['New York 9:30']).rename(columns={'New York 9:30':'value_pall'})
plat_value=pd.DataFrame(platinum['New York 9:30']).rename(columns={'New York 9:30':'value_plat'})
hard=gold_value.join(oil,how='outer',lsuffix='_gold',rsuffix='_oil').join(silver_value,how='outer').join(ruth_value,how='outer').join(irid_value,how='outer').join(pall_value,how='outer').join(rhod_value,how='outer').join(plat_value,how='outer').dropna()

hard_tech=pd.DataFrame()
cols=hard.columns
for x in cols:
    hard_tech['macd'+x[x.find('_'):]]=talib.MACD(hard[x])[0]
    hard_tech['rsi'+x[x.find('_'):]]=talib.RSI(hard[x])
    
hard_tech=hard_tech.dropna()

hard_pct=pd.DataFrame()
cols=hard.columns
for x in cols:
    hard_pct['pct'+x[x.find('_'):]]=hard[x].pct_change()
    
hard_pct=hard_pct.replace([np.inf, -np.inf,np.nan], 0)