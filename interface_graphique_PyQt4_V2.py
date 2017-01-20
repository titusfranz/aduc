# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 19:48:50 2017
@author: Titus Franz, William Dubosclard


PROGRAMME INTERFACE GRAPHIQUE :
Supporte les commandes via boutons + création du plot



Le Futur :
- Création d'une fenêtre pour y stocker la possibilitée de changer la taille
de la fenêtre de plot --> Création d'un widget spécial

- Insértion d'un graphe qui va calculer la DSP, en premier lieu avec un plot fixe
puis, avec un plot déroulant --> Création d'une classe DSP (dans Projet ADUC ??)
"""
from __future__ import division

import sys
from PyQt4 import QtGui ### Module d'interface graphique
from PyQt4 import QtCore

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import Projet_ADUC as ADUC

import collections
import numpy as np

class Realtimeplot(object):
    """
    Cette fonction permet de créer des graphes en temps réel dans l'interface
    graphique
    """
    def __init__(self, sampleinterval=0.1, timewindow=50.):
        self.sampleinterval = sampleinterval
        self.timewindow = timewindow
        self._interval = int(self.sampleinterval)
        self._bufsize = int(self.timewindow/self.sampleinterval)
        self.x = np.linspace(-self.timewindow, 0.0, self._bufsize)     
        self.y = collections.deque(np.zeros(self._bufsize), self._bufsize)
        
        
        ### Pygraph init
        self.canvas_plot = pg.GraphicsLayoutWidget() ### Creation d'un canvas
        self.plt = self.canvas_plot.addPlot(title='ADUC DATA') ### Utilisation du canvas
        #self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))
        
        
    def updateplot(self, data):
        """
        Fonction d'updating du plot
        """
        self.y.extend(data)
        self.curve.setData(self.x, self.y)

    def time_scale(self, timewindow, sampleinterval):
        """
        Cette fonction permet de choisir la taille de la feêtre de plot
        """  
        self._interval = float(sampleinterval)
        self._bufsize = int(timewindow)/float(sampleinterval)
        self.databuffer = collections.deque([0.0], self._bufsize) # mabe maxlen needed (maxlen = 512)
        self.x = np.linspace(-int(timewindow), 0.0, self._bufsize)
        self.y = collections.deque(np.zeros(self._bufsize), self._bufsize)
							
"""
On ajoutera ici une classe RealtimeDSP qui permettra de tracer la DSP du signal.
En fonction de la vitesse de calcul, le plot pourrait être en temps réel
"""
        

class Interface_Graphique(QtGui.QWidget):
    """
    Cette classe va permettre la création de l'interface grapgique
    """
    
    def __init__(self):
        """
        Cette fonction initialise une variable parent qui permettra
        aux différents widgets de se référer à cette base.
        
        De plus, tous les widgets seront inclus dans cette fonction
        d'initialisation.
        
        Widget disponible :
        - Bouton START
        - Bouton STOP
        - Port USB avec Entrer
        - Fenêtre Graphique
        """

        super(Interface_Graphique, self).__init__()
        self.carte = ADUC.ADUC()
        self.plot_set = Realtimeplot()
        self._active = False
        self.panel = Panel_Control()
        self.setWindowTitle("Fenetre Principale")

        self.button_start = QtGui.QPushButton('START', self) ### Bouton START
        #self.button_quit = QtGui.QPushButton('APOCALYPSE', self) ### Bouton STOP HIStoriqUE
        
        self.check_port = QtGui.QPushButton('Ouverture PORT', self) ### Bouton d'ouverture
        self.check_port_close = QtGui.QPushButton('Fermeture PORT', self) ### Bouton de fermeture
								          
        self.entry_port = QtGui.QLineEdit("COM3") ### Case pour entrer le port plus tar remplacer par enter PORT
        self.button_panel = QtGui.QPushButton('Panel Plot', self) ### Affiche le panel pour le controle de plot
								
        self.button_quit = QtGui.QPushButton('Quitter', self) ### Bouton qui permet de quitter l'application
        #self.button_quit.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold)) ###  Change les caracteres d ecriture 			
								
	   ################################################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        global grid
        grid = QtGui.QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,1)
        grid.addWidget(self.check_port, 0,2)
        grid.addWidget(self.check_port_close, 1, 1)
        grid.addWidget(self.entry_port, 1,2)     
        grid.addWidget(self.plot_set.canvas_plot, 3, 1)
        grid.addWidget(self.button_panel, 3, 2)
        grid.addWidget(self.button_quit, 4,1)
        
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################
        self.button_start.clicked.connect(self.button_start_command)

        self.check_port.clicked.connect(lambda : self.carte.open_port(self.entry_port.text()))        
        self.check_port_close.clicked.connect(self.close_port)
								
        self.panel.button_timewindow_sampleinterval.clicked.connect(lambda: self.plot_set.time_scale(self.panel.label_timewindow.text(),self.panel.label_sampleinterval.text()))								
        self.button_quit.clicked.connect(self.button_quit_command)
        
        self.button_panel.clicked.connect(self.panel_control)
        self._active = False
        
        ################################################################
        ############ CREATION DES COMMANDES ############
        ################################################################

    def button_quit_command(self):
        """
        Cette fonction permet de quitter l'interface graphique proprement
        """
        self.close()
								
        
    def button_start_command(self):
        """
        Cette fonction affiche le message de lancement de l'aquisition
        et lance l'aquisition de la carte ADUC
        """
        if not self._active :
            self._active = True
            self.button_start.setText("STOP")
            QtCore.QTimer.singleShot(0, self.freerun)
            print "Aquisition START"
        

        else :
            self._active = False
            self.button_start.setText("START")
            QtCore.QTimer.singleShot(0, self.carte.stop)
            print "Aquisition STOP"

    def freerun(self):
        """
        Programme d'aquisition des données
        """
        self.carte.lancement()
        self._active = True
        while self._active:
            QtGui.qApp.processEvents()
            data = self.carte.freerun_carte()
            self.plot_set.updateplot(data)
            
            if self._active == False:
                break	
															
    def close_port(self):
        """
        Cette fontion va fermer le port de la carte d'aquisition et vérifier
        en renvoyant un FALSE que la commande a été effectué
        """
        print "Fermeture du port"
        carte.close()
        print carte.is_open
		
    def panel_control(self):
        self.panel.show()						
        
class Panel_Control(QtGui.QWidget):
    """
    Cette classe va permettre la création du panel de contrôle de plot
    """
    
    def __init__(self):
        super(Panel_Control, self).__init__()
        self.carte = ADUC.ADUC()
        self.plot_set = Realtimeplot()
        self.setWindowTitle("Controle du Plot")
        
        self.text_timewindow = QtGui.QLabel("Axe du Temps")				
        self.text_sampleinterval = QtGui.QLabel("Echantillonnage")
								
        self.label_timewindow = QtGui.QLineEdit("1") ## Change la taille des abscisses
        self.label_sampleinterval = QtGui.QLineEdit("1") ## Change l'interval d'echantillonage
        #self.button_timewindow = QtGui.QPushButton('Appliquer le temps')	
        #self.button_sampleinterval = QtGui.QPushButton("Appliquer l'intervalle")
								
        self.button_timewindow_sampleinterval = QtGui.QPushButton('Appliquer', self) ## Applique le changement					
					
        global grid
        grid = QtGui.QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
						
        grid.addWidget(self.label_timewindow, 1,1)
        #grid.addWidget(self.button_timewindow, 2,1)
        grid.addWidget(self.text_timewindow, 0,1)								
								
        grid.addWidget(self.label_sampleinterval, 1,2)
        #grid.addWidget(self.button_sampleinterval, 2,2)
        grid.addWidget(self.text_sampleinterval, 0,2)
								
        grid.addWidget(self.button_timewindow_sampleinterval, 3,1)
		

        #self.button_timewindow.clicked.connect(lambda : self.plot.time_scale(self.label_timewindow.text()))
        #self.button_sampleinterval.clicked.connect(lambda : self.plot.time_scale(self.label_sampleinterval.text()))
        						
        
									
if __name__ == "__main__":
    system = QtGui.QApplication(sys.argv)
    graphique = Interface_Graphique()		
    graphique.show()
    sys.exit(system.exec_())
    
