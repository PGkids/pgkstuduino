# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import (LED,Buzzer,DCMotor,Servomotor,Accelerometer,PushSwitch,TouchSensor,
                      IRPhotoreflector,LightSensor,SoundSensor,
                      FWD,BCK,BRAKE,COAST)
from threading import Thread,Event
from time import sleep,clock
from math import ceil


class RobotJob():
    __thread    = None
    __event     = None
    __active    = False
    
    def __init__(self, proc):
        def fn():
            proc(self)
            self.__active = False
            self.__event.set()
        self.__thrproc = fn

    def __call__(self):
        self.start()
        self.join()
        
    def _get_event(self):
        return self.__event

    # Safe Sleep
    def _safe_sleep(self, sec):
        if not self._active: return False
        clock_entered = clock()
        while True:
            if not self.__event.wait(sec):
                # Timed out
                return self.__active
            if not self.__active:
                return False
            self.__event.clear()
            cur_clock = clock()
            if (cur_clock - clock_entered) >= sec:
                return True
            sec -= cur_clock - clock_entered
            clock_entered = cur_clock

    def _wait_for_event(self):
        self.__event.wait(None)
        return self.__active
    
    def is_active(self):
        return self.__active
    
    def __start(self, join, event):
        if not self.__active:
            self.__active = True
            self.__event = event
            self.__thread = Thread(target=self.__thrproc)
            self.__thread.start()
            if join: self.join()
            return self
        else:
            raise(RuntimeError)

    def start(self, join=False):
        return self.__start(join, Event())

    def _start_with(self, event):
        return self.__start(False, event)
    
    def join(self, timeout=None):
        if self.__active:
            self.__thread.join(timeout)
            if self.__thread.is_alive():
                return False
            else:
                self.__thread = None
                self.__active = False
                self.__event.clear()
                return True
        else:
            return True
    def cancel(self):
        if self.__active:
            self.__active = False
            self.__event.set()

def mkjob(proc, *args) -> RobotJob:
    return RobotJob(lambda job:proc(*args))

def parjob(*jobs) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        for job in jobs:
            job._start_with(ev)
        while master_job.is_active():
            still_alive = False
            for job in jobs:
                if job.is_active():
                    still_alive = True
            if still_alive:
                if not master_job._wait_for_event():
                    for job in jobs:
                        if not job.is_active():
                            job.cancel()
            else:
                break
        # join all jobs
        for job in jobs:
            job.join()

    return RobotJob(fn)

def ordjob(*jobs) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        for job in jobs:
            job._start_with(ev)
            # master_jobがキャンセルされた場合
            if not master_job._wait_for_event():
                job.cancel()
            job.join()
            if not master_job.is_active():
                break

    return RobotJob(fn)

def loopjob(job) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        while master_job.is_active():
            job._start_with(ev)
            if not master_job._wait_for_event():
                job.cancel()
            job.join()
            

    return RobotJob(fn)


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

