import RPi.GPIO as GPIO
import time
from subprocess import call

#GPIO configuration
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(7, GPIO.OUT) #Sets up GPIO Pin 7 to Output
GPIO.output(7, False) #Not wake the camera yet



def WakeUpDSLR():
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(1) #Sleep for 1 second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR():
	#Takes a picture with the DSLR camera
	call('gphoto2 --capture-image',shell=True)
	
	
#Main script
WakeUpDSLR()
time.sleep(5) #Some time is required for the camera to come online
TakePicDSLR()	
	
#Clean up	
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
