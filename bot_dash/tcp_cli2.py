import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.219.101', 5102))

while(True):
    # 접속할 서버의 ip주소와 포트번호를 입력. sock.send('Hello'.encode())
    try:
        time.sleep(1)
        data=sock.recv(1024)
        print(data.decode('utf-8')+"\n")
        if ("sensor_out" in data.decode('utf-8')):
            print("TCP over")
            sock.close()
            break
        sock.send("sensor ack".encode()) # 내가 전송할 데이터를 보냄.
    except:
        print("socket end")
        sock.close()
        break