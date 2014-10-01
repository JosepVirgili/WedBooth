import RPi.GPIO as GPIO
import time

#GPIO configuration
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(7, GPIO.OUT) #Wake pin
GPIO.setup(11, GPIO.OUT) #Shoot pin
GPIO.output(7, False) #Not wake the camera yet
GPIO.output(11, False) #Not shoot camera yet

#Test wake up
GPIO.output(7,True)
print "Wake up"
time.sleep(2)
GPIO.output(7,False)

'''	
#Test Shoot
GPIO.output(11,True)
print "Shoot"
time.sleep(2)
GPIO.output(11,False)
'''
	
GPIO.cleanup() #Cleanup of GPIO port
	
	


