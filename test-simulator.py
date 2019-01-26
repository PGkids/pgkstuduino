# -*- coding: utf-8 -*-
from pgkstuduino import *
from sys import argv

st_set_debug('-debug' in argv)  
st_set_real(False)

connect(4)

sw1,led1,led2,led3,bz1,bz2=mkpart('PushSwitch:A0,LED:A1/A2/A3,Buzzer:A4/A5')
dc1,dc2 = mkpart('DCMotor:M1/M2')
sv1,sv2,sv3,sv4 = mkpart('Servo:D9/D10/D11/D12')

s1,s2 = mkpart('LightSensor:A6,Accelerometer:A7')

j1 = par(led1.job_blink(n=5,on=0.4,off=0.1),
         led2.job_blink(n=5,on=0.2,off=0.3),
         led3.job_blink(n=3,on=1,off=0.2))
#j2 = par(s1.job_monitor(lambda x:print(f'light:{x}'),interval=1),
#         s2.job_monitor(lambda x:print(f'light:{x}'),interval=1))
def monitor1(x):
    print(f'light:{x}')
    if x < 50:
        dc1.setPower(x)
        dc1.moveon()
    else:
        sv1.setAngle(x)
        dc1.stop()
j21 = s1.job_monitor(monitor1,interval=1)
j22 = s2.job_monitor(lambda x:print(f'accel:{x}'),interval=1)
j2 = par(j21,j22)
def cancel_job():
    print('終了します')
    #j2.cancel()
    j21.cancel()
    j22.cancel()
j3 = sw1.job_on_pushed(cancel_job,once=True)

job = par(j1,j2,j3)
job()

disconnect()



