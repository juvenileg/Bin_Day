## Bin_Day

![logo](/library/logo.jpg)

### Description: 
Query the Reading website API, format date, display bin information, act on button pressed to display wifi qr code, keep button pressed to display a custom picture
At the bottom it will display a random quote from numbersapi.com
All the hardware build is not explained.

### Calendar link: 
[Reading Councile API](https://api.reading.gov.uk/api/collections/310012705)
### Waveshare installation details: 
[7.5inch Documentation](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Python_2)

Running on a Raspberry Pi Zero W + 8gb SD Card + 7.5inch E-Ink Display HAT 640x384 + Universal e-Paper Raw Panel Driver HAT + Mini Illuminated Momentary Pushbutton + 1kohm rezistor
### Eink: 
[Eink Screen Availability](https://www.aliexpress.com/item/1005002297292956.html?spm=a2g0o.order_list.0.0.72991802a1h7yW)
### HAT: 
[HAT availability](https://thepihut.com/products/universal-e-paper-raw-panel-driver-hat?variant=32051318652990&currency=GBP&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&gclid=CjwKCAjw79iaBhAJEiwAPYwoCKitr6iBemNLsDU0WPlwXrg5jtMarHI3FOI726p-D7dMP21hJZwaOxoCRdMQAvD_BwE)
### Button: 
[Button option & availability](https://thepihut.com/products/mini-illuminated-momentary-pushbutton-red-power-symbol)

### Crontab
This is the crontab that needs to be added to your machine:
```
@reboot python3 /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/bin_day_v3.py &
```
Path might differ based on your configuration and installation
### Other Tips
clone in your working directory
```
git clone https://github.com/juvenileg/Bin_Day.git .
```

You will have to copy all the pictures in the library folder to ~/e-Paper/RaspberryPi_JetsonNano/python/pic

You will also have to create a wifi.jpg file in the same library above as it is git-ignored since it can contain wifi passwords.

You will have to clone the repo into ~/e-Paper/RaspberryPi_JetsonNano/python folder.
