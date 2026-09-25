
%{
Calcul de la diffraction d'une OPPM incidente arrivant dans un diélectrique
%}

% --- Constantes ---

R = 1;
phi = 0; % Angle d'incidence
lambda = 1;
k0 = (2*pi) / lambda;
eps_r = 9;
mu_r = 2;

N = 10; % Nombre de termes que l'on garde dans la série de Fourier (Troncature)
n = -N:N; % Liste des indices de la série

%{
Ces constantes sont définis dans la fonction alpha_n
nu = sqrt(eps_r * mu_r);
Zr = sqrt(eps_r / mu_r);
Jn = besselj(n,k0.*R); % Liste des Jn
Yn = bessely(n,k0.*R); % Liste des Yn
Wn = Wn(n,k0.*R); % Liste des Wn
Xn = (-exp(-1i.*phi)).^n; % Liste des ki_n
H0 = besselh(n,1,k0*R);
J0 = besselj(n,k0*R);
Ji = besselj(n,k0*R*nu);
%}

alpha = alpha_n(n, eps_r, mu_r, k0, R, phi);
for i = 1:length(n)
    printf("alpha_%d = %f\n", n(i), alpha(i));
end
printf("\n");



% --- Onde incidente ---

x = linspace(-10*lambda,10*lambda,100);
y = linspace(-10*lambda,10*lambda,100);
[X,Y] = meshgrid(x,y);
Z = X + 1i*Y;
r=abs(Z);
theta = angle(Z);

E = exp(1i*k0*r.*sin(phi-theta));
rE = real(E);



% --- Onde de sortie ---

U_s = 0;

for val = 1:length(n)
    U_s = U_s + alpha(val) .* besselh(val,1,k0.*r) .* exp(1i.*val*theta);
end

rU_s = real(U_s);



% --- Figure ---

figure(1);
set(gcf, "position", [1 1 1915 1000]);

% Titre général de la figure
annotation("textbox", [0.45 0.94 0.50 0.04], ...
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
zlabel("Re(Ei)");
title("Onde incidente");

subplot(1,2,2);
surf(X,Y,rU_s);
shading flat;
axis square;

xlabel("x");
ylabel("y");
zlabel("Re(U_s)");
title("Onde de sortie");

%{
pcolor(X,Y,rE);
shading flat;
axis square;

xlabel("x");
ylabel("y");
title("Onde incidente en cartésien (2D)");
%}



