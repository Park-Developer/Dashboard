import socket 

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while(1):
    data=input()
    sock.sendto(data.encode(), ('192.168.219.101',20162))

    data,addr=sock.recvfrom(200)

    print("server is received data", data.decode())
