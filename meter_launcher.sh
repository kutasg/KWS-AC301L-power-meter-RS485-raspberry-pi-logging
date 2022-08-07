#!/bin/bash

PROGNAME=/home/pi/KWS-AC301L_logcollect.py

RES=`ps -ef |grep $PROGNAME|grep -v grep |wc -l`

if [[ $RES -eq 0 ]]; then
  python3 $PROGNAME >>$PROGNAME.out

fi
