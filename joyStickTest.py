import serial
from time import sleep

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

try:
    while True:
        if ser.in_waiting >= 4:  # 전체 패킷을 모두 수신할 때까지 기다림
            data = ser.read(4)  # 4바이트 데이터를 읽음

            if len(data) == 4:
                # 두 개의 2바이트 데이터로 분리 (빅 엔디안에서 리틀 엔디안으로 변환)
                data_x = (data[0] << 8) | data[1]
                data_y = (data[2] << 8) | data[3]
                data_to_send = f'{data_x},{data_y}'
                print(data_to_send)
            else:
                print("Incomplete data received")

except serial.SerialException as e:
    print(f"Serial Exception: {e}")

except KeyboardInterrupt:
    ser.close()
    print("Serial port closed due to KeyboardInterrupt")

finally:
    ser.close()