import RPi.GPIO as GPIO
import paho.mqtt.publish as publish
import random
from time import sleep									#this lets us have a time delay (see line 15)


# MQTT Server - Config
MQTT_SERVER = "192.168.0.22"
MQTT_PATH = "home/garage/door"




GPIO.setmode(GPIO.BCM)									# set up BCM GPIO numbering
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)		#set GPIO17 as input (button)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)		#set GPIO18 as input (button)


try:
	while True:							# this will carry on until you hit CTRL+C
		if GPIO.input(17):				# if port 17 == 1
			sPort17 = "Port 17 is 1/HIGH/True"
		else:
			sPort17 = "Port 17 is 0/LOW/False"
		if GPIO.input(18):				# if port 18 == 1
			sPort18 = "Port 18 is 1/HIGH/True"
		else:
			sPort18 = "Port 18 is 0/LOW/False"
		#print (sPort17 + "		  " + sPort18)
		
		
		#Determine Status of the door - OPEN
		if GPIO.input(17) and not(GPIO.input(18)):
			str_Door_Status = "OPEN"
		#Determine Status of the door - CLOSED
		if GPIO.input(18) and not(GPIO.input(17)):
			str_Door_Status = "CLOSED"
		#Determine Status of the door - MOVING
		if not(GPIO.input(18)) and not(GPIO.input(17)):
			str_Door_Status = "MOVING"
		#Determine Status of the door - ERROR
		if GPIO.input(18) and GPIO.input(17):
			str_Door_Status = "ERROR"
		
		
		print( "Door is " + str_Door_Status)
		publish.single(MQTT_PATH, str_Door_Status, hostname=MQTT_SERVER)
		sleep(0.1)				# wait 0.1 seconds
		
		
		

finally:				# this block will run no matter how the try block exits
	publish.single(MQTT_PATH, "OFF", hostname=MQTT_SERVER)
	GPIO.cleanup()		# clean up after yourself
