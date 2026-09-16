#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 08:45:19 2026

@author: magat-j

2e Cours de Simu EM :
    - Tracer de fonctions à 2 variables
"""

#%% Exemple : visualisation de la fonction sinus cardinal

"""
Je ne vais utiliser que le style POO pour utiliser Pyplot
"""

import numpy as np
import matplotlib.pyplot as plt

epsilon = np.finfo(float).eps
print("epsilon =", epsilon)

xmin = -8
xmax = 8
nbx = 41
ymin = -8
ymax = 8
nby = 41

x = np.linspace(xmin, xmax, nbx)
y = np.linspace(ymin, ymax, nby)
X, Y = np.meshgrid(x, y)

R = np.sqrt(X**2 + Y**2) + epsilon
Z = np.sin(R) / R

fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation="bicubic", 
               origin="lower", extent=[xmin,xmax,ymin,ymax])
fig.colorbar(im)

plt.show()

#%% Exemple perso pour une image : rendre une image grise

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open("/skole/nas-edu/home0/mpn1/magat-j/Images/zelda.jpg")

fig, axes = plt.subplots(2,1)
img_couleur = axes[0].imshow(image)

data = img_couleur.get_array()
gris = (
    0.299 * data[:, :, 0] #Le tableau R tout entier
    + 0.587 * data[:, :, 1] #Le tableau G tout entier
    + 0.114 * data[:, :, 2] #Le tableau B tout entier
)
data_gris = np.stack( #Stack fait un array mais avec la dim 3 du RGB à la fin
    [gris, gris, gris],    #C'est donc mieux qu'un simple np.array
    axis=2
).astype(np.uint8) #Convertit en entier les valeurs RGB

img_gris = axes[1].imshow(data_gris)

axes[0].axis("off")
axes[1].axis("off")
plt.show()

#%% TP visualisation : a)

import numpy as np
import matplotlib.pyplot as plt

epsilon = np.finfo(float).eps

xmin = -6
xmax = 6
nbx = 121

x = np.linspace(xmin, xmax, nbx)
y = ( np.sin(x+epsilon)/(x+epsilon) ) * np.sqrt(1+x**2)

fig, ax = plt.subplots()
ax.plot(x,y)
plt.show()

#%% TP visualisation : b)

import numpy as np
import matplotlib.pyplot as plt

xmin = -2
xmax = 2
xpas = 0.2
nbx = int((xmax-xmin)/xpas + 1)

ymin = -7
ymax = 7
ypas = 0.5
nby = int((ymax-ymin)/ypas + 1)

x = np.linspace(xmin, xmax, nbx)
y = np.linspace(ymin, ymax, nby)
X, Y = np.meshgrid(x, y)
Z = np.log(3*X**2+Y**2+1)

fig, ax = plt.subplots()
im = ax.imshow(Z, interpolation="bicubic", 
               origin="lower", extent=[xmin,xmax,ymin,ymax])
fig.colorbar(im)
plt.show()

#%% TP visualisation : c)

import numpy as np
import matplotlib.pyplot as plt


##### DONNEES #####

x = np.linspace(-3, 3, 101)
z = np.exp(-2j*np.pi*x) * np.exp(-(x**2))

X = np.array([x,x])

y0 = np.zeros(len(x))
y = np.abs(z)
Y = np.array([y0,y])

Z = np.array([z,z])
C = np.angle(Z)


##### TRACER DE LA FIGURE #####

fig, ax = plt.subplots()
ax.plot(x, y, "k") #"k" est un raccourci pour color="black"
mesh = ax.pcolormesh(X, Y, C, shading="gouraud", cmap=plt.cm.hsv, vmin=-np.pi, vmax=np.pi)
cbar = fig.colorbar(mesh, ax=ax, orientation="vertical", pad=0.05)


##### PERSONNALISATION DE LA FIGURE #####

ax.set_title(
    r"Tracer de $\mathbf{f(x) = e^{-i2\pi x} \times e^{-x^2}}$",
    fontsize=18,
    fontweight="normal", #Mettre "bold" pour du gras
    pad=20)
ax.set_xlabel(
    "x",
    fontsize=13,
    rotation=0,
    labelpad=5)
ax.set_ylabel(
    r"$\left| z \right|$",
    fontsize=13,
    rotation=0,
    labelpad=10)
ax.set_aspect(6) # Rapport Y/X
ax.set_xlim(-3, 3)
ax.set_ylim(0, 1.01)

cbar.set_label(
    "arg(z)",
    fontsize=13,
    rotation=0,
    labelpad=20)
cbar.ax.tick_params(
    labelsize=10)

"""
ax.set_xticks(np.arange(-5, 6, 1))
ax.set_yticks(np.arange(-4, 5, 1))

ax.tick_params(
    axis="both",
    which="major",
    labelsize=11,
    length=6,
    width=1.2
)
"""

"""
ax.grid(
    True,
    linestyle="--",
    linewidth=0.6,
    alpha=0.4)
"""

plt.show()










































































