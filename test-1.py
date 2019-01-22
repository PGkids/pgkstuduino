# -*- coding: utf-8 -*-
from pgkstuduino import *

connect(4)

led1,led2,led3 = mkpart('LED:A0/A1/A2')
j1 = par(led1.job_blink(n=10,on=0.4,off=0.1),
         led2.job_blink(n=10,on=0.2,off=0.3),
         led3.job_blink(n=10,on=1,off=0.2))
job = j1.start() #lim(j1, 5, False).start()
job.join()

disconnect()
