#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:08:03 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

TP FDTD de M2
"""

# e) du TP M2 (= TP8 de L3)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

c=2.99792458e8
lambda0=1.55e-6 #longueur d'onde telecom, celle de la fibre optique
N_lambda=20
S=0.9
T=lambda0/c
omega=2*np.pi/T
tau=3*T
tc=8*T
xmin=0
xmax=30*lambda0
dx=lambda0/N_lambda
dt=S*dx/c
N=30*N_lambda+1
T_tot=10000

x=np.linspace(xmin,xmax,N)
unm=np.linspace(0,0,N)
un=np.linspace(0,0,N)
unp=np.linspace(0,0,N)

#Permittivité relative
esp_r=np.ones(N) #Vide en dehors de la lame

#Indice de réfraction de la lame diéléctrique
n_lame = 1.45

for i in range(N):
    if N/3 < i < 2/3*N: # Largeur de la lame
        esp_r[i]=n_lame**2

fig, ax = plt.subplots(figsize=(10, 6))
line, = ax.plot([], [], "blue") #label="Paquet d'onde"
espr, = ax.plot(x, esp_r, "red")

"""
#Centrage de la fenetre de la figure
manager = plt.get_current_fig_manager()
window = manager.window

screen = window.screen().availableGeometry()

window.move(
    (screen.width() - window.width()) // 2,
    (screen.height() - window.height()) // 2)
"""

ax.set_xlim(xmin, xmax)
ax.set_ylim(-1.2, 1.2)

ax.set_xlim(xmin, xmax)
ax.set_ylim(-1.2, 1.2)

ax.axvline(
    x=x[int(N/3)],
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Lame allant de  x = {x[int(N/3)]} à x = {x[int(2/3*N)]}")
ax.axvline(
    x=x[int(2/3*N)],
    color="red",
    linestyle="--",
    linewidth=2)

ax.set_title(
    f"Animation via FDTD d'un paquet d'onde\nen présence d'une lame de diélectrique d'indice de réfraction n={n_lame}",
    fontweight="normal",
    pad=10)
ax.set_xlabel(
    "x",
    fontsize=13,
    rotation=0,
    labelpad=5)
ax.set_ylabel(
    r"f(x)",
    fontsize=13,
    rotation=0,
    labelpad=10)

def animate(n): 
    
    tnp = (n+1) * dt
    
    for i in range(1,N-1):
        unp[i]= S**2 / esp_r[i] * (un[i+1]-2*un[i]+un[i-1]) + 2*un[i] - unm[i]
    
    unp[0]=np.cos(omega*(tnp-tc))*np.exp(-((tnp-tc)/tau)**2)
        
    line.set_data(x, unp)
    unm[:]=un[:]
    un[:]=unp[:]
    
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=T_tot,
                              interval=1, blit=True, repeat=False)
ax.legend()
plt.show()