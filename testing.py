import quandl
import pandas as pd
import numpy as np
import talib
import csv
import warnings
import seaborn as sns
from hmmlearn.hmm import GaussianHMM
from matplotlib import cm, pyplot as plt
from matplotlib.dates import YearLocator, MonthLocator
from functools import total_ordering
from trading import generate_signals, eval_signals

def plot_in_sample_hidden_states(hmm_model,df,series):
    """
    Plot the adjusted closing prices masked by 
    the in-sample hidden states as a mechanism
    to understand the market regimes.
    """
    # Predict the hidden states array
    hidden_states = hmm_model.predict(df)
    # Create the correctly formatted plot
    fig, axs = plt.subplots(
        hmm_model.n_components, 
        sharex=True, sharey=True,figsize=[20,20]
    )
    colours = cm.rainbow(
        np.linspace(0, 1, hmm_model.n_components)
    )
    for i, (ax, colour) in enumerate(zip(axs, colours)):
        mask = hidden_states == i
        ax.plot_date(
            df.index[mask], 
            series[mask], 
            ".", linestyle='none', 
            c=colour
        )
        ax.set_title("Hidden State #%s" % i)
        ax.xaxis.set_major_locator(YearLocator())
        ax.xaxis.set_minor_locator(MonthLocator())
        ax.grid(True)
    plt.show()
    
def series_merge(a,b): #sometimes the series will be different length, this function makes each series only have the intersection of their date indices
    for i in a.index:
        if i not in b.index:
            a.drop(i,inplace=True)
    for i in b.index:
        if i not in b.index:
            b.drop(i,inplace=True)
    return(a,b)

@total_ordering
class MarkovStrategy:
    def __init__(self,strat,returns,asset,model=None,params='technical'):
        self.strat=strat #strat function that returns -1,0,1
        self.params=params #the columns of the dataset taht feeds the input to the model
        self.returns=returns # the series actual returns that this portfolio yielded
        self.asset=asset #the name of the asset that this actually traded
        self.model=model #the actual markov model object
    
    def __lt__(self,other):
        return self.returns.iloc[len(self.returns)-1]<other.returns.iloc[len(other.returns)-1]
    
    def __eq__(self,other):
        return self.returns.iloc[len(self.returns)-1]==other.returns.iloc[len(other.returns)-1]
        
    def __str__(self):
        return str(self.returns.iloc[len(self.returns)-1])+' '+self.asset
    
    def __repr__(self):
        return self.__str__()
    
def test_model_mapping(df,assets, model=GaussianHMM,n_components=3,train_size=5000,begin_date='2015-01-01'):
    #makes a Markov model using the df, and finds the optimal mapping from states to trade signals
    train=df.iloc[:train_size]
    hmm=model(n_components=3, covariance_type="full", n_iter=1000).fit(train)
    models=[]
    for mapping in [[x,y,z] for x in [-1,0,1] for y in [-1,0,1] for z in [-1,0,1]]:
        def strat(row,hmm=hmm,mapping=mapping):
            ret=hmm.predict([row])[0]
            return mapping[ret]
        trade=generate_signals(df.loc[begin_date:],strat)
        for asset in assets.columns:
            prices,sigs=series_merge(assets[asset][begin_date:],trade)
            perf=eval_signals(prices,sigs)
            models.append(MarkovStrategy(strat,perf,asset))
    return sorted(models,reverse=True)