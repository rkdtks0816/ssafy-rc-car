import threading
import socket
import requests
import queue
from time import sleep
from Raspi_PWM_Servo_Driver import PWM

# PWM 설정
pwm = PWM(0x6F)
pwm.setPWMFreq(60)

# 핀 정의
servo_pin = 0
cam_x_pin = 14
cam_y_pin = 1
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

# 서보모터 및 카메라 각도 범위 설정
servoLeft, servoCenter, servoRight = 250, 350, 450
cXLeft, cXCenter, cXRight = 170, 370, 570
cYUp, cYCenter, cYDown = 350, 400, 450

# 기본 속도
baseSpeed = 1000
speed = baseSpeed
isStart = 0
power = "OFF"
nowCmd = "rs"

# 우선순위 큐 설정 (낮은 숫자가 높은 우선순위)
command_queue = queue.PriorityQueue()

# PWM 초기화
pwm.setPWM(speed_pin, 0, speed)
pwm.setPWM(servo_pin, 0, servoCenter)
pwm.setPWM(cam_x_pin, 0, cXCenter)
pwm.setPWM(cam_y_pin, 0, cYCenter)

# RC카 이동 함수
def forward():
    pwm.setPWM(dc_pin2, 0, 4096)
    pwm.setPWM(dc_pin1, 4096, 0)

def backward():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 4096, 0)

def stop():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 0, 4096)

# 정지 명령은 최우선으로 실행
def stop_command():
    command_queue.put((0, "stop"))

def steer(value):
    direction = int(servoLeft + 200 * (value / 256))
    pwm.setPWM(servo_pin, 0, direction)

def cam_x(value):
    direction = int(670 - 600 * (value / 256))
    pwm.setPWM(cam_x_pin, 0, direction)

def cam_y(value):
    direction = int(560 - 300 * (value / 256))
    pwm.setPWM(cam_y_pin, 0, direction)

def adjust_speed(value):
    global speed
    speed = int(baseSpeed + (4096 - baseSpeed) * (value / 256))
    pwm.setPWM(speed_pin, 0, speed)

# 명령 실행 함수
def execute_command():
    while True:
        priority, command, value = command_queue.get()
        if command == "stop":
            stop()
        elif command == "forward":
            forward()
        elif command == "backward":
            backward()
        elif command == "steer":
            steer(value)
        elif command == "cam_x":
            cam_x(value)
        elif command == "cam_y":
            cam_y(value)
        elif command == "adjust_speed":
            adjust_speed(value)
        command_queue.task_done()

# 컨트롤러 소켓 서버 (가장 높은 우선순위)
def controller_socket():
    HOST, PORT = '0.0.0.0', 65432
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('컨트롤러 연결:', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    data = data.decode()
                    code, value = map(int, data.split(','))
                    if code == 307:
                        stop_command()
                    elif code == 304 and value == 1:
                        command_queue.put((1, "forward", 0))
                    elif code == 305 and value == 1:
                        command_queue.put((1, "backward", 0))
                    elif code == 0:
                        command_queue.put((2, "steer", value))
                    elif code == 2:
                        command_queue.put((2, "cam_x", value))
                    elif code == 5:
                        command_queue.put((2, "cam_y", value))
                    elif code == 9:
                        command_queue.put((1, "adjust_speed", value))
                except ValueError:
                    print("데이터 오류")

# 조이스틱 소켓 서버 (중간 우선순위)
def joystick_socket():
    HOST, PORT = '0.0.0.0', 65431
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('조이스틱 연결:', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    data = data.decode()
                    data_x, data_y = map(int, data.split(','))
                    command_queue.put((2, "steer", data_x))
                except ValueError:
                    print("조이스틱 데이터 오류")

# DB에서 명령 가져오기 (가장 낮은 우선순위)
def db_command_handler():
    while True:
        sleep(0.1)
        try:
            response = requests.get("http://192.168.110.164:3001/SelectCmd").json()
            if "cmd" in response:
                command_queue.put((3, response["cmd"], 0))
        except Exception as e:
            print("DB 요청 오류:", e)

# 실행 스레드
command_thread = threading.Thread(target=execute_command, daemon=True)
controller_thread = threading.Thread(target=controller_socket, daemon=True)
joystick_thread = threading.Thread(target=joystick_socket, daemon=True)
db_thread = threading.Thread(target=db_command_handler, daemon=True)

command_thread.start()
controller_thread.start()
joystick_thread.start()
db_thread.start()

command_thread.join()
controller_thread.join()
joystick_thread.join()
db_thread.join()
