from Raspi_PWM_Servo_Driver import PWM
import mysql.connector
from threading import Timer, Lock
from time import sleep
import signal
import sys
from sense_hat import SenseHat
import datetime

pwm = PWM(0x6F)
pwm.setPWMFreq(60) 

servo_pin = 0
cam_servo_pin = 1
dc_pin1 = 11
dc_pin2 = 12
speed_pin = 13

servoLeft = 250  # Min pulse length out of 4096
servoCenter = 350
servoRight = 450  # Max pulse length out of 4096
servoCam = 350
speed = 100

pwm.setPWM(speed_pin, 0, speed*16)
pwm.setPWM(servo_pin, 0, servoCenter)
pwm.setPWM(cam_servo_pin, 0, servoCam)

def closeDB(signal, frame):
    print("BYE")
    cur.close()
    db.close()
    timer.cancel()
    timer2.cancel()
    sys.exit(0)

def polling():
    global cur, db, ready
    
    lock.acquire()
    cur.execute("select * from command order by time desc limit 1")
    for (id, time, cmd_string, arg_string, is_finish) in cur:
        if is_finish == 1 : break
        ready = (cmd_string, arg_string)
        cur.execute("update command set is_finish=1 where is_finish=0")

    db.commit()
    lock.release()
     
    global timer
    timer = Timer(0.1, polling)
    timer.start()

def sensing():
    global cur, db, sense

    pressure = sense.get_pressure()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()

    time = datetime.datetime.now()
    num1 = round(pressure / 10000, 3)
    num2 = round(temp / 100, 2)
    num3 = round(humidity / 100, 2)
    meta_string = '0|0|0'
    is_finish = 0

    print(num1, num2, num3)
    query = "insert into sensing(time, num1, num2, num3, meta_string, is_finish) values (%s, %s, %s, %s, %s, %s)"
    value = (time, num1, num2, num3, meta_string, is_finish)

    lock.acquire()
    cur.execute(query, value)
    db.commit()
    lock.release()

    global timer2
    timer2 = Timer(1, sensing)
    timer2.start()

def go():
    pwm.setPWM(dc_pin2, 0, 4096)
    pwm.setPWM(dc_pin1, 4096, 0)

def back():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 4096, 0)

def stop():
    pwm.setPWM(dc_pin1, 0, 4096)
    pwm.setPWM(dc_pin2, 0, 4096)

def left():
    pwm.setPWM(servo_pin, 0, servoLeft)

def mid():
    pwm.setPWM(servo_pin, 0, servoCenter)

def right():
    pwm.setPWM(servo_pin, 0, servoRight)

def up():
    global servoCam
    if servoCam >= 450:
        servoCam = 500
    else: 
        servoCam += 50
    pwm.setPWM(cam_servo_pin, 0, servoCam)

def down():
    global servoCam
    if servoCam <= 250:
        servoCam = 200
    else: 
        servoCam -= 50
    pwm.setPWM(cam_servo_pin, 0, servoCam)

#init
#db = mysql.connector.connect(host='13.125.214.143', user='gamzaking', password='1234', database='gamDB', auth_plugin='mysql_native_password')
db = mysql.connector.connect(host='192.168.110.164', port = '3306', user='root', password='1234', database='RC')
cur = db.cursor()
ready = None
timer = None

sense = SenseHat()
timer2 = None
lock = Lock()

signal.signal(signal.SIGINT, closeDB)
polling()
# sensing()

#main thread
while True:
    sleep(0.1)
    if ready == None : continue

    cmd, arg = ready
    ready = None

    if cmd == "go" : go()
    if cmd == "back" : back()
    if cmd == "stop" : stop()
    if cmd == "left" : left()
    if cmd == "mid" : mid()
    if cmd == "right" : right()
    if cmd == "up" : up()
    if cmd == "down" : down()