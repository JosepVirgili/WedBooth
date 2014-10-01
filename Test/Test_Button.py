#Test if the Button Works
import RPi.GPIO as GPIO
import time
import os

#Configure GPIO pin
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(19,GPIO.IN) 

#Loop and print mesage when button is pressed
while True:
	if (GPIO.input(19) == False):
		print "Button pressed"
		time.sleep(2)
		os.system('clear')
		

