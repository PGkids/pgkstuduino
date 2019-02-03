# -*- coding: utf-8 -*-

from pgkstuduino import *
import midiate
from sys import argv

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)

connect(3)

leds = mkpart('LED:A0/A1/A2')
buzzer = mkpart('Buzzer:A5')
sw = mkpart('PushSwitch:A3')
job = sw.job_on_pushed(lambda:print('終了します'),once=True)

mid = midiate.Midiator()
mid.start_process()

indev = mid.open_input(name='loopMIDI Port');
#indev = mid.open_input(name='UM-1');
#indev = mid.open_input(name='USB Oxygen 8 v2');

def st_bz_on(note):
    #buzzer.on(note % 12, note // 12)
    buzzer.noteon(note)
    print('BUZZER: ',note)
def st_bz_off():
    buzzer.off()
    print('BUZZER OFF')

ptns = [(0,),(1,),(2,),(0,1),(1,2),(0,1,2)]
count = 0
def st_led_on():
    for i in ptns[count%len(ptns)]:
        leds[i].on()
    print('LED on')
def st_led_off():
    for i in ptns[count%len(ptns)]:
        leds[i].off()
    print('LED off')

def on(dev, msg, raw):
    if raw[2] == 0:
        return off(dev,msg,raw)
    global count
    count += 1
    st_bz_on(raw[1])
    #devel.status(f'{count}個の発音信号をスタディーノに送ったよ！')
    st_led_on()
    print('受信: ', dev, msg, raw)

def off(dev, msg, raw):
    st_bz_off()
    st_led_off()
    
mid.callback(indev,'9', on)
mid.callback(indev,'8', off)
mid.listen(indev);


#devel.wait(title='studuino buzzer test',text='studuinoのブザーを鳴らすよ')

job()

mid.stop_process()
disconnect()
