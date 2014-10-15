# Wedding Photo Booth Software
#
#    Copyright 2014 Josep Virgili Llop
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

#--- CODE ---#
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
GPIO.setup(7, GPIO.OUT) #Set up GPIO Pin 7 to Output to wake up camera
GPIO.output(7, False) #Not wake the camera yet
GPIO.setup(19,GPIO.IN) #Set up Pin 19 to input to detect push button

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
#Alpha Values
preview_alpha_CD = 200 #Countdown alpha value
preview_alpha_TXT = 150 #Text alpha value

#Set countdown text font
font_CD = pygame.font.SysFont("arial", screenSize[1])
font_TXT = pygame.font.SysFont("arial", screenSize[1]/5)


#--- Functions ---#
def ConfigureDSLR():
	#Configures the DSLR Camera
	WakeUpDSLR(1) #Wakes up the camera
	time.sleep(2) #Allow some time for the camera to mount
	call('gphoto2 --set-config imageformat=4',shell=True) #Configure Pic format to Small Fine JPG
	
def ReadMAC():
	#Reads from file MAC address of the PoGo printer
	file = open('settings.txt', 'r') #Open file in read mode
	return file.read().replace('\n','') #Return MAC adress
	
def WakeUpDSLR(n):
	#Wakes up the DSLR camera
	GPIO.output(7, True) #Wake up camera
	time.sleep(n) #Sleep for n second to give the camera time to wake up
	GPIO.output(7, False) #Stop waking the camera

def TakePicDSLR(filename):
	#Takes a picture with the DSLR camera and downloads it to the RPi saving it with the specified filename
	call('gphoto2 --capture-image-and-download --keep --filename '+filename+' --force-overwrite',shell=True)
	
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
	#Diplays and image from file into the display when it has transferred.
	image=pygame.image.load(filename) #Load image
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in display
	screen.blit (image, (0,0))
	pygame.display.update()

def DisplayImagePi(image):
	#Display image from an image object.
	image = pygame.transform.scale(image.convert(), screenSize) #Resizes it to fit screen
	#Diplays image in display
	screen.blit(image, (0,0))
	pygame.display.update()
	
def DisplayText_Centre(text_disp):
	#Generate countdown text
	text = font_TXT.render(text_disp, True, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = screen.get_rect().centerx
	textpos.centery = screen.get_rect().centery
	screen.blit(text, textpos)
	pygame.display.update()

def Countdown(count,background):
	#Performs countdown with preview
	cd=1 #Initialize countdown variable
	start_time = pygame.time.get_ticks() #Initialize time
	#Transparency level
	camera.preview_alpha = preview_alpha_CD
	#Remove previous text
	background.fill((0, 0, 0))
	#Start countdown
	while cd>0:
		#Establish countdown
		cd = int(math.ceil((start_time - pygame.time.get_ticks())/1000 + count+0.5))
		#Generate countdown text
		text = font_CD.render(str(cd), True, (255, 255, 255),(0,0,0))
		textpos = text.get_rect()
		textpos.centerx = background.get_rect().centerx
		background.blit(text, textpos)
		# Blit everything to the screen
		screen.blit(background, (0, 0))
		pygame.display.flip()
		
def WaitForButton(camera):
	#Waits until the button is pressed with a text indicating to press button
	
	#Transperency
	camera.preview_alpha = preview_alpha_TXT
	#Remove previous text
	background.fill((0, 0, 0))
	#Generate text
	text_1 = font_TXT.render("Press the button", True, (255, 255, 255),(0,0,0))
	textpos_1 = text_1.get_rect()
	textpos_1.centerx = background.get_rect().centerx
	textpos_1.centery = background.get_rect().centery
	text_2 = font_TXT.render("to start!", True, (255, 255, 255),(0,0,0))
	textpos_2 = text_2.get_rect()
	textpos_2.centerx = background.get_rect().centerx
	textpos_2.centery = textpos_1.centery+textpos_2.height
	background.blit(text_1, textpos_1)
	background.blit(text_2, textpos_2)
	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	#Wait until a button is pressed
	while True:
		if (GPIO.input(19) == False): #Button pressed
			break

def PrintDSLR(filename):
	#Sends file to printer to start printing
	print 'obexftp --nopath --noconn --uuid none --bluetooth '+mac+' --channel 1 -p '+filename
	call('obexftp --nopath --noconn --uuid none --bluetooth '+mac+' --channel 1 -p '+filename,shell=True)

def PostDSLR(filename,t_PicDSLR):
	#Kickstarts the tasks that need to be done when the picture has been taken
	#Sending image to printing thread
	t_PrintDSLR = Thread(target=PrintDSLR,args=(filename,))
	#Wait until the piture has finished
	t_PicDSLR.join()
	#Start sending image to printer
	t_PrintDSLR.start()
	#Display DSLR image
	DisplayImageFile(filename)
	time.sleep(5) #Allow time for unobstructed viewing
	#Display ending to printer message
	DisplayText_Centre('Sending to Printer')
	#Wait until image finishes sending
	t_PrintDSLR.join()
	#Display printing message
	DisplayText_Centre('Sending to Printer')
	#Wait an estimate of the printing process
	time.sleep(60)
	
		
def PicSequence(count,filename):
	#Sequence to take pictures with cd being the countdown time in sec (min 3 seconds) and filename the name of the picture file.
	#Generate threats
	t_PicDSLR_Delay = Thread(target=TakePicDSLR_Delay,args=(count-1.5,filename,))
	t_PostDSLR = Thread(target=PostDSLR,args=(filename,t_PicDSLR_Delay,))
	t_WakeUp = Thread(target=WakeUpDSLR,args=(count-2,))
	#Sequence
	t_WakeUp.start() #Wake up  DSLR camera
	t_PicDSLR_Delay.start() #Take picture using DSLR with a delay
	t_PostDSLR.start() #Start post DSLR image capture tasks thread
	Countdown(count,background) #Countdown
	img = TakePicPiCamStream(camera,cam_resolution) #Take picture using PiCam
	DisplayImagePi(img) #Display image from PiCam
	camera.preview_alpha = 0 #Set transparency of preview to 0
	DisplayText_Centre('Processing') #Display 'processing' text
	t_PostDSLR.join() #Wait until all the post DSLR image capture tasks have finsihed
	
#--- Main script ---#
filename = 'WedBoothPic.jpg' #Filename of the image
count = 5 #Countdown time in sec
ConfigureDSLR() #Configure DSLR
mac = ReadMAC() #Read PoGo MAC address
while True:
	WaitForButton(camera)
	PicSequence(count,filename)
	
#--- Clean up ---#
camera.close()
GPIO.cleanup() #Clean up of the GPIO Port
	
	

	
	
	
