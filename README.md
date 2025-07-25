# OSTCode
This is the code (and maybe the board files) for the SmartTrigPi Project. I have included the SCPI parser thanks to Chris Tan.

In addition to this code, I have included the pymeasure compatible library created smarttrigpi.py. This would have to be added
to the pymeasure library.

**The following libraries are needed on the Pi**, it's possible I will make a package to install all of these, but if not:

lgpio -> sudo apt install python3-lgpio

board and digitalio -> sudo pip3 install --break-system-packages adafruit-blinka

adafruit_rgb_display.st7789 -> sudo pip3 install --break-system-packages adafruit-circuitpython-rgb-display

PIL -> sudo apt install python3-pil

**Additionally**
cp /mnt/usb/trig.jpg /mnt/usb/bees.jpg Desktop
cp /mnt/usb/SCPIParser.py /mnt/usb/OST_SmartTrigPi.py Desktop
sudo nano /etc/rc.local


**Inside of the newly opened file**

#!/bin/sh -e
python3 /home/raspberry/Desktop/OST_SmartTrigPi.py > /home/raspberry/triglog.txt 2>&1 &
exit 0

**Ctrl + x, Y, and enter**

sudo systemctl enable rc-local
sudo systemctl start rc-local

**Check**

sudo systemctl status rc-local
