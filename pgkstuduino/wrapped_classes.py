# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import FWD,BCK,BRAKE,COAST

from .primitives import *
from .robot_job import *

# 出力系パーツ

class PGkLED(LEDWrap):
    # n==None means n is infinity
        
    def job_blink(self, n=None, on=0.3, off=0.3):
        def fn(job):
            cnt = n
            while job.is_active():
                if cnt is not None:
                    if cnt==0: break
                    cnt -= 1
                #print('on')
                self.on()
                if not job._safe_sleep(on):
                    # todo: off にしてから
                    self.off()
                    break
                #print('off')
                self.off()
                job._safe_sleep(off)
                
        return RobotJob(fn)
                               

class PGkBuzzer(BuzzerWrap):
    def on(self, note, octave=0, sec=None, duration=0):
        d = 0
        if sec: d = int(sec*1000)
        elif duration: d = duration
        
        BuzzerWrap.on(self, note, octave=octave, duration=d)
        
    ## MIDI style
    def noteon(self, note, sec=None):
        self.on(note%12, note//12, sec=sec)
    def noteoff(self):
        self.off()

    def job_perform():
        pass
        
        
class PGkDCMotor(DCMotorWrap):
    
    def job_drive(self,sec,*,forward=True,brake=True):
        def fn(job):
            if job.is_active():
                #print('moveon!',forward)
                self.moveon(forward)
                job._safe_sleep(sec)
                #print('brake!!!',brake)
                self.stop(brake=brake)
        return RobotJob(fn)

    def moveon(self,*,forward=True):
        self.move(FWD if forward else BCK)

    def stop(self,*,motion=BRAKE, brake=True):
        if motion==BRAKE and not brake: motion = COAST
        self._stop(self, motion)

class PGkServomotor(ServomotorWrap):
    def job_move(self, angle):
        def f(job):
            self.setAngle(angle)
        return RobotJob(f)

    @staticmethod
    def job_sync_move(servos:[ServomotorWrap], angles:[int], delay=1):
        def f(job):
            ServomotorWrap.syncMove(servos, angles, delay)
        return RobotJob(f)

    
## 入力系パーツ デジタルセンサ

class SensorMonitor():
    def job_monitor(self, callback, interval=1, n=None):
        def f(job):
            cnt = n
            while job.is_active():
                if cnt is not None:
                    if cnt==0: break
                    cnt -= 1
                callback(self.getValue())
                job._safe_sleep(interval)
        return RobotJob(f)

class PGkPushSwitch(PushSwitchWrap,SensorMonitor):
    def job_on_pushed(self, callback, once=True):
        def fn(job):
            ignore = False
            while job.is_active():
                if not ignore and self.getValue()==0:
                    callback()
                    if once: break;
                    ignore = True
                else:
                    ignore = False
                job._safe_sleep(0.1)
        return RobotJob(fn)

class PGkTouchSensor(TouchSensorWrap,SensorMonitor):
    pass

## 入力系パーツ アナログセンサ


class PGkAccelerometer(AccelerometerWrap,SensorMonitor):
    pass


class PGkIRPhotoreflector(IRPhotoreflectorWrap,SensorMonitor):
    pass

class PGkLightSensor(LightSensorWrap,SensorMonitor):
    pass

class PGkSoundSensor(SoundSensorWrap,SensorMonitor):
    pass

