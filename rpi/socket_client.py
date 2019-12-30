# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:34:34 2019

@author: 1903024
"""
import socket
import time
import os
from subprocess import call

if __name__ == '__main__':
    station_no = os.uname()[1][-1]
    server = socket.socket()        
    host = '192.168.1.24'+str(station_no)
    port = 5002     
    while True:
        try:        
            server.bind((host, port))    
        except:
            print('連線失敗')
            time.sleep(5)
        else:
            break   
    server.listen(5)  
    status = 0        
    while True:# conn就是客戶端鏈接過來而在服務端為期生成的一個鏈接實例
        conn,addr = server.accept() #等待鏈接,多個鏈接的時候就會出現問題,其實返回了兩個值    
        try:
            data = conn.recv(1024)  #接收數據
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print('recive:',data.decode()) #打印接收到的數據
            if data.decode() == 'connect':  
                file_name = 'station'+str(station_no)+'_gps.txt'
                f = open(file_name, "r")
                coordinate = f.readline().split(' ')
                lon = coordinate[0]
                lat = coordinate[-1] 
                #status,lat,lon
                msg = str(station_no)+','+str(status)+','+str(lat)+','+str(lon)
                conn.send(msg.encode('utf-8')) #然後再發送數據            
            temp = data.decode().split(',')
            if temp[0] == 'shutdown' and temp[1] == str(station_no):
                msg = temp[0]
                conn.send(msg.encode('utf-8'))
                call('sudo shutdown -h now', shell=True)   
                 
        except ConnectionResetError as e:
            print('關閉了正在佔線的鏈接！')
            break
    conn.close()         
