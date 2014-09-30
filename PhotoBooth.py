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
cam_resolution = (1920,1080)
camera.resolution = cam_resolution
camera.framerate = 15
camera.start_preview()
preview_alpha = 200 #Nominal alpha value
camera.preview_alpha = preview_alpha

#Set countdown text font
font = pygame.font.SysFont("arial", screenSize[1])

#--- Functions ---#
def ConfigureDSLR():
	#Configures the DSLR Camera
	WakeUpDSLR(1) #Wakes up the camera
	time.sleep(2) #Allow some time for the camera to mount
	call('gphoto2 --set-config imageformat=4',shell=True) #Configure Pic format to Small Fine JPG
	
def WakeUpDSLR(n):
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(n) #Sleep for n second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR(filename):
	#Takes a picture with the DSLR camera and downloads it to the RPi saving it with the specified filename
	call('gphoto2 --capture-image-and-download --filename '+filename+' --force-overwrite',shell=True)
	
def TakePicDSLR_Delay(n,filename):
	#Takes a picture with the DSLR using the TakePicDSLR function after n seconds delay
	time.sleep(n) #Sleep for n seconds
	TakePicDSLR(filename) #Take picture with DSLR

def TakePicPiCamStream(camera,cam_resolution):
	#Takes a picture with the Pi camera and returns it
	stream = io.BytesIO() #Create stream
	camera.capture(stream, 'rgb', use_video_port=True) #Capture picture
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
		
def PicSequence(count,filename):
	#Sequence to take pictures with cd being the countdown time in sec (min 3 seconds) and filename the name of the picture file.
	#Generate threats
	t_PicDSLR_Delay = Thread(target=TakePicDSLR_Delay,args=(count-1.5,filename,))
	t_WakeUp = Thread(target=WakeUpDSLR,args=(count-2,))
	#Sequence
	t_WakeUp.start() #Wake up  DSLR camera
	t_PicDSLR_Delay.start() #Take picture using DSLR with a Delay
	Countdown(count,background) #Countdown
	img = TakePicPiCamStream(camera,cam_resolution) #Take picture using PiCam
	DisplayImagePi(img) #Display image from PiCam
	camera.preview_alpha = 0 #Set transparency of preview to 0
	t_PicDSLR_Delay.join() #Wait until the DSLR picture finishes transfering
	DisplayImageFile(filename) #Display DSLR image taken
	time.sleep(5) #Time to appreciate the image taken	
	
	
#--- Main script ---#
filename = 'WedBoothPic.jpg' #Filename of the image
count = 5 #Countdown time in sec
ConfigureDSLR() #Configure DSLR
PicSequence(count,filename)
	
#--- Clean up ---#
camera.close()
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
