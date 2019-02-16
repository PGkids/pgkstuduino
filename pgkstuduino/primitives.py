# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import os
import studuino as st
import tkinter as tk
from threading import Thread,Event
from .vconnectors import *

_reversed_conn_dic = {st.A0:'A0', st.A1:'A1', st.A2:'A2', st.A3:'A3',
                      st.A4:'A4', st.A5:'A5', st.A6:'A6', st.A7:'A7',
                      st.M1:'M1', st.M2:'M2',
                      st.D2:'D2', st.D4:'D4', st.D7:'D7', st.D8:'D8',
                      st.D9:'D9', st.D10:'D10', st.D11:'D11', st.D12:'D12'}
                      
def get_connector_name(conn):
    if conn in _reversed_conn_dic:
        return _reversed_conn_dic[conn]
    elif isinstance(conn, PGkVirtualConnector):
        return conn.id
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

    def close_request(self):
        self.after(1, self.quit_normally)
    
    def create_widgets(self):
        self.quit_btn = tk.Button(self, text='ABORT this process immediately',
                              bg='blue', fg='white', command=self.abort)
        self.quit_btn.pack(pady=8,padx=16,fill=tk.X)
        copyright = tk.Label(self, padx=10, fg='darkgreen',
                             text='STUDUINO SIMULATOR / REALTIME MONITOR / DEVELOPMENT ENVIRONMENT\n'
                             'pgkstuduino. Copyright (c) 2019 PGkids Laboratory')
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

def _check_simulator():
    if not _simulator:
        raise Exception('Simulator not initialized')

def create_label(text='user label'):
    _check_simulator()
    return _simulator.create_label(text)

def create_button(text='user button', command=None):
    _check_simulator()
    return _simulator.create_button(text,command=command)

def _initialize_gui_panel():
    ev = Event()
    def gui():
        root = tk.Tk()
        #root.geometry('600x400')
        root.title('pgkstuduino panel')
        sim = Simulator(root)
        global _simulator
        _simulator = sim
        #_simulator = sim
        ev.set()
        _simulator.mainloop()
    thr = Thread(target=gui)
    thr.start()
    ev.wait()
    
def st_start(com_port:str):
    _initialize_gui_panel()
    if _debug: _debug('st_start', com_port=com_port)
    if _realp: st.start(com_port)

def st_stop(close_panel=False):
    if _debug: _debug('st_stop')
    if _realp: st.stop()
    if close_panel: _simulator.close_request()
    else:           _simulator.toggle_quit_button_operation()

class PartWrap():
    _widget = None
    _part   = None
    _connector = None
    __not_virtual = None
    def __init__(self, real_part_class, name):
        self.name = name
        if _realp: self._part = real_part_class()
        if _simulator:
            w = None
            t = self._frame_type
            if t is 'led':
                self._widget = tk.Label(_simulator.led_frame, text=name, bg='white')
                self._widget.pack()
            elif t is 'buzzer':
                self._widget = tk.Scale(_simulator.buzzer_frame, label=name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=128)
                self._widget.pack()                
            elif self._frame_type is 'dc':
                self._widget = tk.Scale(_simulator.dc_frame, label=name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=100)
                self._widget.pack()
            elif self._frame_type is 'servo':
                self._widget = tk.Scale(_simulator.servo_frame, label=name,orient='h',
                                        bg='white', width='4', sliderlength='4', from_=0,to=180)
                self._widget.pack()
            elif self._frame_type is 'digital':
                self._widget = tk.Scale(_simulator.digital_frame, label=name,orient='h',from_=0,to=1)
                self._widget.set(1)
                self._widget.pack()
            elif self._frame_type is 'analog':
                self._widget = tk.Scale(_simulator.analog_frame, label=name,orient='h',from_=0,to=100)
                self._widget.set(100)
                self._widget.pack()
            elif self._frame_type is 'accel':
                self._widget = tk.Label(_simulator.accel_frame, text=name)
                self._widget.pack()
                self._x_widget = tk.Scale(_simulator.accel_frame, label='X',orient='h',from_=0,to=100)
                self._x_widget.pack()
                self._y_widget = tk.Scale(_simulator.accel_frame, label='Y',orient='h',from_=0,to=100)
                self._y_widget.pack()                
                self._z_widget = tk.Scale(_simulator.accel_frame, label='Z',orient='h',from_=0,to=100)
                self._z_widget.pack()                
            else: raise(RuntimeError)

    def _configure_after_attach(self):
        pass

    def is_real(self):
        return _realp and self.__not_virtual
    
    def attach(self,connector):
        self._connector = connector
        self.__not_virtual = not is_virtual_connector(connector)
        if _debug: _debug(f'{self.name}::attach',connector=connector)
        if self.is_real(): self._part.attach(connector)
        self._configure_after_attach()
        if _simulator:
            t = self._frame_type
            device_name = self.name+'@'+str(get_connector_name(connector))
            if t is 'led' or t is 'accel':
                self._widget.configure(text=device_name)
            elif t is 'digital' or t is 'analog':
                self._widget.configure(label=device_name)
            else:
                self._widget.configure(label=device_name, state='disabled')

class BuzzerWrap(PartWrap):
    _frame_type = 'buzzer'
    def __init__(self):
        super().__init__(st.Buzzer,'Buzzer')
        
    def off(self):
        if _debug: _debug('Buzzer::off')
        self._widget.configure(bg='white')
        if self.is_real(): self._part.off()
    def on(self, sound, octave=0, duration=0):
        if _debug: _debug('Buzzer::on',sound=sound, octave=octave, duration=duration)
        self._widget.configure(bg='yellow', state='active')
        self._widget.set(octave*12+sound)
        self._widget.configure(state='disabled')
        if self.is_real(): self._part.on(sound, octave=octave, duration=duration)
    

_DC_FWDS = ('fwd', 'forward', st.FWD, '前進', '前転')
_DC_BACKS = ('bck', 'back', st.BCK, '後進', '後転')
_DC_BRAKES = ('brk', 'brake','stop', st.BRAKE, None, '停止')
_DC_COASTS = ('coast', st.COAST, '惰性')

class DCMotorWrap(PartWrap):
    _frame_type = 'dc'
    __state = _DC_BRAKES
    
    def __init__(self):
        super().__init__(st.DCMotor,'DC Motor')
        self.__cur_power = 0

    def _configure_after_attach(self):
        if self.is_real(): self._part.setPower(self.__cur_power)

    def move(self, motion):
        if _debug: _debug('DCMotor::move',motion=motion)
        self._widget.configure(bg='yellow' if motion == st.FWD else 'lightblue')
        if self.is_real(): self._part.move(motion)

    def _stop(self, motion):
        if _debug: _debug('DCMotor::stop',motion=motion)
        self._widget.configure(bg='white')
        if self.is_real(): self._part.stop(motion)

    def set_power(self, power):
        if _debug: _debug('DCMotor::setPower',power=power)
        self._widget.configure(state='active')
        self._widget.set(power)
        self._widget.configure(state='disabled')
        if self.is_real(): self._part.setPower(power)

    def get_power(self):
        return __cur_power

    power = property(get_power, set_power)

    def __get_state(self):
        return self.__state
    def __set_state(self, x):
        if x in _DC_FWDS:
            self.move(st.FWD)
            self.__state = _DC_FWDS
        elif x in _DC_BACKS:  
            self.move(st.BCK)
            self.__state = _DC_BACKS
        elif x in _DC_BRAKES:
            self._stop(st.BRAKE)
            self.__state = _DC_BRAKES
        elif x in _DC_COASTS:
            self._stop(st.COAST)
            self.__state = _DC_COASTS
        else: raise(Exception(f'DC Motor: state: invalid state {x}'))
    state = property(__get_state, __set_state)
            

    
class LEDWrap(PartWrap):
    _frame_type = 'led'
    __state = False
    def __init__(self):
        super().__init__(st.LED,'LED')

    def on(self):
        if _debug: _debug('LED::on')
        self._widget.configure(bg='yellow')
        if self.is_real(): self._part.on()
        self.__state = True
    def off(self):
        if _debug: _debug('LED::off')
        self._widget.configure(bg='white')
        if self.is_real(): self._part.off()
        self.__state = False

    def __get_state(self):
        return self.__state
    def __set_state(self, x):
        if x: self.on()
        else: self.off()
        
    state = property(__get_state, __set_state)

class ServomotorWrap(PartWrap):
    _frame_type = 'servo'
    __angle = None
    def __init__(self):
        super().__init__(st.Servomotor,'Servo')

    # このメソッドは実機か非実機によらず必ず呼ばれるため、ここでangleを保存させる
    def _set_angle_for_simulator(self, angle):
        self.__angle = angle
        self._widget.configure(state='active', bg='yellow')
        self._widget.set(angle)
        self._widget.configure(state='disabled', bg='white')
        
    def set_angle(self, angle):
        if _debug: _debug('ServoMotor::setAngle',angle=angle)
        self._set_angle_for_simulator(angle)
        if self.is_real(): self._part.setAngle(angle)

    def setAngle(self, angle):
        self.set_angle(angle)
        
    @staticmethod
    def sync_move(servos, angles, delay):
        if _debug: _debug('ServoMotor::syncMove', servos=servos, angles=angles, delay=delay)
        for (servo,angle) in zip(servos,angles):
            servo._set_angle_for_simulator(angle)
        if _realp:
            real_servos,real_angles = [],[]
            for pair in zip(servos,angles):
                if pair[0].is_real():
                    real_servos.append(pair[0])
                    real_angles.append(pair[1])
            #real_servos = list(map(lambda s:s._part, servos))
            Servomotor.syncMove(real_servos, real_angles, delay)

    @staticmethod
    def syncMove(servos, angles, delay):
        self.sync_move(servos, angles, delay)
    
    def __get_angle(self):
        return self.__angle
    def __set_angle(self, angle):
        self.set_angle(angle)
        
    angle = property(__get_angle, __set_angle)

class SensorWrap():
    def getValue(self):
        if _debug: _debug(f'{self.name}::getValue')
        if self.is_real():
            #print(st.Sensor.getValue(self))
            val = self._part.getValue()
            self._widget.set(val)
            return val
        else:      return self._widget.get()

    def get_value(self):
        return self.getValue()
    
    state = property(getValue)

class PushSwitchWrap(PartWrap,SensorWrap):
    _frame_type = 'digital'
    def __init__(self):
        super().__init__(st.PushSwitch,'Push Switch')

class TouchSensorWrap(PartWrap,SensorWrap):
    _frame_type = 'digital'
    def __init__(self):
        super().__init__(st.TouchSensor, 'Touch Sensor')

class IRPhotoreflectorWrap(PartWrap,SensorWrap):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__(st.IRPhotoreflector, 'Photoreflector')

class LightSensorWrap(PartWrap,SensorWrap):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__(st.LightSensor, 'Light Sensor')

class SoundSensorWrap(PartWrap,SensorWrap):
    _frame_type = 'analog'
    def __init__(self):
        super().__init__(st.SoundSensor, 'Sound Sensor')
        
class AccelerometerWrap(PartWrap):
    _frame_type = 'accel'
    def __init__(self):
        super().__init__(st.Accelerometer, 'Accelerometer')

    def getValue(self):
        if _debug: _debug('Accelerometer::getValue')
        if self.is_real():
            xyz = self._part.getValue()
            self._x_widget.set(xyz[0])
            self._y_widget.set(xyz[1])
            self._z_widget.set(xyz[2])
            return xyz
        else:      return (self._x_widget.get(),
                           self._y_widget.get(),
                           self._z_widget.get())
