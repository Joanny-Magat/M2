%{
Fonction calculant gamma_n en fonction de n, esp_r, mu_r, k0, R et phi
%}
function res = gamma_n(n, eps_r, mu_r, k0, R, phi)

  nu = sqrt(eps_r .* mu_r);
  Zr = sqrt(eps_r ./ mu_r);
  khi = (-exp(-1i.*phi)).^n;

  Ji = besselj(n,k0.*R.*nu);
  dJi = dbesselj(n,k0.*R.*nu);

  J0 = besselj(n,k0.*R);
  dJ0 = dbesselj(n,k0.*R);

  Y0 = bessely(n,k0.*R);
  dY0 = dbessely(n,k0.*R);

  H0 = J0 + 1i .* Y0;
  dH0 = dJ0 + 1i .* dY0;

  res = khi .* ( (dH0 .* J0 - dJ0 .* H0) ./ (dH0 .* Ji - Zr .* H0 .* dJi) );

endfunction
