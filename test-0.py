# -*- coding: utf-8 -*-
from pgkstuduino import *
from sys import argv
from time import sleep
st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)

# 3つのLEDを異なる発光パターンで同時にブリンクさせる並列処理の例


#connect(3)
#sleep(1)
#led1= mkpart('LED:A0')
#job=led1.job_blink(n=3,on=0.5,off=0.3)
#job.start()
#job.join()
#led1.on()
#sleep(1)
st.start('COM3')

led = st.LED()
led.attach(st.A0)

for i in range(2):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)


# job.start().join()と書いてもよいし、job()と書くことも可能

disconnect()
