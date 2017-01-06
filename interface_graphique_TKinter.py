# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 10:56:47 2017

@author: maitre
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 19:48:23 2017

@author: DragoMagnus

Interface Graphique TKinter - Projet

"""

import Tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

class Interface_Graphique(tk.Tk):
    """
    Cette classe permet la configuration de l'interface graphique
    """
    
    def __init__(self,parent):
        """
        La fonction init contient l'initialisation de la fenêtre graphique
        De plus un paramètre parent est implémenté. Ce paramètre sert de base
        aux différents widgets (boutons, graphes) qui seront implémentés
        dans la suite.
        """
        tk.Tk.__init__(self,parent)
        self.parent = parent ### Garde en memoire la reference parent
        self.interface_graphique()
        self.mainloop() ### Permet une boucle infinie afin que la fenetre
                        ### de l'interface ne disparait pas

    def interface_graphique(self):
        """
        Cette fonction a pour but de générer les élements de l'interface
        graphique. Elle contient tous les widgets nécessaires à la 
        réalisation de l'interface ADUC
        """
        self.grid() ### Creation d'une grille. Cette grille facilite la mise
                    ### en place des differents elements de l'interface
        
        """
        open_port est un widget qui va permettre l'ouverture ou la fermeture
        du port usb lié à la carte d'aquisition.
        """
        self.open_port = tk.Checkbutton(self, text="Port USB") ### Creation
        self.open_port.grid(column = 0, row = 0, sticky = 'EW') ### Mise en place dans le grid
        
        """
        - usb_value correspond numero du port usb auquel est connecté
        la carte d'aquisition ADUC
        - entry_usb est une fenêtre de l'interface graphique dans laquelle
        on peut entrer le port usb en question et qui donnera la valeur
        à usb_value
        """
        global usb_value
        usb_value = tk.StringVar() ### Variable string qui autorise les lettres
        usb_value.set("Entrer le port USB") ### Donne la valeur
        
        self.entry_usb = tk.Entry(self, textvariable=usb_value, width=30)
        self.entry_usb.grid()
        
        
        """
        button_start et button_stop sont les deux boutons qui permettrons
        la prise d'aquisition de la carte ADUC
        """
        self.button_start = tk.Button(self, text="START", command=self.start)
        self.button_stop = tk.Button(self, text="STOP", command=self.stop)
        self.button_start.grid() ### Mise en place des boutons dans le grid
        self.button_stop.grid()
        
        """
        Mise en place d'une fenêtre Matplot
        """
        self.plot = tk.Button(self, text="Graphe", command=self.plot_aquisition)
        self.plot.grid(column = 3, row = 0)
        """
        Mise en place d'un canevas pour y déposer le graphe matplot
        """
        global figure
        figure = tk.Canvas(self, width=250, height=50)
        figure.grid(column=3, row=1)
              
    def start(self):
        """
        Cette fonction va permettre l'event start
        """
        print 'Aquisition START'
        
    def stop(self):
        """
        Cette fonction va permettre l'event stop
        """
        print 'Aquisition STOP'
        
    def plot_aquisition(self):
        x = np.arange(0, 5, 0.1);
        y = np.sin(x)
        plt.plot(x,y)
        
        
    
        
        
        
graphique = Interface_Graphique(None)
graphique.interface_graphique
graphique.entry_usb
graphique.plot
