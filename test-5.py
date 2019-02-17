# -*- coding: utf-8 -*-

from pgkstuduino import *
import midiate
from sys import argv
from time import sleep

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)
connect(4)

led1,led2,led3 = mkpart('LED:A0/A1/A2')
servo1,servo2  = mkpart('Servo:D2/D4')

led_job = None

status_label = create_label('')

def reset():
    global led_job
    status_label('Gディミニッシュスケールの構成音だけを鳴らしてください')
    #サーボモータ初期角度
    servo1.angle = servo2.angle = 90
    if led_job:
        led_job.cancel().join()
        led_job = None

create_button('リセット', reset)
reset()

sw = mkpart('PushSwitch:A3*')
job = sw.job_on_pushed(lambda:print('終了します'),once=True)

mid = midiate.Midiator()
mid.start_process()

indev = mid.open_input(name='loopMIDI Port');
#indev = mid.open_input(name='UM-1');

def on_succeeded():
    status_label('おめでとうございます！')
    def routine():
        led1.on(); sleep(0.1); led1.off()
        led2.on(); sleep(0.1); led2.off()
        led3.on(); sleep(0.1); led3.off()
        led2.on(); sleep(0.1); led2.off()
    global led_job
    led_job = rep(mkjob(routine))
    led_job.start()
    
def on_failed():
    status_label('残念でした… もっと練習してください！')
    def routine():
        led1.state = led2.state = led3.state = True
        sleep(0.3)
        led1.state = led2.state = led3.state = False
    global led_job
    led_job = rep(mkjob(routine),interval=0.3)
    led_job.start()

CORRECT_NOTES = {0,1,3,4,6,7,9,10}
def check_note(dev, msg, raw):
    if led_job: return None
    #if True: #raw[0]&0xF0==0x90 and raw[2]>0:
    if raw[2]:
        note = raw[1]
        if note%12 in CORRECT_NOTES:
            status_label(f'OK {raw[1]}')
            led1.state = led2.state = True
            servo1.angle += 1
            if servo1.angle >= 180: on_succeeded()
        else:
            status_label('NG')
            led3.state = led2.state = True
            servo2.angle += 10
            if servo2.angle >= 180: on_failed()
    elif False:
        if led1.state: led1.state = False
        if led2.state: led2.state = False
        if led3.state: led3.state = False

def on_noteoff(dev, msg, raw):
    if led1.state: led1.state = False
    if led2.state: led2.state = False
    if led3.state: led3.state = False

        
mid.callback(indev,'8,9***00', on_noteoff)
mid.callback(indev,'9',check_note)

mid.listen(indev)

job()

mid.stop_process()
disconnect()
