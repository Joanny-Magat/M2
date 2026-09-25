%{
Fonction calculant la dérivée de la fonction de Bessel Yn pour x
%}
function res = dbessely(n,x)
  res = 0.5 * ( bessely(n-1,x) - bessely(n+1,x) );
endfunction
