# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 10:40:04 2017

@author: shiyunchao
"""


import pandas as pd
import cx_Oracle

def wind_trade_day():
    db=cx_Oracle.connect('rwind','rwind','10.180.10.139:1521/WINDB')
    cr=db.cursor() 
    
    sql="select TRADE_DAYS from WIND.ASHARECALENDAR where S_INFO_EXCHMARKET='SZSE' and TRADE_DAYS>='20050101'"
    cr.execute(sql) 
    rs=cr.fetchall()  
    data = pd.DataFrame(list(rs))
    data.columns = ['trade_day']
    data = data.sort_values('trade_day', ascending=True)
    data.index = range(len(data))
    data.to_csv('trade_day.csv')
    
    cr.close()
    db.close()


def wind_mkt(start, end):
    db=cx_Oracle.connect('rwind','rwind','10.180.10.139:1521/WINDB')
    cr=db.cursor() 
    
    sql="select s_info_windcode,trade_dt,s_dq_preclose,s_dq_close,\
        s_dq_pctchange,s_dq_adjfactor,s_dq_tradestatus\
        from WIND.ASHAREEODPRICES where (trade_dt>='%s-01-01') AND (trade_dt<'%s-01-01')"%(start, end)
                            
    #sql="select s_info_windcode,trade_dt,s_dq_preclose,s_dq_open,s_dq_high,s_dq_low,s_dq_close,\
    #    s_dq_pctchange,s_dq_volume,s_dq_amount,s_dq_adjfactor,S_dq_avgprice,s_dq_tradestatus\
    #    from WIND.ASHAREEODPRICES where trade_dt>='20170801'"
    cr.execute(sql) 
    rs=cr.fetchall()  
    data = pd.DataFrame(list(rs))
    data.columns = ['windcode','trade_dt','preclose','close',\
        'pctchange','adjfactor','tradestatus']
    data['tradestatus'] = data['tradestatus'].apply(lambda x: x.decode('gbk'))
    data = data.sort_values('trade_dt', ascending=True)
    data.index = range(len(data))
    data.to_csv('data/%s.csv'%start)
    
    cr.close()
    db.close()
    
def wind_adjmkt(start, end):
    db=cx_Oracle.connect('rwind','rwind','10.180.10.139:1521/WINDB')
    cr=db.cursor() 
    
    sql="select s_info_windcode,trade_dt,s_dq_adjpreclose,s_dq_adjclose,\
        s_dq_pctchange,s_dq_adjfactor,s_dq_tradestatus\
        from WIND.ASHAREEODPRICES where (trade_dt>='%s-01-01') AND (trade_dt<'%s-01-01')"%(start, end)
                            
    #sql="select s_info_windcode,trade_dt,s_dq_preclose,s_dq_open,s_dq_high,s_dq_low,s_dq_close,\
    #    s_dq_pctchange,s_dq_volume,s_dq_amount,s_dq_adjfactor,S_dq_avgprice,s_dq_tradestatus\
    #    from WIND.ASHAREEODPRICES where trade_dt>='20170801'"
    cr.execute(sql) 
    rs=cr.fetchall()  
    data = pd.DataFrame(list(rs))
    data.columns = ['windcode','trade_dt','adjpreclose','adjclose',\
        'pctchange','adjfactor','tradestatus']
    data = data.sort_values('trade_dt', ascending=True)
    data.index = range(len(data))
    data.to_csv('dataadj/%s.csv'%start)
    
    cr.close()
    db.close()

year_list = range(2010,2019)

for i in range(len(year_list)-1):
    start = year_list[i]
    end = year_list[i+1]
    print('get %s'%start)
#    wind_mkt(start, end)
    wind_mkt(start, end)

