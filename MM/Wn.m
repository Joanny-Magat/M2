%{
Fonction calculant Wn = Y'nJn - YnJ'n
%}
function res = Wn(n,x)
  res = dbessely(n,x).*besselj(n,x) - bessely(n,x).*dbesselj(n,x);
endfunction
