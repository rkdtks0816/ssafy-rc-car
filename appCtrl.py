from Raspi_PWM_Servo_Driver import PWM
from time import sleep
import socket
import requests

HOST = '0.0.0.0'  # 모든 인터페이스에서 접속 허용
PORT = 65431   # 사용할 포트

pwm = PWM(0x6F)
pwm.setPWMFreq(60) 

servo_pin = 0
cam_x_pin = 1 # 170 370 570 좌 우 200
cam_y_pin = 14
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

baseSpeed = 1000
speed = baseSpeed
cam_x = 150
cam_y = 710
power = 'OFF'
cmd = 'P'

def InsertState():
    url = f"http://192.168.110.164:3001/InsertState?mode=controller&{cmd}&power={power}"
    # GET 요청 보내기
    requests.get(url)
def D():
    global cam_x, cmd
    if speed == 0:
        pwm.setPWM(dc_pin2, 0, 4096)
        pwm.setPWM(dc_pin1, 4096, 0)
        cmd = 'D'
        InsertState()
def R():
    global cam_x, cmd
    if speed == 0:
        pwm.setPWM(dc_pin1, 0, 4096)
        pwm.setPWM(dc_pin2, 4096, 0)
        cmd = 'R'
        InsertState()
def P():
    global nowgear
    if speed == 0:
        pwm.setPWM(dc_pin1, 0, 4096)
        pwm.setPWM(dc_pin2, 0, 4096)
        cmd = 'P'
        InsertState()
def X(value):
    direction = int(250 + 200 * (value / 256))
    pwm.setPWM(servo_pin, 0, direction)
def CamX(value):
    global cam_x
    cam_x = int(570 - 400 * (value / 256))
    pwm.setPWM(cam_x_pin, 0, cam_x)
def CamY(value):
    global cam_y
    cam_y = int(450 - 100 * (value / 256))
    pwm.setPWM(cam_y_pin, 0, cam_y)
def Accel(value):
    global speed
    if speed >= baseSpeed:
        speed = int(baseSpeed + (4096 - baseSpeed) * (value / 256))
        pwm.setPWM(speed_pin, 0, speed)
def Break(value):
    global speed
    speed = int(baseSpeed - (baseSpeed * (value / 255)))
    pwm.setPWM(speed_pin, 0, speed)
def StartUp():
    global power
    if speed == 0:
        if power == 'OFF':
            power = 'ON'
        elif power == 'ON':
            power = 'OFF'
        InsertState()
        print(power)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('클라이언트 접속:', addr)
        accumulated_data = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                data = data.decode()  # 바이트를 문자열로 변환
                accumulated_data += data
                
                # 데이터가 끝에 줄 바꿈 문자가 있는지 확인
                if '\n' in accumulated_data:
                    lines = accumulated_data.split('\n')
                    for line in lines[:-1]:
                        data_values = line.split(',')
                        if len(data_values) == 2:
                            code, value = map(int, data_values)
                            if code == 308 and value == 1:
                                StartUp()
                            elif code == 10:
                                Break(value)
                            if power == 'ON':
                                if code == 304 and value == 1:
                                    D()
                                elif code == 305 and value == 1:
                                    R()
                                elif code == 307 and value == 1:
                                    P()
                                elif code == 0:
                                    X(value)
                                elif code == 2:
                                    CamX(value)
                                elif code == 5:
                                    CamY(value)
                                elif code == 9:
                                    Accel(value)
                                elif code == 10:
                                    Break(value)
                        else:
                            print("잘못된 데이터 형식:", data_values)
                    accumulated_data = lines[-1]  # 남은 데이터를 다음 반복에서 처리
            except ValueError as e:
                print("데이터 디코딩 오류:", e)
