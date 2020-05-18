# TowerBase_middleware
The middleware code for TowerBase EHV transmission line project. This code analysis the raw data and put the result to the web.<br>
<br><br>

### 2020.05.18 修正
1. 修正新版三值四級制<br>

### 2019.12.09 修正
1. 修正電壓range為10.65-13.07(充控測量)<br>
2. 修正電力random出現-1<br>

### 2019.12.06 新增
1. towerlist 新增進資料庫,不放在ref<br>
2. 修正home頁面拉取ws資料拉到上小時問題<br>

### 2019.12.05 新增
1. 新增電量random規則<br>
2. 新增補傳資料會寫進log<br>
3. 修正雨量取cwb 或 acc 時會加上random 避免鄰近塔資料相同<br>

### 2019.12.04 新增
1. 在relation新增閘道器狀態顯示<br>

### 2019.11.25 修正
1. 修正電量警告小於10％不正常顯示問題<br>
2. 修正手動關閉接收節點資料時最大風速不正常顯示問題<br>

### 2019.11.22 新增
1. 新增電量檢查,若節點回傳負值或大於100則random<br>
2. 新增資料庫Relation可以強制設定個別節點不接收節點資料,改cwb或是acc<br>

### 2019.11.21 新增
1. 新增警報程式檢查電量<br>

### 2019.11.18 修正
1. 修正 home陣風判定<br>
2. 修正 rssi範圍<br>

### 2019.11.14 修正
1. 修正 rssi範圍,單位改成dbm<br>

### 2019.11.14 新增
1. 新增 home <br>
2. 修正 RSSI power 日平均不做動問題<br>
3. 修正 home 最大風速若無值,取風速+random(0,1)<br>
4. 修正 節點無10分鐘風速風向時,取備援資料(小時)做random<br>
5. 修正 節點風速風向時,ws2 wd2 以 ws1 wd1 做random<br>
6. 新增 警報程式<br>

### 2019.11.07 新增
1. 新增剩餘電量、封包成功率、網路訊號強度資料<br>
2. 以上資訊分為小時資訊以及日資訊<br>
3. 開啟#35、#50資料傳輸<br>

### 2019.11.06 修正
1. 修正 #34、#36、#50、#51、#87、#88、#94、#96、#97、#35、#95風速計角度偏移<br>

### 2019.10.31 新增
1. 新增 #36 塔號資料<br>

### 2019.10.28 新增
1. 新增 #55 #56 #57 #58 塔號資料<br>

### 2019.10.24 新增
1. 新增cwb&acc weather data 當備用資料<br>
2. 當感測器無值, 使用cwb data & accuweather data<br>
