import serial
from time import sleep
import socket

HOST = '192.168.110.165'  # 서버의 IP 주소
PORT = 65432           # 사용 중인 서버의 포트

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        if ser.in_waiting >= 4:  # 전체 패킷을 모두 수신할 때까지 기다림
            data = ser.read(4)  # 4바이트 데이터를 읽음

            # 두 개의 2바이트 데이터로 분리 (빅 엔디안에서 리틀 엔디안으로 변환)
            data_x = (data[0] << 8) | data[1]
            data_y = (data[2] << 8) | data[3]
            data_to_send = f'{data_x},{data_y}'
            s.sendall(data_to_send.encode())  # 문자열을 바이트로 변환하여 전송
            # data = s.recv(1024)
            
            # print('Received', data.decode())  # 받은 데이터를 문자열로 변환하여 출력