# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import (LED,Buzzer,DCMotor,Servomotor,Accelerometer,PushSwitch,TouchSensor,
                      IRPhotoreflector,LightSensor,SoundSensor,
                      FWD,BCK,BRAKE,COAST)


# 出力系パーツ

class LED_wrap(LED):
    # n==None means n is infinity
        
    def job_blink(self, n=None, on=0.3, off=0.3):
        def fn(job):
            cnt = n
            while job.is_active():
                if cnt is not None:
                    if cnt==0: break
                    cnt -= 1
                print('on')
                if not job._safe_sleep(on):
                    # todo: off にしてから
                    break
                print('off')
                job._safe_sleep(off)
                
        return RobotJob(fn)
                               

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

    def job_perform():
        pass
        
        
class DCMotor_wrap(DCMotor):
    def job_drive(self,sec,forward=True,brake=True):
        def fn(job):
            if job.is_active():
                print('moveon!',forward)
                #self.moveon(forward)
                job._safe_sleep(sec)
                print('brake!!!',brake)
                #self.stop(brake=brake)
        return RobotJob(fn)

    def moveon(self,forward=True):
        self.move(FWD if forward else BCK)

    # DCMotor.stop()を遮蔽することに注意（互換性あり）
    def stop(motion=BRAKE, brake=True):
        if motion==BRAKE and not brake: motion = COAST
        DCMotor.stop(self, motion)

class Servomotor_wrap(Servomotor):
    def job_move(self, angle):
        def f(job):
            self.setAngle(angle)
        return RobotJob(f)

    @staticmethod
    def job_sync_move(servos:[Servomotor], angles:[int], delay=1):
        def f(job):
            Servomotor.syncMove(servos, angles, delay)
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

class PushSwitch_wrap(PushSwitch,SensorMonitor):
    def job_op_pushed(self, callback, once=True):
        def f(job):
            ignore = False
            while job.is_active():
                if not ignore and self.getValue()==1:
                    callback(*args)
                    if once: break;
                    ignore = True
                else:
                    ignore = False
                job._safe_sleep(0.1)
    

class TouchSensor_wrap(TouchSensor,SensorMonitor):
    pass

## 入力系パーツ アナログセンサ


class Accelerometer_wrap(Accelerometer,SensorMonitor):
    pass


class IRPhotoreflector_wrap(IRPhotoreflector,SensorMonitor):
    pass

class LightSensor_wrap(LightSensor,SensorMonitor):
    pass

class SoundSensor_wrap(SoundSensor,SensorMonitor):
    pass

