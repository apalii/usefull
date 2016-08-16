#!/usr/bin/env python

'''Very simple pinger written in Python  +  bash
for day-to-day routine
'''

import ping, socket
from datetime import datetime
from datetime import date

try:
    print date.today(),'-',datetime.time(datetime.now())
    ping.verbose_ping('web.centracom.co.za', count=1)
except socket.error, e:
    print "Ping Error:", e

#-------------------------------------------------------

#!/bin/bash

COUNTER=0
while [  $COUNTER -lt 6 ]; do
python pinger.py
let COUNTER=COUNTER+1 
sleep 20m
done

#-------------------------------------------------------

# $ pinger.sh >> pinger.log
# $ pinger.sh | tee -a pinger.log 
