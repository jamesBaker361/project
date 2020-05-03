## James Baker and Arnav Lohe Data Science Project

### Contents of this Repo:

#### Helpers:
##### commodities.py
this provides functionality to pull in data for the prices of the commodities, and then analyze the data for technical factors that we want to study
##### spy.py
pulls in data for the spy, which we're using as a benchmark to measure up against (does not work; the data source we were pulling from is out of commission due to corona)
##### trading.py
provides functionality for analyzing data and devleoping trading signals
##### testing.py
provides functionality for discovering which models are better

#### Examples: 
##### commoditiesnotebook.ipynb
shows off the dataframes generated by commodoties.py
##### testingnotebook.ipynb
shows an example using the functions for comparing models
##### tradingnotebook.ipynb
shows an example using the functions for generating trading signals from a strategy

#### Results: 
##### finaloutcome.ipynb
This is the result of running the model using the real data

#### Comparisons:
##### q_learning.ipynb, lstm.ipynb, hmm_strats.ipynb
used to generate and save dataframes as csvs with the respective performances of each strategy \n
##### q_results.csv,lstm_results.csv, hmm_results.csv
csvs showing the performance of trading each asset using a strategy generated by the respective model
##### comparisons.ipynb
compares and graphs results of trading each asset under each of the three models
