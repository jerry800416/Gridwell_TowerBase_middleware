# -*- coding: utf-8 -*-
 

#####################################################################
#                              original                      by 瑞昌 #
#####################################################################
# for DB
# db_info = ('localhost','gridwell','gridwell123')
db_info = ('211.23.162.130','gridwell','gridwell123')
#DB_name
weather = 'TowerBase_Weather'
web = 'TowerBase_WEB'
#web table
WSWD_list =['chart_WSWD_avg10min','chart_WSWD_avghour','chart_WSWD_avgday','chart_WSWD_avgmonth']
RF_list = ['0','chart_Rainfall_avghour','chart_Rainfall_avgday','chart_Rainfall_avgmonth']
# Tower_list information
tower_list = [
    {'tbname':'Tower_1','TowerID':87,'RouteID':2,'wd1_deflection':-90,'wd2_deflection':90},
    {'tbname':'Tower_2','TowerID':88,'RouteID':2,'wd1_deflection':0,'wd2_deflection':90},
    {'tbname':'Tower_3','TowerID':94,'RouteID':2,'wd1_deflection':45,'wd2_deflection':135},
    {'tbname':'Tower_4','TowerID':97,'RouteID':2,'wd1_deflection':-23,'wd2_deflection':67},
    {'tbname':'Tower_7','TowerID':34,'RouteID':1,'wd1_deflection':23,'wd2_deflection':113},
    {'tbname':'Tower_9','TowerID':95,'RouteID':2,'wd1_deflection':-23,'wd2_deflection':67},
    {'tbname':'Tower_10','TowerID':96,'RouteID':2,'wd1_deflection':-23,'wd2_deflection':67},
    {'tbname':'Tower_11','TowerID':51,'RouteID':1,'wd1_deflection':60,'wd2_deflection':150}]


log_path = './log.txt'