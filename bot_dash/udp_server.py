import socket 

sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

sock.bind(('127.0.0.1',8080))
while(1):
    data,addr=sock.recvfrom(200)

    print("server is received data", data.decode())

