'''
Created on 31 dic 2021

@author: davide bolognesi

@see: https://it.wikipedia.org/wiki/Minchiate#Regole
'''

import decks.mazzo
import logic.Carta
import Game.Player
from Game.Player import Giocatore
from logic.Carta import GetGreater
from logic.Carta import IsCartiglia
from pickle import NONE
from decks import mazzo_97
import pygame
from threading import Thread
from oggetti.stringhe import Stringhe
from Game.fsm_cartapiualta import FsmCartaPiuAlta
from Game.general_manager import GeneralManager

class game(object):
    man = None
    '''
    classdocs
    '''

    nord = ""
    sud = ""
    est = ""
    ovest = ""
    
    text = "Inizio"

    gioco_carta = None

    def __init__(self, g, hndl = None):
        '''
        Constructor
        '''
        self.nomegiocatori = g
        self.mazzo = mazzo_97.Mazzo97(None)
        self.gioco_carta = FsmCartaPiuAlta()
        self.man = GeneralManager()
    
    def GetPlayerOwner(self, c):
        for key, value in self.carte.items():
            if (value == c):
                return key
        return None
        
    def GetHighestCard(self):
        cAlta = None
        player = None

        for key, value in self.carte.items():
            if (cAlta == None):
                cAlta = value
                player = key
            else:
                c = GetGreater(cAlta, value)
                if (cAlta != c):
                    cAlta = c
                    player = key
        return player, cAlta
      
    def GetMazziere(self):
        return str(self.mazziere)

    def GetTesto(self):
        return self.text

    def Manche(self):
        print("\nIl mazziere scozza le carte terminando dopo aver verificato che vi sia una cartiglia in fondo al mazzo")
        self.Step_mescola()
    
    def Restore(self):    
        print("Raccoglie tutte le carte...")
        self.carte.clear()   
        self.tavola.clear()
        self.text = ""
        self.mazzo.Ripristina()

    def CarteCalate(self, player):
        try:
            return self.tavola[player]
        except Exception as e:
            print("CarteCalate: An error occurred:", e.args[0])
            return None
        
    def ThreadWorker(self):
        if (self.gioco_carta):
            self.gioco_carta.update_game()

        #print("Waiting for input.")
    
    def inizia_gioco_c(self):
        self.gioco_carta = FsmCartaPiuAlta()
        self.gioco_carta.start_game()
        
    def termina_gioco_c(self):
        self.gioco_carta.end_game()
        self.gioco_carta = None

    def FormaCoppie(self):
        self.inizia_gioco_c()

        try:
            self.mazziere = None
            self.coppia1.clear()
            self.coppia2.clear()
    
            print("\nPer formare le coppie i giocatori pescano una carta")
            
            for count, player in enumerate(self.nomegiocatori):         
                self.carte[player] = self.mazzo.Estrai()
                self.tavola[player] = self.carte[player]
                print(player + " ha preso " + self.carte[player].__str__())
            
            print(self.carte)
            
            # Giocatore 1 (Mazziere)
            player, win = self.GetHighestCard()
            self.mazziere = player
            self.coppia1.insert(0, player)
            self.giocatori.append(Giocatore(player, self.posizioni[0]))
            self.carte.pop(player)
            self.text = "Vince " + player + " con " + Stringhe.get_card_name(win)
            print (self.giocatori[0].GetPosition() + " : " + self.giocatori[0].GetName() + " con " + str(win) + " (Mazziere).")
            
            # Giocatore 2 (Compagno del mazziere)
            player, win = self.GetHighestCard()
            self.coppia1.insert(1, player)
            self.giocatori.append(Giocatore(player, self.posizioni[2]))
            self.carte.pop(player)
            print (self.giocatori[1].GetPosition() + " : " + self.giocatori[1].GetName() + " con " + str(win) + ".")
            
            # Giocatore 3
            player, win = self.GetHighestCard()
            self.coppia2.insert(0, player)
            self.giocatori.append(Giocatore(player, self.posizioni[1]))
            self.carte.pop(player)
            print (self.giocatori[2].GetPosition() + " : " + self.giocatori[2].GetName() + " con " + str(win) + ".")
            
            # Giocatore 4 (Compagno del giocatore 3)
            player, win = self.GetHighestCard()
            self.coppia2.insert(1, player)
            self.giocatori.append(Giocatore(player, self.posizioni[3]))
            self.carte.pop(player)            
            print (self.giocatori[3].GetPosition() + " : " + self.giocatori[3].GetName() + " con " + str(win) + ".")
                
        except Exception as e:
            print("FormaCoppie: An error occurred:", e.args[0])
        
        return self.coppia1, self.coppia2        
    
    def Step_mescola(self):
        '''
        Il mazziere mescola le carte e, al momento di passare il mazzo al tagliatore, verifica che l'ultima sia una cartiglia; in caso contrario mischia ancora.
        '''
        try:
            found = False
            self.mazzo.Ripristina()
            print("Mescola...")
            
            while found == False:
                self.mazzo.Shuffle()
                c = self.mazzo.GetLast()
                if IsCartiglia(c):
                    print("Ultima carta:" + str(c) + " -> Ok")
                    found = True
                    break
                else:
                    print("Ultima carta:" + str(c) + " -> Mescola di nuovo")
                    continue
            else:
                print("")
        except Exception as e:
            print("Step_mescola: An error occurred:", e.args[0])
        