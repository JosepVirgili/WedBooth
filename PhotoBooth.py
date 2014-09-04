import RPi.GPIO as GPIO
import time
from subprocess import call
import pygame
import picamera
import math

#GPIO configuration
GPIO.setmode(GPIO.BOARD) #Set the Board Mode
GPIO.setup(7, GPIO.OUT) #Sets up GPIO Pin 7 to Output
GPIO.output(7, False) #Not wake the camera yet

#Pygame configuration
pygame.init()
pygame.mouse.set_visible(0)
screenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
screen = pygame.display.set_mode(screenSize,pygame.FULLSCREEN)

# Fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

#Initialize Camera
camera = picamera.PiCamera()
camera.resolution = (1296,730)
camera.framerate = 30
camera.start_preview()
preview_alpha = 200 #Nominal alpha value
camera.preview_alpha = preview_alpha

#Set countdown text font
font = pygame.font.SysFont("arial", screenSize[1])

#--- Functions ---#
def WakeUpDSLR():
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(1) #Sleep for 1 second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR(filename):
	#Takes a picture with the DSLR camera and downloads it to the RPi saving it with the specified filename
	call('gphoto2 --capture-image-and-download --filename '+filename+' --keep --force-overwrite',shell=True)

def DisplayImageFile(filename):
	#Diplays and image from file into the display
	image=pygame.image.load(filename) #Load image
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in siplay
	screen.blit (image, (0,0))
	pygame.display.update()

#Countdown
def Countdown(count,background):
	cd=1 #Initialize countdown variable
	start_time = pygame.time.get_ticks() #Initialize time
	#Start countdown
	while cd>0:
		#Establish countdown
		cd = int(math.ceil((start_time - pygame.time.get_ticks())/1000 + count+0.5))
		#Generate countdown text
		text = font.render(str(cd), True, (255, 255, 255),(0,0,0))
		textpos = text.get_rect()
		textpos.centerx = background.get_rect().centerx
		background.blit(text, textpos)
		# Blit everything to the screen
		screen.blit(background, (0, 0))
		pygame.display.flip()
	
	
#--- Main script ---#
filename = 'WedBoothPic.jpg' #Filename of the image
WakeUpDSLR()
Countdown(5,background)
TakePicDSLR(filename)
camera.preview_alpha = 0
DisplayImageFile(filename)
time.sleep(5) #Time to appreciate the image taken.
	
#--- Clean up ---#
camera.close()
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
