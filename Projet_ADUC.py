# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 16:37:24 2017

@author: Franz et Dubosclard

Programme Projet


"""

import serial as serial

class ADUC(serial.Serial):
    """
    Classe principale qui va permettre :
    - Free Run
    - Stop
    """

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
            print self.read(512)

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

