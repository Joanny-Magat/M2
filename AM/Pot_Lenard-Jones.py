#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Script permettant de visualiser la simulation créée en C.
Prend en argument le chemin du csv quui a été créé par la simulation.
Affiche une animation de l'évolution de toutes les particules.

"""

import numpy as np
import matplotlib.pyplot as plt

tmin = 0
tmax = 4
nbt = 41
dt = (tmax-tmin) / (nbt-1)

xmin = -3
xmax = 13
nbx = 161

x = np.linspace(xmin, xmax, nbx)


for i in range(T):

    t = i * dt
    y = x + t

    if i == 0:
        line, = plt.plot(x, y)
        #Astuce Python : l, permet de prendre directement l'élément de la liste à un élément [a]
    else:
        line.set_data(x, y)
    plt.pause(0.04) # pause avec duree en secondes
    
plt.show()



