
# KWS-AC301L-power-meter-RS485-raspberry-pi-logging
This is a python script to log data from KWS-AC301L power meter

Logging data from KWS-AC301L power meter
from China stores.

This equipment is sutable for measuring household electricity consumption.
![Alt text](pictures/KWS-AC301-1.png?raw=true "Title")

It measures AC 1 phase Voltage 50-300V, Current up to 100A with coil.
![Alt text](pictures/KWS-AC301-3.png?raw=true "Title")

Values displayed:
V, A, (k)W, power factor, kWh, elapsed time, temperature, Hz

The *L model has RS485 interface, to read actual data from the box.
![Alt text](pictures/KWS-AC301-2.png?raw=true "Title")

---
It comes with a very basic software that can be downloaded from chinese file sharing
site.

It only runs on windows

Showed graphs disappear when program closed.

No zoom functions.

Logging only a daily kWh value into an sqlite db.

---

I decided to change it to a more affordable raspberry PI environment.

I used CH340/CH341type USB-RS485 adapter. It worked with windows 7,10 and
also has driver for raspbian.
![Alt text](pictures/CH340.jpg?raw=true "Title")


The serial communication must have been analized.
I used free-serial-analyzer to dump communication.

There are 9 values that can be read from the box.

You can use the attached python3 script to log data to file (csv or key-value)
Logging parameters inside the script.

Feel free to use and develop this script as you need!

---

# Installation

Tested on Raspberry PI 3B
with Raspbian 11	5.15.32

- update your repo

  sudo apt-get update
- install pip3

  sudo apt-get install python3-pip
- install pyserial
  
  sudo pip3 install pyserial
- clone this repo

  git clone https://github.com/kutasg/KWS-AC301L-power-meter-RS485-raspberry-pi-logging

- Connect your CH340/CH341 USB converter
  
  It is working plug and play.

- check if module loaded, device exists:
  
  lsmod |grep ch3
  ls -l /dev/ttyUSB0

- Modify parameters in the script if necessary
  ```
  serialdev="/dev/ttyUSB0"
  loginterval=5   #sec
  logfilepath="/home/pi/"
  logfilename="power_meter_" #prefix
  logfileextension=".log"
  logmode="csv"   #csv|keyvalue
  csv_delimiter=","
  kv_delimiter=" "
  kv_separator="="
  newline="\n"
  ```
- test run

  python3 KWS-AC301L_logcollect.py

-  Look for the log file e.g.
  
  cat power_meter_2022-07-16.log


# sample output

```
Time,Volt,Amp,Watt,minutes,kWh,Power_factor,unknown,Hz,degC
2022-07-16 21:52:18,235.7,2.994,652.1,9081.0,50.883,0.88,30656.0,50.0,29.0
2022-07-16 21:52:24,235.9,2.958,632.7,9082.0,50.884,0.88,30656.0,50.0,29.0
```

#if you want to run it in the background all day long,

#edit meter_launcher.sh program path

#add this line to crontab (replace path if necessary)
```
* * * * * /home/pi/meter_launcher.sh
```
#It launches KWS-AC301L_logcollect.py script every minute if it's not running.

