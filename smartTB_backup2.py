import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import sys
import requests

GPIO.setmode(GPIO.BCM)

TRIG = 18
ECHO = 24

distance = 0
totallevel = 30.00
templevel = 0
level = 0

EMULATE_HX711=False

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

hx = HX711(5, 6)

hx.set_reference_unit(252)

hx.reset()

hx.tare()

print "loadcell ready, Add weight now.."
print "HCSR-04 ready,  calculating..."
print "DHT11 ready, calculating..."
print ".."

def jarak():
	global distance
	global level
	global totallevel
	global templevel

	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)

	GPIO.output(TRIG, False)
	time.sleep(2)

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while (GPIO.input(ECHO)==0):
		pulse_start = time.time()

	while (GPIO.input(ECHO)==1):
		pulse_end=time.time()


	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	if distance > 26:
		distance = 26
	elif distance < 0:
		distance = 0
	templevel = distance/totallevel * 100
	level = 100 - templevel

	return jarak

try:
	while True:
		jarak()
		dist = distance
		lvl = level
		val = max(0, int(hx.get_weight(5)))
		humidity, temperature = Adafruit_DHT.read_retry(11,2)

		kode_seri = 'Ctv7MyA2'
		massa = "%.1f" % val
		suhu = "%.1f" % temperature
		hum = "%.1f" % humidity
		jarak2 = "%.1f" % dist
		level2 = "%.1f" % lvl

		print "Distance:",dist,"cm"
		print "Level :",(round(lvl)),"%"
		print "Kelembapan:",humidity,", Suhu:",temperature
        	print "Berat : ", val ,"gram"

		hx.power_down()
      		hx.power_up()
		send = requests.post("http://api-sotrashbin.chiqors.xyz/add_data.php?kode_seri=" + kode_seri + "&kelembapan=" + hum + "&jarak=" + jarak2 + "&suhu=" + suhu + "&berat=" + massa + "&level=" + level2)
		print (send.status_code)
		print (send.text)
		print ".."
		time.sleep(5)

except KeyboardInterrupt:
	print"cleanup"
	GPIO.cleanup()
