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

import time
import serial as serial
import numpy as np
from itertools import izip #in python 3 not needed, replace here izip by zip



class ADUC(serial.Serial):
    """
    Classe principale qui va permettre :
    - Free Run
    - Stop
    """
    
    def __init__(self, CLOCK=4178., NUM_TIME_POINTS=256., PRESCALER=1., TIMEBASE=10., TRIGPOSITION=100, TRIGLEVEL=1000, TRIGSLOPE ='+', timeout=2):
        super(serial.Serial, self).__init__()
        self.CLOCK = CLOCK
        self.NUM_TIME_POINTS = NUM_TIME_POINTS
        self.PRESCALER = PRESCALER
        self.TIMEBASE = TIMEBASE
        self.TRIGPOSITION = TRIGPOSITION
        self.TRIGLEVEL = TRIGLEVEL
        self.TRIGSLOPE = TRIGSLOPE
        self.timeout = timeout
        self.data = np.ndarray([])
    
        
        
  
    def open_port(self,entry_port='PORT'):
        """
        Cette fonction permet d'ouvrir le port USB lié à la carte ADUC
        et envoie un message de confirmation d'ouverture. Renvoie un
        TRUE si la commande fonctionne
        """
        print "Ouverture du port"
        
        self.port = entry_port
        print self.port, self.name
        self.baudrate = 38400
								
        self.open() ### affiche des caracteres et fait planter le programme
        print self.isOpen()
        
    def stop(self):
        """
        On définit la fonction stop qui va stopper l'aquisition des données 
        de la carte ADUC
        """
        self.reset_input_buffer()
        self.write('s')
        while True:
            if self.read() == 's':
                break
        print 'succescully stopped'

    def lancement_freerun(self): 
        self.stop()
        self.write('f')
        print self.read()
        self.write2Ndigits(int(self.TIMEBASE*self.CLOCK/self.NUM_TIME_POINTS/self.PRESCALER), 6)
        print self.read2Ndigits(6)
        
    def read2Ndigits(self, number_of_digits=4):
        if(number_of_digits%2!=0):
            print 'number of digits must be even in read2Ndigits'
        bytes_list = self.read(number_of_digits/2)
        return int(''.join([str(ord(byte)).zfill(2) for byte in bytes_list]))
        

    def freerun_carte(self):
        """
        Cette fonction permet de lancer l'aquisition des données de la carte
        ADUC
        """	
        if(self.read()=='d'):
            self.data = self.asciitoint(self.read(512))
            print len(self.data)
        else:
            self.reset_input_buffer()
        return self.data
        
    def lancement_normal(self):
        self.stop()
        self.write('n')
        print self.read()        
        self.write2Ndigits(int(self.TIMEBASE*self.CLOCK/self.NUM_TIME_POINTS/self.PRESCALER), 6)
        print self.read2Ndigits(6)
        self.write2Ndigits(self.TRIGPOSITION, 4)
        print self.read2Ndigits(4)
        self.write2Ndigits(self.TRIGLEVEL, 4)
        print self.read2Ndigits(4)
        self.write(self.TRIGSLOPE)
        print self.read()
        
        
        
        
    def search_for_d(self):
        while self.read(1) != 'd' :
            continue
        print "d detected"
    
    def write2Ndigits(self, string, number_of_digits=4): 
        if(number_of_digits%2!=0):
            print 'number of digits must be even in write2Ndigits'
        strvalue = str(string).zfill(number_of_digits)
        bytes_list = [str(unichr(int(strvalue[i:i+2]))) for i in range(0, number_of_digits, 2)]
        print [ord(byte) for byte in bytes_list]
        for byte in bytes_list:
            self.write(byte)    
               

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
        
        
    