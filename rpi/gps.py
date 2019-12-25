import time
import serial
from ftplib import FTP
import os

def upload(path,file_name,ip,account,password,dir_name): 
    try:
        t1 = time.time()
        ftp=FTP() 
        ftp.set_debuglevel(0) 
        ftp.connect(ip,21) 
        ftp.login(account,password)
        bufsize=1024 
        ftp.storbinary('STOR /'+dir_name+'/'+file_name,open(path, 'rb'), bufsize)
        ftp.quit() 
        print('ip:'+ip+' time:'+str(time.time()-t1)+'\n')
    except:
        f = open("error.log", "w")
        f.write('upload error: '+ip+' '+file_name+'\n')
        f.close()

def parseGPS(data):    
    sdata = data.split(",")
    if sdata[2] == 'V':
        print ("no satellite data available")
        return 
    print ("-----Parsing GPRMC-----")
    time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
    lat = decode(sdata[3]) #latitude
    dirLat = sdata[4]      #latitude direction N/S
    lon = decode(sdata[5]) #longitute
    dirLon = sdata[6]      #longitude direction E/W
    speed = sdata[7]       #Speed in knots
    trCourse = sdata[8]    #True course
    date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]
                       #date
    variation = sdata[10]  #variation
    degreeChecksum = sdata[11]
    dc = degreeChecksum.split("*")
    degree = dc[0]        #degree
    checksum =  0     #checksum  
    print(time,lat,dirLat,lon,dirLon,speed,trCourse,date,variation,degree,checksum)
    return [lon,lat]

def decode(coord):
    #Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
    x = str(float(coord)/100).split(".")
    head = x[0]
    tail = round(float(x[1])/60)
    return str(head)+'.'+str(tail)

if __name__ == '__main__':	
    portwrite = "/dev/ttyUSB2"
    port = "/dev/ttyUSB1"
    
    station_no = os.uname()[1][-1]
    station_id = 'thb00'+str(station_no)+'_'
    ftp_ip_1 = ''
    ftp_ip_2 = ''
    rpi_ip = '192.168.1.24'+str(station_no)
    dir_name_1 = 'station'+str(station_no)
    dir_name_2 = 'station'+str(station_no)
    
    print ("Connecting port")
    serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1)
    serw.write(bytes('AT+QGPS=1\r', 'utf8'))
    serw.close()
    time.sleep(2)
    
    print ("Receiving GPS data")
    ser = serial.Serial(port, baudrate = 115200, timeout = 0.5)
    
    while True:
        data = ser.readline()
        print(data)
        data = str(data, encoding = "utf-8")
        if data[0:6] == "$GPRMC":
            gps = parseGPS(data)           
            file_name = 'station'+str(station_no)+'_gps.txt'
            f = open(file_name, "w")
            if gps == None:
                print(str(gps)+'\n')
                serw = serial.Serial(portwrite, baudrate = 115200, timeout = 1)
                serw.write(bytes('AT+QGPS=1\r', 'utf8'))
                serw.close()
                time.sleep(2)                
                print ("Receiving GPS data")
                ser = serial.Serial(port, baudrate = 115200, timeout = 0.5)
                f.write('Null Null')
            else:      
                print(str(gps[0])+','+str(gps[1]))  
                f.write(str(gps[0])+' '+str(gps[1]))
                upload(file_name,file_name,ftp_ip_2,'','',dir_name_2)  
            f.close()   
            time.sleep(30)
 
