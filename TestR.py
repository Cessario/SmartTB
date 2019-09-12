import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(21,GPIO.IN)
GPIO.setup(24,GPIO.OUT)

while True:
	if GPIO.input(21):
		print ("Tidak Ada Api")
		GPIO.output(24,False)
		time.sleep(1)
	else:
		print("Ada Api Coy")
		GPIO.output(24,True)
		time.sleep(1)

