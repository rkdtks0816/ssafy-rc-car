from Raspi_PWM_Servo_Driver import PWM
from time import sleep
import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 접속 허용
PORT = 65431   # 사용할 포트

pwm = PWM(0x6F)
pwm.setPWMFreq(60) 

servo_pin = 0
cam_x_pin = 14
cam_y_pin = 1
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

servoLeft = 250  # Min pulse length out of 4096
servoCenter = 350
servoRight = 430  # Max pulse length out of 4096
servoCam = 350
baseSpeed = 1000
speed = baseSpeed
isStart = 0

pwm.setPWM(speed_pin, 0, speed)
pwm.setPWM(servo_pin, 0, servoCenter)

def D():
    pwm.setPWM(dc_pin2, 0, 4096)
    pwm.setPWM(dc_pin1, 4096, 0)
def R():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 4096, 0)
def P():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 0, 4096)
def X(value):
    direction = int(servoLeft + 200 * (value / 256))
    pwm.setPWM(servo_pin, 0, direction)
def CamX(value):
    global servoCam
    direction = int(670 - 600 * (value / 256))
    pwm.setPWM(cam_x_pin, 0, direction)
def CamY(value):
    global servoCam
    direction = int(560 - 300 * (value / 256))
    pwm.setPWM(cam_y_pin, 0, direction)
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
    global isStart
    if speed == 0:
        if isStart == 0:
            isStart = 1
        elif isStart == 1:
            isStart = 0
            P()
    print(isStart)

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
                            if isStart == 1:
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
