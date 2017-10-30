# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 11:35:39 2017

@author: leiton
"""

import pandas as pd 
import numpy as np



data = pd.DataFrame([])
for i in np.arange(2010,2018):
    df = pd.read_csv('data/%s.csv'%i,index_col=0)
    data= pd.concat([data,df])
data['tradestatus'] = data['tradestatus'].apply(lambda x: x.decode('gbk'))


Close = data.pivot(index='trade_dt', columns='windcode', values='close')
ret = data.pivot(index='trade_dt', columns='windcode', values='pctchange')

adj_factor = data.pivot(index='trade_dt', columns='windcode', values='adjfactor')
adjclose = Close*adj_factor

Close.to_csv('../market_data/Close.csv')
ret.to_csv('../market_data/return.csv')
adjclose.to_csv('../market_data/adjclose.csv')

zxczxc













            