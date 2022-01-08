'''
Created on 31 dic 2021

@author: david
'''

import logic.Carta
import Game
import Output
import Game.Germini
import Game.Germini.Gioco
import keyboard

from Game import Germini
from Game.Germini.Gioco import game
from oggetti.stringhe import nomigiocatore
from oggetti import *
import pygame
import pygame.freetype
import time
from pygame.locals import *
from oggetti.button import Button
from images.image_manager import ImageManager
from pickle import NONE

buttons = []

card_size = (200, 400)
desk_size = (0, 0)
desk_pos = (0, 0)

desk_pos_n = (0, 0)
desk_pos_s = (0, 0)
desk_pos_e = (0, 0)
desk_pos_o = (0, 0)

titolo_pos = None
text_pos = None
g = None
running = True
title = None
text = None
desk_area = None
screen = None
img_man = None
carta_man = None
font = None

def set_areas():
    global desk_area, card_size, desk_pos
    global desk_pos_n, desk_pos_s, desk_pos_e, desk_pos_o
    
    desk_area = pygame.Surface((screen.get_width()/1.25, screen.get_height()/1.25))
    desk_pos = ((screen.get_width() / 2) - (desk_area.get_width()/2), (screen.get_height() / 2) - (desk_area.get_height()/2))
    
    #card_size = (desk_area.get_width()/8, desk_area.get_height()/8)
    
    desk_pos_n = (desk_area.get_width()/2 - card_size[0]/2, 0)
    desk_pos_s = (desk_area.get_width()/2 - card_size[0]/2, desk_area.get_height() - card_size[1])
    desk_pos_o = (0, (desk_area.get_height() - card_size[1]) / 2)
    desk_pos_e = (desk_area.get_width() - card_size[0], (desk_area.get_height() - card_size[1]) / 2)
    
    
def set_positions():
    global titolo_pos, text_pos
    titolo_pos = title.get_rect(centerx=screen.get_width()/2)
    text_pos = text.get_rect(centerx=50, centery=screen.get_height()-50)
    
def on_init():
    global title, text
    global desk, font
    global screen
    global img_man
    global carta_man
    
    print("Inizio")
    pygame.init()
    pygame.font.init()    
    
    try:
        # DBG non si riesce a caricare un file ttf locale all'applicazione?
        #font = pygame.font.Font("None", 36)
        font = pygame.font.SysFont('Bodoni', 30)
        title = font.render("Il nobilissimo gioco delle Minchiate Fiorentine", 1, (10, 10, 10))
        text = font.render("...", 1, (10, 10, 10))
        
        img_man = ImageManager()    
        screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)        
        carta_man = logic.Carta.carta
        set_areas()
        set_positions()
        
    except Exception as e:
            print("on_init: An error occurred:", e.args[0])
    
def desk_draw():
    desk_area.fill((0, 148, 135))
    pass
    
def buttons_draw():
    for b in buttons:
        b.draw()

def draw_carta(player, pos):
    try:
        carta = g.CarteCalate(player)
        if carta:
            img = img_man.get_image(carta)
            width = card_size[0]
            height = width*(card_size[1]/width)
    
            img = pygame.transform.scale(img, (width, height))    
            #pygame.draw.rect(desk_area,(0,255,255), (desk_pos_n[0],desk_pos_n[1],card_size[0],card_size[1]))
            desk_area.blit(img, pos)
    
    except Exception as e:
            print("draw_carta: An error occurred:", e.args[0])  

def buttons_events():
    for b in buttons:
        b.check_click()
        
def on_nuovo():
    global g
    g = game(nomigiocatore)
    g.Step_mescola()
    g.FormaCoppie()

def on_termina():
    if (g != None):
        g.Restore()

def on_exit():
    global running
    running = False

def on_update():
    global g, font
    global title, text
    global screen
    global titolo_pos

    try:
        screen.fill((163, 148, 135))
    
        screen.blit(title, titolo_pos)
        screen.blit(text, text_pos)
        
        desk_draw()
        buttons_draw()
        
        if g:
            g.ThreadWorker()
            text = font.render(g.GetTesto(), 1, (10, 10, 10))            
            draw_carta(nomigiocatore[0], desk_pos_n)
            draw_carta(nomigiocatore[1], desk_pos_s)
            draw_carta(nomigiocatore[2], desk_pos_e)
            draw_carta(nomigiocatore[3], desk_pos_o)
        #pygame.draw.rect(desk_area,(0,255,255), desk_pos_n, card_size)
        #pygame.draw.rect(desk_area,(255,0,255), desk_pos_s, card_size)
        #pygame.draw.rect(desk_area,(255,0,255), desk_pos_e, card_size)
        #pygame.draw.rect(desk_area,(255,0,255), desk_pos_o, card_size)

        screen.blit(desk_area, (desk_pos))
        
    except Exception as e:
            print("__main__: An error occurred:", e.args[0])


if __name__ == '__main__':   
    try:
        on_init()
        
        #screen = pygame.display.set_mode((1000, 700))
        screen.fill((163, 148, 135)) #produces a green-color background
        pygame.display.set_caption('Gui Menu')
        clock = pygame.time.Clock()
        gui_font = pygame.font.Font(None,30)
         
        nuovoButton = Button(screen,"Nuovo",200,40,(10,200), on_nuovo)
        buttonEsc = Button(screen,"Termina",200,40,(10,250), on_termina)
        button3 = Button(screen,"XXX",200,40,(10,300), None)
        button3 = Button(screen,"YYY",200,40,(10,350), None)
        closeButton = Button(screen,"Esci",200,40,(10,400), on_exit)
        
        buttons.append(nuovoButton)
        buttons.append(buttonEsc)
        buttons.append(button3)
        buttons.append(closeButton)

        pygame.display.flip()

        running = True
        
        while running == True:
            on_update()
            pygame.display.update()
            
            for event in pygame.event.get():
                #if user clicks the close X
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    break
                    
                elif event.type == pygame.MOUSEBUTTONUP:
                    buttons_events()
                        
            clock.tick(60)

    except Exception as e:
            print("__main__: An error occurred:", e.args[0])
    
    
    
    finally:
        print("Exit...")
    pass