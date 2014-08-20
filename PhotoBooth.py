import RPi.GPIO as GPIO
import time

#GPIO configuration
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(7, GPIO.OUT) #Sets up GPIO Pin 7 to Output
GPIO.output(7, False) #Not wake the camera yet



def WakeUpDSLR():
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(1) #Sleep for 1 second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera
	
#Main script
WakeUpDSLR()
time.sleep(5) #Some time is required for the camera to come online
WakeUp()	
	
#Clean up	
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
