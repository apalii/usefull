#!/usr/bin/env python

''' Very simple pinger written in Python  +  bash
from day by day routine'''

import ping, socket,time
from datetime import datetime
from datetime import date

try:
    print date.today(),'-',datetime.time(datetime.now())
    ping.verbose_ping('web.centracom.co.za', count=1)
except socket.error, e:
    print "Ping Error:", e

#-------------------------------------------------------

#!/bin/bash
while [ True ]
do
    sudo python pinger.py
    sleep 5
done

#-------------------------------------------------------

# $ pinger.sh >> pinger.log
# $ pinger.sh | tee -a pinger.log 
