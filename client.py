import socket
from multiprocessing import Queue
import threading


keywords = {'exit' : ['/exit', '/quit', '/leave', '/q'],
            'me' : ['/me'],
            }


class Client():
    
    def __init__(self):
        print('=CLIENT=')
        self.set_host()
        self.run_flag = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            print('Connecting to {} port {}'.format(self.host, self.port))
            self.sock.connect((self.host, self.port))
            self.sender = threading.Thread(name='sender', target=self.send_msg).start()
            
            while(self.run_flag):
                self.data = self.sock.recv(1024)
                if(self.data):
                    print(self.data.decode('utf-8'))

    def set_host(self):
        self.host, self.port = '192.168.127.254', 23  # default
        host = input('Host (press <Enter> for {})>> '.format(self.host))
        if '' != host:
            self.host = host
        
        while True:
            port = input('Port (press <Enter> for {})>> '.format(self.port))
            if '' != port:
                try:
                    self.port = int(port)
                    break
                except:
                    print('Port must be num type!')
            break

    def send_msg(self):
        while self.run_flag:
            self.msg = input('').replace('\n', '')
            if self.msg not in keywords['exit']:
                self.sock.send(self.msg.encode())
            elif self.msg in keywords['exit']:
                self.sock.send(' '.encode()) # dirty hack to unblock rcv_msg and then close the connection
                self.run_flag = False
    
    def __del__(self):
        print('Disconnecting')



if __name__ == '__main__':
    Client()



