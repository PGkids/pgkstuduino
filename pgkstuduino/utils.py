# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from studuino import * #Part,Connector,A0,A1,A2,A3,A4,A5,A6,A7,M1,M2,D2,D4,D7,D8,D9,D10,D11,D12
from .wrapped_classes import *

conn_dic = {'A0':A0, 'A1':A1, 'A2':A2, 'A3':A3,
            'A4':A4, 'A5':A5, 'A6':A0, 'A7':A0,
            'M1':M1, 'M2':M2,
            'D2':D2, 'D4':D4, 'D7':D7, 'D8':D8,
            'D9':D9, 'D10':D10, 'D11':D11, 'D12':D12
            }
            

def ensure_connector(obj):
    if isinstance(obj, Connector):
        return obj
    elif obj in conn_dic:
        return conn_dic[obj]

part_dic = {'DCMotor':PGkDCMotor, 'DC':PGkDCMotor, 'DCモーター':PGkDCMotor, 'モーター':PGkDCMotor,
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
        return part_dic[x]
    elif issubclass(x, Part):
        return x
    
        
    
# コネクタ
def conn(ident):
    ident = ident.upper()
    if ident == 'A':
        return (A0,A1,A2,A3,A4,A5,A6,A7)
    elif ident == 'D':
        return (D2,D4,D7,D8,D9,D10,D11,D12)
    elif ident == 'M':
        return (M1,M2)
    elif ident in conn_dic:
        return conn_dic[ident]
    else:
        raise(NameError)


note_dic = {'C':0,
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
    return 12 + 12*note_dic[ident]

