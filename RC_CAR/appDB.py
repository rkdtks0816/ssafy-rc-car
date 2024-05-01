from Raspi_PWM_Servo_Driver import PWM
from time import sleep
import requests

pwm = PWM(0x6F)
pwm.setPWMFreq(60) 

servo_pin = 0
cam_x_pin = 1 # 170 370 570 좌 우 200
cam_y_pin = 14
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

rLeft = 250
rCenter = 350
rRight = 450
cXLeft = 170
cXCenter = 370
cXRight = 570
cYUp = 350
cYCenter = 400
cYDown = 450

speed = 2048

power = "OFF"
nowCmd = "rs"

pwm.setPWM(speed_pin, 0, speed)
pwm.setPWM(servo_pin, 0, rCenter)
pwm.setPWM(cam_x_pin, 0, cXCenter)
pwm.setPWM(cam_y_pin, 0, cYCenter)

def rg():
    pwm.setPWM(dc_pin2, 0, 4096)
    pwm.setPWM(dc_pin1, 4096, 0)
def rs():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 0, 4096)
def rb():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 4096, 0)
def rl():
    pwm.setPWM(servo_pin, 0, rLeft)
def rm():
    pwm.setPWM(servo_pin, 0, rCenter)
def rr():
    pwm.setPWM(servo_pin, 0, rRight)

def cg():
    pwm.setPWM(cam_y_pin, 0, cYUp)
def cs():
    pwm.setPWM(cam_y_pin, 0, cYCenter)
def cb():
    pwm.setPWM(cam_y_pin, 0, cYDown)
def cl():
    pwm.setPWM(cam_x_pin, 0, cXLeft)
def cm():
    pwm.setPWM(cam_y_pin, 0, cXCenter)
def cr():
    pwm.setPWM(cam_x_pin, 0, cXRight)

def su():
    global speed
    if speed >= 4046:
        speed = 4096
    else:
        speed += 500
    pwm.setPWM(speed_pin, 0, speed)
def sd():
    global speed
    if speed <= 1074:
        speed = 1024
    else:
        speed -= 500
    pwm.setPWM(speed_pin, 0, speed)
def SelectCmd():
    url = f"http://192.168.110.164:3001/SelectCmd"
    # GET 요청 보내기
    resp = requests.get(url)
    return resp.json()
def InsertState():
    url = f"http://192.168.110.164:3001/InsertState?mode={mode}&cmd={nowCmd}&power={power}"
    # GET 요청 보내기
    requests.get(url)
#main thread
while True:
    sleep(0.1)
    ready = SelectCmd()
    if "mode" not in ready: continue

    mode = ready["mode"]
    cmd = ready["cmd"]

    if mode != "controller":
        if cmd == "ON" : 
            power = "ON"
            InsertState()
        if cmd == "OFF" : 
            power = "OFF"
            InsertState()
        if power == "ON" :
            if cmd == "rgl" :
                rg()
                rl()
                nowCmd = cmd
                InsertState()
            if cmd == "rg" : 
                rg()
                rm()
                nowCmd = cmd
                InsertState()
            if cmd == "rgr" : 
                rg()
                rr()
                nowCmd = cmd
                InsertState()
            if cmd == "rl" : 
                rs()
                rl()
                nowCmd = cmd
                InsertState()
            if cmd == "rs" : 
                rs()
                rm()
                nowCmd = cmd
                InsertState()
            if cmd == "rr" : 
                rs()
                rr()
                nowCmd = cmd
                InsertState()
            if cmd == "rbl" : 
                rb()
                rl()
                nowCmd = cmd
                InsertState()
            if cmd == "rb" : 
                rb()
                rm()
                nowCmd = cmd
                InsertState()
            if cmd == "rbr" : 
                rb()
                rr()
                nowCmd = cmd
                InsertState()
            if cmd == "su" : 
                su()
            if cmd == "sd" : 
                sd()
            if cmd == "cgl" : 
                cg()
                cl()
            if cmd == "cg" : 
                cg()
                cm()
            if cmd == "cgr" : 
                cg()
                cr()
            if cmd == "cl" : 
                cs()
                cl()
            if cmd == "cs" : 
                cs()
                cm()
            if cmd == "cr" : 
                cs()
                cr()
            if cmd == "cbl" : 
                cb()
                cl()
            if cmd == "cb" : 
                cb()
                cm()
            if cmd == "cbr" : 
                cb()
                cr()