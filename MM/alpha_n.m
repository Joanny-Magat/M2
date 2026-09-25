%{
Fonction calculant alpha_n en fonction de n, esp_r, mu_r, k0, R et phi
%}
function res = alpha_n(n, eps_r, mu_r, k0, R, phi)

  nu = sqrt(eps_r .* mu_r);
  Zr = sqrt(eps_r ./ mu_r);
  X = (-exp(-1i.*phi)).^n; %liste des ki_n

  J0 = besselj(n,k0.*R);
  dJ0 = dbesselj(n,k0.*R);
  Y0 = bessely(n,k0.*R);
  dY0 = dbessely(n,k0.*R);
  Ji = besselj(n,k0.*R.*nu);
  dJi = dbesselj(n,k0.*R.*nu);

  res = X .* ( -1 ./ ( 1 + 1i .* ( (dY0 .* Ji - Zr .* Y0 .* dJi) ./ (dJ0 .* Ji - Zr .* J0 .* dJi) ) ) );

endfunction
