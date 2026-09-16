#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Script permettant de visualiser la simulation créée en C.
Prend en argument le chemin du csv quui a été créé par la simulation.
Affiche une animation de l'évolution de toutes les particules.

"""

import csv
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

if len(sys.argv) < 2:
    print("Erreur : Mettre en argument le nom du csv")
    sys.exit(1)

FICHIER_CSV = sys.argv[1]

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
    print(lecteur.fieldnames)

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

marge_x = (max(toutes_les_x) - min(toutes_les_x)) * 0.05
marge_y = (max(toutes_les_y) - min(toutes_les_y)) * 0.05

ax.set_xlim(
    min(toutes_les_x) - marge_x,
    max(toutes_les_x) + marge_x
)

ax.set_ylim(
    min(toutes_les_y) - marge_y,
    max(toutes_les_y) + marge_y
)

# ============================================================
# Création des particules
# ============================================================

# Une couleur différente pour chaque particule
couleurs = plt.cm.tab10(range(nb_particules))

points = []

for i in range(nb_particules):
    point, = ax.plot(
        [],
        [],
        "o",
        markersize=8,
        color=couleurs[i],
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
    interval=1,
    blit=True,
    repeat=True
)

plt.show()



