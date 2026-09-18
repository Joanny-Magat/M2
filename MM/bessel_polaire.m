x = linspace(-10,10,100);
y = linspace(-10,10,100);
[X,Y] = meshgrid(x,y);
Z = besselj(0,sqrt(X.^2+Y.^2));


figure(1);

% Prend toute la taille de l'écran
set(gcf, "position", [1 1 1915 1000]);


% --- 2D pcolor ---
subplot(1,3,1);

pcolor(X,Y,Z);
shading interp;
axis square;

xlabel("x");
ylabel("y");
title("2D - pcolor");


% --- 3D mesh ---
subplot(1,3,2);

mesh(X,Y,Z);
shading interp;
axis square;

xlabel("x");
ylabel("y");
zlabel("Z");
title("3D - mesh");


% --- 3D surf ---
subplot(1,3,3);

surf(X,Y,Z);
shading interp;
axis square;

xlabel("x");
ylabel("y");
zlabel("Z");
title("3D - surf");
