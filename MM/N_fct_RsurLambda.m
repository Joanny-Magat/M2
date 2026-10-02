%{
Analyse de alpha afin de trouver une relation de N en fonction de R/lambda
tel que il n'y a que quelques valeurs au bord de alpha qui soit 100x moins grandes que les autres valeurs
%}

clear;
clc;

eps_r = 12;
mu_r = 1;
phi = 0;

%N = []; % Liste de triplet (R,lambda,N)
dico = containers.Map('KeyType', 'double', 'ValueType', 'any'); % dico qui pour chaque clé R/lambda associe la liste de tous les N trouvées pour ce ratio

for R = 1:100
  for lambda = 1:100
    RsurLambda = R/lambda;
    k0 = (2*pi) / lambda;
    alpha_n_moins_un = alpha_n(0, eps_r, mu_r, k0, R, phi);
    n = 1;
    N_trouvee = 0; % Condition du while
    while N_trouvee == 0;
      alpha = alpha_n(n, eps_r, mu_r, k0, R, phi);
      %disp(alpha)
      if isnan(alpha)
        N_trouvee = 1;
      endif
      if 100*alpha < alpha_n_moins_un
        N_trouvee = 1;
        if isKey(dico, RsurLambda)
            liste = dico(RsurLambda);
            liste(end+1) = n+2;
            dico(RsurLambda) = liste;
        else
            dico(RsurLambda) = [n+2]; % +2 pour laisser une marge
        end
        %N(end+1,:) = [R, lambda, n+2];
      endif
      alpha_n_moins_un = alpha;
      n = n + 1;
    end
  end
end

l_RsurLambda = [];
l_Nmoyen = [];

cles = keys(dico);

for i = 1:length(cles)
    cle = cles{i};
    Nmoyen = mean(dico(cle));
    l_RsurLambda(end+1,:) = cle;
    l_Nmoyen(end+1,:) = Nmoyen;
end

bar(l_RsurLambda, l_Nmoyen)
xlabel("R/lambda")
ylabel("N moyen")

