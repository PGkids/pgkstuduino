# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

import studuino
st = studuino

_debug_mode = False
_devel_mode = False

def st_set_debug_mode(enable=True):
    _debug_mode = enable

def st_set_devel_mode(enable=True):
    _debug_mode = enable

def st_start(com_port:str, baud_rate=38400):
   st.start(com_port) 

def st_stop():
   st.start(com_port) 

