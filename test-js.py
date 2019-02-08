# -*- coding: utf-8 -*-

from pgkstuduino import *
import pygame as pgm
from time import sleep
from sys import argv

JS_QUITBTN  = 7  #終了ボタン
JS_ACCELBTN = 3 #アクセルボタン
JS_RACCELBTN = 1 #反転アクセルボタン

pgm.mixer.init(44100, -16, 2, 2048)
sound_up   = pgm.mixer.Sound('js-up.wav')
sound_down = pgm.mixer.Sound('js-down.wav')

pgm.init()
pgm.joystick.init()
try:
    js = pgm.joystick.Joystick(0)
    js.init()
except pgm.error:
    raise Exception('Joystick not found')

st_set_debug('-debug' in argv)
st_set_real('-devel' not in argv)
connect(4)

led_left,led_accel,led_right = mkpart('LED:A0/A1/A2')
dc_left,dc_right,buzzer = mkpart('DCMotor:M1/M2,Buzzer:A3')
direction = None # 'left' or 'right'
back_job  = None

powers = [(50,30),(60,30),(70,40),(80,40),(90,50),(100,50)]
power_index = len(powers) - 1
dc_left.power = dc_right.power = powers[power_index][0]

# J.S.Bachの教会カンタータの有名な旋律(BWV147)
SONG_DATA = (0,2,4,7,5,5,9,7,7,12,11,12,7,4,0,2,4,5,7,9,7,5,4,2,4,0, -1,0,2,-5,-1,2,5,4,2,4,
            0,2,4,7,5,5,9,7,7,12,11,12,7,4,0,2,4, 2,7,5,4,2,0,-5,0,-1,0,4,7,12,7,4,0,4, 6,
            7,-5,-3,-1,2,1,1,4,2,2,5,4,5,2,-3,-7,-5,-3,-2,7,5,7,4,1,-3,-1,1,
            2,5,4,5,9,7,7,10,9,9,14,13,14,9,5,2,4,5, 10,9,7,5,4,2,-3,2,1,2,5,9,14,9,5,2)

def mk_back_job():
    cnt,length = 0,len(SONG_DATA)
    def perform_song():
        nonlocal cnt
        current_note = 55 + SONG_DATA[cnt%length] #カンタータ原曲どおりト長調で
        cnt += 1
        buzzer.noteon(current_note)
        sleep(0.15)
        buzzer.noteoff()
    return par(led_accel.job_blink(on=0.2,off=0.3),
               rep(mkjob(perform_song), interval=0.05))

status = create_label('初期状態です')
power_status = create_label('')
def set_power_status():
    power_status(f'DCモーター出力: {powers[power_index][0]}%')

set_power_status()

while True:
    e = pgm.event.wait()
    if e.type==pgm.JOYBUTTONDOWN and e.button==JS_QUITBTN:
        status('ロボットとの通信を終了します')
        break
    elif e.type==pgm.JOYAXISMOTION and e.axis==0:
        # 十字ボタンX軸 (方向制御)
        hi,lo = powers[power_index]
        if e.value > 0.5: #############  右折   ################
            dc_left.power,dc_right.power = hi,lo
            led_right.on()
            direction = 'right'
        elif e.value < -0.5: ##########  左折   ################
            dc_left.power,dc_right.power = lo,hi
            led_left.on()
            direction = 'left'
        else:                ##########  直進   #################
            dc_left.power,dc_right.power = hi,hi
            if direction   is 'left':  led_left.off()
            elif direction is 'right': led_right.off()
            direction = None

    elif e.type==pgm.JOYAXISMOTION and e.axis==1:
        # 十字ボタンY軸 (パワー制御)
        if e.value > 0.5:
            if power_index > 0: power_index -= 1; sound_down.play()
            else: continue
        elif e.value < -0.5:
            if power_index < len(powers)-1: power_index += 1; sound_up.play()
            else: continue
        else:
            continue
        hi,lo = powers[power_index]
        if direction   is 'left':  dc_left.power,dc_right.power = lo,hi
        elif direction is 'right': dc_left.power,dc_right.power = hi,lo
        else:                      dc_left.power = dc_right.power = hi
        set_power_status()
            
    elif e.type==pgm.JOYBUTTONDOWN and (e.button==JS_ACCELBTN or
                                        e.button==JS_RACCELBTN):
        fwdp = e.button==JS_ACCELBTN
        dc_left.state = dc_right.state = 'fwd' if fwdp else 'back'
        if fwdp:
            led_accel.on()
            status('出発進行～！ THE VOICE OF ROCK! GLENN HUGHES!!')
            pgm.mixer.music.load('js-drive.wav')
        else:
            back_job = mk_back_job().start()
            status('バックします。ご注意ください！')
            pgm.mixer.music.load('js-back.wav')
        pgm.mixer.music.set_volume(1.0)
        pgm.mixer.music.play(-1)
    elif e.type==pgm.JOYBUTTONUP and (e.button==JS_ACCELBTN or
                                      e.button==JS_RACCELBTN):
        dc_left.state = dc_right.state = 'brake'
        status('停車')
        if back_job: 
            back_job.cancel().join()
            back_job = None
        else:
            led_accel.off()
        pgm.mixer.music.stop()

disconnect()
