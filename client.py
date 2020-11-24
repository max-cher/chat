import socket
from multiprocessing import Queue
import sys
import threading
import configparser
import os




keywords = {'exit' : ['/exit', '/quit', '/leave', '/q'],
            'me' : ['/me'],
            }



def get_input():
    global run_flag
    #for line in iter(input, 0):#sys.stdin.readline, ''):
    while run_flag:
        q_send.put(input(''))
    sys.stdin.close()


def send_msg():
    global run_flag
    while run_flag:
        msg = q_send.get().replace('\n', '')
        if msg not in keywords['exit']:
            sock.send(msg.encode())
        elif msg in keywords['exit']:
            sock.send('Press <Enter>'.encode()) # dirty hack to unblock rcv_msg and then close the connection
            run_flag = False


def rcv_msg():
    global run_flag
    while run_flag:
        data = sock.recv(1024)
        if(data):
            print(data.decode('utf-8'))


def get_host():
    #config = configparser.ConfigParser()
    #if os.path.exists('config.ini'):          
    #    config.read('config.ini')
    #    #print(config.sections())
    #    host = config['DEFAULT']['host']
    #    port = int(config['DEFAULT']['port'])
    
    host, port = '192.168.127.254', 23  # debug mode!
    host1 = input('host (press <enter> for {})>> '.format(host))
    if '' != host1:
        host = host1
    
    port1 = input('port (press <enter> for {})>> '.format(port))
    if '' != port1:
        port = int(port1)
    
    return host, port




print('CLIENT')
host, port = get_host()
run_flag = True
msg = ''

q_send = Queue()
q_recv = Queue()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('connecting to {} port {}'.format(host, port))
    sock.connect((host, port))
    #sock.setblocking(False)
    
    
    
    input_getter = threading.Thread(name='input-getter', target=get_input).start()
    sender = threading.Thread(name='sender', target=send_msg).start()
    receiver = threading.Thread(name='receiver', target=rcv_msg).start()
    
    
    while(run_flag):
        pass

