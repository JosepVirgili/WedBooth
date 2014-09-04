# Wedding PhotoBooth

A nice weeding PhotoBooth for Sandra and Josep's wedding.

### Required Hardware
The required components are:

- Raspberry Pi (RPi)
- Display (about 10') with HDMI input
- HDMI cable (to connect the RPi with the display)
- Pi Camera
- Nicer camera as a DSLR
- Remote shutter for the DSLR
- USB connector for the DSLR
- Protoboard
- Jumper cables
- Push button 

### Set-up

First the RPi needs to be configured. Follow this [guide]().
When done install all the required dependencies:

```
sudo apt-get install gphoto2
```

Then the software needs to be uploaded into the 

### Start the photo-booth software

To start the software just:

```
python PhotoBooth.py
```

 