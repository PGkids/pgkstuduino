# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import os
import studuino as st
import tkinter as tk
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
        self.quit_btn.configure(text='EXIT NORMALLY',
                                bg='white', fg='green', command=self.quit_normally)
    def create_widgets(self):
        self.quit_btn = tk.Button(self, text='ABORT this process immediately',
                              bg='blue', fg='white', command=self.abort)
        self.quit_btn.pack(pady=8,padx=16,fill=tk.X)
        copyright = tk.Label(self, padx=10, fg='darkgreen',
                             text='STUDUINO SIMULATOR / REALTIME MONITOR\npgkstuduino. Copyright (c) 2019 PGkids Laboratory')
        copyright.pack(side=tk.TOP)
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP)
        self.led_frame = tk.LabelFrame(frame, text='LEDs')
        self.led_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.buzzer_frame = tk.LabelFrame(frame, text='Buzzers')
        self.buzzer_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.dc_frame = tk.LabelFrame(frame, text='DC Motors')
        self.dc_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.servo_frame = tk.LabelFrame(frame, text='Servomotors')
        self.servo_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.digital_frame = tk.LabelFrame(frame, text='Digital Sensors')
        self.digital_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.analog_frame = tk.LabelFrame(frame, text='Analog Sensors')
        self.analog_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)
        self.accel_frame = tk.LabelFrame(frame, text='Accelerometers')
        self.accel_frame.pack(side=tk.LEFT,anchor=tk.N,padx=8)

    def create_label(self,text):
        w = tk.Label(self, bg='white', padx=8, text=text)
        w.pack(side=tk.TOP);
        def set(text):
            w.configure(text=text)
        return set
    def create_button(self,text, command=None):
        if command is None:
            command = lambda:print(text,'PRESSED!')
        w = tk.Button(self,text=text, bg='white', padx=8, command=command)
        w.pack(side=tk.TOP)
        def set(text):
            w.configure(text=text)
        return set
    
                        
_debug = None
_realp = True
_simulator = None

def st_set_debug(enable=True):
    global _debug
    if enable:
        def debugPrint(name,**arg_pairs):
            print(f'DEBUG: {name}(',end='')
            for k in arg_pairs:
                print(f'{k}={arg_pairs[k]},',end='')
            print(')')
        _debug = debugPrint
    else:
        _debug = None

def st_set_real(enable=True):
    global _realp
    _realp = enable
    ev = Event()
    def gui():
        root = tk.Tk()
        #root.geometry('600x400')
        root.title('STUDUINO SIMULATOR / REALTIME MONITOR')
        sim = Simulator(root)
        global _simulator
        _simulator = sim
        #_simulator = sim
        ev.set()
        _simulator.mainloop()
    thr = Thread(target=gui)
    thr.start()
    ev.wait()

def _check_simulator():
    if not _simulator:
        raise Exception('Simulator not initialized')

def create_label(text='user label'):
    _check_simulator()
    return _simulator.create_label(text)

def create_button(text='user button', command=None):
    _check_simulator()
    return _simulator.create_button(text,command=command)


    
def st_start(com_port:str):
    if _debug: _debug('st_start', com_port=com_port, baud_rate=baud_rate)
    if _realp: st.start(com_port)

def st_stop():
    if _debug: _debug('st_stop')
    if _realp: st.stop()
    _simulator.toggle_quit_button_operation()

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
        if _realp: st.Part.attach(self,connector)
        if _simulator:
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
    def __init__(self):
        super().__init__()
        if _realp: st.Buzzer.__init__(self)
        
    def off(self):
        if _debug: _debug('Buzzer::off')
        self._widget.configure(bg='white')
        if _realp: st.Buzzer.off(self)
    def on(self, sound, octave=0, duration=0):
        if _debug: _debug('Buzzer::on',sound=sound, octave=octave, duration=duration)
        self._widget.configure(bg='yellow', state='active')
        self._widget.set(octave*12+sound)
        self._widget.configure(state='disabled')
        if _realp: st.Buzzer.on(self, sound, octave=octave, duration=duration)
    

class DCMotorWrap(PartWrap,st.DCMotor):
    _frame_type = 'dc'
    def __init__(self):
        super().__init__()
        if _realp: st.DCMotor.__init__(self)

    def move(self, motion):
        if _debug: _debug('DCMotor::move',motion=motion)
        self._widget.configure(bg='yellow' if motion == st.FWD else 'lightblue')
        if _realp: st.DCMotor.move(self, motion)
    def stop(self, motion):
        if _debug: _debug('DCMotor::stop',motion=motion)
        self._widget.configure(bg='white')
        if _realp: st.DCMotor.stop(self, motion)
    def setPower(self, power):
        if _debug: _debug('DCMotor::setPower',power=power)
        self._widget.configure(state='active')
        self._widget.set(power)
        self._widget.configure(state='disabled')
        if _realp: st.DCMotor.setPower(self, power)

class LEDWrap(PartWrap,st.LED):
    _frame_type = 'led'
    def __init__(self):
        super().__init__()
        if _realp: st.LED.__init__(self)

    def on(self):
        if _debug: _debug('LED::on')
        self._widget.configure(bg='yellow')
        if _realp: st.LED.on(self)
    def off(self):
        if _debug: _debug('LED::off')
        self._widget.configure(bg='white')
        if _realp: st.LED.off(self)

class ServomotorWrap(PartWrap,st.Servomotor):
    _frame_type = 'servo'
    def __init__(self):
        super().__init__()
        if _realp: st.Servomotor.__init__(self)

    def _set_angle_for_simulator(self, angle):
        self._widget.configure(state='active', bg='yellow')
        self._widget.set(angle)
        self._widget.configure(state='disabled', bg='white')
        
    def setAngle(self, angle):
        if _debug: _debug('ServoMotor::setAngle',angle=angle)
        _set_angle_for_simulator(angle)
        if _realp: st.Servomotor.setAngle(self,angle)

    @staticmethod
    def syncMove(self, servos, angles, delay):
        if _debug: _debug('ServoMotor::syncMove', servos=servos, angles=angles, delay=delay)
        for (servo,angle) in zip(servos,angles):
            servo._set_angle_for_simulator(angle)
        if _realp: st.Servomotor.syncMove(servos, angles, delay)

class SensorWrap():
    def getValue(self):
        if _debug: _debug(f'{self.name}::getValue')
        if _realp:
            #print(st.Sensor.getValue(self))
            return st.Sensor.getValue(self)
        else:      return self._widget.get() 

class PushSwitchWrap(PartWrap,SensorWrap,st.PushSwitch):
    _frame_type = 'digital'
    def __init__(self):
        super().__init__()
        if _realp: st.PushSwitch.__init__(self)


class TouchSensorWrap(PartWrap,SensorWrap,st.TouchSensor):
    _frame_type = 'digital'
    def __init__(self):
        super().__init__()
        if _realp: st.TouchSensor.__init__(self)


class IRPhotoreflectorWrap(PartWrap,SensorWrap,st.IRPhotoreflector):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__()
        if _realp: st.IRPhotoreflector.__init__(self)



class LightSensorWrap(PartWrap,SensorWrap,st.LightSensor):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__()
        if _realp: st.LightSensor.__init__(self)

class SoundSensorWrap(PartWrap,SensorWrap,st.SoundSensor):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__()
        if _realp: st.SoundSensor.__init__(self)
        
class AccelerometerWrap(PartWrap,st.Accelerometer):
    _frame_type = 'accel'
    def __init__(self):
        super().__init__()
        if _realp: st.Accelerometer.__init__(self)

    def getValue(self):
        if _debug: _debug('Accelerometer::getValue')
        if _realp: return st.Accelerometer.getValue(self)
        else:      return (self._x_widget.get(),
                           self._y_widget.get(),
                           self._z_widget.get())
