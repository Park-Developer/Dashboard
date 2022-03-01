import socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.connect(('192.168.219.101', 5100)) # 접속할 서버의 ip주소와 포트번호를 입력. sock.send('Hello'.encode())
sock.send('Hello'.encode()) # 내가 전송할 데이터를 보냄.

