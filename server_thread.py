import sys
import socket
#import selectors
import types

from multiprocessing import Queue
import threading


keywords = ['/exit',
            '/nick',
            '/me',
            '/who',
            '/help',
            ]


def accept_wrapper(sock):
    '#Callback for new connections'
    conn, addr = sock.accept()  # Should be ready to read
    print('#accepted connection from', addr)
    #clients.append(client(sock))
    clients[addr[1]] = client(sock, int(addr[1]))
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            clients.pop(data.addr[1])
            #print(sock)
            sel.unregister(sock)
            sock.close()
            
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            
            msg_from = data.outb.decode('utf-8')
            if len(msg_from.split()) > 1:
                keyword  = msg_from.split()[0]
                msg_tail = msg_from.replace(keyword + ' ', '')
            else:
                keyword  = msg_from
                msg_tail = ''
            client_from = clients[sock.getpeername()[1]]
            #print('keyword: [', type(keyword), '] : [', keyword , '] len = ', len(keyword), sep='')
            
            
            if keyword not in keywords:
                send_all(client_from.nick + ': ' + msg_from)
                #if(len(clients) > 1):
                #    sent = sock.send(data.outb)  # Should be ready to write
                #data.outb = data.outb[sent:]
            elif keyword == '/nick':
                client_from.set_nick(msg_tail)
            elif keyword == '/who':
                for cl in clients:
                    client_from.send_msg(clients[cl].nick)
            elif keyword == '/me':
                send_all('#' + client_from.nick + ' ' + msg_tail)
            else:
                print('en tieda...')
                
            data.outb = ''.encode()#None

def send_all(msg):
    for client_id in clients:
        clients[client_id].send_msg(msg)

class client():
    
    counter = 0
    
    def __init__(self, sock, id):
        self.sock = sock
        self.id = id
        client.counter += 1
        self.nick = 'client_' + str(self.id)
        self.send_msg('Welcome to server! your nick is{}.\nType "/nick <new nick>" to change it'.format(self.nick))
        send_all('#' + self.nick + ' connected')
        client.print_clients()
    
    def __del__(self):
        client.counter -= 1
        print('#closing connection to', self.nick)
        #sel.unregister(self.sock)
        #self.sock.close()
        #print(self.sock)
        client.print_clients()
    
    def set_nick(self, nick):
        print('#now {} is {}'.format(self.nick, nick))
        self.nick = nick
    
    def send_msg(self, msg):
        '''
        msg can be bytes or str
        '''
        if type(msg) == type('a'.encode()):
            msg =  msg.decode('utf-8')
        print('sending to: {}, msg: {}'.format(self.nick, msg))
        self.sock.send(msg.encode())
        pass
    
    def print_clients():
        print('Total clients connected: {}'.format(client.counter))




def get_host():
    '''
    get host, port from keyboard
    '''
    #host, port = sys.argv[1], int(sys.argv[2])
    #print(type(input()))
    
    #host = input('host (press <enter> to listen all hosts)>> ')
    #port = input('port (press <enter> for 6667)>> ')
    #if '' == port:
    #	port = 6667
    #else:
    #	port = int(port)
    host, port =  '', 6667 # debug mode
    return host, port

host, port = get_host()

sel = selectors.DefaultSelector()

print('SERVER')

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('listening on', (host, port))
lsock.setblocking(False)

sel.register(lsock, selectors.EVENT_READ, data=None)

clients = {}

#try:
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            #print('accept_wrapper()')
            accept_wrapper(key.fileobj)
        else:
            #print('service_connection()')
            service_connection(key, mask)
#except KeyboardInterrupt:
#    print("caught keyboard interrupt, exiting")
#except:
#	input('END/n')
#finally:
#    sel.close()
sel.close()

