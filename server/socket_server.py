from flask import Flask, request, render_template, url_for
from flask_socketio import SocketIO
import socket
import time

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

@app.route('/')
def index():
    url_for('static', filename='style.css')   
    url_for('static', filename='connect.js')  
    ip = '140.110.27.122'
    port = list(range(8893,8898+1))
    device = []
    for i in range(6):
        device.append({'name': str("%03d" % (i+1)), 'source': 'http://'+ip+':'+str(port[i])+'/?action=stream', 'id': str(i+1)})   
    device.append({'name': 'Test', 'source':'http://140.110.27.122:600/?action=stream'} )
    
    return render_template('rpi_web_v2.0.html',device = device)

@socketio.on('client_event')
def client_msg(msg):               
    host_all = []
    for i in range(6):
        host_all.append('192.168.1.24'+str(i+1))
        
    port = 5002   
    for host in host_all:         
        try:   
            client = socket.socket()
            client.connect((host,port)) #建立一個鏈接   
        except:
            socketio.emit('server_response', {'data': host[-1]+',1,0,0'})   
        else :
            if msg['data'] != None:            
                client.send(msg['data'].encode('utf-8'))  #發送一條信息 python3 只接收btye流
                data = client.recv(1024) #接收一個信息，並指定接收的大小 為1024字節
                if data.decode() != 'shutdown':
                    socketio.emit('server_response', {'data': data.decode()})    
        client.close() #關閉這個鏈接
        
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5001)    

