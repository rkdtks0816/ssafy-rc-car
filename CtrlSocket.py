import socket
import evdev

HOST = '192.168.110.165'  # 서버의 IP 주소
PORT = 65431  # 사용 중인 서버의 포트

# 이벤트 디바이스 경로 설정 (아래 경로는 실제 경로가 아닌 예시입니다)
device_path = '/dev/input/event0'

# evdev 디바이스 열기
device = evdev.InputDevice(device_path)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    # 이벤트 루프 시작
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_ABS:
            data_to_send = f'{event.code},{event.value}\n'
            s.sendall(data_to_send.encode())  # 문자열을 바이트로 변환하여 전송
        elif event.type == evdev.ecodes.EV_KEY:
            data_to_send = f'{event.code},{event.value}\n'
            s.sendall(data_to_send.encode())  # 문자열을 바이트로 변환하여 전송
