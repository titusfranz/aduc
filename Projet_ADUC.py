# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 16:37:24 2017

@author: Franz et Dubosclard

Programme Projet


"""

import serial as serial
import numpy as np
from itertools import izip #in python 3 not needed, replace here izip by zip

class ADUC():
    """
    Classe principale qui va permettre :
    - Free Run
    - Stop
    """
    def

    def stop(self):
        """
        On définit la fonction stop qui va stopper l'aquisition des données 
        de la carte ADUC
        """
        global modus
        modus = 's'
        self.write('s')
        print self.read(1)
        
    def freerun(self):
        """
        On définit la fonction freerun qui permet de lancer l'aquisition
        des données de la carte ADUC
        """
        global modus
        modus = 'f'
        self.write('f')
        print self.read(1)
        while modus == 'f':
            print self.read(1)
            ascii =  self.read(512)
            print ascii
            asciitoint(ascii)
    
    def asciitoint(ascii):
        raw = iter(map(ord, ascii)) #creates a list of all ASCII-numbers, 
        # eg from R?:! to [62, 96, 21, 99, 74, 80] and transforms it to an
        # iteratable object
        data = np.array([x*100 + y for x,y in izip(raw,raw)] # zips the list to a list of tuples,
        # e.g [62, 96, 21, 99, 74, 80] to [(62, 96),(21, 99), (74, 80)] and
        # transforms each tuple to one number, eg [6296, 2199, 7480]
        # note: in python 3 izip may be replaced by zip
        
        
carte = ADUC()
carte.port = 'COM3'
carte
print carte.name

carte.baudrate = 115200

carte.open()
print carte.is_open

# carte.freerun()

carte.stop()

carte.close()
print carte.is_open

