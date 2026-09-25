#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: magat-j
joanny.magat@etu.umontpellier.fr

Script permettant de visualiser la simulation Pot_Lenard-Jones_perio.c
Affiche une animation de l'évolution de toutes les particules.

Arguments (optionnels) :
1er argu : Nombre d'intervalle de l'animation (100 par défaut)
2eme argu : Chemin complet du csv simulé

Fac :
/bin/python3 /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/AM/Pot_Lenard-Jones_perio.py

PC portable :
source .venv/bin/activate
"""


# --- bibliothèques ---

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from pathlib import Path
import re
import os
from datetime import datetime


# --- Constantes ---

assert 1 <= len(sys.argv) <= 3, "\n\nErreur : Il faut entre 0 et 2 arguments :"\
"\n\n- 0 : par défaut le nombre d'intervalle de l'animation est 10 et le csv simulé est le plus récent du dossier data."\
"\n\n- 1 : Nombre d'intervalle de l'animation et le csv simulé est le plus récent du dossier data."\
"\n\n- 2 : Nombre d'intervalle de l'animation et chemin complet du csv simulé.\n "

if len(sys.argv) < 3: # 0 ou 1 argument 

    if len(sys.argv) == 2: # 1 argument
        nb_interval = int(sys.argv[1])
    
    else : # 0 argument
        nb_interval = 100
    
    dossier = "data"

    fichier_recent = None
    date_recente = None

    for fichier in os.listdir(dossier):

        # Vérifie que c'est un CSV du bon format
        match = re.match(
            r"^PotLJ_perio_date=(\d+)h_(\d+)min_(\d+)s_(\d+)_(\d+)_(\d+)_N=(\d+)_T=(\d+)_NbLignes=(\d+)_L=(\d+)\.csv$",
            fichier
        )

        if match:
            heure = int(match.group(1))
            minute = int(match.group(2))
            seconde = int(match.group(3))
            jour = int(match.group(4))
            mois = int(match.group(5))
            annee = int(match.group(6))

            date = datetime(annee, mois, jour, heure, minute, seconde)

            jour = match.group(4) #Remet les 0 si on est par ex le 09/09/2026
            mois = match.group(5) #Permet de faire jolie sur le titre du plot

            if date_recente is None or date > date_recente:
                date_recente = date
                fichier_recent = fichier

    nom_csv = f"{dossier}/{fichier_recent}"
    
else : # 2 arguments

    nb_interval = int(sys.argv[1])
    nom_csv = f"{sys.argv[2]}"    


print(f"CSV simulé : {nom_csv}")

match = re.search(r"PotLJ_perio_date=(.*?)_N=(\d+)_T=(\d+)_NbLignes=(\d+)_L=(\d+)\.csv$", nom_csv)

date = match.group(1)
N = int(match.group(2))
T = int(match.group(3))
NbLignes = int(match.group(4))
L = int(match.group(5))



# --- Récupération des positions ---


num_tour = [] #Liste de tous les numéros de tour save dans le csv

x = [[] for t in range(NbLignes)] # liste de liste où x[t][i] est la position x de la particule i au tour t
y = [[] for t in range(NbLignes)] # liste de liste où y[t][i] est la position y de la particule i au tour t

with open(f"{nom_csv}", "r") as fichier:
    
    for ligne in fichier: # chaque ligne a pour colonnes : particule_i,x,y,vx,vy,ax,ay
        
        ligne = ligne.strip()

        if not re.match(r"^//", ligne):
            
            if re.match(r"^#", ligne) :
                match = re.search(r"^###### Tour (\d+) ######$", ligne)
                num_tour.append(int(match.group(1)))
            
            else :
                match = re.match(r"^(\d+),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),", ligne)
                if match:
                    i = int(match.group(1)) #inutile en soit
                    x[len(num_tour)-1].append(float(match.group(2)))
                    y[len(num_tour)-1].append(float(match.group(3)))
                    
x = np.array(x)
y = np.array(y)

print(x)
print(y)

# --- Tracer du plot ---

fig, ax = plt.subplots(figsize=(8, 8))

if len(sys.argv) < 3: # 0 ou 1 argument 
    ax.set_title(
        f"Potentiel de Lenard-Jones (boîte périodique)\nAnimation de la simulation réalisée à {heure}h{minute} le {jour}/{mois}/{annee}",
        fontweight="normal",
        pad=10)

else : # Chemin du csv mis manuellement
    ax.set_title(
        f"Potentiel de Lenard-Jones (boîte périodique)\nAnimation de la simulation du csv :\n{nom_csv}",
        fontweight="normal",
        pad=10)

ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")


# --- limites des axes ---
ax.set_xlim(-L, L)
ax.set_ylim(-L, L)



# Texte indiquant le tour actuel
texte_tour = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12
)

# objet "points" qu'on va déplacer à chaque image
points, = ax.plot([], [], "o", markersize=10)

def init():
    points.set_data([], [])
    texte_tour.set_text("")
    return points,texte_tour

def update(t):
    points.set_data(x[t], y[t])
    texte_tour.set_text(f"tour {num_tour[t]}")
    return points, texte_tour

ani = FuncAnimation(fig, update, frames=len(num_tour),
                    init_func=init, interval=nb_interval, blit=True, repeat=True)

plt.show()



