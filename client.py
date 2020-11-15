import socket


def print_msg(msg):
    for byte in msg:
        print(chr(byte), end='')


#host = input('host (press <enter> for localhost)>> ')
#if '' == host:
#    host = '127.0.0.1'
#port = input('port (press <enter> for 6667)>> ')
#if '' == port:
#	port = 6667
#else:
#	port = int(port)
host, port = '127.0.0.1', 6667


msg = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    while(msg != 'exit'):
        msg = input('msg>> ')
        #print_msg(msg.encode())
        sock.send(msg.encode())
        #data = s.recv(1024)

#print("Received", repr(data))
