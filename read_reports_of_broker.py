# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 08:57:51 2017

@author: shiyunchao
"""


import chardet  
import pandas as pd
import cx_Oracle
  
db=cx_Oracle.connect('rwind','rwind','10.180.10.139:1521/WINDB')
cr=db.cursor() 
sql='select ANN_DT,REPORT_PERIOD,IFLISTED_DATA,OPER_REV,\
    NET_PROFIT_INCL_MIN_INT_INC,NET_PROFIT_EXCL_MIN_INT_INC,TOT_SHRHLDR_EQY_EXCL_MIN_INT,\
    TOT_SHRHLDR_EQY_INCL_MIN_INT, S_INFO_COMPNAME, S_INFO_COMPCODE, OPDATE,OPMODE from wind.asharemonthlyreportsofbrokers'
cr.execute(sql) 
rs=cr.fetchall()  
data = pd.DataFrame(list(rs))
data.columns = ['ANN_DT','REPORT_PERIOD','IFLISTED_DATA','OPER_REV',\
    'NET_PROFIT_INCL_MIN_INT_INC','NET_PROFIT_EXCL_MIN_INT_INC','TOT_SHRHLDR_EQY_EXCL_MIN_INT',\
    'TOT_SHRHLDR_EQY_INCL_MIN_INT', 'S_INFO_COMPNAME', 'S_INFO_COMPCODE', 'OPDATE','OPMODE']
data['S_INFO_COMPNAME'] = data['S_INFO_COMPNAME'].apply(lambda x: x.decode('gbk'))

cr.close()
db.close()

stock_name = pd.read_excel('stock_fullname.xlsx')
stock_name = stock_name.iloc[:-2]
#stock_name[u'公司中文名称'] = stock_name[u'公司中文名称'].apply(lambda x: x.decode('ascii').encode('UTF-8'))
stock_name = stock_name.set_index(u'公司中文名称')
stock_name = stock_name[[u'证券代码']]
stock_name_dict = stock_name[u'证券代码'].to_dict()

data['code'] = data['S_INFO_COMPNAME'].replace(stock_name_dict)

data1 = data[data['code'].isin(stock_name[u'证券代码'].values.tolist())]
data1['code'].unique()

data1.to_csv('data.csv', encoding = 'gb18030')


zxc

company = {'东方花旗证券有限公司':'东方证券股份有限公司',
'上海东方证券资产管理有限公司':'东方证券股份有限公司',
'中信证券(浙江)有限责任公司':'中信证券股份有限公司',
'中信证券(山东)有限责任公司':'中信证券股份有限公司',
'上海光大证券资产管理有限公司':'光大证券股份有限公司',
'兴证证券资产管理有限公司':'兴业证券股份有限公司',
'华泰证券(上海)资产管理有限公司':'华泰证券股份有限公司',
'华泰联合证券有限责任公司':'华泰证券股份有限公司',
'上海国泰君安证券资产管理有限公司':'国泰君安证券股份有限公司',
'广发证券资产管理(广东)有限公司':'广发证券股份有限公司',
'招商证券资产管理有限公司':'招商证券股份有限公司',
'浙江浙商证券资产管理有限公司':'浙商证券股份有限公司',
'上海海通证券资产管理有限公司':'海通证券股份有限公司',
'第一创业摩根大通证券有限责任公司':'第一创业证券股份有限公司',
'长江证券承销保荐有限公司':'长江证券股份有限公司',
'长江证券(上海)资产管理有限公司':'长江证券股份有限公司',
'申万宏源证券承销保荐有限责任公司':'申万宏源证券有限公司',
'申万宏源西部证券有限公司':'申万宏源证券有限公司'}

