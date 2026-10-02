%{
Calcul de la diffraction d'une OPPM incidente arrivant dans un diélectrique
%}

clear;
clc;



% --- Constantes ---

N = 20; % Nombre de termes que l'on garde dans la série de Fourier (Troncature)
n = -N:N; % Liste des indices de la série

R = 1;
phi = 0; % Angle d'incidence
lambda = 2;
k0 = (2*pi) / lambda;
eps_r = 12;
mu_r = 1;
nu = sqrt(eps_r * mu_r);

alpha = alpha_n(n, eps_r, mu_r, k0, R, phi);
gamma = gamma_n(n, eps_r, mu_r, k0, R, phi);



% --- Champ incident ---

Nx = 200;
Ny = 200;
taille = 2;

x = linspace(-taille*lambda,taille*lambda,Nx);
y = linspace(-taille*lambda,taille*lambda,Ny);
[X,Y] = meshgrid(x,y);

Z = X + 1i*Y;
r=abs(Z);
theta = angle(Z);

E = exp(1i*k0*r.*sin(phi-theta));
rE = real(E);



% --- Champ total ---

U_s_int = 0;
U_s_ext = 0;

for val = 1:length(n)
    U_s_ext = U_s_ext + alpha(val) .* besselh(n(val),1,k0.*r) .* exp(1i.*n(val)*theta);
    U_s_int = U_s_int + gamma(val) .* besselj(n(val),k0*r*nu) .* exp(1i.*n(val)*theta);
end

U_t_ext = U_s_ext + E;
rU_t_ext = real(U_t_ext);
rU_t_int = real(U_s_int);

flagcyl=r>R;
rU_t=flagcyl.*rU_t_ext + ~flagcyl.*rU_t_int;



% --- Figure ---

figure(1);
set(gcf, "position", [1 1 1915 1000]);

% Titre général de la figure avec [x,y,largeur,hauteur]
annotation("textbox", [0.39 0.94 0.50 0.04], ...
           "string", "OPPM diffractée par un diéléctrique", ...
           "fontsize", 30, ...
           "horizontalalignment", "center", ...
           "linestyle", "none");

subplot(1,2,1);
surf(X,Y,rE);
shading flat;
axis square;

xlabel("x");
ylabel("y");
zlabel("Re(U_i)");
title("Champ incident");

subplot(1,2,2);
surf(X,Y,rU_t);
shading flat;
axis square;
colorbar;

xlabel("x");
ylabel("y");
zlabel("Re(U_t)");
title("Champ total");



