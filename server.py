import sys
import socket
import selectors
import types




def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        #print('EVENT_READ')
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            ##print(type(recv_data))
            ##print_msg(recv_data)
            data.outb += recv_data
        #else:
            #print("closing connection to", data.addr)
            #sel.unregister(sock)
            #sock.close()
    if mask & selectors.EVENT_WRITE:
        #print('EVENT_WRITE')
        if data.outb:
            print(repr(data.outb))
            #print("echoing", repr(data.outb), "to", data.addr)
            #print_msg(data.outb)
            #sent = sock.send(data.outb)  # Should be ready to write
            #data.outb = data.outb[sent:]
            data.outb = ''.encode()#None


def print_msg(msg):
    for byte in msg:
        print(chr(byte), end='')
    


#if len(sys.argv) != 3:
#    print("usage:", sys.argv[0], "<host> <port>")
#    sys.exit(1)
#host, port = sys.argv[1], int(sys.argv[2])
#print(type(input()))

#host = input('host (press <enter> to listen all hosts)>> ')
#port = input('port (press <enter> for 6667)>> ')
#if '' == port:
#	port = 6667
#else:
#	port = int(port)
host, port = '', 6667

sel = selectors.DefaultSelector()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

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

