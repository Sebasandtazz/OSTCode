# OSTCode
## This is the code (and maybe the board files) for the SmartTrigPi Project. I have included the SCPI parser thanks to Chris Tan.

The goal of this project is to create a drop-in replacement for a standard lab waveform generator (~2000CHF) and provide a custom-programmable solution to free up such resources. As a result of this, I created the SmartTrigPi. 
I was tasked with making a device that would pair with a raspberry pi (I know, I know) and use Python code for maximum flexibility and readibility. Additionally, there were no timing or computing-critical tasks in this that would push a need for (my more fluent) C or C++. 

I created a custom header board that would allow the user to connect either remotely over ethernet or wifi, or use local control to send out a square-wave signal. This square wave could be remotely customized to either 5V or 3V3 depending on the output needs. 

It is able to be powered over USB-C or benchtop power supply, using a set of banana jacks, and has a set of indicators and a screen to allow the user to read at-a-glance information from the device.

On the user end, I have created a pymeasure-style library file to allow the user to change only the instrument declaration in their testing automation code. This allows the  switch between the original waveform gen and my device to be completed in <5 mins. 

Overall, some improvements could be made, but since I am not around to complete them, this serves as an incredibly robust, seamless solution to the problem provided.


In addition to this code, I have included the pymeasure compatible library created smarttrigpi.py. This would have to be added
to the pymeasure library, or otherwise run in the correct folder.

In order to set up the pi, make sure the correct peripherals are on.
Using
sudo raspi-config -> interface options -> enable all of [SSH, i2c, and SPI]


## **The following libraries are needed on the Pi**, it's possible I will make a package to install all of these, but if not:

lgpio -> sudo apt install python3-lgpio

board and digitalio -> sudo pip3 install --break-system-packages adafruit-blinka

adafruit_rgb_display.st7789 -> sudo pip3 install --break-system-packages adafruit-circuitpython-rgb-display

PIL -> sudo apt install python3-pil

**Additionally**

Mount a USB

sudo mkdir /mnt/usb

sudo mount /dev/sda1 /mnt/usb

cp /mnt/usb/trig.jpg /mnt/usb/bees.jpg Desktop

cp /mnt/usb/SCPIParser.py /mnt/usb/OST_SmartTrigPi.py Desktop

sudo nano /etc/rc.local


**Inside of the newly opened file**

#!/bin/sh -e

python3 /home/raspberry/Desktop/OST_SmartTrigPi.py &

exit 0


**Ctrl + x, Y, and enter**

chmod +x /home/raspberry/Desktop/OST_SmartTrigPi.py

sudo chmod +x /etc/rc.local

**Reboot**

sudo reboot

**Check**

sudo systemctl status rc-local
