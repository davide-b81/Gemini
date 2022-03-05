'''
Created on 31 dic 2021

@author: david
'''
import sys
from importlib import resources

from pygame import HWSURFACE, DOUBLEBUF, RESIZABLE

from main.globals import *
from main.gestore import Gestore
from grafica.sprite_carta import *
from main.exception_man import ExceptionMan
import pygame_gui
import os

clock = None
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
ui_manager = None

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
    global text_boxes
    global root
    global gestore, ui_manager
    global surface, clock

    try:
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Minchiate Fiorentine')
        screen = pygame.display.set_mode((0, 0), HWSURFACE | DOUBLEBUF | RESIZABLE | pygame.FULLSCREEN)
        surface = pygame.Surface((screen.get_width(), screen.get_height()))
        path = resources.path('style', 'theme.json')
        ui_manager = pygame_gui.UIManager((screen.get_width(), screen.get_height()), path)
        gestore = Gestore(ui_manager, screen, debug)

        pygame.display.init()
        pygame.display.update()
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
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def on_run():
    global running
    global gestore
    global surface

    try:
        if running:
            check_events()

            running = gestore.on_update(surface)

            pygame.display.update()

    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

    return running

def display_name(pos):
    global gioco_man
    try:
        posm = gioco_man.get_position_manager()
        player = gioco_man.get_player_at_pos(pos)

        if gioco_man.game is not None:
            game = gioco_man.game
            if game is not None:
                t = game._player
                if t is not None:
                    if t.position == pos:
                        text = font.render(player.get_label(), True, RED)
                    else:
                        if t._caduto:
                            text = font.render(player.get_label(), 1, WHITE)
                        else:
                            text = font.render(player.get_label(), 1, BLACK)

                    text_rect = text.get_rect()
                    px = posm.get_etichetta_pos(pos)[0]
                    py = posm.get_etichetta_pos(pos)[1]

                    if (pos == "Est"):
                        px = px - text_rect.width
                    elif (pos == "Sud"):
                        px = px - text_rect.width / 2
                        py = py - text_rect.height
                    elif (pos == "Nord"):
                        px = px - text_rect.width / 2
                    elif (pos == "Ovest"):
                        py = py - text_rect.height
                    screen.blit(text, (px, py))
                else:
                    text = font.render(player.get_label(), 1, BLACK)
    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

def check_events():
    """ Update events manager """
    global slider
    global screen
    global running
    global gestore
    global ui_manager

    try:
        assert gestore != None

        for evt in pygame.event.get():

            gestore.event_handler(evt)

            # if user clicks the close X
            if evt.type == pygame.QUIT:
                running = False
                gestore.on_exit(evt)
                pygame.quit()
            if evt.type == pygame_gui.UI_BUTTON_PRESSED:
                pass
            if evt.type == pygame.MOUSEBUTTONUP:
                pass
            if evt.type == pygame.MOUSEMOTION:
                pass
            if evt.type == pygame.KEYDOWN:
                pass
            if evt.type == pygame.VIDEORESIZE:
                #echo_message("Resize")
                pygame.display.flip()

            # Consume event
            ui_manager.process_events(evt)

        if running:
            gestore.on_update(screen)

    except Exception as e:
        ExceptionMan.manage_exception("", e, True)

if __name__ == '__main__':
    """ Main program cycle """
    running = True

    try:
        on_init(False)

        while running == True:
            running = on_run()
    except Exception as e:
        echo_message(e.args[0])
        sys.exit(-1)
    sys.exit(0)