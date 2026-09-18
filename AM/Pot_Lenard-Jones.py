#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: magat-j
joanny.magat@etu.umontpellier.fr

Script permettant de visualiser la simulation créée en C.
Prend en argument le nombre d'interval de l'animation
Affiche une animation de l'évolution de toutes les particules.

/bin/python3 /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/AM/Pot_Lenard-Jones.py /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/AM/Pot_LJ_N=5_T=1000_date=14h_05min_24s_17_09_2026.csv

"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys
from pathlib import Path
import re

if len(sys.argv) < 2:
    print("Erreur : Mettre en argument le nom du csv et le nombre d'interval de l'animation")
    sys.exit(1)

nb_interval = int(sys.argv[1])

dossier = "data"
num_tour = []

for f in Path(dossier).iterdir() :
    if f.is_file() :
        num_tour.append(int(re.search(r'tour_(\d+)\.csv$', str(f)).group(1)))

num_tour.sort()
num_tour = np.array(num_tour)


# --- charge tous les fichiers : positions x et y de chaque tours ---
x = []
y = []
for t in num_tour:
    data = np.loadtxt(f"{dossier}/tour_{t}.csv", delimiter=",", skiprows=1)
    # chaque csv a une ligne par particule, colonnes : i,x,y,vx,vy
    x.append(data[:, 1])   # colonne x
    y.append(data[:, 2])   # colonne y
x = np.array(x)
y = np.array(y)


fig, ax = plt.subplots()

ax.set_aspect("equal")
ax.set_xlabel("x")
ax.set_ylabel("y")

# --- limites des axes : on prend les min/max sur toute la simu ---
#ax.set_xlim(x.min() - 0.1, x.max() + 0.1)
#ax.set_ylim(y.min() - 0.1, y.max() + 0.1)

ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

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



