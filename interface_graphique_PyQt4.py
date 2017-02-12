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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import time
import sys
import numpy as np
import collections
import pyqtgraph as pg
import threading

import Projet_ADUC_V3 as ADUC

class Test(object):
        
    def wait(self):
        print 'hallo'
        time.sleep(5)
        print 'hmm'


class Realtimeplot(object):
    """
    Cette fonction permet de créer des graphes en temps réel dans l'interface
    graphique
    """
    def __init__(self, samplerate=41.78e6, bufsize=512):
        self.sampleinterval = 1/samplerate
        self._bufsize = int(bufsize)
        self.timewindow = self.sampleinterval*self._bufsize
        self._interval = int(self.sampleinterval)
        
        self.x = np.linspace(-self.timewindow, 0.0, self._bufsize)
        self.y = collections.deque(np.zeros(self._bufsize), self._bufsize)
        
        self.x_dsp = np.fft.rfftfreq(self._bufsize,samplerate)[1:]
        self.y_dsp = collections.deque(np.zeros(self._bufsize//2), self._bufsize//2)
        
        
        ### Pygraph init
        self.canvas_plot = pg.GraphicsLayoutWidget() ### Creation d'un canvas
        self.plt = self.canvas_plot.addPlot(title='ADUC DATA') ### Utilisation du canvas
        
        self.canvas_plot_dsp = pg.GraphicsLayoutWidget() ### Creation d'un canvas
        self.plt_dsp = self.canvas_plot_dsp.addPlot(title='ADUC DSP') ### Utilisation du canvas
        

        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel('left', 'amplitude', 'V')
        self.plt.setLabel('bottom', 'time', 's')
        self.curve = self.plt.plot(self.x, self.y, pen=(255,0,0))
        
        self.plt_dsp.showGrid(x=True, y=True)
        self.plt_dsp.setLabel('left', 'amplitude', 'V')
        self.plt_dsp.setLabel('bottom', 'frequency', 'Hz')
        self.plt_dsp.setLogMode(x=True, y=True)
        self.curve_dsp = self.plt_dsp.plot(self.x_dsp, self.y_dsp, pen=(255,0,0))
        
        
    def updateplot(self, data):
        """
        Fonction d'updating du plot
        """
        self.y.extend(data)
        self.y_dsp = self.dsp(np.array(self.y))
        self.curve.setData(self.x, self.y)
        self.curve_dsp.setData(self.x_dsp, self.y_dsp[1:])
             

    
    def dsp(self, data):
        dsp = (np.abs(np.fft.rfft(data)))**2
        return dsp
							

class Oscilloscope(QObject):
    def __init__(self):
        super(Oscilloscope, self).__init__()
        
        self.stopMutex = threading.Lock()
        
        self.carte = ADUC.ADUC()
        self.data = np.ndarray([])
    
    data_transfer = pyqtSignal(np.ndarray)
    started_ok = pyqtSignal()
    mode = pyqtSignal(str)
    
    
    @pyqtSlot(str)
    def open_port(self,portname):
        print 'hello'
        self.carte.open_port(portname)
        print 'hello'
        with self.stopMutex:
            self.stop = True
    
    @pyqtSlot(str)
    def start(self, mode='normal'):
        if mode=='normal':
            self.carte.lancement_normal()
        elif mode=='freerun':
            self.carte.lancement_freerun()
        else:
            print mode + ' is no appropriate mode. Please enter either normal or freerun'
        print 'hm'
        #self.started_ok.emit()
        self.acquire_data()
    @pyqtSlot(np.ndarray)
    def acquire_data(self):
        'acquire'
        self.data = self.carte.freerun_carte()
        self.data_transfer.emit(self.data)
        
            
    
    @pyqtSlot()
    def close_port(self):
        """
        Cette fontion va fermer le port de la carte d'aquisition et vérifier
        en renvoyant un FALSE que la commande a été effectué
        """
        print "Fermeture du port"
        carte.close()
        print carte.is_open   
        

        
        
        
class Interface_Graphique(QWidget):
    def __init__(self, parent = None):
        super(Interface_Graphique, self).__init__()

        self.initUi()
        self.setupThread()
        self._active = False
        

    def initUi(self):
        self.realtimeplot = Realtimeplot()
        self.setWindowTitle("Fenetre Principale")

        self.button_start = QPushButton('START', self) ### Bouton START
        self.button_normal = QPushButton('Normal ON', self) ### Bouton Trigger
        self.button_openport = QPushButton('Ouverture PORT', self) ### Bouton d'ouverture
        self.button_closeport = QPushButton('Fermeture PORT', self) ### Bouton de fermeture						          
        self.entry_port = QLineEdit("/dev/ttyUSB1") ### Case pour entrer le port plus tar remplacer par enter PORT
        self.button_panel = QPushButton('Panel Plot', self) ### Affiche le panel pour le controle de plot
        self.button_quit = QPushButton('Quitter', self) ### Bouton qui permet de quitter l'application
        #self.button_quit.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold)) ###  Change les caracteres d ecriture 			
								
	   ################################################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        global grid
        grid = QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,0)
        grid.addWidget(self.button_normal, 0,1)
        grid.addWidget(self.button_openport, 0,2)
        grid.addWidget(self.button_closeport, 1, 1)
        grid.addWidget(self.entry_port, 1,2)     
        grid.addWidget(self.realtimeplot.canvas_plot, 3, 0)
        grid.addWidget(self.button_panel, 3, 2)
        grid.addWidget(self.button_quit, 4,1)
        grid.addWidget(self.realtimeplot.canvas_plot_dsp, 3, 1)        
        
    
        ################################################################
        ########### APPEL DES COMMANDES ############
        ################################################################

    
        
    def setupThread(self):
        self.thread = QThread()
        self.oscilloscope = Oscilloscope()
        self.oscilloscope.moveToThread(self.thread)
        
        self.button_openport.clicked.connect(lambda : self.oscilloscope.open_port(self.entry_port.text()))        
        self.button_closeport.clicked.connect(self.oscilloscope.close_port)
        self.button_start.clicked.connect(lambda: self.button_start_command('freerun'))
        self.button_normal.clicked.connect(lambda: self.button_start_command('normal'))
        self.oscilloscope.data_transfer.connect(self.data_processing) 
        self.button_quit.clicked.connect(self.button_quit_command)
        
        self.thread.start()
    
    
    @pyqtSlot()               
    def button_start_command(self, mode):
        """
        Cette fonction affiche le message de lancement de l'aquisition
        et lance l'aquisition de la carte ADUC
        """ 
        print mode + ' clicked'
        
        if not self._active :
            self._active = True
            if mode=='normal':
                self.button_normal.setText('STOP')
            elif mode=='freerun':
                self.button_start.setText('STOP')
            else:
                print mode + ' is no appropriate mode. Please enter either normal or freerun'
            self.oscilloscope.start(mode)
            
        else :
            self._active = False
            if mode=='normal':
                self.button_normal.setText('NormalOn')
            elif mode=='freerun':
                self.button_start.setText('Freerun')
            else:
                print mode + ' is no appropriate mode. Please enter either normal or freerun'
            QTimer.singleShot(0, self.oscilloscope.carte.stop)
            print "Aquisition STOP"

    @pyqtSlot(np.ndarray)
    def data_processing(self, data):
        print 'procesing'
        qApp.processEvents()
        self.realtimeplot.updateplot(data)
        if self._active:
            self.oscilloscope.acquire_data()
        

    def button_quit_command(self):
        """
        Cette fonction permet de quitter l'interface graphique proprement
        """
        app.kernel.do_shutdown(True)  
        self.close()
								
        
        

if __name__ == "__main__":
    system = QApplication(sys.argv)
    graphique = Interface_Graphique()		
    graphique.show()