x = linspace(0,1,10);
y = besselj(0,x); #Bessel
z = bessely(0,x); #Neuman

figure (1)
plot(x,y);
grid on

#hold on; # Evite d'écraser le premier plot

figure(2)
plot(x,z);
grid on

figure(3)

