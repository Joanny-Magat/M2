%{
Fonction calculant la dérivée de la fonction de Bessel Jn pour x
%}
function res = dbesselj(n,x)
  res = 0.5 * ( besselj(n-1,x) - besselj(n+1,x) );
endfunction
