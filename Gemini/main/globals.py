'''
Created on 23 gen 2022

@author: david
'''
import threading, queue
import warnings

from oggetti.posizioni import Posizioni

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DEG_SIDE_FRONT = 180
DEG_SIDE_BACK = 0

DEG_NORMAL = 0
DEG_CLOC_RECT = 90
DEG_ANTC_RECT = -90
DEG_FLIP = 180

POSTAZIONE_NORD = "Nord"
POSTAZIONE_OVEST = "Ovest"
POSTAZIONE_EST = "Est"
POSTAZIONE_SUD = "Sud"

LEFT_CLICK = 1
MIDDLE_CLICK = 2
RIGHT_CLICK = 3
SCROLL_UP= 4
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

    def __init__(self):
        self._evt_queue = queue.Queue()

    def set_debug(self, dbg):
        self._debug = dbg

    def get_debug(self):
        return self._debug

    def get_quick(self):
        return False

    def get_autoclose(self):
        return True

    def get_demo_mode(self):
        return True

    def controlla_ultima(self):
        return False

    def get_instant(self):
        return True

    def get_uncover(self):
        return False

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
