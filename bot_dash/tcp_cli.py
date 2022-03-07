import socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('192.168.219.101', 5101)) 

while(True):
    # 접속할 서버의 ip주소와 포트번호를 입력. sock.send('Hello'.encode())
    #inputdata=input()
    sock.send("cli send".encode()) # 내가 전송할 데이터를 보냄.
    data=sock.recv(1024)
    print(data.decode('utf-8'))
