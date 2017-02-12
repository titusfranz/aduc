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

import Projet_ADUC as ADUC



class Realtimeplot(object):
    """
    Cette fonction permet de créer des graphes en temps réel dans l'interface
    graphique
    """
    def __init__(self, timebase=10, bufsize=512):
        self.set_axis(timebase, bufsize)
        
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
        
    def set_axis(self, timebase, bufsize):
        self.bufsize = int(bufsize)
        self.timebase =  float(timebase) #self.sampleinterval*self.bufsize
        self.samplerate = self.bufsize/self.timebase
        
        self.x = np.linspace(-self.timebase, 0.0, self.bufsize)
        self.y = collections.deque(np.zeros(self.bufsize), self.bufsize)
        
        self.x_dsp = np.fft.rfftfreq(self.bufsize, self.samplerate)[1:]
        self.y_dsp = collections.deque(np.zeros(self.bufsize//2), self.bufsize//2)
        
    def __str__(self):
        return 'Realtimeplot() with timebase ' + str(self.timebase) + 'and buffersize ' + str(self.bufsize)
        
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
        self.carte = ADUC.ADUC()
        self.data = np.ndarray([])
    
    data_transfer = pyqtSignal(np.ndarray)
    trigger_settings_transfer = pyqtSignal(int, float, float, float, int, int, str, int)
    started_ok = pyqtSignal()
    mode = pyqtSignal(str)
    
    
    @pyqtSlot(str)
    def open_port(self,portname):
        self.carte.open_port(portname)
    
    @pyqtSlot(str)
    def start(self, mode='normal'):
        self.carte.stop()
        if mode=='normal':
            self.carte.lancement_normal()
        elif mode=='freerun':
            self.carte.lancement_freerun()
        else:
            print mode + ' is no appropriate mode. Please enter either normal or freerun'
        self.acquire_data()
        
        
    @pyqtSlot(np.ndarray)
    def acquire_data(self):
        self.data = self.carte.freerun_carte()
        self.data_transfer.emit(self.data)
        
            
    
    @pyqtSlot()
    def close_port(self):
        """
        Cette fontion va fermer le port de la carte d'aquisition et vérifier
        en renvoyant un FALSE que la commande a été effectué
        """
        print "Fermeture du port"
        self.carte.close()
        print self.carte.is_open  
    
        
        
        
class Interface_Graphique(QWidget):
    def __init__(self, parent = None):
        super(Interface_Graphique, self).__init__()

        self.initUi()
        self.setupThread()
        
        
        self._active = False
        

    def initUi(self):
        self.trig = Panel_Trigger()
        self.realtimeplot = Realtimeplot(self.trig.TIMEBASE/1000., self.trig.NUM_TIME_POINTS)
        self.setWindowTitle("Fenetre Principale")

        self.button_trig = QPushButton('Trigger Options', self)
        self.button_start = QPushButton('START', self) ### Bouton START
        self.button_normal = QPushButton('Normal ON', self) ### Bouton Trigger
        self.button_openport = QPushButton('Ouverture PORT', self) ### Bouton d'ouverture
        self.button_closeport = QPushButton('Fermeture PORT', self) ### Bouton de fermeture						          
        self.entry_port = QLineEdit("/dev/ttyUSB1") ### Case pour entrer le port plus tar remplacer par enter PORT
        self.button_panel = QPushButton('Panel Plot', self) ### Affiche le panel pour le controle de plot
        self.button_quit = QPushButton('Quitter', self) ### Bouton qui permet de quitter l'application
        
        #############################################
        ############ POSITION DES WIDGETS ############
        ################################################################
        
        global grid
        grid = QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.button_start, 0,0)
        grid.addWidget(self.button_normal, 0,1)
        grid.addWidget(self.button_openport, 0,2)
        grid.addWidget(self.button_trig, 1, 0)
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
        self.button_trig.clicked.connect(self.panel_trig)	
        
        self.trig.getdata_button.clicked.connect(self.pass_trigger_settings)
        
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
            qApp.processEvents()
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
        
        
    def pass_trigger_settings(self):
        self.oscilloscope.carte.stop()
        self.trig.get_trigger_settings()
        qApp.processEvents()
        print self.trig.TIMEBASE
        self.oscilloscope.carte.CLOCK = self.trig.CLOCK
        self.oscilloscope.carte.NUM_TIME_POINTS = self.trig.NUM_TIME_POINTS
        self.oscilloscope.carte.PRESCALER = self.trig.PRESCALER
        self.oscilloscope.carte.TIMEBASE = self.trig.TIMEBASE
        self.oscilloscope.carte.TRIGPOSITION = self.trig.TRIGPOSITION
        self.oscilloscope.carte.TRIGLEVEL = self.trig.TRIGLEVEL
        self.oscilloscope.carte.TRIGSLOPE = self.trig.TRIGSLOPE
        self.oscilloscope.carte.timeout = self.trig.timeout
        #self.oscilloscope.carte.baudrate = self.trig.baudrate
        self.realtimeplot.set_axis(self.trig.TIMEBASE/1000., self.trig.NUM_TIME_POINTS)
        self.trig.close()
        
        
    def panel_trig(self):
        self.trig.show()    

    def button_quit_command(self):
        """
        Cette fonction permet de quitter l'interface graphique proprement
        """
        app.kernel.do_shutdown(True)  
        self.close()
								
class Panel_Trigger(QWidget):
    """
    Cette classe va permettre la création du panel de contrôle de plot
    """
    
    def __init__(self, baudrate=38400, CLOCK=4178., NUM_TIME_POINTS=256., PRESCALER=1., TIMEBASE=10., TRIGPOSITION=100, TRIGLEVEL=1000, TRIGSLOPE ='+', timeout=2):
        super(Panel_Trigger, self).__init__()
        
        self.CLOCK = CLOCK
        self.NUM_TIME_POINTS = NUM_TIME_POINTS
        self.PRESCALER = PRESCALER
        self.TIMEBASE = TIMEBASE
        self.TRIGPOSITION = TRIGPOSITION
        self.TRIGLEVEL = TRIGLEVEL
        self.TRIGSLOPE = TRIGSLOPE
        self.timeout = timeout
        self.baudrate = baudrate
        
        
        self.setWindowTitle("Contrôle du mode Trigger")
		
        self.clock_lineEdit = QLineEdit(str(CLOCK)) ### Modification parametre Clock
        self.clock_button = QLabel('CLOCK', self)
								
        self.num_time_point_lineEdit = QLineEdit(str(NUM_TIME_POINTS)) 
        self.num_time_point_button = QLabel('NUM_TIME_POINT', self)

        self.baudrate_lineEdit = QLineEdit(str(baudrate))
        self.baudrate_button = QLabel('BAUDRATE', self)

        self.prescaler_lineEdit = QLineEdit(str(PRESCALER))
        self.prescaler_button = QLabel('PRESCALER', self)

        self.timebase_lineEdit = QLineEdit(str(TIMEBASE))
        self.timebase_button = QLabel('TIMEBASE', self)

        self.trigposition_lineEdit = QLineEdit(str(TRIGPOSITION))
        self.trigposition_button = QLabel('TRIGPOSITION', self)

        self.triglevel_lineEdit = QLineEdit(str(TRIGLEVEL))
        self.triglevel_button = QLabel('TRIGLEVELE', self)

        self.trigslope_lineEdit = QLineEdit(str(TRIGSLOPE))						
        self.trigslope_button = QLabel('TRIGSLOPE', self)	
        
        self.getdata_button = QPushButton('Apply settings')

        global grid
        grid = QGridLayout() ### Ouverture de la grid (matrice)
        self.setLayout(grid)
        
        grid.addWidget(self.clock_button, 0,0)
        grid.addWidget(self.clock_lineEdit, 0,1)
        grid.addWidget(self.num_time_point_button, 1,0)
        grid.addWidget(self.num_time_point_lineEdit, 1,1)
        grid.addWidget(self.baudrate_button, 2, 0)
        grid.addWidget(self.baudrate_lineEdit, 2,1)     
        grid.addWidget(self.prescaler_button, 3, 0)
        grid.addWidget(self.prescaler_lineEdit, 3, 1)
        grid.addWidget(self.timebase_button, 4, 0)
        grid.addWidget(self.timebase_lineEdit, 4,1)
        grid.addWidget(self.trigposition_button, 5, 0)
        grid.addWidget(self.trigposition_lineEdit, 5,1)        
        grid.addWidget(self.triglevel_button, 6,0)
        grid.addWidget(self.triglevel_lineEdit, 6,1)
        grid.addWidget(self.trigslope_button, 7,0)							
        grid.addWidget(self.trigslope_lineEdit, 7,1)	
        grid.addWidget(self.getdata_button,8,0)
        
    def get_trigger_settings(self):
        self.CLOCK = float(self.clock_lineEdit.text())
        self.NUM_TIME_POINTS = float(self.num_time_point_lineEdit.text())
        self.PRESCALER = float(self.prescaler_lineEdit.text())
        self.TIMEBASE = float(self.timebase_lineEdit.text())
        self.TRIGPOSITION = int(self.trigposition_lineEdit.text())
        self.TRIGLEVEL = int(self.triglevel_lineEdit.text())
        self.TRIGSLOPE = str(self.trigslope_lineEdit.text())
        self.timeout = 2 
        self.baudrate = int(self.baudrate_lineEdit.text())
        
   
        
        
        				
if __name__ == "__main__":
    system = QApplication(sys.argv)
    graphique = Interface_Graphique()		
    graphique.show()
    sys.exit(system.exec_())