#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 09:58:31 2024

@author: joanny.magat@etu.umontpellier.fr
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

N=200 #Nombre de point dans l'espace
T=1000 #Temps total de l'animation
S = 1 #Facteur de stabilité
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



    
    

    
