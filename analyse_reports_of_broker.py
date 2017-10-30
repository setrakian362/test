# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 10:33:39 2017

@author: shiyunchao
"""



import pandas as pd
import numpy as np
import QUANTAXIS as QA
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

from pylab import mpl   #画图显示中文
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False



factor = 'OPER_REV'#u'TOT_SHRHLDR_EQY_EXCL_MIN_INT'
n_quantile = 3
ret_range = 20
index_code = '000300'
pct_quantiles = 1/ float(n_quantile)

data = pd.read_csv('data.csv', encoding= 'gb18030', index_col = 0)
data.index = range(len(data))
col = [u'ANN_DT', u'REPORT_PERIOD', u'IFLISTED_DATA', u'OPER_REV',\
       u'NET_PROFIT_INCL_MIN_INT_INC', u'NET_PROFIT_EXCL_MIN_INT_INC',\
       u'TOT_SHRHLDR_EQY_EXCL_MIN_INT', u'TOT_SHRHLDR_EQY_INCL_MIN_INT',\
       u'S_INFO_COMPNAME', u'S_INFO_COMPCODE', u'OPDATE', u'OPMODE', u'code']


data['group'] = data['ANN_DT'].apply(lambda x: int(str(x)[:6]+'11'))

df = data[['ANN_DT',factor,'code','group']]
df = df[df.ANN_DT < df.group]
singal_day = df.group.sort_values().unique().tolist()
del df['ANN_DT']

all_code = df.code.apply(lambda x: x.split('.')[0]).unique().tolist()

stock_data = QA.QA_fetch_stock_day_adv(all_code,'2010-01-01','2017-10-01')
HS300_data = QA.QA_fetch_index_day_adv(index_code,'2010-01-01','2017-10-01')



trade_day = QA.QA_fetch_trade_date()
trade_day = pd.Series(trade_day)

def getEndDay(sday, trade_day):
    sday = str(sday)
    sday = sday[:4] + '-' + sday[4:6] + '-' + sday[6:]
    
    day_part = trade_day[trade_day>sday]
    eday = day_part.iloc[ret_range-1]
    return sday, eday

def caculate_ret(stock_code, start, end,stock_data):
    df_close = stock_data.select_time(start, end).to_hfq().pivot('close')
    df_ret = df_close.iloc[-1]/df_close.iloc[0]  - 1
    return df_ret.loc[stock_code].mean()

def caculate_benchmark_ret(index_code, start, end,index_data):
    df_index = index_data.select_time(start, end).pivot('close')
    df_index = df_index[index_code]
    ret = df_index.iloc[-1]/df_index.iloc[0]  - 1
    return ret
                      

df_factorRet = pd.DataFrame(columns = ['group%s'%(ii+1) for ii in range(n_quantile)])
for tday in singal_day:
    print(tday)
    sday, eday = getEndDay(tday, trade_day)
    df_part = df[df['group'] == tday]
    df_part = df_part.dropna()
    
    
    if not df_part.empty:
        score = df_part[['code',factor]].set_index('code')[factor]
        for k in range(n_quantile):
            groupi ='group' + str(k+1)
            down = score.quantile(pct_quantiles*k)
            up = score.quantile(pct_quantiles*(k+1))
            stock_code = score[(score<=up) & (score>=down)].index.tolist()
            stock_code = list(map(lambda x: x.split('.')[0], stock_code))
    #        df.ix[j,porti] = caculate_ret(port, weight, ret, j)
            df_factorRet.loc[sday,groupi] = caculate_ret(stock_code, sday, eday, stock_data)
    else: 
        df_factorRet.loc[sday,groupi] = np.zeros(n_quantile)
        
        
df_factorRet = df_factorRet.reset_index()
#df_factorRet['index'] = df_factorRet['index'].apply(lambda x: str(x)[:4] + '-' + str(x)[4:6] + '-' + str(x)[6:])
df_factorRet.columns = ['singal day'] + df_factorRet.columns.tolist()[1:]
df_factorRet.set_index('singal day',inplace =True)

cumret = (df_factorRet+1).cumprod()

#a = cumret.plot(title = u'%s分组收益率'%factor,figsize=(16, 10))
#fig = a.get_figure()
#fig.savefig('%s.png'%factor)


df_benchmark = pd.DataFrame(columns = ['benchmark'])
for tday in singal_day:
    print(tday)
    sday, eday = getEndDay(tday, trade_day)
    df_benchmark.loc[sday,'benchmark'] = caculate_benchmark_ret(index_code, sday, eday,HS300_data)

cumret_benchmark = (1+df_benchmark).cumprod()

cumret['benchmark'] = cumret_benchmark['benchmark']

a = cumret.plot(title = u'%s分组收益率'%factor,figsize=(16, 10))
fig = a.get_figure()
fig.savefig('%s.png'%factor)


col_active = ['ActiveRet%s'%(i+1) for i in range(n_quantile)]
for i in range(n_quantile):
    cumret[col_active[i]] = cumret['group%s'%(i+1)] - cumret['benchmark'] 

b = cumret[col_active].plot(title = u'%s分组收益率'%factor,figsize=(16, 10))
fig2 = b.get_figure()
fig2.savefig('%s_activeRet.png'%factor)