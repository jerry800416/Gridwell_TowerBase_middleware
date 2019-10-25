# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
import MySQLdb
import time
import csv
import os
import towerbase_ref as ref
import numpy as np
import random


#####################################################################
#                           General                          by 瑞昌 #
#####################################################################

def go_to_log(log_path, e):
    '''
    寫進log\n
    now_time:現在時間\n
    log_path:log存檔路徑\n
    e:要寫入的錯誤訊息\n
    '''
    time = datetime.now()
    with open(log_path, 'a', newline='') as f:
        f.write('{} :{}\n'.format(time.strftime("%Y-%m-%d %H:%M:%S"), e))


def connect_DB(db_info, dbname, sql, sql_type, fetch):
    '''
    資料庫操作\n
    db_info: secret\n
    db_name: 要操作的db名稱\n
    sql: sql語法\n
    sql_type: chose select or insert\n
    fetch:fetch all or fetch one
    '''
    try:
        conn = MySQLdb.connect(
            host=db_info[0],
            user=db_info[1],
            passwd=db_info[2],
            db=dbname)
        cur = conn.cursor()
        cur.execute(sql)
        if sql_type == 'select':
            if fetch == 0:
                result = cur.fetchall()
            else:
                result = cur.fetchone()
            cur.close()
            conn.commit()
            conn.close()
            return result
        elif sql_type == 'insert' or sql_type == 'delete' or sql_type == 'update':
            cur.close()
            conn.commit()
            conn.close()
    except Exception as e:
        go_to_log(ref.log_path, str(e))


def check_newData(time):
    '''

    '''
    min_time = time.strftime("%Y-%m-%d %H:%M:00")
    hour_time = time.strftime("%Y-%m-%d %H:00:00")
    day_time = time.strftime("%Y-%m-%d 00:00:00")
    month_time = time.strftime("%Y-%m-01 00:00:00")

    for i in range(len(ref.WSWD_list)) :
        try:
            if i == 'Home':  # TODO
                pass

            elif ref.WSWD_list[i].split('_')[2] == 'avg10min':
                m = time.minute
                sql = "SELECT time FROM {} WHERE time = '{}' LIMIT 1".format(ref.WSWD_list[i],min_time)
                result = connect_DB(ref.db_info,ref.web,sql,'select',1)
                if result:
                    print('avg10min data is new')
                elif m % 10 != 0 :
                    print('not avg10min data renew time')
                else :
                    weather(time,'10min',WSWD = ref.WSWD_list[i],RF = ref.RF_list[i])

            elif ref.WSWD_list[i].split('_')[2] == 'avghour':
                sql = "SELECT time FROM {} WHERE time = '{}' LIMIT 1".format(ref.WSWD_list[i],hour_time)
                result = connect_DB(ref.db_info,ref.web,sql,'select',1)
                if result:
                    print('avghour data is new')
                else :
                    weather(time,'hour',WSWD = ref.WSWD_list[i],RF = ref.RF_list[i])

            elif ref.WSWD_list[i].split('_')[2] == 'avgday':
                sql = "SELECT time FROM {} WHERE time = '{}' LIMIT 1".format(ref.WSWD_list[i],day_time)
                result = connect_DB(ref.db_info,ref.web,sql,'select',1)
                if result:
                    print('avgday data is new')
                else :
                    weather(time,'day',WSWD = ref.WSWD_list[i],RF = ref.RF_list[i])

            elif ref.WSWD_list[i].split('_')[2] == 'avgmonth':
                sql = "SELECT time FROM {} WHERE time = '{}' LIMIT 1".format(ref.WSWD_list[i],month_time)
                result = connect_DB(ref.db_info,ref.web,sql,'select',1)
                if result:
                    print('avgmonth data is new')
                else :
                    weather(time,'month',WSWD = ref.WSWD_list[i],RF = ref.RF_list[i])

        except Exception as e:
            go_to_log(ref.log_path,e)


def check_miss_time(dbname,tablename,timerange,interval):
    '''
    檢查資料庫裡面某個時間區段是否有漏傳資料,若有,則執行補執行該時間程式\n
    timerange: 要檢查幾個小時前到目前的資料(type:int)\n
    dbname : 要檢查的db(type:str)
    interval : 正常時間的時間間隔(ex:timedelta(hours=1))
    '''
    result_list = []
    miss_list =[]
    st_time = (datetime.now()- timedelta(hours=timerange)).strftime("%Y-%m-%d %H:00:00")
    sql = "SELECT DISTINCT time FROM {} WHERE time > '{}' ORDER BY time ASC".format(tablename,st_time)
    result = list(connect_DB(ref.db_info,dbname,sql,'select',0))
    
    for i in result:
        result_list.append(i[0])
    for i in range(len(result_list)):
        if i < (len(result_list)-1):
            while result_list[i+1] != result_list[i]+interval:
                result_list[i] += interval
                miss_list.append(result_list[i])
    if len(miss_list) != 0:
        for i in miss_list:
            check_newData(i)


def check_miss_data(time):
    hour_delta = [0,4,8,12,16]  #check hour
    min_delta = [30]  #check minute
    check_hour = time.hour
    check_min = time.minute
    #檢查開始,不檢查rainfall是因為rainfall資料是跟著wswd跑的,不須重複檢查
    if (check_hour in hour_delta) and (check_min in min_delta) :
        # 10min 往前檢查4小時資料
        check_miss_time(ref.web,"chart_WSWD_avg10min",4,timedelta(minutes=10))
        # hour 往前檢查12小時資料
        check_miss_time(ref.web,"chart_WSWD_avghour",12,timedelta(hours=1))
        # day 往前檢查兩天資料
        check_miss_time(ref.web,"chart_WSWD_avgday",48,timedelta(days=1))
        # month 往前檢查2個月資料
        check_miss_time(ref.web,"chart_WSWD_avgmonth",1440,timedelta(days=30))


def check_err_data(time,data_type,data_list):
    '''
    尋找web上資料為-1的時間,並拉取cwb或acc取代
    '''

    for i in range(len(data_list)):
        if -1 in data_list[i]:
            # 取 cwb 資料
            sql = "SELECT WS,WD,rainfall,time FROM `#{}` WHERE time = '{}'".format(data_list[i][0],(time.strptime(data_list[i][-1],'%Y-%m-%d %H:%M:%S')-timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00'))
            result = connect_DB(ref.db_info,'DTR_realtime_cwb',sql,'select',1)
            # 若cwb 沒資料 取acc 資料
            if -1 in result:
                sql = "SELECT WS,WD,rainfall,time FROM `#{}` WHERE time = '{}'".format(data_list[i][0],(time.strptime(data_list[i][-1],'%Y-%m-%d %H:%M:%S')).strftime('%Y-%m-%d %H:00:00'))
                result = connect_DB(ref.db_info,'DTR_realtime_acc',sql,'select',1)
            # 若 acc 也沒資料或是資料比較慢近來
            if (-1 not in result) and (len(result)!=0):
                # 替代 rainfall -1值
                if data_type == 'rainfall':
                    data_list[i][2] = result[2] #rainfall
                # 替代 wswd -1 值
                elif data_type == 'wswd':
                    data_list[i][2] = result[0] #ws1
                    data_list[i][3] = result[0] #ws2
                    data_list[i][4] = result[1] #wd1
                    data_list[i][5] = result[1] #wd2
            
    return data_list



#####################################################################
#                           WSWD &  rainfall                 by 瑞昌 #
#####################################################################


# WSWD 10min 1hr day month select
def get_weather(dbname,tbname,sttime,edtime):
    sql = "SELECT wind_speed_1,wind_speed_2,wind_direction_1,wind_direction_2,rainfall,Date FROM {} WHERE Date BETWEEN '{}' AND '{}'".format(tbname,sttime,edtime)
    result = connect_DB(ref.db_info,dbname,sql,'select',0)
    return result


#get WSWD from WEB db
def get_wswd(dbname,tbname,sttime,edtime,towerid):
    sql = "SELECT WS,WS2,WD,WD2 FROM {} WHERE TowerID = {} AND (time BETWEEN '{}' AND '{}' ) AND WS != -1 AND WS2 !=-1 AND WD != -1 AND WD2 != -1".format(tbname,towerid,sttime,edtime)
    result = connect_DB(ref.db_info,dbname,sql,'select',0)
    return result


# get rainfall from WEB db
def get_rf(dbname,tbname,sttime,edtime,towerid):
    sql = "SELECT rainfall FROM {} WHERE TowerID = {} AND (time BETWEEN '{}' AND '{}' AND rainfall != -1)".format(tbname,towerid,sttime,edtime)
    result = connect_DB(ref.db_info,dbname,sql,'select',0)
    return result


# WSWD 10min 1hr day month insert
def post_wswd(dbname,tbname,data):
    sql = "INSERT INTO {}(TowerID,RouteID,WS,WS2,WD,WD2,time) VALUES ".format(tbname)
    for i in data:
        sql_body = "({},{},{},{},{},{},'{}'),".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
        sql += sql_body
    sql = sql[:-1]
    connect_DB(ref.db_info,dbname,sql,'insert',0)


# rainfall 1hr day month insert
def post_rf(dbname,tbname,data):
    sql = "INSERT INTO {}(TowerID,RouteID,rainfall,time) VALUES ".format(tbname)
    for i in data:
        sql_body = "({},{},{},'{}'),".format(i[0],i[1],i[2],i[3])
        sql += sql_body
    sql = sql[:-1]
    connect_DB(ref.db_info,dbname,sql,'insert',0)


# wswd && rainfall
def chart_weather(dbname,tbname,time,stamp,web_dbname,towerid):
    list_ws1,list_ws2,list_rf,last_list_rf = [],[],[],[]
    # 確認時間並拉取風速風向雨量資料
    if stamp == '10min':
        edtime = time.strftime("%Y-%m-%d %H:%M:00")
        sttime = (time - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:00")

    elif stamp == 'hour':
        edtime = time.strftime("%Y-%m-%d %H:00:00")
        sttime = (time - timedelta(hours=1)).strftime("%Y-%m-%d %H:00:00")
        last_sttime = (time - timedelta(hours=2)).strftime("%Y-%m-%d %H:00:00")
        
    elif stamp == 'day':
        edtime = time.strftime("%Y-%m-%d 00:00:00")
        sttime = (time - timedelta(days=1)).strftime("%Y-%m-%d 00:00:00")

    elif stamp == 'month':
        edtime = time.strftime("%Y-%m-01 00:00:00")
        sttime = (time - timedelta(days=30)).strftime("%Y-%m-01 00:00:00")

    if stamp in ['day','month'] :
        wswd_tbname = 'chart_WSWD_avghour'
        rf_tbname = 'chart_Rainfall_avghour'
        wswd_result = get_wswd(web_dbname,wswd_tbname,sttime,edtime,towerid)
        rf_result = get_rf(web_dbname,rf_tbname,sttime,edtime,towerid)

        if len(wswd_result) > 0 and len(rf_result) > 0:
            for i in wswd_result:
                list_ws1.append(i[0])
                list_ws2.append(i[1])
            wd1 = wswd_result[-1][2]
            wd2 = wswd_result[-1][3]
            for i in rf_result:
                list_rf.append(i[0])
        else :
            list_ws1,list_ws2,list_rf,wd1,wd2 = -1,-1,-1,-1,-1

    else :
        result = get_weather(dbname,tbname,sttime,edtime)
        
        if len(result) > 0:
            for i in result:
                list_ws1.append(i[0])
                list_ws2.append(i[1])
                list_rf.append(i[4])
            wd1 = result[-1][2]
            wd2 = result[-1][3]
        else: #若時間範圍內沒有資料,則返回-1
            list_ws1,list_ws2,list_rf,wd1,wd2 = -1,-1,-1,-1,-1
        if stamp != '10min':
            last_result = get_weather(dbname,tbname,last_sttime,sttime)
            if len(last_result) > 0 :
                for i in last_result:
                    last_list_rf.append(i[4])
            else :
                last_list_rf = -1

    return list_ws1,list_ws2,list_rf,last_list_rf,wd1,wd2,edtime


def cal_wswd(list_ws1,list_ws2,wd1,wd2,wd1_deflection,wd2_deflection,stamp):
    '''
    拉下來的風速做平均,風向做角度偏移換算
    '''
        
    if -1 not in [list_ws1,list_ws2,wd1,wd2]:
        # 計算風速平均值
        ws1 = round(sum(list_ws1)/len(list_ws1),2)
        ws2 = round(sum(list_ws2)/len(list_ws2),2)
        # 計算風向角度偏移
        if stamp not in ['day','month']:
            wd1 = wd_deflection(wd1,wd1_deflection)
            wd2 = wd_deflection(wd2,wd2_deflection)

    else:
        ws1 = list_ws1
        ws2 = list_ws2
    return ws1,ws2,wd1,wd2


def wd_deflection(wd,deflection):
    '''
    計算風向偏移\n
    wd:原始風向值\n
    deflection:偏移角度
    '''
    if wd not in [-1,None]:
        wd += deflection
        if wd >360:
            wd-= 360
        elif wd <0:
            wd += 360
    return wd

def cal_rf(list_rf,last_list_rf,time,RF,towerid,stamp):
    '''
    計算雨量
    因為雨量計會歸零,所以必須比較當小時雨量有沒有歸零並將數值加回
    list_rf:拉下來的rainfall原始資料
    time:時間,作為搜索上一個小時累積雨量的依據
    RF:WEB rainfall 資料表,作為搜索上一個小時累積雨量的依據
    
    TODO :若剛好於整點歸零,且歸零後的累積雨量大於歸零前,則數值會不準確
    '''
    if list_rf != -1 and last_list_rf != -1:
        if stamp in ['day','month']:
            rf = round(sum(list_rf),2)
        else:
            if list_rf != -1:
                accu_rf = rf_deflection(list_rf)
            else:
                list_rf = 0

            if last_list_rf != -1 :
                last_accu_rf = rf_deflection(last_list_rf)
            else:
                last_accu_rf = 0

            if (last_accu_rf in [None,-1]):
                last_accu_rf = 0
            rf = accu_rf -last_accu_rf

    elif list_rf == -1 and last_list_rf != -1:
        rf = -1
    elif list_rf != -1 and last_list_rf == -1:
        accu_rf = rf_deflection(list_rf)
        rf = accu_rf
    else :
        rf = -1
    # 若剛好遇到整點歸零,則返回新的累積雨量,不扣掉上一小時
    if rf < 0 and rf != -1 :
        rf = accu_rf
    return rf
    
def rf_deflection(list_rf):
    c = 0 
    d = 0 
    for i in list_rf:
        if c > i :
            d = c
        c = i
    accu_rf = round(d + list_rf[-1],2)

    return accu_rf


def weather(time,stamp,WSWD,RF):
    wswd,rainfall = [],[]

    # 遍歷所有電塔
    for i in ref.tower_list:
        try:
            # 拉取風速風向雨量資料
            list_ws1,list_ws2,list_rf,last_list_rf,wd1,wd2,edtime = chart_weather(ref.weather,i['tbname'],time,stamp,ref.web,i['TowerID'])

            if RF != '0':
                #計算雨量
                rf = cal_rf(list_rf,last_list_rf,time,RF,i['TowerID'],stamp)
                rainfall.append([i['TowerID'],i['RouteID'],rf,edtime])

            # 計算風速風向
            ws1,ws2,wd1,wd2=cal_wswd(list_ws1,list_ws2,wd1,wd2,i['wd1_deflection'],i['wd2_deflection'],stamp)
            wswd.append([i['TowerID'],i['RouteID'],ws1,ws2,wd1,wd2,edtime])
            
        except Exception as e:
            go_to_log(ref.log_path,i['TowerID']+':'+e)
    
    if RF != '0':
        # check -1 data ,catch cwb and acc data replace
        rainfall = check_err_data(time,'rainfall',rainfall)
        # insert rainfall
        post_rf(ref.web,RF,rainfall)
    # check -1 data ,catch cwb and acc data replace
    wswd = check_err_data(time,'wswd',wswd)
    # insert wswd
    post_wswd(ref.web,WSWD,wswd)



if __name__ == "__main__":
    # 風速可用小時平均,10分鐘平均...
    # 風向須取整點風向

    time = datetime.now()
    check_newData(time)
    check_miss_data(time)