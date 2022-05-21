'''
Created on 31 dic 2021

@author: david
'''
import sys

from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE

from main.globals import *
from main.gestore import *
from grafica.sprite_carta import *
from main.exception_man import ExceptionMan
import os

text_pos = None
running = False
title = None
text = None
desk_area = None
desk_pos = None
mano_area = None
screen = None
carta_man = None
font = None
gioco_man = None
slider = None
root = None
gestore = None
surface = None
_globals = Globals()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

def set_positions():
    global titolo_pos, text_pos
    titolo_pos = title.get_rect(centerx=screen.get_width() / 2)
    text_pos = text.get_rect(centerx=50, centery=screen.get_height() - 50)

def slider_consumer(index):
    echo_message('Current index : %s' % index)

def on_init(debug):
    global title, text
    global font
    global screen
    global running
    global _globals
    global root
    global gestore
    global surface

    try:
        pygame.init()
        pygame.display.set_caption('Minchiate Fiorentine')
        if _globals.get_fullscreen():
            screen = pygame.display.set_mode((0, 0), HWSURFACE | DOUBLEBUF | RESIZABLE | pygame.FULLSCREEN)
        else:
            (width, height) = (1920, 1050)
            screen = pygame.display.set_mode((width, height))

        surface = pygame.Surface((screen.get_width(), screen.get_height()))
        gestore = Gestore(screen, debug)
        gestore.set_delegate_exit(on_exit)
        gestore.set_delegate_run(on_run)
        running = True
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)
    
def box_draw():
    global text_boxes
    try:
        for box in text_boxes:
            box.on_draw(screen)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def on_exit():
    try:
        global running
        running = False
        print("Quit application")
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def on_run():
    global running
    try:
        print("Start game")
        running = True
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def on_exec():
    global running
    global gestore
    global surface

    try:
        check_events()

        if gestore != None:
            gestore.on_update()

            gestore.on_update_ui()

        pygame.display.update()

    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

    return running

def check_events():
    """ Update events manager """
    global slider
    global screen
    global running
    global gestore

    try:
        for evt in pygame.event.get():

            if evt.type == pygame.QUIT:
                on_exit()

            if gestore != None:
                gestore.event_handler(evt)

                # Consume event
                gestore.process_events(evt)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

if __name__ == '__main__':
    """ Main program cycle """
    running = True

    try:
        on_init(False)

        while running == True:
            running = on_exec()
    except Exception as e:
        echo_message(e.args[0])
        sys.exit(-1)
    sys.exit(0)