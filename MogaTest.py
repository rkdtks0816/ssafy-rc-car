import evdev

# 이벤트 디바이스 경로 설정 (아래 경로는 실제 경로가 아닌 예시입니다)
device_path = '/dev/input/event0'

# evdev 디바이스 열기
device = evdev.InputDevice(device_path)

# 이벤트 루프 시작
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_ABS:
        print(f"Absolute event - Code: {event.code}, Value: {event.value}")
    elif event.type == evdev.ecodes.EV_KEY:
        print(f"Key event - Code: {event.code}, Value: {event.value}")
