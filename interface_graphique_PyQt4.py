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
        
        ################################################################
        ############ ECRITURE DES WIDGETS ############
        ################################################################
        self.button_start = QtGui.QPushButton('START', self) ### Bouton START
        
        self.button_stop = QtGui.QPushButton('STOP', self) ### Bouton STOP
        
        self.check_port = QtGui.QCheckBox(self) ### Case d'ouverture de port
        self.check_port.setChecked(False) ### Initialise le Check               
        
        self.entry_port = QtGui.QLineEdit("PORT USB") ### Case pour entrer le port
        
        
        self.figure = plt.figure()
        self.canvas_plot = FigureCanvas(self.figure) ### Insertion d'une case figure
        
        ################################################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        grid = QtGui.QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,1)
        grid.addWidget(self.button_stop, 0,2)
        grid.addWidget(self.check_port, 1,1)
        grid.addWidget(self.entry_port, 1,2)     
        grid.addWidget(self.canvas_plot, 3, 1)
        

        
        self.show()
        
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################
        self.button_start.clicked.connect(self.button_start_command)
        self.button_stop.clicked.connect(self.button_stop_command)
        
        ### Cliquer sur la case va appeler la fonction open_port
        ### ouvrant ou fermant ainsi le port usb de la carte ADUC
        ### Ne fonctionne pour l'instant PAS
        self.check_port.connect(self.check_port, QtCore.SIGNAL('stateChanged(int'), self.open_port)

        
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
        x = np.linspace(0., 4*np.pi, 100)
        plt.plot(x, np.sin(x))
        show()
        print "Aquisition START"     

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
        if self.check_port.isChecked() :
            self.lineEdit.setText("Port USV - Open")
        else :
            self.lineEdit.setText("Port  USB - Close")

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