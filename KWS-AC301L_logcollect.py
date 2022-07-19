# KWS-AC301L power meter + rs485-usb converter log collector
# 2022.07.16 kutasg
import serial
import time
import sys

serialdev="/dev/ttyUSB0"

loginterval=5   #sec

logfilepath="/home/pi/"
logfilename="power_meter_"
logfileextension=".log"

logmode="csv"   #csv|keyvalue
#logmode="keyvalue"
csv_delimiter=","
kv_delimiter=" "
kv_separator="="
newline="\n"

#serial timeouts
readwait=200    #ms
nextwait=5      #ms

fieldname= [ "Volt",              #0 x10
             "Amp",               #1 x1000
             "Watt",              #2 x10
             "minutes",           #3 minutes
             "kWh",               #4 x1000
             "Power_factor",      #5 x100
             "unknown",           #6
             "Hz",                #7 x10
             "degC"]              #8 degC

multiplier= [ 10.0,
              1000.0,
              10.0,
              1,
              1000.0,
              100.0,
              1,
              10.0,
              1]

value=      [ 0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0.0]

senddata= [ bytearray.fromhex("0203000E0001E5FA"),
            bytearray.fromhex("0203000F0002F43B"),
            bytearray.fromhex("020300110002943D"),
            bytearray.fromhex("02030019000155FE"),
            bytearray.fromhex("020300170002743C"),
            bytearray.fromhex("0203001D0001143F"),
            bytearray.fromhex("0203001F0001B5FF"),
            bytearray.fromhex("0203001E0001E43F"),
            bytearray.fromhex("0203001A0001A5FE")]


def sendrequest(num):
    ser.write(senddata[num])

def receive():

    #waiting for data
    counter=readwait
    result= []
    while counter>0 and ser.in_waiting == 0:
        counter=counter-1
        time.sleep(0.001)
    #print("read wait:",readwait-counter)
    if counter == 0:
        print("Serial read timeout")
        return []

    #reading data
    counter=nextwait
    while counter > 0:
        data = ser.read()
        result.append(ord(data))
        #waiting for next byte
        counter=nextwait
        while counter>0 and ser.in_waiting == 0:
            counter=counter-1
            time.sleep(0.001)
        #print("nextwait:",nextwait-counter)
    if len(result)<7:
        print(gettimestamp," Not enough bytes received")
        return []
    else:
        return result

def decode(num,data):
    result=0
    if len(data)<7:
        print(gettimestamp(),"decode error",data)
        return None
    if data[2] == 2:
        #short data (2byte)
        result=data[3]*256+data[4]
    else:
        #long data (4byte)
        result=data[3]*256+data[4]+256*256*256*data[5]+256*256*data[6]

    result=result/multiplier[num]

    return result

def gettimestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def getlogfilename():
    return logfilepath+logfilename+time.strftime("%Y-%m-%d")+logfileextension

def logheader() :
    if logmode == "csv":
        row="Time"+csv_delimiter
        for s in fieldname:
            row=row+s+csv_delimiter
        return row[:-1]
    else:
        return

def logrow(value) :
    if logmode == "csv":
        row=gettimestamp()+csv_delimiter
        for s in value:
            if s == None:
                return None #bad value
            else:
                row=row+str(s)+csv_delimiter
        return row[:-1]+newline
    if logmode == "keyvalue":
        row=gettimestamp()+kv_delimiter
        for i in range(0,len(value)):
            row=row+fieldname[i]+kv_separator+str(value[i])+kv_delimiter
        return row+newline
    else:
        return


def writeheader(logfile) :
    print("Collecting logs from "+serialdev+" to "+logfilefullname)
    lh=logheader()
    if lh :
        logfile.write(lh+newline)

#--------------------------------------------------------------------------

#print(gettimestamp())
#print(getlogfilename())

#open serial port
ser = serial.Serial(serialdev, 9600)

#open log file
logfilefullname = getlogfilename()
logfile = open(logfilefullname, "a" )
writeheader(logfile)

while True:
    #read data from meter
    for i in range(0,9):
        sendrequest(i)
        #print(i)
        value[i]=decode(i,receive())

    #reopen file if necessary
    newlogfilename = getlogfilename()
    if newlogfilename != logfilefullname:
        logfile.close()
        logfilefullname = newlogfilename
        logfile = open(logfilefullname, "a" )
        writeheader(logfile)

    #print(logrow(value))
    row=logrow(value)
    if row != None:
        logfile.write(logrow(value))
        logfile.flush()

    time.sleep(loginterval)

logfile.close()
exit
