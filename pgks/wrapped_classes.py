# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import (LED,Buzzer,DCMotor,Servomotor,Accelerometer,PushSwitch,TouchSensor,
                      IRPhotoreflector,LightSensor,SoundSensor)
from threading import Thread
from time import sleep

class RobotJob():
    def __init__(self, proc):
        self.polling = True
        self.thread = Thread(target=proc,args=[self])
        self.thread.start()
        
    def wait(self):
        self.thread.join()
    
    def cancel(self):
        self.polling = False
        self.wait()
    

class LED_wrap(LED):
    # n==None means n is infinity
    def blink(self, n=None, on=0.3, off=0.3):
        def f(job):
            nonlocal n
            while job.polling:
                if n is not None:
                    if n==0: break
                    n -= 1
                print('on')
                sleep(on)
                print('off')
                sleep(off)
                
        return RobotJob(f)
                               
                        
class Buzzer_wrap(Buzzer):
    pass

class DCMotor_wrap(DCMotor):
    pass

class Servomotor_wrap(Servomotor):
    pass

class Accelerometer_wrap(Accelerometer):
    pass

class PushSwitch_wrap(PushSwitch):
    pass

class TouchSensor_wrap(TouchSensor):
    pass

class IRPhotoreflector_wrap(IRPhotoreflector):
    pass

class LightSensor_wrap(LightSensor):
    pass

class SoundSensor_wrap(SoundSensor):
    pass

