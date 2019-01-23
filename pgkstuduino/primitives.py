# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import studuino
st = studuino

_debug = None
_realp = True

def st_set_debug(enable=True):
    def debugPrint(name,**arg_pairs):
        print(f'DEBUG: {name}(',end='')
        for k in arg_pairs:
            print(f'{k}={arg_pairs[k]},',end='')
        print(')')
    global _debug
    _debug = debugPrint

def st_set_real(enable=True):
    global _realp
    _realp = enable

def st_start(com_port:str, baud_rate=38400):
    if _debug: _debug('st_start', com_port=com_port, baud_rate=baud_rate)
    if _realp: st.start(com_port, baud_rate)

def st_stop():
    if _debug: _debug('st_stop')
    if _realp: st.stop() 

class PartWrap():
    def attach(self,connector):
        if _debug: _debug(f'{self.name}::attach')
        if _realp: self.attach(connector)

class BuzzerWrap(st.Buzzer,PartWrap):
    def off(self):
        if _debug: _debug('Buzzer::off')
        if _realp: st.Buzzer.off(self)
    def on(self, sound, octave=0, duration=0):
        if _debug: _debug('Buzzer::on',sound=sound, octave=octave, duration=duration)
        if _realp: st.Buzzer.on(self, sound, octave=octave, duration=duration)
    

class DCMotorWrap(st.DCMotor,PartWrap):
    def move(self, motion):
        if _debug: _debug('DCMotor::move',motion=motion)
        if _realp: st.DCMotor.move(self, motion)
    def stop(self, motion):
        if _debug: _debug('DCMotor::stop',motion=motion)
        if _realp: st.DCMotor.stop(self, motion)
    def setPower(self, power):
        if _debug: _debug('DCMotor::setPower',power=power)
        if _realp: st.DCMotor.power(self, power)

class LEDWrap(st.LED,PartWrap):
    def on(self):
        if _debug: _debug('LED::on')
        if _realp: st.LED.on(self)
    def off(self):
        if _debug: _debug('LED::off')
        if _realp: st.LED.off(self)

class ServomotorWrap(st.Servomotor,PartWrap):
    def setAngle(self, angle):
        if _debug: _debug('ServoMotor::setAngle',angle=angle)
        if _realp: st.Servomotor.setAngle(self,angle)

    @staticmethod
    def syncMove(self, servos, angles, delay):
        if _debug: _debug('ServoMotor::setAngle', servos=servos, angles=angles, delay=delay)
        if _realp: st.Servomotor.syncMove(serves, angles, delay)

class SensorWrap():
    def getValue(self):
        if _debug: _debug(f'{self.name}::getValue')
        if _realp: return self.getValue()
        else:      return 1 

class PushSwitchWrap(st.PushSwitch,PartWrap,SensorWrap):
    pass

class TouchSensorWrap(st.TouchSensor,PartWrap,SensorWrap):
    pass

class IRPhotoreflectorWrap(st.IRPhotoreflector,PartWrap,SensorWrap):
    pass

class LightSensorWrap(st.LightSensor,PartWrap,SensorWrap):
    pass

class SoundSensorWrap(st.SoundSensor,PartWrap,SensorWrap):
    pass

class AccelerometerWrap(st.Accelerometer,PartWrap):
    def getValue(self):
        if _debug: _debug('Accelerometer::getValue')
        if _realp: return self.getValue()
        else:      return (0,0,0)
