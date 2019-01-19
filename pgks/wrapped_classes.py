# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import (LED,Buzzer,DCMotor,Servomotor,Accelerometer,PushSwitch,TouchSensor,
                      IRPhotoreflector,LightSensor,SoundSensor,
                      FWD,BCK,BRAKE,COAST)
from threading import Thread,Event
from time import sleep
from math import ceil


class RobotJob():
    __thread = None
    __event = None
    
    def __init__(self, proc):
        #def f():
        #    proc(self)
        self.__thrproc = lambda:proc(self)

    def __call__(self):
        self.start()
        self.wait()
        
    # def _ssleep(self, sec):
    #     if not self._active:
    #         return False
    #     elif sec>0.1:
    #         m = ceil(sec/0.1)
    #         shredded_sec = sec/m
    #         while self._active and m>0:
    #             m -= 1
    #             sleep(shredded_sec)
    #     else:
    #         sleep(sec)
    #     return self._active

    def _ssleep(self, sec):
        if not self.__event:
            return False
        return self.__event.wait(sec)

    def is_active(self):
        return (self.__event and not self.__event.is_set())
    
    def start(self):
        self.__event = Event()
        self.__thread = Thread(target=self.__thrproc)
        self.__thread.start()
        return self

    def wait(self):
        self.__thread.join()
        self.__thread = None
    
    def cancel(self):
        self.__event.set()
        self.wait()

def mkjob(proc) -> RobotJob:
    return RobotJob(lambda job:proc())

def parjobs(*jobs) -> RobotJob:
    pass

# 出力系パーツ

class LED_wrap(LED):
    # n==None means n is infinity
    def blink(self, n=None, on=0.3, off=0.3):
        def f(job):
            cnt = n
            while job.is_active():
                if cnt is not None:
                    if cnt==0: break
                    cnt -= 1
                print('on')
                if not job._ssleep(on):
                    # todo: off にしてから
                    break
                print('off')
                job._ssleep(off)
                
        return RobotJob(f)
                               

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
    def drive(self,sec,forward=True,brake=True):
        pass

    def moveon(self,forward=True):
        self.move(FWD if forward else BCK)

    # DCMotor.stop()を遮蔽することに注意（互換性あり）
    def stop(motion=BRAKE, brake=True):
        if motion==BRAKE and not brake: motion = COAST
        DCMotor.stop(self, motion)
    
    
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

