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
WSWD_list =['chart_WSWD_avg10min','chart_WSWD_avghour','chart_WSWD_avgday','chart_WSWD_avgmonth','Home']
RF_list = ['0','chart_Rainfall_avghour','chart_Rainfall_avgday','chart_Rainfall_avgmonth','0']
NI_list = ['0','chart_nodeinfo_avghour','chart_nodeinfo_avgday','0','0']
# Tower_list information
tower_list = [
    {'tbname':'Tower_1','TowerID':87,'RouteID':2,'wd1_deflection':275,'wd2_deflection':185},
    {'tbname':'Tower_2','TowerID':88,'RouteID':2,'wd1_deflection':106,'wd2_deflection':16},
    {'tbname':'Tower_3','TowerID':94,'RouteID':2,'wd1_deflection':-9,'wd2_deflection':81},
    {'tbname':'Tower_4','TowerID':97,'RouteID':2,'wd1_deflection':-21,'wd2_deflection':69},
    {'tbname':'Tower_5','TowerID':35,'RouteID':1,'wd1_deflection':-126,'wd2_deflection':54},
    {'tbname':'Tower_6','TowerID':50,'RouteID':1,'wd1_deflection':255,'wd2_deflection':165},
    {'tbname':'Tower_7','TowerID':34,'RouteID':1,'wd1_deflection':98,'wd2_deflection':8},
    {'tbname':'Tower_8','TowerID':36,'RouteID':1,'wd1_deflection':76,'wd2_deflection':31},
    {'tbname':'Tower_9','TowerID':95,'RouteID':2,'wd1_deflection':86,'wd2_deflection':-4},
    {'tbname':'Tower_10','TowerID':96,'RouteID':2,'wd1_deflection':67,'wd2_deflection':-23},
    {'tbname':'Tower_11','TowerID':51,'RouteID':1,'wd1_deflection':66,'wd2_deflection':156},
    {'tbname':'Tower_12','TowerID':56,'RouteID':3,'wd1_deflection':174,'wd2_deflection':84},
    {'tbname':'Tower_13','TowerID':58,'RouteID':3,'wd1_deflection':69,'wd2_deflection':159},
    {'tbname':'Tower_14','TowerID':57,'RouteID':3,'wd1_deflection':-7,'wd2_deflection':173},
    {'tbname':'Tower_15','TowerID':55,'RouteID':3,'wd1_deflection':152,'wd2_deflection':62}]




log_path = './log.txt'