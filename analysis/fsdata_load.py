# -*- coding: utf-8 -*-
import tushare as ts
import datetime
import time
import toptrade as tp
import sql
import logging as log
import traceback
import pandas as pd

def fs_load(code =None,date =None,retry_count =5,pause=1):
    cur = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if cur==date:
        param = {}
        param['code'] = code
        param['date'] = date
        try:
            pd.read_sql_query('delete FROM db_test.fs_st_data  where code=%(code)s and date=%(date)s',sql.engine, params=param)
        except Exception, e:
            log.error(traceback.print_exc())
        df=ts.get_today_ticks(code=code,retry_count=retry_count,pause=pause)
        df.drop('pchange',axis=1,inplace=True)
    else:
        df = ts.get_tick_data(code=code,date =date,retry_count=retry_count,pause=pause)
    df.insert(0, 'date', date)
    df.insert(0,'code',code)
    return df

def fs_load_batch(code_list=None,start=None,end=None,table_name=None):
    result=[]
    format_x="%Y-%m-%d"
    for code in code_list:
        first=datetime.datetime.strptime(start,format_x)
        last=datetime.datetime.strptime(end,format_x)
        while first<=last:
            try:
                date_str=first.strftime(format_x)
                first=first+datetime.timedelta(days=1)
                fs_df=fs_load(code,date_str)
                if (fs_df is not None)&(len(fs_df.index)>4):#没有数据情况返回
                    res= tp.save_db(data=fs_df,table_name=table_name,con=sql.engine,flag='append')
                result.append(res)
            except Exception,e:
                log.error(code)
                log.error(first)
                log.error(last)
                log.error(traceback.print_exc())
                log.error(e)
                continue
    return result

if __name__ == '__main__':
    rse=fs_load_batch(code_list=['002125'],start='2016-07-07',end='2016-11-25',table_name='fs_st_data')