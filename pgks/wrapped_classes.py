# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import (LED,Buzzer,DCMotor,Servomotor,Accelerometer,PushSwitch,TouchSensor,
                      IRPhotoreflector,LightSensor,SoundSensor,
                      FWD,BCK)
from threading import Thread
from time import sleep
from math import ceil

class RobotJob():
    def __init__(self, proc, initializer=None, finalizer=None):
        self._active = True
        def f():
            if initializer: initializer(self)
            proc(self)
            if finalizer: finalizer(self)
        self._thread = Thread(target=f)
        self._thread.start()

    def _ssleep(self, rsec):
        if not self._active:
            return False
        elif rsec>0.1:
            m = ceil(rsec/0.1)
            shredded_rsec = rsec/m
            while self._active and m>0:
                m -= 1
                sleep(shredded_rsec)
        else:
            sleep(rsec)
        return self._active
    
    def wait(self):
        self._thread.join()
    
    def cancel(self):
        self._active = False
        self.wait()

    def get_thread(self):
        return self._thread

# 出力系パーツ

class LED_wrap(LED):
    # n==None means n is infinity
    def blink(self, n=None, on=0.3, off=0.3, initializer=None, finalizer=None):
        def f(job):
            nonlocal n
            while job._active:
                if n is not None:
                    if n==0: break
                    n -= 1
                print('on')
                if not job._ssleep(on):
                    # todo: off にしてから
                    break
                print('off')
                job._ssleep(off)
                
        return RobotJob(f,initializer,finalizer)
                               
                        
class Buzzer_wrap(Buzzer):
    def on(self, note, octave=0, sec=None, duration=None):
        if sec: d = int(sec*1000)
        elif duration: d = duration
        Buzzer.on(self, note, octave=octave, duration=d)

    ## MIDI style
    def noteon(self, note, sec=None):
        self.on(note%12, note//12, sec=sec)
    def noteoff(self):
        self.off()

class DCMotor_wrap(DCMotor):
    _direction = FWD
    def setdirection(self):
        pass
    def setbreak(self):
        pass
    def drive(self,sec):
        pass

## 入力系パーツ デジタルセンサ

class PushSwitch_wrap(PushSwitch):
    pass

class TouchSensor_wrap(TouchSensor):
    pass

## 入力系パーツ アナログセンサ

class Servomotor_wrap(Servomotor):
    pass

class Accelerometer_wrap(Accelerometer):
    pass


class IRPhotoreflector_wrap(IRPhotoreflector):
    pass

class LightSensor_wrap(LightSensor):
    pass

class SoundSensor_wrap(SoundSensor):
    pass

