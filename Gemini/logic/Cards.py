'''
Created on 31 dic 2021

@author: david
'''
from enum import Enum

class Semi(Enum):
    BASTONI = 0
    COPPE = 1
    SPADE = 2
    DENARI = 3
    TRIONFI = 4

class CarteLunghe(Enum):
    CL_I = 1
    CL_II = 2
    CL_III = 3
    CL_IV = 4
    CL_V = 5
    CL_VI = 6
    CL_VII = 7
    CL_VIII = 8
    CL_IX = 9
    CL_X = 10
    CL_FA = 11
    CL_CAV = 12
    CL_REG = 13
    CL_REX = 14

class CarteCorte(Enum):
    CL_A = 1
    CL_2 = 2
    CL_3 = 3
    CL_4 = 4
    CL_5 = 5
    CL_6 = 6
    CL_7 = 7
    CL_8 = 8
    CL_9 = 9
    CL_X = 10