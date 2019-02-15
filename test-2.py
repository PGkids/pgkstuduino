# -*- coding: utf-8 -*-
from pgkstuduino import *
from sys import argv

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)

connect(4)
p1,p2,p3,p4 = mkpart('PushSwitch:A0/A1/A2/A3')

print('すべてのプッシュスイッチを押してね！')
j1 = p1.job_on_pushed(lambda:print('A0 pushed!!'),True)
j2 = p2.job_on_pushed(lambda:print('A1 pushed!!'),True)
j3 = p3.job_on_pushed(lambda:print('A2 pushed!!'),True)
j4 = p4.job_on_pushed(lambda:print('A3 pushed!!'),True)
job = par(j1,j2,j3,j4)
job.start()
job.join()
print('全部押されました！')


disconnect()
