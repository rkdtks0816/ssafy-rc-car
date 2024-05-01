from Raspi_PWM_Servo_Driver import PWM
from time import sleep
import socket

HOST = '0.0.0.0'  # 모든 인터페이스에서 접속 허용
PORT = 65432      # 사용할 포트

pwm = PWM(0x6F)
pwm.setPWMFreq(60) 

servo_pin = 0
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

servoLeft = 250  # Min pulse length out of 4096
servoCenter = 350
servoRight = 450  # Max pulse length out of 4096
speed = 100

pwm.setPWM(speed_pin, 0, speed*16)
pwm.setPWM(servo_pin, 0, servoCenter)

def Y(dataY):
    if dataY > 3500:
        pwm.setPWM(dc_pin2, 0, 4096)
        pwm.setPWM(dc_pin1, 4096, 0)
    elif dataY > 1500:
        pwm.setPWM(dc_pin1, 0, 4096)
        pwm.setPWM(dc_pin2, 0, 4096)
    else:
        pwm.setPWM(dc_pin1, 0, 4096)
        pwm.setPWM(dc_pin2, 4096, 0)
def X(dataX):
    if dataX > 3500:
        pwm.setPWM(servo_pin, 0, servoRight)
    elif dataX > 1500:
        pwm.setPWM(servo_pin, 0, servoCenter)
    else:
        pwm.setPWM(servo_pin, 0, servoLeft)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('클라이언트 접속:', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            data = data.decode()  # 바이트를 문자열로 변환
            data_x, data_y = data.split(',')  # 쉼표를 기준으로 데이터 분리
            data_x = int(data_x)
            data_y = int(data_y)
            X(data_x)
            Y(data_y)