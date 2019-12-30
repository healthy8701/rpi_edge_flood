# rpi_edge_flood
利用樹梅派建立邊緣裝置用於淹水監控

# 所需硬體設備
- [x] Raspberry Pi 3+
- [x] 8MP Raspberry Pi Camera Module(v2)
- [x] Sixfab 4G/LTE Shield
- [x] Quectel EC25 Mini PCle 4G/LTE Module

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

## GPS設定
   1. 設定GPS抓取座標後，上傳到指定的FTP伺服器
   2. 編輯rpi/gps.py
   3. 找到以下這段程式碼，並設定以下變數，目前上傳至2個FTP伺服器，可視情況更改要上傳的FTP數量
      * ftp_ip_1和ftp_ip_2為FTP伺服器IP
      * station_no為臨時站編號(系統自動抓取無須設定)
      * station_id為臨時站ID(系統自動抓取無須設定)
      * dir_name_1和dir_name_2為FTP資料夾名稱   
   
![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/gps1.JPG)

   4. 找到以下這段程式碼，設定upload()函式，參數依序為影像路徑、影像檔名、FTP IP、FTP帳號、FTP密碼、FTP資料夾
   
![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/gps2.JPG)

   5. 儲存程式碼並複製到樹莓派中的以下路徑中取代
   
    /home/pi

## 影像上傳設定
   1. 設定上傳影像到指定的FTP伺服器
   2. 編輯rpi/rpi_img.py
   3. 找到以下這段程式碼，並設定以下變數，目前上傳至2個FTP伺服器，可視情況更改要上傳的FTP數量
      * ftp_ip_1和ftp_ip_2為FTP伺服器IP
      * station_no為臨時站編號(系統自動抓取無須設定)
      * station_id為臨時站ID(系統自動抓取無須設定)
      * dir_name_1和dir_name_2為FTP資料夾名稱   
      
   ![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/img1.JPG)
   
   4. 找到以下這段程式碼，設定upload()函式，參數依序為影像路徑、影像檔名、FTP IP、FTP帳號、FTP密碼、FTP資料夾
    
   ![demo](https://raw.githubusercontent.com/healthy8701/rpi_edge_flood/master/img/img2.JPG)
   
   5. 儲存程式碼並複製到樹莓派中的以下路徑中取代
   
    /home/pi
    
## 後台設定
   1. 後台無須更改設定，VPN連上後即會自動傳送訊息
   2. 後台程式路徑rpi/socket_client.py
