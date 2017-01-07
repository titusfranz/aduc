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

from pylab import*
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


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
        
        self.main_layout = QtGui.QHBoxLayout() ### Permission d'ecriture de widget
        self.setLayout(self.main_layout) ### Application des widgets
        
        ################################################################
        ############ ECRITURE DES WIDGETS ############
        ################################################################
        self.button_start = QtGui.QPushButton('START', self) ### Bouton START
        self.main_layout.addWidget(self.button_start)
        
        self.button_stop = QtGui.QPushButton('STOP', self) ### Bouton STOP
        self.main_layout.addWidget(self.button_stop)
        
        self.check_port = QtGui.QCheckBox(self) ### Case d'ouverture de port
        self.main_layout.addWidget(self.check_port)
        self.entry_port = QtGui.QLineEdit("PORT USB") ### Case pour entrer le port
        self.main_layout.addWidget(self.entry_port)
        
        
        self.fig = Figure()
        self.x = linspace(-pi, pi, 30)
        self.y = cos(self.x)
        
        self.canvas = FigureCanvas(self.fig) ### Insertion d'une case figure
        self.main_layout.addWidget(self.canvas)
        
        
        self.show()
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################
        self.button_start.clicked.connect(self.button_start_command)
        self.button_stop.clicked.connect(self.button_stop_command)

        
        ################################################################
        ############ CREATION DES COMMANDES ############
        ################################################################
    def button_start_command(self):
        """
        Cette fonction affiche le message de lancement de l'aquisition
        et lance l'aquisition de la carte ADUC
        """
        ### Ajouter les commandes disponibles dans le programme principal
        ### pour la commande START, ie :
        ### - carte.freerun()
        print "Aquisition START"        
        self.y = cos(self.x) ### Test d'ouverture de plot
        self.line.set_ydata(self.y)
        self.canvas.draw()

        

    def button_stop_command(self):
        """
        Cette fonction stop l'aquisition de la carte ADUC et affiche
        le message d'arrêt
        """
        ### Ajouter les commandes disponibles dans le programme principal
        ### pour la commande STOP, ie :
        ### - carte.close()
        ### - carte.is_close() instead of print "Aquisition STOP"
        print "Aquisition STOP"
        
    def open_port(self):
        """
        Cette fonction permet d'ouvrir le port USB lié à la carte ADUC
        et envoie un message de confirmation d'ouverture
        """
        ### - carte.open()
        ### - carte.is_open() instead of print "Port USB - Open"        
        if self.check_port.isChecked :
            print "Port USB - Open"

    def port_value(self):
        """
        Cette fonction permet de donné au port la valeur à laquelle
        il peut lire la carte ADUC
        """
        ### Remplacer usb_value par carte.port = " "
        ### Cela permettra de donner la valeur correspondante en changeant le
        ### pc sur lequel est branche la carte ADUC
        usb_value = QtGui.QTableWidget(self.entry_port)
        print usb_value
        


if __name__ == "__main__":
    system = QtGui.QApplication(sys.argv)
    graphique = Interface_Graphique()
    sys.exit(system.exec_())