# KWS-AC301L-power-meter-RS485-raspberry-pi-logging
python script to log data from KWS-AC301L power meter

This is for logging data from KWS-AC301L power meter
from China stores.

This equipment is sutable for measuring household electricity consumption.
It measures AC Voltage 50-300V, Current up to 100A with coil.

Computed values displayed:
V, A, (k)W, power factor, kWh, elapsed time, temperature, Hz

The *L model has RS485 interface, to read actual data from the box.

It comes with a very basic software that can be downloaded from chinese file sharing
site.

It only runs on windows
Showed graphs disappear when program closed.
No zoom functions.
Logging only a daily kWh value into an sqlite db.


I decided to change it to a more affordable rasperry pi environment.

I used CH340/CH341type USB-RS485 adapter. It worked with windows 7,10 and
also has driver for raspbian.

The serial communication must have been analized.
I used free-serial-analyzer to dump communication.

There are 9 values that can be read from the box.

You can use the attached python3 script to log data to file (csv or key-value)
Logging parameters inside the script.

Feel free to use and develop this script as you need!
