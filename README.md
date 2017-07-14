# Raspberry Pi / Linux OLED Display Library
All the scripts needed to display some images on a monochrome OLED Display

Requirements:
1. One of these: ![OLED Display](https://cdn-shop.adafruit.com/970x728/326-18.jpg)
   Link: [SPI Variant](https://www.adafruit.com/product/326)
   Link: [I2C Variant](https://www.adafruit.com/product/931)
2. This Library [Adafruit Driver](https://github.com/adafruit/Adafruit_Python_SSD1306)
3. This Tutorial: [Adaruit Tutorial](https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black)

When you install this driver and unpacked this repo somewhere save, you need to config the files!
All the scripts contain a section that looks like this:

```python

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

# 128x32 display with hardware I2C:
#disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# 128x64 display with hardware I2C:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

```

You need to uncomment your display configuration (and comment the bottom one out) and config your pin setup!

If you need some pictures to test with here is my gif repo: [PJOG.de Gif Repo](https://gif.pjog.de)
