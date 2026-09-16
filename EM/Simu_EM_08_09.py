# -*- coding: utf-8 -*-

"""
Fichier du 1er cours de simu EM (08/09/2026) :
    - Bases de Python
    - Animations Matplotlib
"""

#%% Boucle while

prix = int(input("Entrez un prix initial (entier) : "))
print("")

while prix > 10 :
    print(f"{prix} € est trop cher !")
    prix -= 1


print(f"\n{prix} € est un bon prix :)")

#%% Dictionnaire

import re

jours = {2:"lundi",3:"mardi",4:"mercredi",5:"jeudi",6:"vendredi",0:"samedi",1:"dimache"}
mois = {"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"août","09":"septembre","10":"octobre","11":"novembre","12":"décembre"}

date = input("Entrez une date sous la forme jj/mm/aaaa : ")

if re.search("^\d\d/\d\d/-?\d\d?\d?\d?$",date) :
    
    l = re.split("/",date)
    
    if 0<int(l[0])<32 and 0<int(l[1])<13 :
        
        #Congruence de Zeller#
        
        m = int(l[1])
        if m == 1 :
            m = 13
        elif m == 2 :
            m = 14
        q = int(l[0])
        j = int(int(l[2])/100)
        k = int(l[2])%100
        
        h = ( q + int( (13*(m+1))/5 ) + k + int(k/4) + int(j/4) + 5*j ) % 7
        
        print(f"\n{date} s'écrit en toute lettre : {jours[h]} {int(l[0])} {mois[l[1]]} {l[2]}")
        
    else :
        print("\nFormat valide mais la valeur du jour ou du mois est absurde :(")

else :
    print("\nLe format rentré n'est pas valide :(")
    
#%% Animation Matplotlib (d) du TP Visualisation)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

tmin = 0
tmax = 4
nbt = 41
dt = (tmax-tmin) / (nbt-1)

xmin = -3
xmax = 13
nbx = 161

x = np.linspace(xmin, xmax, nbx)

fig = plt.figure() # initialise la figure
line, = plt.plot([], []) 
plt.xlim(xmin, xmax)
plt.ylim(0, 1)

def animate(i): 
    t = i * dt
    y = 1 / ( 1 + (x-4.8*t)**2)
    line.set_data(x, y)
    return line,
 
ani = animation.FuncAnimation(fig, animate, frames=35,
                              interval=10, blit=True, repeat=False)
plt.show()


#%% Animation Matplotlib sans module animation : d) de TP Visualisation

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


for i in range(41):
    t = i * dt
    y = 1 / ( 1 + (x-4.8*t)**2)
    if i == 0:
        line, = plt.plot(x, y)
        #Astuce Python : l, permet de prendre directement l'élément de la liste à un élément [a]
    else:
        line.set_data(x, y)
    plt.pause(0.04) # pause avec duree en secondes
    
plt.show()










































