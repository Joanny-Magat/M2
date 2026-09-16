#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:08:03 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

TP FDTD de M2
"""

# c) du TP M2

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

n1 = 1 #Indice de réfraction dans le vide

for i in range(N): #Ici la boucle ne sert à rien mais c'est pour les questions suivantes
    esp_r[i]=n1**2

fig, ax = plt.subplots(figsize=(10, 6)) #largeur, hauteur
line, = ax.plot([], [], "blue") #label="Paquet d'onde"

#Centrage de la fenetre de la figure
manager = plt.get_current_fig_manager()
window = manager.window

screen = window.screen().availableGeometry()

window.move(
    (screen.width() - window.width()) // 2,
    (screen.height() - window.height()) // 2)

ax.set_xlim(xmin, xmax)
ax.set_ylim(-1.2, 1.2)

ax.set_title(
    f"Animation via FDTD d'un paquet d'onde\ndans un milieu diélectrique d'indice de réfraction n={n1}",
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
plt.show()