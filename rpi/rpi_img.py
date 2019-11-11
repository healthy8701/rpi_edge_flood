import cv2
import time
import os
import subprocess
from ftplib import FTP 

def detect(image1, image2, size=(256, 256)):    
    grey1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grey2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    grey1 = cv2.resize(grey1, size)
    grey2 = cv2.resize(grey2, size)    
    blur1 = cv2.GaussianBlur(grey1, (7,7), 0)
    blur2 = cv2.GaussianBlur(grey2, (7,7), 0)   
    img_delta = cv2.absdiff(blur1, blur2)
    thresh = cv2.threshold(img_delta, 25, 255 , cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    image, contours , hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    degree = 0   
    if contours != []:
      num = 0
      for i in contours:
        degree = degree+cv2.contourArea(i)
        num= num+1
      degree = degree/num
      
    return degree


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
        print('ip:'+ip+' time:'+str(time.time()-t1))
    except:
        f = open("upload_error.log", "w")
        f.write('upload error: '+ip+' '+file_name+'\n')
        f.close()

def cap(localtime,station_id,ftp_ip_1,ftp_ip_2,dir_name_1,dir_name_2):    
    cap = cv2.VideoCapture('http://127.0.0.1:8080/?action=stream')
 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  
    ret, frame = cap.read()   
    dir_name = '_'.join(map(str,localtime[:3]))
    file_name = station_id+'_'.join(map(str,localtime[:6]))
    if not os.path.exists('/home/pi/Desktop/img_backup/'+dir_name):
        os.makedirs('/home/pi/Desktop/img_backup/'+dir_name)
    path = '/home/pi/Desktop/img_backup/'+dir_name+'/'+file_name+'.jpg'
    print(file_name) 
    cv2.imwrite(path,frame)    
    photo_mame = file_name+'.jpg'
    upload(path,photo_mame,ftp_ip_1,'tbh','picv0624',dir_name_1)
    upload(path,photo_mame,ftp_ip_2,'wraflood','wra@nchc',dir_name_2)  
  
    cap.release()


def standby():
    port = 8080
    command = "sudo netstat -tulpn|grep :%s" % port
    pids = subprocess.check_output(command, shell=True)
    pid = int(str(pids).split('LISTEN')[1].split('/')[0])
    command = 'sudo kill -9 %s' % pid
    os.system(command)

def start():
    mjpggo = 'sudo modprobe bcm2835-v4l2 && LDPRELOAD=/usr/lib/uv4l/uv4lext/armv6l/libuv4lext.so sudo /home/pi/code/mjpg-streamer/mjpg_streamer -i "/home/pi/code/mjpg-streamer/input_uvc.so -n -y -f 15 -r 1280x720" -o "/home/pi/code/mjpg-streamer/output_http.so -n -w /usr/local/www" &'
    os.system(mjpggo)
    
if __name__ == '__main__':	 
    station_no = int(os.uname()[1][-3:])
    station_id = 'thb00'+str(station_no)+'_'
    ftp_ip_1 = '140.110.27.122'
    ftp_ip_2 = '140.110.17.176'
    dir_name_1 = 'station'+str(station_no)+'/input'
    dir_name_2 = 'station'+str(station_no)+'/input'    
    
    standby_bool = 0
    time_standby = 19
    time_start = 6
    
    start()    
    time.sleep(5)
    localtime = list(time.localtime(time.time()))
    min_temp = localtime[4]
    cap(localtime,station_id,ftp_ip_1,ftp_ip_2,dir_name_1,dir_name_2)
    
    while(1):
        localtime = list(time.localtime(time.time()))    
        if localtime[3] >= time_standby and standby_bool == 1:
            standby()
            print('standby...')
            while localtime[3] != time_start :                 
                time.sleep(60)
                localtime = list(time.localtime(time.time())) 
            start()  
            print('stream start: '+str(localtime[3])+':'+str(localtime[4]))
          
        if min_temp != localtime[4]:              
            cap(localtime,station_id,ftp_ip_1,ftp_ip_2,dir_name_1,dir_name_2)
            min_temp = localtime[4]
