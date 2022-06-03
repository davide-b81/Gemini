#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from abc import ABCMeta, abstractmethod
from threading import Timer
from time import monotonic
import random

import pygame

from main.globals import echo_message, Globals
from main.exception_man import ExceptionMan


class Action(metaclass=ABCMeta):
    _id_action = None
    _status = None
    _newsts = None
    _fsm = None
    _popup_box = None
    _tout_popup = None
    _wait_popup = None
    _wait_delay = None
    _popup_hover = None
    _t_action = None

    ACTSTATUS_DEFAULT = "ACTSTATUS_DEFAULT"
    ACTSTATUS_START = "ACTSTATUS_START"
    ACTSTATUS_END = "ACTSTATUS_END"


    def __init__(self, fsm):
        assert fsm is not None
        self._id_action = str(self)
        self._status = self.ACTSTATUS_START
        self._newsts = self.ACTSTATUS_START
        self._fsm = fsm
        self._wait_popup = False
        self._popup_hover = False
        self._wait_delay = monotonic()
        self._globals = Globals()

    def __str__(self):
        return type(self).__name__

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def update_sub(self):
        pass

    @abstractmethod
    def on_carta_click(self, cid):
        pass

    def termina(self):
        try:
            self.end()
            if self._tout_popup is not None:
                self._tout_popup.cancel()
                self._tout_popup = None
            if self._wait_popup is not None:
                self._fsm.on_hide_popup()
                self._popup_box = None
                self._wait_popup = False
            self.reset()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_status(self):
        try:
            return self._status
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def get_new_status(self):
        try:
            return self._newsts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_status(self, sts):
        try:
            self._status = sts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def set_new_status(self, sts):
        try:
            self._newsts = sts
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta(self, cid):
        try:
            if not self._wait_popup:
                self.on_carta_click(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def reset(self):
        try:
            print("Reset action " + str(self))
            self._status = self.ACTSTATUS_START
            self._newsts = self.ACTSTATUS_START
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def finished(self):
        try:
            if self._wait_popup or self._wait_delay > monotonic():
                return False
            return self._status == self.ACTSTATUS_END or self._newsts == self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def wait_seconds(self, s, onlysim=False):
        try:
            if self._globals.get_quick():
                s = 0.1
            if not onlysim or self.simulated():
                self._wait_delay = monotonic() + s
                echo_message("Attende " + str(s) + " secondi")
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self):
        try:
            if self._wait_delay < monotonic():
                if self._wait_popup:
                    pass
                elif self._newsts != self._status:
                    if self._newsts is not None:
                        self._status = self._newsts
                        echo_message("Action status: " + self._status)
                    else:
                        self._newsts = self._status
                elif self._status == self.ACTSTATUS_DEFAULT:
                    pass
                elif self._status == self.ACTSTATUS_START:
                    self.start()
                elif self._status == self.ACTSTATUS_END:
                    pass
                else:
                    self.update_sub()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_popup(self):
        try:
            if self._tout_popup is not None:
                self._tout_popup.cancel()
                self._tout_popup = None
            if self._wait_popup:
                self._fsm.on_hide_popup()
                self._popup_box.kill()
                self._popup_box = None
                self._wait_popup = False
                echo_message("Restore status: " + str(self._status))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_timed_popup(self, txt, tout=3):
        try:
            if self._globals.get_quick():
                tout=0.05
            self.show_popup(txt)
            if self._globals.get_autoclose():
                # Autoclose popup
                if tout is not None:
                    self._tout_popup = Timer(tout, self.on_popup)
                    self._tout_popup.start()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_popup(self, txt):
        try:
            echo_message(txt)
            self._popup_box = self._fsm.on_show_popup(txt)
            self._wait_popup = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_event(self, evt):
        try:
            if self._wait_popup and self._popup_box is not None:
                if evt.type == pygame.MOUSEMOTION:
                    self._popup_hover = self._popup_box.rect.collidepoint(pygame.mouse.get_pos())

                if evt.type == pygame.MOUSEBUTTONUP:
                    if self._popup_hover is not None:
                        self.on_popup()
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def __dict__(self):
        return dict(
            _id_action=self._id_action,
            _status=self._status,
            _newsts=self._newsts)

    @abstractmethod
    def reprJSON(self):
        return dict(
            _id_action=self._id_action,
            _status=self._status,
            _newsts=self._newsts)

    @abstractmethod
    def fromJSON(self, json_object):
        pass