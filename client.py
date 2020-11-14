import socket


host = input('host (press <enter> for localhost)>> ')
if '' == host:
    host = '127.0.0.1'

port = input('port (press <enter> for 6667)>> ')

if '' == port:
	port = 6667
else:
	port = int(port)

msg = input('msg>> ')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    sock.send(msg.encode())
    #data = s.recv(1024)

#print("Received", repr(data))
