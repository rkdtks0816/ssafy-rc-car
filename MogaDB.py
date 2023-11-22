import evdev
import requests

# 이벤트 디바이스 경로 설정 (아래 경로는 실제 경로가 아닌 예시입니다)
device_path = '/dev/input/event0'

# evdev 디바이스 열기
device = evdev.InputDevice(device_path)

# API 엔드포인트 및 명령 설정
api_url = 'http://192.168.110.164:3001/InsertCmd?Cmd='

def Y(dataY):
    if dataY > 150:
        return 'back'
    elif dataY > 100:
        return 'stop'
    else:
        return 'go'
def X(dataX):
    if dataX > 150:
        return 'right'
    elif dataX > 100:
        return 'mid'
    else:
        return 'left'
def CAM(value):
    if value == -1:
        return 'up'
    elif value == 1:
        return 'down'

# 이벤트 루프 시작
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_ABS:
        if event.code == 1:
            requests.get(f"{api_url}{Y(event.value)}")
            print(Y(event.value))
        if event.code == 0:
            requests.get(f"{api_url}{X(event.value)}")
            print(X(event.value))
        if event.code == 17 and event.value != 0:
            requests.get(f"{api_url}{CAM(event.value)}")
            print(CAM(event.value))
    # elif event.type == evdev.ecodes.EV_KEY:
