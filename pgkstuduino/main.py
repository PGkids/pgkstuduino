# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import studuino
from .primitives import *
from .utils import ensure_part,ensure_connector

def connect(comPort):
    if isinstance(comPort, str):
        st_start(comPort)
    else:
        st_start(f'COM{comPort}')

def disconnect(close_panel=False):
    st_stop(close_panel)

def build(p):
    ctor = p[0]
    conn = p[1]
    part = ctor()
    if conn: part.attach(conn)
    return part

def mkpart(format):
    result = []
    for x in format.replace(' ','').split(','):
        if ':' not in x:
            ctor = ensure_part(x)
            result.append((ctor,None))
        elif x.count(':') == 1:
            [part_name, conn_fmt] = x.split(':')
            ctor = ensure_part(part_name)
            for c in conn_fmt.split('/'):
                conn = ensure_connector(c)
                result.append((ctor,conn))
        else:
            raise(ValueError)
    if len(result) == 1:
        return build(result[0])
    else:
        return tuple(map(build,result))

#mkpart('DCMotor/A0/A1/A2,DC/M1/M2')
#
#a,b,c = mkpart('DCMotor:A0/A1/A2,DC:M1/M2')


            
    
    
