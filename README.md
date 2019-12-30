# rpi_edge_flood
利用樹梅派建立邊緣裝置用於淹水監控

# 安裝樹莓派作業系統
1. 下載系統映像檔，執行下列指令
   
       $git clone https://drive.narlabs.org.tw/navigate/s/0C13973B723C45F2BED82D7562A6AD21GUY
   
2. 安裝系統映像檔，詳細安裝說明請參考
   
       https://sites.google.com/site/raspberypishare0918/home/di-yi-ci-qi-dong
   
3. 開機啟動腳本和code，已整合至樹莓派映像檔，不需額外安裝其它套件

# 樹莓派相關參數設定
## 系統設定
   1. 目前有6台主機，因此主機名稱編排格式為thb001~thb006
   2. 設定主機名稱，執行下列步驟
   
          選單>>偏好設定>>Raspberry PI設定>>主機名稱   
       
   __程式會根據主機名稱進行判斷請依照格式編號__
   
![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/menu_config.JPG)
![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/name.JPG)

## 網路設定
   1. 建議4G網卡使用:中華電信/遠傳電信/台灣大哥大
   2. 首先須將sim卡密碼清除，將sim卡裝入手機中進行清除，使用android手機為例:
   
    設定>>安全性>>設定SIM卡鎖定>>輸入PIN1碼>>SIM卡鎖關閉
   
   3. 關機並將SIM卡移除並安裝至臨時影像辨識站，即完成4G網路設定
   4. VPN連線設定，設定VPN帳號、密碼、IP，執行下列指令進行更改

    $sudo nano /etc/ppp/peers/picv

![demo](https://github.com/healthy8701/rpi_edge_flood/blob/master/img/vpn.JPG?raw=true)

   5. 設定完成，重新開機即完成VPN設置

