
%{
Calcul de la diffraction d'une OPPM incidente arrivant dans un diélectrique
%}

% --- Constantes ---

eps_r = 9;
mu_r = 3;
nu = sqrt(eps_r * mu_r);
Zr = sqrt(eps_r / mu_r);

lambda = 1;
k0 = (2*pi) / lambda;
R0 = 1;
phi = 0;

H0 = besselh(n,1,k0*R0);
J0 = besselj(n,k0*R0);
Ji = besselj(n,k0*R0*nu);


% --- Onde incidente ---

x = linspace(-10*lambda,10*lambda,100);
y = linspace(-10*lambda,10*lambda,100);
[X,Y] = meshgrid(x,y);
Z = X + 1i*Y;
r=abs(Z);
theta = angle(Z);

E = exp(1i*k0*r.*sin(phi-theta));
rE = real(E);


figure(1);
set(gcf, "position", [1 1 1915 1000]);

% Titre général de la figure
annotation("textbox", [0.45 0.94 0.50 0.04], ...
           "string", "OPPM incidente", ...
           "fontsize", 30, ...
           "horizontalalignment", "center", ...
           "linestyle", "none");

subplot(1,2,1);
pcolor(X,Y,rE);
shading flat;
axis square;

xlabel("x");
ylabel("y");
title("Onde incidente en cartésien (2D)");

subplot(1,2,2);
surf(X,Y,rE);
shading flat;
axis square;

xlabel("x");
ylabel("y");
zlabel("Re(Ei)");
title("Onde incidente en cartésien (3D)");


