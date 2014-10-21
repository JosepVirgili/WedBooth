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


When done install gphoto2:

```
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh
chmod +x gphoto2-updater.sh
sudo ./gphoto2-updater.sh
```

Install the bluetooth tools required to operate the PoGo printer:

```
sudo apt-get install bluez bluez-utils obexftp
```

Find the mac adress of your printer:

```
hcitool scan
```

The mac adress will appear as YY:YY:YY:YY:YY:YY Polaroid ZZ ZZ ZZ where YY:YY:YY:YY:YY:YY is the mac adress.
Then we need to include the pin code of the pogo into the system:

```
sudo mkdir /var/lib/bluetooth/YY:YY:YY:YY:YY:YY
sudo nano /var/lib/bluetooth/YY:YY:YY:YY:YY:YY/pincodes
```

Include the line `YY:YY:YY:YY:YY:YY 6000` into the file and save.

Then the software needs to be uploaded into the Raspberry Pi:

```
git clone https://github.com/JosepVirgili/WedBooth.git
```

Then, create a `settings.txt` file to save the PoGo mac adress.


```
cd WedBooth
nano settings.txt
```

Add at the beginning of the file insert the YY:YY:YY:YY:YY:YY mac adress of your PoGo.


### Start the photo-booth software

To start the software just:

```
cd WedBooth
sudo python PhotoBooth.py
```

If you want the software to start when booting then:

```
sudo nano /etc/rc.local
```

At the end of the file add (change pi for your own username if you have change it):

```
# Auto run WedBooth
cd /home/pi/WedBooth
sudo python /home/pi/WedBooth/PhotoBooth.py
```

### Legal Boring Stuff

Copyright 2014 Josep Virgili Llop

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

 
