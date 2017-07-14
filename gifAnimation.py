# Copyright (c) 2014 Adafruit Industries
# Copyright (c) 2017 PrinzJuliano
# Authors: Tony DiCola, PrinzJuliano
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
WARNING: This API can only read GIF encoded images. 
All other images use a different way of storing data 
thus an error message is displayed
'''

'''
NOTE: The API could work with RGB Displays. 
The only changes that need to be done are:
1. Change the Driver (Maybe)
2. Replace all "convert('1')" with "convert('RGBA')" 
'''

# =========[INCLUDES]=========
import time
import sys

# This is the library found under https://github.com/adafruit/Adafruit_SSD1306 for the Adafruit OLED Display
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image


# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# =========[CHOOSE YOUR DEVICE]=========

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))


# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()



def processImage(path):
    '''
    Iterate the GIF, extracting each frame and copying the last frame into the next.
    Taken from: https://gist.github.com/BigglesZX/4016539
    Modified slightly by PrinzJuliano
    '''
    
    im = Image.open(path)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('1')
    
    seq = []
    
    try:
        while True:
            
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('1', im.size)
            
            new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.copy().convert('1'))
            
            #load the duration of the frame or give it a duration of 100 ms
            try:
               new_frame.info['duration'] = im.info['duration']
            except KeyError: new_frame.info['duration'] = 100
            
         
            #Instead of saving all frames as files, here the frame is copied, resized, and converted to 1 bit color
            seq.append(new_frame.copy().resize((disp.width, disp.height), Image.ANTIALIAS).convert('1'))

            i += 1
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    finally:
		return seq


#if there are arguments then use them
if len(sys.argv) > 1:
   #convert arguments to single string disregarding the first argument (a.k.a the program name)
   st = ""
   for s in sys.argv[1:]:
      st += s + " "
   st = st.strip()
   
   #Call the image processor
   seq = processImage(st)
   
   #print some stats
   print("Loaded " + st)
   print("Found [" + str(len(seq)) + "] Frames!")
   
   #no frames are found
   if len(seq) == 0:
	   print("\n+-------+")
	   print("| ERROR |")
	   print("+-------+----------------------------------------------------+")
	   print("| This program can read GIF files ONLY!                      |")
	   print("| Please consider a different program to display this image! |")
	   print("+------------------------------------------------------------+\n")
	   exit(0)
   
   #if there are multiple frames, iterate through them until CTRL-C is pressed
   if len(seq) > 1:
	   try:
		 print("Press 'CTRL + C' to exit")
		 while 1:
			 disp.clear()
			 disp.display()
			 for img in seq:
				disp.image(img)
				disp.display()
				time.sleep(img.info['duration']/1000.0)
	   except KeyboardInterrupt:
		  disp.clear()
		  disp.display()
		  print("Exit")
   else: #if only one frame is present, just display it
	   disp.clear()
	   disp.image(seq[0])
	   disp.display()
	   print("Done displaying one Frame!")
else: #if there are no arguments (disregarding the first one), we can not proceed. Thus a usage message is printed
   print("Usage: "+sys.argv[0]+" <Path>")
