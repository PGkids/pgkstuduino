# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import os
import studuino
st = studuino
import tkinter
tk = tkinter
from threading import Thread,Event

class Simulator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def abort(self):
        self.master.destroy()
        os._exit(-1)

    def create_widgets(self):
        abort_btn = tk.Button(self, text='ABORT this process', bg='blue', fg='white', command=self.abort)
        abort_btn.pack()
        self.led_frame = tk.LabelFrame(self, text='LEDs')
        self.led_frame.pack()
        self.buzzer_frame = tk.LabelFrame(self, text='Buzzers')
        self.buzzer_frame.pack()
        self.dc_frame = tk.LabelFrame(self, text='DC Motors')
        self.dc_frame.pack()
        self.servo_frame = tk.LabelFrame(self, text='Servomotors')
        self.servo_frame.pack()
        self.digital_frame = tk.LabelFrame(self, text='Digital Sensors')
        self.digital_frame.pack()
        self.analog_frame = tk.LabelFrame(self, text='Analog Sensors')
        self.analog_frame.pack()
                        
_debug = None
_realp = True
_simulator = None

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
    ev = Event()
    obj = None
    def gui():
        root = tk.Tk()
        root.geometry('600x400')
        root.title('Studuino Simulator')
        sim = Simulator(root)
        ev.set()
        global _simulator
        _simulator = sim
        sim.mainloop()
    thr = Thread(target=gui)
    thr.start()
    ev.wait()
    btn = tk.Button(_simulator, text='test')
    btn.pack()


def st_start(com_port:str, baud_rate=38400):
    if _debug: _debug('st_start', com_port=com_port, baud_rate=baud_rate)
    if _realp: st.start(com_port, baud_rate)

def st_stop():
    if _debug: _debug('st_stop')
    if _realp: st.stop() 

class PartWrap():
    _widget = None
    def __init__(self):
        if _simulator:
            w = None
            if self._frame_type is 'led':
                w = tk.Label(_simulator.led_frame, text=self.name)
            elif self._frame_type is 'buzzer':
                w = tk.Label(_simulator.buzzer_frame, text=self.name)
            elif self._frame_type is 'dc':
                w = tk.Label(_simulator.dc_frame, text=self.name)
            elif self._frame_type is 'servo':
                w = tk.Label(_simulator.servo_frame, text=self.name)
            elif self._frame_type is 'digital':
                w = tk.Label(_simulator.digital_frame, text=self.name)
            elif self._frame_type is 'analog':
                w = tk.Label(_simulator.analog_frame, text=self.name)            
            w.pack()
            self._widget = w
            
    def attach(self,connector):
        if _debug: _debug(f'{self.name}::attach',connector=connector)
        if _realp: self.attach(connector)
        else:
            self._widget.configure(text=self.name+':'+str(connector))

class BuzzerWrap(PartWrap,st.Buzzer):
    _frame_type = 'buzzer'
    def off(self):
        if _debug: _debug('Buzzer::off')
        if _realp: st.Buzzer.off(self)
    def on(self, sound, octave=0, duration=0):
        if _debug: _debug('Buzzer::on',sound=sound, octave=octave, duration=duration)
        if _realp: st.Buzzer.on(self, sound, octave=octave, duration=duration)
    

class DCMotorWrap(PartWrap,st.DCMotor):
    _frame_type = 'dc'
    def move(self, motion):
        if _debug: _debug('DCMotor::move',motion=motion)
        if _realp: st.DCMotor.move(self, motion)
    def stop(self, motion):
        if _debug: _debug('DCMotor::stop',motion=motion)
        if _realp: st.DCMotor.stop(self, motion)
    def setPower(self, power):
        if _debug: _debug('DCMotor::setPower',power=power)
        if _realp: st.DCMotor.power(self, power)

class LEDWrap(PartWrap,st.LED):
    _frame_type = 'led'
    def on(self):
        if _debug: _debug('LED::on')
        if _realp: st.LED.on(self)
    def off(self):
        if _debug: _debug('LED::off')
        if _realp: st.LED.off(self)

class ServomotorWrap(PartWrap,st.Servomotor):
    _frame_type = 'servo'
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

class PushSwitchWrap(PartWrap,SensorWrap,st.PushSwitch):
    _frame_type = 'digital'

class TouchSensorWrap(PartWrap,SensorWrap,st.TouchSensor):
    _frame_type = 'digital'

class IRPhotoreflectorWrap(PartWrap,SensorWrap,st.IRPhotoreflector):
    _frame_type = 'analog'

class LightSensorWrap(PartWrap,SensorWrap,st.LightSensor):
    _frame_type = 'analog'
    pass

class SoundSensorWrap(PartWrap,SensorWrap,st.SoundSensor):
    _frame_type = 'analog'

class AccelerometerWrap(PartWrap,st.Accelerometer):
    _frame_type = 'analog'

    def getValue(self):
        if _debug: _debug('Accelerometer::getValue')
        if _realp: return self.getValue()
        else:      return (0,0,0)
