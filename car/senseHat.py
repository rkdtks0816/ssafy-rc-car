from sense_hat import SenseHat
from gpiozero import DistanceSensor
from time import sleep

sense = SenseHat()
sensor = DistanceSensor(echo=15, trigger=14)

while True:
    humid = sense.get_humidity()
    temp = sense.get_temperature()
    
    print("Humidity(%) : ", humid)
    print("Temperature(oC) :", temp)
    print(sensor.distance, 'm')
    sleep(1)