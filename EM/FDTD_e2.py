#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 08:08:03 2026

@author: magat-j
joanny.magat@etu.umontpellier.fr

e2) du TP FDTD de M2 (= TP8 de L3)
La lame fait maintenant une longueur lambda/2

/bin/python3 /skole/nas-edu/home0/mpn2/magat-j/Documents/M2/EM/FDTD_e2.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
unm=np.linspace(0,0,N)
un=np.linspace(0,0,N)
unp=np.linspace(0,0,N)


#Permittivité relative

n_air = 1.000272 #Indice de réfraction de l'air
n_lame = 1.45 #Indice de réfraction de la lame diéléctrique
esp_r=np.ones(N) #Vide en dehors de la lame
esp_r[int(N/2)-int(lambda0/(4*n_lame*dx)):int(N/2)+int(lambda0/(4*n_lame*dx))+1]=n_lame**2

# print(f"\nlambda = lambda0/n_lame = {lambda0/n_lame}")
# print(f"\nlambda/(2*dx) = {lambda0/(n_lame*2*dx)}")
# print(f"\nlargeur lame simulé\n= int(N/2)+int(lambda0/(4*n_lame*dx))\n- ( int(N/2)-int(lambda0/(4*n_lame*dx)) )\n= {int(N/2)+int(lambda0/(4*n_lame*dx)) - ( int(N/2)-int(lambda0/(4*n_lame*dx)) )}\n")
# print(f"\nlargeur lame simulé\n= int( N/2+lambda0/(4*n_lame*dx)\n- (N/2-lambda0/(4*n_lame*dx)) )\n= {int( N/2+lambda0/(4*n_lame*dx) - (N/2-lambda0/(4*n_lame*dx)) )}\n")
# ==> le int fait passer que la largeur est pas de lambda/2 qui équivaut à une largeur discrète de 6.9 mais est de 6

# for i in range(N):
#     if N/3 < i < 2/3*N: # Largeur de la lame
#         esp_r[i]=n_lame**2

"""
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
"""


fig, ax = plt.subplots(figsize=(16, 10))
line, = ax.plot([], [], "blue", label="Paquet d'onde")
espr, = ax.plot(x, esp_r, "black")

ax.axvspan(
    x[int(N/2)-int(lambda0/(4*n_lame*dx))-1],
    x[int(N/2)+int(lambda0/(4*n_lame*dx))],
    color="grey",
    alpha=0.35,
    label=r"Lame $\lambda/2$")

"""
fig.subplots_adjust(
    left=0.08,
    right=0.65,
    top=0.90,
    bottom=0.10) #Met le graphe à gauche pour avoir la place de mettre les légendes à droite
"""

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

"""
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
largeur_zone = N/9
gg = int(N/6 - largeur_zone)
gd = int(N/6 + largeur_zone)
cg = int(2*N/4 - largeur_zone)
cd = int(2*N/4 + largeur_zone)
dg = int(5*N/6 - largeur_zone)
dd = int(5*N/6 + largeur_zone)

ax.axvspan(
    x[gg],
    x[gd],
    color="red",
    alpha=0.35,
    label=
    "Zone où est mesurée le max de l'amplitude\n"\
    "de l'onde incidente puis de celle réfléchie\n"\
    "du premier dioptre\n"\
    f"(x de {x[gg]:.2e} à {x[gd]:.2e})")

ax.axvspan(
    x[cg],
    x[cd],
    color="green",
    alpha=0.35,
    label=
    "Zone où est mesurée le max de l'amplitude\n"\
    "de l'onde transmise du premier dioptre,\n"\
    "de celle incidente du deuxième dioptre puis\n"\
    "de celle réfléchie du deuxième dioptre\n"\
    f"(x de {x[cg]:.2e} à {x[cd]:.2e})")

ax.axvspan(
    x[dg],
    x[dd],
    color="blue",
    alpha=0.35,
    label=
    "Zone où est mesurée le max de l'amplitude\n"\
    "de l'onde transmise du premier dioptre\n"\
    f"(x de {x[dg]:.2e} à {x[dd]:.2e})")
"""

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

"""
legend = ax.legend(
    loc="upper left",
    bbox_to_anchor=(1.01, 1.01)) #[gauche, bas]
legend.get_frame().set_edgecolor("grey")
"""

"""
#Zone de texte
ax_txt = fig.add_axes([0.65, -0.11, 0.3, 0.8]) #[gauche, bas, largeur, hauteur]
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
"""


def animate(n): 
    
    """
    #Test pour connaitre n :
    if n >= 840 :
        return line, texte
    """

    """
    global Ei_d1
    global Er_d1
    global Et_d1
    global r_exp_d1
    global t_exp_d1

    global Ei_d2
    global Er_d2
    global Et_d2
    global r_exp_d2
    global t_exp_d2
    """

    tnp = (n+1) * dt
    
    # for i in range(1,N-1):
    #     unp[i] = S**2 / esp_r[i] * (un[i+1]-2*un[i]+un[i-1]) + 2*un[i] - unm[i]
    
    unp[1:N-1] = S**2 / esp_r[1:N-1] * (un[2:N]-2*un[1:N-1]+un[0:N-2]) + 2*un[1:N-1] - unm[1:N-1] # la notation l[i:j] marche comme un range : il fait de i à j exclu
    
    if tnp < 2*tc :
        unp[0] = np.cos(omega*(tnp-tc))*np.exp(-((tnp-tc)/tau)**2)
    
    else :
        unp[0] = un[1]
    
    unp[N-1] = un[N-2]
        
    line.set_data(x, unp)
    unm[:]=un[:]
    un[:]=unp[:]
    
    """
    if n == 290 : 
        Ei_d1 = max(np.abs(unp[gg:gd])) #Onde Incidente d1 pour T_tot = 1000
    
    if n == 515 : 
        Er_d1 = max(np.abs(unp[gg:gd])) #Onde Réfléchie d1 pour T_tot = 1000
    
    if n == 560 : 
        Et_d1 = max(np.abs(unp[cg:cd])) #Onde Transmise d1 pour T_tot = 1000
        Ei_d2 = max(np.abs(unp[cg:cd])) #Onde Incidente d2 pour T_tot = 1000
    
    if n > 560 and n < 840 :
        r_exp_d1 = - (Er_d1 / Ei_d1)
        t_exp_d1 = Et_d1 / Ei_d1
        texte.set_text(
            f"Coefficients de réflexion et de transmission\ndu premier dioptre :\n\n"\
            f"r_theo_d1 = {r_theo_d1:.3f}\nt_theo_d1 = {t_theo_d1:.3f}\n\n"\
            f"r_exp_d1 = {r_exp_d1:.3f}\nt_exp_d1 = {t_exp_d1:.3f}\n\n"\
            f"Ei_d1 = {Ei_d1:.3f}\nEr_d1 = {Er_d1:.3f}\nEt_d1 = {Et_d1:.3f}\n\n"\
            f"Coefficients de réflexion et de transmission\ndu deuxième dioptre :\n\n"\
            f"r_theo_d2 = {r_theo_d2:.3f}\nt_theo_d2 = {t_theo_d2:.3f}\n\n"\
            f"r_exp_d2 = {r_exp_d2}\nt_exp_d2 = {t_exp_d2}\n\n"\
            f"Ei_d2 = {Ei_d2}\nEr_d2 = {Er_d2}\nEt = {Et_d2}")

    if n == 840 : 
        Er_d2 = max(np.abs(unp[cg:cd])) #Onde Réfléchie d2 pour T_tot = 1000
        Et_d2 = max(np.abs(unp[dg:dd])) #Onde Transmise d2 pour T_tot = 1000
     
    if n > 840 :
        r_exp_d1 = - (Er_d1 / Ei_d1)
        t_exp_d1 = Et_d1 / Ei_d1
        r_exp_d2 = Er_d2 / Ei_d2
        t_exp_d2 = Et_d2 / Ei_d2
        texte.set_text(
            f"Coefficients de réflexion et de transmission\ndu premier dioptre :\n\n"\
            f"r_theo_d1 = {r_theo_d1:.3f}\nt_theo_d1 = {t_theo_d1:.3f}\n\n"\
            f"r_exp_d1 = {r_exp_d1:.3f}\nt_exp_d1 = {t_exp_d1:.3f}\n\n"\
            f"Ei_d1 = {Ei_d1:.3f}\nEr_d1 = {Er_d1:.3f}\nEt_d1 = {Et_d1:.3f}\n\n"\
            f"Coefficients de réflexion et de transmission\ndu deuxième dioptre :\n\n"\
            f"r_theo_d2 = {r_theo_d2:.3f}\nt_theo_d2 = {t_theo_d2:.3f}\n\n"\
            f"r_exp_d2 = {r_exp_d2:.3f}\nt_exp_d2 = {t_exp_d2:.3f}\n\n"\
            f"Ei_d2 = {Ei_d2:.3f}\nEr_d2 = {Er_d2:.3f}\nEt = {Et_d2:.3f}")
    """    

    return line, #texte
 
ani = animation.FuncAnimation(fig, animate, frames=T_tot,
                              interval=1e-10, blit=True, repeat=False)

ax.legend()
plt.show()