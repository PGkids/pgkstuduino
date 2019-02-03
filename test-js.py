# -*- coding: utf-8 -*-

from pgkstuduino import *
import pygame as pgm
from time import sleep
from sys import argv

JS_QUITBTN  = 7  #終了ボタン
JS_ACCELBTN = 3 #アクセルボタン
JS_RACCELBTN = 1 #反転アクセルボタン

pgm.init()
pgm.joystick.init()
try:
    js = pgm.joystick.Joystick(0)
    js.init()
except pgm.error:
    raise Exception('Joystick not found')

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)
connect(3)

dc_left,dc_right = mkpart('DCMotor:M1/M2')
led_left,led_accel,led_right = mkpart('LED:A0/A1/A2')
buzzer = mkpart('Buzzer:A3')
direction = None # 'left' ir 'right'
blinkjob = None
buzzerjob = None

# J.S.Bachの教会カンタータの有名な旋律
songdata = [0,2,4,7,5,5,9,7,7,12,11,12,7,4,0,2,4,5,7,9,7,5,4,2,4,0, -1,0,2,-5,-1,2,5,4,2,4,
            0,2,4,7,5,5,9,7,7,12,11,12,7,4,0,2,4, 2,7,5,4,2,0,-5,0,-1,0,4,7,12,7,4,0,4, 6,
            7,-5,-3,-1,2,1,1,4,2,2,5,4,5,2,-3,-7,-5,-3,-2,7,5,7,4,1,-3,-1,1,
            2,5,4,5,9,7,7,10,9,9,14,13,14,9,5,2,4,5, 10,9,7,5,4,2,-3,2,1,2,5,9,14,9,5,2]

def new_buzzer_job():
    cnt = 0
    def perform_song():
        nonlocal cnt
        current_note = 60 + songdata[cnt%len(songdata)]
        cnt += 1
        buzzer.noteon(current_note)
        sleep(0.2)
        buzzer.noteoff()
    return rep(mkjob(perform_song))

status = create_label('status')
user_btn = create_button()


while True:
    e = pgm.event.wait()
    if e.type==pgm.JOYBUTTONDOWN and e.button==JS_QUITBTN:
        status('ロボットとの通信を終了します')
        break
    elif e.type==pgm.JOYAXISMOTION and e.axis==0:
        # 十字ボタンX軸
        if e.value > 0.5:
            dc_left.setPower(10)
            dc_right.setPower(100)
            led_right.on()
            direction = 'right'
        elif e.value < -0.5:
            dc_left.setPower(100)
            dc_right.setPower(10)
            led_left.on()
            direction = 'left'
        else:
            dc_left.setPower(100)
            dc_right.setPower(100)
            if direction is 'left': led_left.off()
            elif direction is 'right': led_right.off()
        
    elif e.type==pgm.JOYBUTTONDOWN and (e.button==JS_ACCELBTN or
                                        e.button==JS_RACCELBTN):
        fwdp = e.button==JS_ACCELBTN
        dc_left.moveon(forward=fwdp)
        dc_right.moveon(forward=fwdp)
        if fwdp:
            led_accel.on()
            status('出発進行～ッ！')
        else:
            status('バックします。ご注意ください！')
            blinkjob = led_accel.job_blink(on=0.2,off=0.3)
            blinkjob.start()
            buzzerjob = new_buzzer_job()
            buzzerjob.start()
    elif e.type==pgm.JOYBUTTONUP and (e.button==JS_ACCELBTN or
                                      e.button==JS_RACCELBTN):
        dc_left.stop()
        dc_right.stop()
        status('停車中')
        if blinkjob:
            blinkjob.cancel().join()
            #blinkjob.join()
            blinkjob = None
            buzzerjob.cancel().join()
            buzzerjob = None
        else:
            led_accel.off()

disconnect()
