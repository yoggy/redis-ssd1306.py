#!/usr/bin/python
#
# redis-ssd1306.py - Display driver program for Adafruit PiOLED
#
#  setup:
#    # see also... https://learn.adafruit.com/adafruit-pioled-128x32-mini-oled-for-raspberry-pi/usage
#    $ sudo apt-get update
#    $ sudo apt-get install build-essential python-dev python-pip
#    $ sudo pip install RPi.GPIO
#    $ sudo apt-get install python-imaging python-smbus
#    $ git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
#    $ cd Adafruit_Python_SSD1306
#    $ sudo python setup.py install
#
#    $ sudo apt-get install redis-server redis-tools
#    $ sudo pip install redis
#
#    $ mkdir ~/work
#    $ cd ~/work
#    $ git clone https://github.com/yoggy/redis-ssd1306.py.git
#    $ cd ./redis-ssd1306.py/
#
#    # exec in the foreground
#    $ python redis-ssd1306.py
#
#    # for supervisor
#    $ sudo cp redis-ssd1306.conf.sample /etc/supervisor/conf.d/
#    $ sudo vi /etc/supervisor/conf.d/redis-ssd1306.conf
#    $ sudo supervisorctl reread
#    $ sudo supervisorctl add redis-ssd1306
#
#  how to display messages:
#    $ redis-cli set "oled:0" `hostname`
#    $ redis-cli set "oled:1" `date "+%Y/%m/%d-%H:%M:%S"`
#    $ redis-cli set "oled:2" `LANG=C /sbin/ifconfig | grep -v 127.0.0.1 | grep inet | awk '{print $2}' | sed -e 's/addr://' | head -1`
#    
#  github:
#    https://github.com/yoggy/redis-ssd1306.py
#
#  license:
#    Copyright(c) 2018 yoggy<yoggy0@gmail.com>
#    Released under the MIT license
#    http://opensource.org/licenses/mit-license.php;
#

import os
import time
import subprocess
 
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import redis
 
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
 
os.chdir(os.path.abspath(os.path.dirname(__file__)))

r = redis.StrictRedis(db=0)

disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)
disp.begin()

disp.clear()
disp.display()
image = Image.new('1', (disp.width, disp.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

def clear():
  global draw, disp
  draw.rectangle(((0,0),(disp.width, disp.height)),outline=0, fill=0)

def text(y, str):
  global draw, font
  draw.text((0, y*8-2), str, font=font, fill=255)

def flush():
  global disp, image
  disp.image(image)
  disp.display()

def main():
  # banner
  clear()
  text(0, "redis-ssd1306.py")
  text(1, "ver 0.0.1")
  flush()
  time.sleep(3)

  while True:
    clear()
    for i in range(4):
      str = r.get("oled:{0}".format(i))
      if str is None:
        str = ""
      text(i, str)
    flush()
    time.sleep(0.5)
  
main()

