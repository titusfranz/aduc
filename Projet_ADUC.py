# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 16:37:24 2017

@author: Franz et Dubosclard

Programme Projet


"""

import serial as serial
import numpy as np
from itertools import izip #in python 3 not needed, replace here izip by zip

import pylab
from pylab import *


class ADUC(serial.Serial):
    """
    Classe principale qui va permettre :
    - Free Run
    - Stop
    """
    
    """
    def __init__(self):
        self.ser = serial
    """
    
    def stop(self):
        """
        On définit la fonction stop qui va stopper l'aquisition des données 
        de la carte ADUC
        """
        global modus
        modus = False
        self.write('s')
        print self.read(1)

        
    def freerun(self):
        """
        On définit la fonction freerun qui permet de lancer l'aquisition
        des données de la carte ADUC
        """
        global modus
        modus = True
        self.write('f')
        print self.read(1)
        while modus :
            print self.read(1)
            ascii = self.read(512)
            print ascii
            self.asciitoint(ascii)

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


#carte = 0
#carte = ADUC()
#carte.port = 'COM3'
#carte


#carte.open()
#print carte.is_open

#carte.freerun()

#carte.stop()

#carte.close()
#print carte.is_open
