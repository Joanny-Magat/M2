import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

NBPAS = 1000          # nombre de fichiers
DOSSIER = "data"

# --- charger tous les fichiers : positions x et y de chaque pas ---
xs, ys = [], []
for t in range(NBPAS):
    data = np.loadtxt(f"{DOSSIER}/etat_{t}.csv", delimiter=",", skiprows=1)
    # data a une ligne par particule, colonnes : i,x,y,vx,vy,ax,ay,fx,fy
    xs.append(data[:, 1])   # colonne x
    ys.append(data[:, 2])   # colonne y
xs = np.array(xs)
ys = np.array(ys)

# --- limites des axes : on prend les min/max sur toute la simu ---
fig, ax = plt.subplots()
ax.set_xlim(xs.min() - 0.1, xs.max() + 0.1)
ax.set_ylim(ys.min() - 0.1, ys.max() + 0.1)
ax.set_aspect("equal")
ax.set_xlabel("x"); ax.set_ylabel("y")

# objet "points" qu'on va déplacer à chaque image
points, = ax.plot([], [], "o", markersize=10)

def init():
    points.set_data([], [])
    return points,

def update(t):
    points.set_data(xs[t], ys[t])
    ax.set_title(f"pas {t}")
    return points,

ani = FuncAnimation(fig, update, frames=NBPAS,
                    init_func=init, interval=20, blit=True)

plt.show()