# -*- coding: utf-8 -*-
from pgkstuduino import *

connect(4)

led = mkpart('LED:A0')
job = lim(led.job_blink(), 5).start()
job.join()

disconnect()
