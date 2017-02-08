# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 16:37:24 2017
@author: Titus Franz, William Dubosclard
PROGRAMME DRIVERS :
Utilise les commandes de la carte ADUC et les envoie sur le
projet de l'interface graphique
Le Futur :
- Création d'une fenêtre pour y stocker la possibilitée de changer la taille
de la fenêtre de plot --> Création d'un widget spécial
- Insértion d'un graphe qui va calculer la DSP, en premier lieu avec un plot fixe
puis, avec un plot déroulant --> Création d'une classe DSP (dans Projet ADUC ??)
"""

import serial as serial
import numpy as np
from itertools import izip #in python 3 not needed, replace here izip by zip

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from interface_graphique_PyQt4_V3 import Realtimeplot


class ADUC(serial.Serial):
    """
    Classe principale qui va permettre :
    - Free Run
    - Stop
    """
    
    
    def __init__(self):
        super(serial.Serial, self).__init__()
        
  
    def open_port(self,entry_port='PORT'):
        """
        Cette fonction permet d'ouvrir le port USB lié à la carte ADUC
        et envoie un message de confirmation d'ouverture. Renvoie un
        TRUE si la commande fonctionne
        """
        print "Ouverture du port"
        
        self.port = entry_port
        print self.port, self.name
        self.baudrate = 115200
								
        self.open() ### affiche des caracteres et fait planter le programme
        print self.is_open
    def stop(self):
        """
        On définit la fonction stop qui va stopper l'aquisition des données 
        de la carte ADUC
        """
        self.write('s')
        print self.read(1)

    def lancement_freerun(self):        
        self.write('f')
        print self.read(1)
        

    def freerun_carte(self):
        """
        Cette fonction permet de lancer l'aquisition des données de la carte
        ADUC
        """				
        self.inwaiting()
        ascii = self.read(512)
        #print carte.asciitoint(ascii)
        data = self.asciitoint(ascii)
        return data
        
    def normal_carte(self):
        self.write('n')
        print self.read(1)
        
        self.write2Ndigits(164589, 6)
        print 'the card answers ', self.read()
        
        #print 'in the buffer is', self.asciitoint(self.read())
        
        self.stop()
        
        
    def inwaiting(self):
        while self.read(1) != 'd' :
            continue
        print "d detected"
    
    def write2Ndigits(self,size,aucuneidee):
        ascii = ''
        size = str(size)
        for i in range(0, aucuneidee, 2):
            ascii = ascii + chr(int(size[i:i+2]))
        print 'the ascii of ', size, ' is ', ascii
        self.write(ascii)
            

    def asciitoint(self, ascii):
        raw = iter(map(ord, ascii)) 
        """       
        creates a list of all ASCII-numbers, 
        eg from ASCII to (62, 96, 21, 99, 74, 80) and transforms it to an
        iteratable object
        """
        data = np.array([x*100 + y for x,y in izip(raw,raw)]) 
        return data
        """      
        zips the list to a list of tuples,
        e.g (62, 96, 21, 99, 74, 80) to ((62, 96),(21, 99), (74, 80)) and
        transforms each tuple to one number, eg (6296, 2199, 7480)
        note: in python 3 izip may be replaced by zip
        """
        
    def dsp(self, data):
        N = len(data)
        dsp = np.abs(np.fft.fft(data))**2/N
        return dsp
        

