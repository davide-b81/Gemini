'''
Created on 2 gen 2022

@author: david
'''
import tkinter as tk

from oggetti.button_bar import ButtonBar
from Output.Immagini import Foto
from tkinter.ttk import Frame, Button, Style
from oggetti.stringhe import nomigiocatore
import Game

from Game.Germini.Gioco import game

class App:
    master = None
    newgame_callback = None
    g = None
    
    def init_imags(self):
        self.fm = Foto()

    def __init__(self) -> None:
        self.master = tk.Tk()
        self.master.attributes('-fullscreen', True)    
        # Windows area manager
        self.winm = WinManager(self)
    
    def main_loop(self):
        self.master.mainloop()

    def on_closing(self):
        self.master.destroy()
        
    def set_newgame_callback(self, f):
        self.newgame_callback = f
 
    def on_newgame(self):
        try:

            g = game(nomigiocatore)
    
            g.forma_coppie()
            #print("Mazziere: " + g.GetMazziere())            
            g.manche()
            print("\n")
            self.newgame_callback()
        except Exception as e:
            print("on_newgame: An error occurred:", e.args[0])


class WinManager(Frame):
    '''
    classdocs
    '''
    nord = None
    sud = None
    est = None
    ovest = None
    desk = None
    bar = None
    frame_menu = None
    frame_main = None
    app = None
    
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.master.title("Buttons")
        self.style = Style()
        self.style.theme_use("default")

        self.frame_main = tk.Frame(self, bg="green", relief=tk.RAISED, borderwidth=1)
        self.frame_main.pack(fill=tk.BOTH, expand=True)
        
        self.frame_menu = tk.Frame(self, bg="red", relief=tk.RAISED, borderwidth=1)
        self.frame_menu.pack(fill=tk.Y, expand=False)     

        self.pack(fill=tk.BOTH, expand=True)
 
        closeButton = Button(self.frame_menu, text="Esci", command=self.master.destroy)
        closeButton.pack(side=tk.RIGHT, padx=5, pady=5)
        okButton = Button(self.frame_menu, text="Nuovo", command=self.app.on_newgame)
        okButton.pack(side=tk.RIGHT)
        tk.Label(self.frame_main, text="Il nobilissimo giuoco delle Minchiate Fiorentine", font=("Bodoni MT Black", 25)).pack()
        self.create_layout()
                
     
    def create_layout(self):
        # With pack manager create button bar and main frame     
        #self.bar = ButtonBar()
        self.desk = tk.Canvas(self.frame_main, bd=2, bg="green", height=250, width=300)
        self.desk.pack()
        self.est = tk.Canvas(self.frame_main, bd=2, bg="yellow", height=350, width=200)
        self.est.pack(side=tk.RIGHT)
        self.ovest = tk.Canvas(self.frame_main, bd=2, bg="yellow", height=350, width=200)
        self.ovest.pack(side=tk.LEFT)
        self.nord = tk.Canvas(self.frame_main, bd=2, bg="yellow", height=350, width=200)
        self.nord.pack(side=tk.TOP)
        self.sud = tk.Canvas(self.frame_main, bd=2, bg="yellow", height=350, width=200)
        self.sud.pack(side=tk.BOTTOM)
        #self.sbar = tk.Scrollbar(self, orient=tk.VERTICAL)

        #self.sbar.pack(side=tk.RIGHT, fill=tk.Y)
        #self.canvas.pack(side=tk.LEFT, expand="YES", fill=tk.BOTH)
    
        