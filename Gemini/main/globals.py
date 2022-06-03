'''
Created on 23 gen 2022

@author: david
'''
import json
import threading, queue
import warnings

from oggetti.posizioni import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DEG_SIDE_FRONT = 0
DEG_SIDE_BACK = 180

DEG_NORMAL = 0
DEG_CLOC_RECT = 90
DEG_ANTC_RECT = -90
DEG_FLIP = 180

LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3
SCROLL_UP = 4
SCROLL_DOWN = 5

FRONTE_COPERTA = True
FRONTE_SCOPERTA = False

def echo_message(txt):
    print(txt)

def check_locals(dic):
    for key, value in dic.items():
        if value is None:
            raise Exception("Argument " + key + " = None")

# Singleton decorator
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Globals(object):
    _evt_queue = None
    _delegate_show_popup = None
    _posizioni = None
    _debug = None
    _carte_tutte = None

    def __init__(self):
        self._evt_queue = queue.Queue()

    def get_carta(self, id):
        for c in self._carte_tutte:
            if c.get_id() == id:
                return c
        return None

    def get_carte(self):
        return self._carte_tutte

    def set_carte(self, ca):
        self._carte_tutte =  ca

    def set_debug(self, dbg):
        self._debug = dbg

    def get_debug(self):
        return True

    def get_autostart(self):
        return False

    def get_verbose(self):
        return False

    def get_quick(self):
        return False

    def get_autoclose(self):
        return True

    def get_demo_mode(self):
        return False

    def controlla_ultima(self):
        return False

    def get_instant_flip(self):
        return False

    def get_instant_pos(self):
        return False

    def get_instant_rot(self):
        return True

    def get_instant(self):
        return True

    def get_uncover(self):
        return False

    def get_force_mazziere(self):
        return False

    def get_fullscreen(self):
        return True

    def init_positions(self, screen):
        self._posizioni = Posizioni(screen)
        return self._posizioni

    def get_positions(self):
        return self._posizioni

    def set_delegate_show_popup(self, f):
        self._delegate_show_popup = f

    def show_popup(self, txt, visible=True):
        assert self._delegate_show_popup is not None
        self._delegate_show_popup(txt, visible)

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            raise TypeError(f'Il tipo {obj.__class__.__name__} non ha il metodo reprJSON')