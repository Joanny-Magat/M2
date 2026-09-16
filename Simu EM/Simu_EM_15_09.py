#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:24:47 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

FDTD comme en L3 :
    - littéralement le code de L3 
    - Deux courbes sur le meme plot
"""

#%% FDTD exo 1 (L3)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=200 #Nombre de point dans l'espace
T=1000 #Temps total de l'animation
S = 1 #Facteur de stabilité car si S > 1 l'onde diverge
dt=0.01
c=1
dx=c*dt/S # S = c*dt / dx
xmin=0
xmax= xmin + (N-1)*dx
x=np.linspace(xmin,xmax,N)

unm=np.linspace(0,0,N)
un=np.linspace(0,0,N)
unp=np.linspace(0,0,N)



fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-1.2, 1.2)

def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1,N-1):
        unp[i]= S**2 * (un[i+1]-2*un[i]+un[i-1]) \
                + 2*un[i] - unm[i]                # le \ permet de continuer la meme ligne en allant à la ligne dans le script
    
    if 10*dt < tnp < 20*dt:
        unp[0]=1
    else:
        unp[0]=0
        
    line.set_data(x, unp)
    unm[:]=un[:]
    un[:]=unp[:]
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=T,
                              interval=10, blit=True, repeat=False)
plt.show()


#%% FDTD exo 2 (L3)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=200 #Nombre de point dans l'espace
T=1000 #Temps total de l'animation
S = 0.5 #Facteur de stabilité != 1 donc il y a des perturbations
dt=0.01
c=1
dx=c*dt/S
xmin=0
xmax= xmin + (N-1)*dx
x=np.linspace(xmin,xmax,N)

unm=np.linspace(0,0,N)
un=np.linspace(0,0,N)
unp=np.linspace(0,0,N)



fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(-1.2, 1.2)

def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1,N-1):
        unp[i]= S**2 * (un[i+1]-2*un[i]+un[i-1]) +2*un[i] -unm[i]
    
    tc=1
    tau=0.1
    unp[0]=np.exp(-((tnp-tc)/tau)**2)
        
    line.set_data(x, unp)
    unm[:]=un[:]
    un[:]=unp[:]
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=T,
                              interval=10, blit=True, repeat=False)
plt.show()


#%% FDTD Gausienne avec deux plots en meme temps

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=200 #Nombre de point dans l'espace
T=1000 #Temps total de l'animation
S0 = 0.9
S1 = 1
dt=0.01
c=1
dx0=c*dt/S0
dx1=c*dt/S1
xmin=0
xmax0= xmin + (N-1)*dx0
xmax1= xmin + (N-1)*dx1
x0=np.linspace(xmin,xmax0,N)
x1=np.linspace(xmin,xmax1,N)

unm0=np.linspace(0,0,N)
un0=np.linspace(0,0,N)
unp0=np.linspace(0,0,N)
unm1=np.linspace(0,0,N)
un1=np.linspace(0,0,N)
unp1=np.linspace(0,0,N)


fig, ax = plt.subplots(2,1)
line0, = ax[0].plot([], [], "blue")
line1, = ax[1].plot([], [], "red")
ax[0].set_xlim(xmin, xmax1)
ax[0].set_ylim(-1.2, 1.2)
ax[1].set_xlim(xmin, xmax1)
ax[1].set_ylim(-1.2, 1.2)

def animate(n): 
    tnp = (n+1) * dt
    
    for i in range(1,N-1):
        unp0[i]= S0**2 * (un0[i+1]-2*un0[i]+un0[i-1]) +2*un0[i] -unm0[i]
        unp1[i]= S1**2 * (un1[i+1]-2*un1[i]+un1[i-1]) +2*un1[i] -unm1[i]
    
    tc=1 # Centre de la gausienne
    tau=0.1 # Largeur de la gausienne
    unp0[0]=np.exp(-((tnp-tc)/tau)**2)
    unp1[0]=np.exp(-((tnp-tc)/tau)**2)
        
    line0.set_data(x0, unp0)
    line1.set_data(x1, unp1)
    
    unm0[:]=un0[:]
    un0[:]=unp0[:]
    unm1[:]=un1[:]
    un1[:]=unp1[:]
    
    return line0,line1,
 
ani = animation.FuncAnimation(fig, animate, frames=T,
                              interval=10, blit=True, repeat=False)


plt.show()



#%% FDTD Gausienne avec deux courbes en meme temps sur le meme plot

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=200 #Nombre de point dans l'espace
T=1000 #Temps total de l'animation
S0 = 0.9
S1 = 1
dt=0.01
c=1
dx0=c*dt/S0
dx1=c*dt/S1
xmin=0
xmax0= xmin + (N-1)*dx0
xmax1= xmin + (N-1)*dx1
x0=np.linspace(xmin,xmax0,N)
x1=np.linspace(xmin,xmax1,N)

unm0=np.linspace(0,0,N)
un0=np.linspace(0,0,N)
unp0=np.linspace(0,0,N)
unm1=np.linspace(0,0,N)
un1=np.linspace(0,0,N)
unp1=np.linspace(0,0,N)


fig, ax = plt.subplots()
line0, = ax.plot([], [], "blue", label=f"S = {S0}")
line1, = ax.plot([], [], "red", label=f"S = {S1}")

ax.set_xlim(xmin, xmax1)
ax.set_ylim(-1.2, 1.2)

ax.set_title(
    r"Animation d'une gausienne via FDTD avec deux valeurs de S différentes",
    fontweight="normal", #Mettre "bold" pour du gras
    pad=20)
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
        unp0[i]= S0**2 * (un0[i+1]-2*un0[i]+un0[i-1]) +2*un0[i] -unm0[i]
        unp1[i]= S1**2 * (un1[i+1]-2*un1[i]+un1[i-1]) +2*un1[i] -unm1[i]
    
    tc=1 # Centre de la gausienne
    tau=0.1 # Largeur de la gausienne
    unp0[0]=np.exp(-((tnp-tc)/tau)**2)
    unp1[0]=np.exp(-((tnp-tc)/tau)**2)
        
    line0.set_data(x0, unp0)
    line1.set_data(x1, unp1)
    
    unm0[:]=un0[:]
    un0[:]=unp0[:]
    unm1[:]=un1[:]
    un1[:]=unp1[:]
    
    return line0,line1,
 
ani = animation.FuncAnimation(fig, animate, frames=T,
                              interval=10, blit=True, repeat=False)

ax.legend()
plt.show()












