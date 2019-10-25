# -*- coding: utf-8 -*-
from towerbase_lib import check_newData,check_miss_data
# from towerbase_ref import *
from datetime import datetime,timedelta


time = datetime.now()
# 檢查有無新資料
check_newData(time)
# 檢查漏傳資料
check_miss_data(time)