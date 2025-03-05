import serial
import socket
import struct
import time

# 서버 설정
HOST = '192.168.110.165'  # 서버의 IP 주소
PORT = 65432              # 사용 중인 서버의 포트

# UART 설정 (패리티 비트 추가 가능)
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1, parity=serial.PARITY_EVEN)

def compute_checksum(data):
    """ 간단한 체크섬 계산 (XOR 방식) """
    checksum = 0
    for byte in data:
        checksum ^= byte  # XOR 연산
    return checksum

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    while True:
        if ser.in_waiting >= 5:  # 4바이트 데이터 + 1바이트 체크섬
            data = ser.read(5)   # 5바이트(데이터 4바이트 + 체크섬 1바이트) 읽음
            
            # 체크섬 검증
            received_checksum = data[-1]  # 마지막 바이트가 체크섬
            computed_checksum = compute_checksum(data[:-1])  # 앞 4바이트의 체크섬 계산
            
            if received_checksum == computed_checksum:
                # 두 개의 2바이트 데이터 변환 (빅 엔디안에서 리틀 엔디안으로 변환)
                data_x = (data[0] << 8) | data[1]
                data_y = (data[2] << 8) | data[3]
                
                data_to_send = f'{data_x},{data_y}'
                s.sendall(data_to_send.encode())  # 문자열을 바이트로 변환하여 전송
                
                print(f'Sent: {data_to_send}')
            else:
                print('Checksum error: Discarding packet')
        
        time.sleep(0.01)  # CPU 부하 방지
