import socket


keywords = {'exit' : ['/exit', '/quit', '/leave', '/q'],
            'me' : ['/me'],
            }

def print_msg(msg):
    for byte in msg:
        print(chr(byte), end='')

def get_host():
    #host = input('host (press <enter> for localhost)>> ')
    #if '' == host:
    #    host = '127.0.0.1'
    #port = input('port (press <enter> for 6667)>> ')
    #if '' == port:
    #    port = 6667
    #else:
    #    port = int(port)
    host, port = '127.0.0.1', 6667  # debug mode!
    return host, port


host, port = get_host()

print('CLIENT')

msg = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    print('connecting to {} port {}'.format(host, port))
    sock.connect((host, port))
    sock.setblocking(False)
    while(True):
        msg = input('msg>> ')
        if msg not in keywords['exit']:
            sock.send(msg.encode())
        elif msg in keywords['exit']:
            print('closeing connection')
            sock.close()
            break
        #data = s.recv(1024)
    input('press <Enter>')

#print("Received", repr(data))
