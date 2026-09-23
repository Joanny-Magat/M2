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
tau=2*T #Largeur de la Gausienne
tc=8*T #Centre de la Gausienne
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
esp_r=np.ones(N) #Vide en dehors de la lame

n_air = 1.000272 #Indice de réfraction de l'air
n_lame = 1.45 #Indice de réfraction de la lame diéléctrique

for i in range(N):
    if N/3 < i < 2/3*N: # Largeur de la lame
        esp_r[i]=n_lame**2

#Dioptre 1
r_theo_d1 = (n_air - n_lame) / (n_air + n_lame) 
t_theo_d1 = (2*n_air) / (n_air + n_lame)
Ei_d1 = "Pas encore calculé"
Er_d1 = "Pas encore calculé"
Et_d1 = "Pas encore calculé"
r_exp_d1 = "Pas encore calculé"
t_exp_d1 = "Pas encore calculé"

#Dioptre 2
r_theo_d2 = (n_lame - n_air) / (n_air + n_lame) 
t_theo_d2 = (2*n_lame) / (n_air + n_lame)
Ei_d2 = "Pas encore calculé"
Er_d2 = "Pas encore calculé"
Et_d2 = "Pas encore calculé"
r_exp_d2 = "Pas encore calculé"
t_exp_d2 = "Pas encore calculé"



fig, ax = plt.subplots(figsize=(14, 6))
line, = ax.plot([], [], "black") #label="Paquet d'onde"
espr, = ax.plot(x, esp_r, "grey")

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


ax.axvline(
    x=x[int(N/3)],
    color="grey",
    linestyle="--",
    linewidth=2,
    label=f"Lame allant de  x = {x[int(N/3)]} à x = {x[int(2/3*N)]}")
ax.axvline(
    x=x[int(2/3*N)],
    color="grey",
    linestyle="--",
    linewidth=2)

#Positions des zones de mesures (zone gauche, centrale et droite)
gg = int(N/4 - N/6)
gd = int(N/4 + N/6)
cg = int(N/4 - N/6)
cd = int(N/4 + N/6)
dg = int(3*N/4 - N/6)
dd = int(3*N/4 + N/6)

ax.axvspan(
    x[gg],
    x[gd],
    color="red",
    alpha=0.35,
    label=
    f"Zone où est mesurée le max de l'amplitude\n"\
    f"de l'onde incidente puis de celle réfléchie\n"\
    f"(x de {x[gg]:.2e} à {x[gd]:.2e})")

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

legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.01, 1.015))
legend.get_frame().set_edgecolor("grey")

#Zone de texte
ax_txt = fig.add_axes([0.652, 0.07, 0.3, 0.8]) #[gauche, bas, largeur, hauteur]
ax_txt.axis("off")

texte = ax_txt.text(
    0.05, 0.95,
    f"Coefficients de réflexion et de transmission\ndu premier dioptre :\n\n"\
    f"r_theo_d1 = {r_theo_d1:.3f}\nt_theo_d1 = {t_theo_d1:.3f}\n\n"\
    f"r_exp_d1 = {r_exp_d1}\nt_exp_d1 = {t_exp_d1}\n\n"\
    f"Ei_d1 = {Ei_d1}\nEr_d1 = {Er_d1}\nEt_d1 = {Et_d1}\n\n\n"\
    f"Coefficients de réflexion et de transmission\ndu deuxième dioptre :\n\n"\
    f"r_theo_d2 = {r_theo_d2:.3f}\nt_theo_d2 = {t_theo_d2:.3f}\n\n"\
    f"r_exp_d2 = {r_exp_d2}\nt_exp_d2 = {t_exp_d2}\n\n"\
    f"Ei_d2 = {Ei_d2}\nEr_d2 = {Er_d2}\nEt = {Et_d2}",
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
    
    #Test pour connaitre n :
    if n >= 290 :
     return line, texte

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
    

    if n == 290 : #Onde Incidente d1 pour T_tot = 1000
        Ei_d1 = max(np.abs(unp[gg:gd]))
    
    if n == 677 : #Onde Réfléchie d1 pour T_tot = 1000
        Er_d1 = max(np.abs(unp[gg:gd]))
    
    if n == 750 : #Onde Transmise d1 pour T_tot = 1000
        Et_d1 = max(np.abs(unp[dg:dd]))

    if n == 340 : #Onde Incidente d2 pour T_tot = 1000
        Ei_d2 = max(np.abs(unp[gg:gd]))
    
    if n == 677 : #Onde Réfléchie d2 pour T_tot = 1000
        Er_d2 = max(np.abs(unp[gg:gd]))
    
    if n == 750 : #Onde Transmise d2 pour T_tot = 1000
        Et_d2 = max(np.abs(unp[dg:dd]))
     
    if n > 750 :
        r_exp = - (Er / Ei)
        t_exp = Et / Ei
        texte.set_text(
            f"Coefficients de réflexion et de transmission du premier dioptre :\n\n"\
            f"r_theo_d1 = {r_theo_d1:.3f}\nt_theo_d1 = {t_theo_d1:.3f}\n\n"\
            f"r_exp_d1 = {r_exp_d1:.3f}\nt_exp_d1 = {t_exp_d1:.3f}\n\n"\
            f"Ei_d1 = {Ei_d1:.3f}\nEr_d1 = {Er_d1:.3f}\nEt_d1 = {Et_d1:.3f}\n\n"\
            f"Coefficients de réflexion et de transmission du deuxième dioptre :\n\n"\
            f"r_theo_d2 = {r_theo_d2:.3f}\nt_theo_d2 = {t_theo_d2:.3f}\n\n"\
            f"r_exp_d2 = {r_exp_d2:.3f}\nt_exp_d2 = {t_exp_d2:.3f}\n\n"\
            f"Ei_d2 = {Ei_d2:.3f}\nEr_d2 = {Er_d2:.3f}\nEt = {Et_d2:.3f}")
    
    return line, texte
 
ani = animation.FuncAnimation(fig, animate, frames=T_tot,
                              interval=1, blit=True, repeat=False)

plt.show()