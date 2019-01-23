# -*- coding: utf-8 -*-
from pgkstuduino import *

# 3つのLEDを異なる発光パターンで同時にブリンクさせる並列処理の例

st_set_debug()
st_set_real(False)

connect(4)

led1,led2,led3 = mkpart('LED:A0/A1/A2')
job = par(led1.job_blink(n=10,on=0.4,off=0.1),
          led2.job_blink(n=10,on=0.2,off=0.3),
          led3.job_blink(n=5,on=1,off=0.2))
job.start()
job.join()

# job.start().join()と書いてもよいし、job()と書くことも可能

disconnect()
