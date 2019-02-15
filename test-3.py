# -*- coding: utf-8 -*-
from pgkstuduino import *
from sys import argv

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)

# 光センサの値をモニタリングする
# A3スイッチで終了

connect(4)

p,s1,s2 = mkpart('PushSwitch:A2,LightSensor:A4,SoundSensor:A5')
#p,s1,s2 = mkpart('PushSwitch:A3,LightSensor:A4,SoundSensor:A7')
j1 = s1.job_monitor(lambda x:print(f'    light:value={x}') ,interval=0.3)
j2 = s2.job_monitor(lambda x:print(f'sound:value={x}') ,interval=0.3)
def cancel_monitor():
    j1.cancel()
    j2.cancel()
j3 = p.job_on_pushed(cancel_monitor)
job = par(j1,j2,j3)
job.start()
job.join()

disconnect()



