# -*- coding: utf-8 -*-
"""
Created on Thu Jan 05 19:48:23 2017

@author: DragoMagnus

Interface Graphique TKinter - Projet

"""

import Tkinter as tk
import matplotlib

fenetre = tk.Tk()
label = tk.Label(fenetre, text="Interface ADUC").pack()


"""
Case à cocher qui indique le port.
Si la case est coché alors le port est ouvert, dans le cas contraire le port
est fermé. Un message sera envoyé
"""
open_port = tk.Checkbutton(fenetre, text="Port USB").pack(side=tk.LEFT)


"""
Case qui permet d'entrer le numero de port usb auquel est
connecté la carte ADUC
"""
usb_value = tk.StringVar()
usb_value.set("Entrer le port USB")
entry_usb = tk.Entry(fenetre, textvariable=usb_value, width=30).pack(side=tk.LEFT)


"""
Création des boutons START et STOP qui
permettrons le lancement ou l'arret de l'aquisition des données
"""
start_button = tk.Button(fenetre, text="START", command=fenetre.quit).pack(side=tk.RIGHT, padx=5, pady=5)
stop_button = tk.Button(fenetre, text="STOP", command=fenetre.quit).pack(side=tk.RIGHT, padx=5, pady=5)



"""
Création d'une fenêtre qui permettra d'afficher le plot
de données de la carte ADUC
"""
tk.Canvas(fenetre, width=250, height=50, bg='black').pack(side=tk.BOTTOM, padx=5, pady=5)


fenetre.mainloop() 