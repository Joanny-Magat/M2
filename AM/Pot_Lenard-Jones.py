#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: magat-j
joanny.magat@etu.umontpellier.fr

Script permettant de visualiser la simulation créée en C.
Prend en 1er argument le chemin du csv quui a été créé par la simulation.
Prend en 2eme argument le nombre d'interval de l'animation
Affiche une animation de l'évolution de toutes les particules.

/bin/python3 /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/AM/Pot_Lenard-Jones.py /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/AM/Pot_LJ_N=5_T=1000_date=14h_05min_24s_17_09_2026.csv

"""

import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

if len(sys.argv) < 3:
    print("Erreur : Mettre en argument le nom du csv et le nombre d'interval de l'animation")
    sys.exit(1)

FICHIER_CSV = sys.argv[1]
nb_interval = int(sys.argv[2])

# ============================================================
# Lecture du CSV
# ============================================================

tours = []

# positions[i] = [(x, y), (x, y), ...] pour la particule i
positions = []

# vitesses[i] = [(vx, vy), (vx, vy), ...] pour la particule i
vitesses = []

with open(FICHIER_CSV, "r", newline="", encoding="utf-8-sig") as fichier:
    lecteur = csv.DictReader(
    ligne for ligne in fichier
    if ligne.strip() and not ligne.strip().startswith("//"))

    # Récupération automatique du nombre de particules
    noms_colonnes = lecteur.fieldnames

    nb_particules = sum(
        1 for colonne in noms_colonnes
        if colonne.startswith("x")
    )

    positions = [[] for _ in range(nb_particules)]
    vitesses = [[] for _ in range(nb_particules)]

    for ligne in lecteur:
        tours.append(int(ligne["Tour"]))

        for i in range(nb_particules):
            x = float(ligne[f"x{i}"])
            y = float(ligne[f"y{i}"])
            vx = float(ligne[f"vx{i}"])
            vy = float(ligne[f"vy{i}"])

            positions[i].append((x, y))
            vitesses[i].append((vx, vy))

# ============================================================
# Création de la figure
# ============================================================

fig, ax = plt.subplots(figsize=(9, 7))

ax.set_title("Animation des particules")
ax.set_xlabel("Position X")
ax.set_ylabel("Position Y")

ax.grid(True, alpha=0.3)
ax.set_aspect("equal", adjustable="box")

# ============================================================
# Détermination des limites de l'animation
# ============================================================

toutes_les_x = []
toutes_les_y = []

for i in range(nb_particules):
    for x, y in positions[i]:
        toutes_les_x.append(x)
        toutes_les_y.append(y)


ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)

# ============================================================
# Création des particules
# ============================================================


points = []

for i in range(nb_particules):
    point, = ax.plot(
        [],
        [],
        "o",
        markersize=8,
        color="red",
        label=f"Particule {i}"
    )

    points.append(point)

#ax.legend()

# Texte indiquant le tour actuel
texte_tour = ax.text(
    0.02,
    0.95,
    "",
    transform=ax.transAxes,
    fontsize=12
)

# ============================================================
# Fonction d'initialisation
# ============================================================

def init():
    for point in points:
        point.set_data([], [])

    texte_tour.set_text("")

    return points + [texte_tour]


# ============================================================
# Fonction appelée à chaque image
# ============================================================

def update(frame):
    for i in range(nb_particules):
        x, y = positions[i][frame]

        points[i].set_data([x], [y])

    texte_tour.set_text(f"Tour : {tours[frame]}")

    return points + [texte_tour]


# ============================================================
# Création de l'animation
# ============================================================

animation = FuncAnimation(
    fig,
    update,
    frames=len(tours),
    init_func=init,
    interval=nb_interval,
    blit=True,
    repeat=True
)

plt.show()



