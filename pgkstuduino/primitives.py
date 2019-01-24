# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import os
import studuino
st = studuino
import tkinter
tk = tkinter
from threading import Thread,Event

_reversed_conn_dic = {st.A0:'A0', st.A1:'A1', st.A2:'A2', st.A3:'A3',
                      st.A4:'A4', st.A5:'A5', st.A6:'A6', st.A7:'A7',
                      st.M1:'M1', st.M2:'M2',
                      st.D2:'D2', st.D4:'D4', st.D7:'D7', st.D8:'D8',
                      st.D9:'D9', st.D10:'D10', st.D11:'D11', st.D12:'D12'}
def get_connector_name(conn):
    if conn in _reversed_conn_dic:
        return _reversed_conn_dic[conn]
    else:
        raise(ValueError)

class Simulator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def abort(self):
        #self.master.destroy()
        os._exit(-1)
    def quit_normally(self):
        self.master.quit()

    def toggle_quit_button_operation(self):
        self.quit_btn.configure(text='EXIT normally',
                                bg='white', fg='green', command=self.quit_normally)
    def create_widgets(self):
        self.quit_btn = tk.Button(self, text='ABORT this process immediately',
                              bg='blue', fg='white', command=self.abort)
        self.quit_btn.pack(pady=8,padx=16,fill=tk.X)
        self.led_frame = tk.LabelFrame(self, text='LEDs')
        self.led_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.buzzer_frame = tk.LabelFrame(self, text='Buzzers')
        self.buzzer_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.dc_frame = tk.LabelFrame(self, text='DC Motors')
        self.dc_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.servo_frame = tk.LabelFrame(self, text='Servomotors')
        self.servo_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.digital_frame = tk.LabelFrame(self, text='Digital Sensors')
        self.digital_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.analog_frame = tk.LabelFrame(self, text='Analog Sensors')
        self.analog_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.accel_frame = tk.LabelFrame(self, text='Accelerometers')
        self.accel_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
                        
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
    def gui():
        root = tk.Tk()
        #root.geometry('600x400')
        root.title('Studuino Simulator')
        sim = Simulator(root)
        global _simulator
        _simulator = sim
        #_simulator = sim
        ev.set()
        _simulator.mainloop()
    thr = Thread(target=gui)
    thr.start()
    ev.wait()


def st_start(com_port:str, baud_rate=38400):
    if _debug: _debug('st_start', com_port=com_port, baud_rate=baud_rate)
    if _realp: st.start(com_port, baud_rate)

def st_stop():
    if _debug: _debug('st_stop')
    if _realp: st.stop()
    else: _simulator.toggle_quit_button_operation()

class PartWrap():
    _widget = None
    def __init__(self):
        if _simulator:
            w = None
            t = self._frame_type
            if t is 'led':
                self._widget = tk.Label(_simulator.led_frame, text=self.name, bg='white')
                self._widget.pack()
            elif t is 'buzzer':
                self._widget = tk.Scale(_simulator.buzzer_frame, label=self.name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=128)
                self._widget.pack()                
            elif self._frame_type is 'dc':
                self._widget = tk.Scale(_simulator.dc_frame, label=self.name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=100)
                self._widget.pack()
            elif self._frame_type is 'servo':
                self._widget = tk.Scale(_simulator.servo_frame, label=self.name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=100)
                self._widget.pack()
            elif self._frame_type is 'digital':
                self._widget = tk.Scale(_simulator.digital_frame, label=self.name,orient='h',from_=0,to=1)
                self._widget.set(1)
                self._widget.pack()
            elif self._frame_type is 'analog':
                self._widget = tk.Scale(_simulator.analog_frame, label=self.name,orient='h',from_=0,to=100)
                self._widget.set(100)
                self._widget.pack()
            elif self._frame_type is 'accel':
                self._widget = tk.Label(_simulator.accel_frame, text=self.name)
                self._widget.pack()
                self._x_widget = tk.Scale(_simulator.accel_frame, label='X',orient='h',from_=0,to=100)
                self._x_widget.pack()
                self._y_widget = tk.Scale(_simulator.accel_frame, label='Y',orient='h',from_=0,to=100)
                self._y_widget.pack()                
                self._z_widget = tk.Scale(_simulator.accel_frame, label='Z',orient='h',from_=0,to=100)
                self._z_widget.pack()                
            else: raise(RuntimeError)
            
    def attach(self,connector):
        if _debug: _debug(f'{self.name}::attach',connector=connector)
        if _realp: self.attach(connector)
        else:
            t = self._frame_type
            device_name = self.name+'@'+str(get_connector_name(connector))
            if t is 'led' or t is 'accel':
                self._widget.configure(text=device_name)
            elif t is 'digital' or t is 'analog':
                self._widget.configure(label=device_name)
            else:
                self._widget.configure(label=device_name, state='disabled')

class BuzzerWrap(PartWrap,st.Buzzer):
    _frame_type = 'buzzer'
    def off(self):
        if _debug: _debug('Buzzer::off')
        if _realp: st.Buzzer.off(self)
        else: self._widget.configure(bg='white')
    def on(self, sound, octave=0, duration=0):
        if _debug: _debug('Buzzer::on',sound=sound, octave=octave, duration=duration)
        if _realp: st.Buzzer.on(self, sound, octave=octave, duration=duration)
        else:
            self._widget.configure(bg='yellow', state='active')
            self._widget.set(octave*12+sound)
            self._widget.configure(state='disabled')
    

class DCMotorWrap(PartWrap,st.DCMotor):
    _frame_type = 'dc'
    def move(self, motion):
        if _debug: _debug('DCMotor::move',motion=motion)
        if _realp: st.DCMotor.move(self, motion)
        else: self._widget.configure(bg='yellow')
    def stop(self, motion):
        if _debug: _debug('DCMotor::stop',motion=motion)
        if _realp: st.DCMotor.stop(self, motion)
        else: self._widget.configure(bg='white')
    def setPower(self, power):
        if _debug: _debug('DCMotor::setPower',power=power)
        if _realp: st.DCMotor.power(self, power)
        else:
            self._widget.configure(state='active')
            self._widget.set(power)
            self._widget.configure(state='disabled')

class LEDWrap(PartWrap,st.LED):
    _frame_type = 'led'
    def on(self):
        if _debug: _debug('LED::on')
        if _realp: st.LED.on(self)
        else: self._widget.configure(bg='yellow')
    def off(self):
        if _debug: _debug('LED::off')
        if _realp: st.LED.off(self)
        else: self._widget.configure(bg='white')

class ServomotorWrap(PartWrap,st.Servomotor):
    _frame_type = 'servo'
    def setAngle(self, angle):
        if _debug: _debug('ServoMotor::setAngle',angle=angle)
        if _realp: st.Servomotor.setAngle(self,angle)
        else:
            self._widget.configure(state='active', bg='yellow')
            self._widget.set(angle)
            self._widget.configure(state='disabled', bg='white')

    @staticmethod
    def syncMove(self, servos, angles, delay):
        if _debug: _debug('ServoMotor::syncMove', servos=servos, angles=angles, delay=delay)
        if _realp: st.Servomotor.syncMove(servos, angles, delay)
        else:
            for (servo,angle) in zip(servos,angles):
                servo.setAngle(angle)

class SensorWrap():
    def getValue(self):
        if _debug: _debug(f'{self.name}::getValue')
        if _realp: return self.getValue()
        else:      return self._widget.get() 

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
    _frame_type = 'accel'

    def getValue(self):
        if _debug: _debug('Accelerometer::getValue')
        if _realp: return self.getValue()
        else:      return (self._x_widget.get(),
                           self._y_widget.get(),
                           self._z_widget.get())
