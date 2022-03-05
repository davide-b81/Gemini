#   '''
#  Created on 16 2 2022
#  @author: david
#  '''
from abc import ABCMeta, abstractmethod
from time import monotonic
import random
from main.exception_man import ExceptionMan
from main.globals import echo_message


class Action(metaclass=ABCMeta):
    _status = None
    _fsm = None
    _wait_popup = None
    _wait_delay = None

    ACTSTATUS_DEFAULT = "ACTSTATUS_DEFAULT"
    ACTSTATUS_START = "ACTSTATUS_START"
    ACTSTATUS_END = "ACTSTATUS_END"


    def __init__(self, fsm):
        self._status = self.ACTSTATUS_START
        self._fsm = fsm
        self._wait_popup = False
        self._wait_delay = monotonic()

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

    def get_status(self):
        try:
            return self._status
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def on_carta(self, cid):
        try:
            if not self._wait_popup:
                self.on_carta_click(cid)
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def finished(self):
        try:
            if self._wait_popup or self._wait_delay > monotonic():
                return False
            return self._status == self.ACTSTATUS_END
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def wait_seconds(self, s, onlysim=False):
        try:
            if not onlysim or self.simulated(self.giocatore_turno):
                self._wait_delay = monotonic() + s
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def update(self):
        try:
            if self._wait_delay < monotonic():
                if self._wait_popup:
                    pass
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
            self._fsm.game_man.on_show_popup("", False)
            self._wait_popup = False
            echo_message("Stato: " + str(self._status))
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)

    def show_popup(self, txt, visible=True):
        try:
            echo_message(txt)
            self._fsm.game_man.on_show_popup(txt, visible)
            self._wait_popup = True
        except Exception as e:
            ExceptionMan.manage_exception("", e, True)