import RPi.GPIO as GPIO
import time
from subprocess import call
import pygame

#GPIO configuration
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(7, GPIO.OUT) #Sets up GPIO Pin 7 to Output
GPIO.output(7, False) #Not wake the camera yet

#Pygame configuration
pygame.init()
screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
pygame.mouse.set_visible(0)
pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
screen = pygame.display.set_mode(screenSize)

#--- Functions ---#
def WakeUpDSLR():
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(1) #Sleep for 1 second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR(filename):
	#Takes a picture with the DSLR camera and downloads it to the RPi saving it with the specified filename
	call('gphoto2 --capture-image-and-download --filename '+filename+' --keep --force-overwrite',shell=True)

def DisplayImage(filename):
	#Diplays and image from file into the display
	image=pygame.image.load(filename) #Load image
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in siplay
	screen.blit (image, (0,0))
	pygame.display.update()
	
	
#--- Main script ---#
filename = 'WedBoothPic.jpg' #Filename of the image
WakeUpDSLR()
time.sleep(5) #Some time is required for the camera to come online
TakePicDSLR(filename)
DisplayImage(filename)
time.sleep(5) #Time to appreciate the image taken.
	
#--- Clean up ---#	
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
