from Raspi_PWM_Servo_Driver import PWM
from time import sleep

servo = PWM(0x6F)
servo.setPWMFreq(60)

while True:
	val = int(input('val(range 200~500) : '))
	servo.setPWM(1,0,val) #channel num, on, off	