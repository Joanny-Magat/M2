#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:08:03 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

e3) du TP FDTD de M2 (= TP8 de L3)
La lame fait une longueur lambda/2
On applique la FDTD 1D avec E et H séparés

/bin/python3 /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/EM/FDTD_e3.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


##### Constantes #####

c=2.99792458e8
lambda0=1.55e-6 #longueur d'onde telecom, celle de la fibre optique
N_lambda=20 #lambda0/dx
S=1 # Pas magique
T=lambda0/c
omega=2*np.pi/T
tau=2*T #Largeur de la Gausienne
tc=8*T #Centre de la Gausienne
xmin=0
xmax=30*lambda0
dx=lambda0/N_lambda
#nbx = int((xmax -xmin)/dx) +1 # = N
dt=S*dx/c
N=30*N_lambda+1
T_tot=1000

x=np.linspace(xmin,xmax,N)
E=np.linspace(0,0,N)
H=np.linspace(0,0,N)
J=np.ones(N)
M=np.ones(N)

n_air = 1.000272 #Indice de réfraction de l'air
n_lame = 1.45 #Indice de réfraction de la lame diéléctrique
eps=np.ones(N) #Vide en dehors de la lame
eps[int(N/2)-int(lambda0/(4*n_lame*dx)):int(N/2)+int(lambda0/(4*n_lame*dx))+1]=n_lame**2
mu=np.ones(N) #Vide en dehors de la lame
mu[int(N/2)-int(lambda0/(4*n_lame*dx)):int(N/2)+int(lambda0/(4*n_lame*dx))+1]=1
sig=np.ones(N) #sigma
sim=np.ones(N) #sigma*

ca = (1-sig*dt/(2*eps)) / (1+sig*dt/(2*eps))
cb = dt/(dx*eps) / (1+sig*dt/(2*eps))  
da = (1-sim*dt/(2*mu)) / (1+sim*dt/(2*mu))
db = dt/(dx*mu) / (1+sim*dt/(2*mu))


##### Figure #####

fig, ax = plt.subplots(figsize=(16, 10))
lineE, = ax.plot([], [], "blue", label="Champ Ez")
lineH, = ax.plot([], [], "red", label="Champ Hy")
lame, = ax.plot(x, eps, "black")

ax.axvspan(
    x[int(N/2)-int(lambda0/(4*n_lame*dx))-1],
    x[int(N/2)+int(lambda0/(4*n_lame*dx))],
    color="grey",
    alpha=0.35,
    label=r"Lame $\lambda/2$")

ax.set_xlim(xmin, xmax)
ax.set_ylim(-1.2, 1.2)

ax.set_title(
    f"Animation via FDTD du champ Ez et Hy d'un paquet d'onde\nen présence d'une lame de diélectrique d'indice de réfraction n={n_lame}",
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


##### Animation #####

def animate(n):

    tnp = (n+1) * dt
    
    """
    M = M #à faire
    J = J #à faire
    """

    #Calcul des champs au temps n+1
    H[1:N-1] = da[1:N-1]*H[1:N-1] + db[1:N-1]*(E[1:N-1]-E[0:N-2]-M[1:N-1]*dx)
    E[1:N-1] = ca[1:N-1]*E[1:N-1] + cb[1:N-1]*(H[1:N-1]-H[0:N-2]-J[1:N-1]*dx)

    """
    if tnp < 2*tc :
        unp[0] = np.cos(omega*(tnp-tc))*np.exp(-((tnp-tc)/tau)**2)
    
    else :
        unp[0] = un[1]
    
    unp[N-1] = un[N-2]
    """

    lineE.set_data(x, E)
    lineH.set_data(x, H)
    
    return lineE, lineH,
 
ani = animation.FuncAnimation(fig, animate, frames=T_tot,
                              interval=1e-10, blit=True, repeat=False)

ax.legend()
plt.show()