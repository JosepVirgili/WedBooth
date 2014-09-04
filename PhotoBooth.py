import RPi.GPIO as GPIO
import time
from subprocess import call
import pygame
import picamera
import math
import io
from threading import Thread

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
cam_resolution = (640,480)
camera.resolution = cam_resolution
camera.framerate = 15
camera.start_preview()
preview_alpha = 200 #Nominal alpha value
camera.preview_alpha = preview_alpha

#Configure DSLR camera
WakeUpDSLR()
call('gphoto2 --set-config imageformat=7')

#Set countdown text font
font = pygame.font.SysFont("arial", screenSize[1])

#--- Functions ---#
def WakeUpDSLR():
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(2) #Sleep for 2 second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR(filename):
	#Takes a picture with the DSLR camera and downloads it to the RPi saving it with the specified filename
	call('gphoto2 --capture-image-and-download --filename '+filename+' --keep --force-overwrite',shell=True)

def TakePicPiCamStream(camera,cam_resolution):
	#Takes a picture with the Pi camera and returns it
	stream = io.BytesIO() #Create stream
	camera.capture(stream, 'rgb') #Capture picture
	rgb = bytearray(cam_resolution[0] * cam_resolution[1] * 3) 	# Buffers for PiCamera picture
	#Read picture into buffer
	stream.seek(0)
	stream.readinto(rgb)
	#Return the image
	return pygame.image.frombuffer(rgb[0:cam_resolution[0]*cam_resolution[1]*3],cam_resolution, 'RGB')

def DisplayImageFile(filename):
	#Diplays and image from file into the display
	image=pygame.image.load(filename) #Load image
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in display
	screen.blit (image, (0,0))
	pygame.display.update()

def DisplayImagePi(image):
	#Display image from an image object
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in display
	screen.blit (image, (0,0))
	pygame.display.update()


def Countdown(count,background):
	#Performs countdown with preview
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
t_PicDSLR = Thread(target=TakePicDSLR,args=(filename,))
t_WakeUp = Thread(target=WakeUpDSLR,args=())
t_WakeUp.start()
Countdown(5,background)
t_PicDSLR.start()
img = TakePicPiCamStream(camera,cam_resolution)
camera.preview_alpha = 0
DisplayImagePi(img)
t_PicDSLR.join()
DisplayImageFile(filename)
time.sleep(5) #Time to appreciate the image taken.
	
#--- Clean up ---#
camera.close()
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
