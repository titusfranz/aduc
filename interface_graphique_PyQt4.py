# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 19:48:50 2017

@author: DragoMagnus

Interface Graphique PyQt4 - Projet
Cette première version utilise le module PyQt4, une mise à jour vers PyQt5
sera effectuée après création de la première interface graphique

"""

import sys
from PyQt4 import QtGui ### Module d'interface graphique
from PyQt4 import QtCore

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


import Projet_ADUC as ADUC

from pylab import*
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

carte = ADUC.ADUC()


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
        
        ################################################################
        ############ ECRITURE DES WIDGETS ############
        ################################################################
        self.button_start = QtGui.QPushButton('START', self) ### Bouton START
        
        self.button_stop = QtGui.QPushButton('APOCALYPSE', self) ### Bouton STOP
        
        self.check_port = QtGui.QPushButton('Ouverture PORT', self) ### Bouton d'ouverture
        self.check_port_close = QtGui.QPushButton('Fermeture PORT', self) ### Bouton de fermeture
        """
        On tentera ici de faire une case check pour remplacer les deux boutons
        et ainsi n'avoir qu'une seule fonction avec un if
        """
        #self.check_port = QtGui.QCheckBox(self) ### Case d'ouverture de port
        #self.check_port.setChecked(False) ### Initialise le Check               
        
        self.entry_port = QtGui.QLineEdit("Enter Port") ### Case pour entrer le port
        
        
        self.figure = plt.figure()
        self.canvas_plot = pg.GraphicsLayoutWidget() #self.figure) ### Insertion d'une case figure
        
        ################################################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        global grid
        grid = QtGui.QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,1)
        grid.addWidget(self.button_stop, 4,1)
        grid.addWidget(self.check_port, 0,2)
        grid.addWidget(self.check_port_close, 1, 1)
        grid.addWidget(self.entry_port, 1,2)     
        grid.addWidget(self.canvas_plot, 3, 1)
        
        
        self.show()
        
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################
        self.button_start.clicked.connect(self.button_start_command)
        self.button_stop.clicked.connect(self.button_stop_command)
        
        self.check_port.clicked.connect(self.open_port)        
        self.check_port_close.clicked.connect(self.close_port)
        
        self._active = False
        
        ### Cliquer sur la case va appeler la fonction open_port
        ### ouvrant ou fermant ainsi le port usb de la carte ADUC
        ### Ne fonctionne pour l'instant PAS
        #self.check_port.connect(self.check_port, QtCore.SIGNAL('stateChanged(int'), self.open_port)

        
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
            self.scrollplot()
            QtCore.QTimer.singleShot(0, self.freerun)
            print "Aquisition START"
        else :
            self._active = False
            self.button_start.setText("START")
            QtCore.QTimer.singleShot(0, self.button_stop_command)
            print "Aquisition STOP"

    def button_stop_command(self):
        """
        Cette fonction stop l'aquisition de la carte ADUC et affiche
        le message d'arrêt, cette fonction peut êtr obsolète si la fonction
        précédente fonctionne.
        """
        carte.stop()
        print "Aquisition STOP"
        
    def open_port(self):
        """
        Cette fonction permet d'ouvrir le port USB lié à la carte ADUC
        et envoie un message de confirmation d'ouverture. Renvoie un
        TRUE si la commande fonctionne
        """
        print "Ouverture du port"
        
        carte.port = self.entry_port.text()
        print carte.port, carte.name
        carte.baudrate = 115200
        
        carte.open()
        print carte.is_open

    def close_port(self):
        """
        Cette fontion va fermer le port de la carte d'aquisition et vérifier
        en renvoyant un FALSE que la commande a été effectué
        """
        print "Fermeture du port"
        carte.close()
        print carte.is_open
        
        
        
    ################################################################
    ############ FONCTIONS UTILES ############
    ################################################################ 
    def freerun(self):
        from time import sleep
        carte.write('f')
        print carte.read(1)
        sleep(0.05)        
        while self._active:
            print carte.name
            QtGui.qApp.processEvents()
            print carte.read(1)
            ascii = carte.read(512)
            print carte.asciitoint(ascii)
            self.data = carte.asciitoint(ascii)
            
            if self._active == False:
                break
            
        carte.stop()        
        self.button_start.setText('START')
        self._active = False
        
    def scrollplot(self):
        win = self.canvas_plot.GraphicsWindow()
        win.setWindowTitle('Graphe ... peut etre')
        
        p1 = win.addPlot()
        data1 = self.data
        curve1 = p1.plot(data1)
        ptr1 = 0
        def update1():
            global data1, curve1, ptr1
            data1[:-1] = data1[1:]  # shift data in the array one sample left
                            # (see also: np.roll)
            data1[-1] = np.random.normal()
            curve1.setData(data1)
        
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update1)
        timer.start(50)


if __name__ == "__main__":
    system = QtGui.QApplication(sys.argv)
    graphique = Interface_Graphique()
    graphique.show()
    sys.exit(system.exec_())
    
    
    
"""
   #if self.check_port.isChecked() :
         #   self.lineEdit.setText("Port USB - Open")
          #  print "Port USB - Open"
        #else :
          #  self.lineEdit.setText("Port  USB - Close")
"""