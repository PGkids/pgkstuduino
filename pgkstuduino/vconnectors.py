# -*- coding: utf-8 -*-

# 仮想コネクタ
class PGkVirtualConnector():
    __slots__ = ['id']
    def __init__(self, id):
        self.id = id

def is_virtual_connector(obj):
    return isinstance(obj, PGkVirtualConnector)

A0v,A1v,A2v,A3v,A4v,A5v,A6v,A7v = tuple(map(PGkVirtualConnector,
                                           ['A0*','A1*','A2*','A3*','A4*','A5*','A6*','A7*']))
D2v,D4v,D7v,D8v,D9v,D10v,D11v,D12v = tuple(map(PGkVirtualConnector,
                                               ['D2*','D4*','D7*','D8*','D9*','D10*','D11*','D12*']))
M1v,M2v = tuple(map(PGkVirtualConnector,['M1*','M2*']))

