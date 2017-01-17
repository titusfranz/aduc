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
        self.plt = self.canvas_plot.addPlot(title='Dynamic Plotting with PyQtGraph') ### Utilisation du canvas
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
        self.plot = Realtimeplot()
        self._active = False

        self.button_start = QtGui.QPushButton('START', self) ### Bouton START
        #self.button_quit = QtGui.QPushButton('APOCALYPSE', self) ### Bouton STOP HIStoriqUE
        
        self.check_port = QtGui.QPushButton('Ouverture PORT', self) ### Bouton d'ouverture
        self.check_port_close = QtGui.QPushButton('Fermeture PORT', self) ### Bouton de fermeture
								          
        self.entry_port = QtGui.QLineEdit("COM3") ### Case pour entrer le port plus tar remplacer par enter PORT

        """
        Créer une fenêtre Labler
        """
        self.label_timewindow = QtGui.QLineEdit("20") ## Change la taille des abscisses
        self.label_sampleinterval = QtGui.QLineEdit("0.1")
        self.button_timewindow_sampleinterval = QtGui.QPushButton('Apply Time Scale', self) ## Applique le changement
								      						
	   ################################################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        global grid
        grid = QtGui.QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,0)
        grid.addWidget(self.check_port, 0,2)
        grid.addWidget(self.check_port_close, 1, 1)
        grid.addWidget(self.entry_port, 1,2)     
        grid.addWidget(self.plot.canvas_plot, 3, 1)
        grid.addWidget(self.label_timewindow, 5,1)
        grid.addWidget(self.label_sampleinterval, 5,2)
        grid.addWidget(self.button_timewindow_sampleinterval, 5, 3)
        
        
        self.show()
        
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################
        self.button_start.clicked.connect(self.button_start_command)

        self.check_port.clicked.connect(lambda : self.carte.open_port(self.entry_port.text()))        
        self.check_port_close.clicked.connect(self.close_port)
        
        self.button_timewindow_sampleinterval.clicked.connect(lambda: self.plot.time_scale(self.label_timewindow.text(),self.label_sampleinterval.text()))
        
        self._active = False
        
        ################################################################
        ############ CREATION DES COMMANDES ############
        ################################################################
        
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
            self.plot.updateplot(data)
            
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
        


if __name__ == "__main__":
    system = QtGui.QApplication(sys.argv)
    graphique = Interface_Graphique()
    graphique.show()
    sys.exit(system.exec_())
    
    
