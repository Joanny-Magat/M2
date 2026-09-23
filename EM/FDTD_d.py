#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:08:03 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

TP FDTD de M2
"""

# d) du TP M2

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
T_tot=1000

x=np.linspace(xmin,xmax,N)
unm=np.linspace(0,0,N)
un=np.linspace(0,0,N)
unp=np.linspace(0,0,N)

#Permittivité relative
esp_r=np.ones(N)

n1 = 1.000272 #Indice de réfraction de l'air (Atmosphère terrestre à 20 °C et 1 atm)
n2 = 1.45

r_theo = (n1 - n2) / (n1 + n2)
t_theo = (2*n1) / (n1 + n2)

Ei = "Pas encore calculé"
Er = "Pas encore calculé"
Et = "Pas encore calculé"
r_exp = "Pas encore calculé"
t_exp = "Pas encore calculé"

for i in range(N): #Ici la boucle ne sert à rien mais c'est pour les questions suivantes
    if i < N/2 :
        esp_r[i]=n1**2
    else :
        esp_r[i]=n2**2


fig, ax = plt.subplots(figsize=(14, 6)) #largeur, hauteur
line, = ax.plot([], [], "black") #label="Paquet d'onde"

fig.subplots_adjust(
    left=0.08,
    right=0.65,
    top=0.90,
    bottom=0.10) #Met le graphe à gauche pour avoir la place de mettre les légendes à droite

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

milieu = int(N/2)
gg = int(N/4 - N/6)
gd = int(N/4 + N/6)
dg = int(3*N/4 - N/6)
dd = int(3*N/4 + N/6)

ax.axvline(
    x=x[milieu],
    color="black",
    linestyle="--",
    linewidth=1,
    label=f"Dioptre séparant les deux milieux\nen  x = {x[milieu]:.2e}")

ax.axvspan(
    x[gg],
    x[gd],
    color="blue",
    alpha=0.35,
    label=f"Zone où est mesurée le max de l'amplitude\nde l'onde incidente puis de celle réfléchie\n(x de {x[gg]:.2e} à {x[gd]:.2e})")

ax.axvspan(
    x[dg],
    x[dd],
    color="red",
    alpha=0.35,
    label=f"Zone où est mesurée le max de l'amplitude\nde l'onde transmise\n(x de {x[dg]:.2e} à {x[dd]:.2e})")

ax.set_title(
    f"Animation via FDTD d'un paquet d'onde dans deux milieux diélectriques\nd'indice de réfraction n1 = {n1} (air) et n2 = {n2}",
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


legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.01, 1.015))
legend.get_frame().set_edgecolor("grey")

#Zone de texte
ax_txt = fig.add_axes([0.652, 0.1, 0.3, 0.5])
ax_txt.axis("off")

texte = ax_txt.text(
    0.05, 0.95,
    f"Coefficients de réflexion et de transmission :\n\nr_theo = {r_theo:.3f}\nt_theo = {t_theo:.3f}\n\nr_exp = {r_exp}\nt_exp = {t_exp}\n\nEi = {Ei}\nEr = {Er}\nEt = {Et}",
    ha="left",
    va="top",
    fontsize=10,
    transform=ax_txt.transAxes,
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="grey",
        alpha=0.8))






def animate(n): 
    
    global Ei
    global Er
    global Et
    global r_exp
    global t_exp
    
    tnp = (n+1) * dt
    
    for i in range(1,N-1):
        unp[i]= S**2 / esp_r[i] * (un[i+1]-2*un[i]+un[i-1]) + 2*un[i] - unm[i]
    
    unp[0]=np.cos(omega*(tnp-tc))*np.exp(-((tnp-tc)/tau)**2)
    
    line.set_data(x, unp)
    unm[:]=un[:]
    un[:]=unp[:]
    
    if n == 340 : #Onde Incidente pour T_tot = 1000
        Ei = max(np.abs(unp[gg:gd]))
    
    if n == 677 : #Onde Réfléchie pour T_tot = 1000
        Er = max(np.abs(unp[gg:gd]))
    
    if n == 750 : #Onde Transmise pour T_tot = 1000
        Et = max(np.abs(unp[dg:dd]))
     
    if n > 750 :
        r_exp = - (Er / Ei)
        t_exp = Et / Ei
        texte.set_text(f"Coefficients de réflexion et de transmission :\n\nr_theo = {r_theo:.3f}\nt_theo = {t_theo:.3f}\n\nr_exp = {r_exp:.3f}\nt_exp = {t_exp:.3f}\n\nEi = {Ei:.3f}\nEr = {Er:.3f}\nEt = {Et:.3f}")
    
    return line, texte
 
ani = animation.FuncAnimation(fig, animate, frames=T_tot,
                              interval=1, blit=True, repeat=False)
plt.show()