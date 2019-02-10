# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import * #Part,Connector,A0,A1,A2,A3,A4,A5,A6,A7,M1,M2,D2,D4,D7,D8,D9,D10,D11,D12
from .vconnectors import *
from .wrapped_classes import *

_conn_dic = {'A0':A0, 'A1':A1, 'A2':A2, 'A3':A3,
             'A4':A4, 'A5':A5, 'A6':A6, 'A7':A7,
             'M1':M1, 'M2':M2,
             'D2':D2, 'D4':D4, 'D7':D7, 'D8':D8,
             'D9':D9, 'D10':D10, 'D11':D11, 'D12':D12,
             # virtual connectors
             'A0*':A0v, 'A1*':A1v, 'A2*':A2v, 'A3*':A3v,
             'A4*':A4v, 'A5*':A5v, 'A6*':A6v, 'A7*':A7v,
             'M1*':M1v, 'M2*':M2v,
             'D2*':D2v, 'D4*':D4v, 'D7*':D7v, 'D8*':D8v,
             'D9*':D9v, 'D10*':D10v, 'D11*':D11v, 'D12*':D12v}

def ensure_connector(obj):
    if isinstance(obj, Connector) or isinstance(obj, PGkVirtualConnector):
        return obj
    elif obj in _conn_dic:
        return _conn_dic[obj]

    
_part_dic = {'DCMotor':PGkDCMotor, 'DC':PGkDCMotor, 'DCモーター':PGkDCMotor, 'モーター':PGkDCMotor,
             '車輪':PGkDCMotor,
             'Servomotor':PGkServomotor, 'Servo':PGkServomotor, 'サーボモーター':PGkServomotor,
             'サーボ':PGkServomotor,
             'LED':PGkLED, '発光ダイオード':PGkLED,
             'Buzzer':PGkBuzzer, 'ブザー':PGkBuzzer,
             'PushSwitch':PGkPushSwitch, 'スイッチ':PGkPushSwitch, 'ボタン':PGkPushSwitch,
             'TouchSensor':PGkTouchSensor, 'タッチセンサー':PGkTouchSensor,
             'Accelerometer':PGkAccelerometer, '加速度センサー':PGkAccelerometer,
             'IRPhotoreflector':PGkIRPhotoreflector, 'フォトリフレクター':PGkIRPhotoreflector,
             'LightSensor':PGkLightSensor, '光センサー':PGkLightSensor,
             'SoundSensor':PGkSoundSensor, '音センサー':PGkSoundSensor
             }

def ensure_part(x):
    if isinstance(x, str):
        return _part_dic[x]
    elif issubclass(x, Part):
        return x
    else:
        raise(ValueError)            
    
# コネクタ
def conn(ident):
    ident = ident.upper()
    if ident in _conn_dic:
        return _conn_dic[ident]
    else:
        raise(NameError)


_note_dic = {'C':0,
            'C+':1, 'D-':1,
            'D':2,
            'D+':3,'E-':3,
            'E':4, 'F-':4,
            'F':5, 'E+':5,
            'F+':6, 'G-':6,
            'G':7,
            'G+':8, 'A-':8,
            'A':9,
            'A+':10,'B-':10,
            'B':11,'C-':11}

# note('C')==60, note('C',3)=48
# MIDI互換
def note(ident, octave=4):
    return 12 + 12*_note_dic[ident]

