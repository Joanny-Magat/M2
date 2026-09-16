/*
Compare le temps d'exécution entre N multiplications et N divisions en faisant l'expérience M fois
N = argv[1]
M = argv[2]
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>

int main(int argc, char *argv[]) {


    int est_entier(const char *s) {
        for (int i = 0; s[i] != '\0'; i++) {
            if (!isdigit(s[i]))
                return 0;
        }
        return 1;
    }

    if (argc < 3 || !est_entier(argv[1]) || !est_entier(argv[2]) ) {
        printf("%s: Erreur : Arguments absents ou non entiers !\n", argv[0]);
        return -1;
    }


    int N = atoi(argv[1]);
    int M = atoi(argv[2]);

    char mul[100];
    char div[100];
    snprintf(mul, sizeof(mul), "./mul.out %d", N);
    snprintf(div, sizeof(div), "./div.out %d", N);

    double *l_mul = malloc(M * sizeof(double));
    double *l_div = malloc(M * sizeof(double));

    for (int i = 0; i < M; i++) {
        
        struct timespec debut_mul, fin_mul, debut_div, fin_div;
        
        clock_gettime(CLOCK_MONOTONIC, &debut_mul);
        system(mul);
        clock_gettime(CLOCK_MONOTONIC, &fin_mul);
        double temps_mul = (fin_mul.tv_sec - debut_mul.tv_sec) + (fin_mul.tv_nsec - debut_mul.tv_nsec)*1e-9; //Convertit les ns en s
        l_mul[i] = temps_mul;

        clock_gettime(CLOCK_MONOTONIC, &debut_div);
        system(div);
        clock_gettime(CLOCK_MONOTONIC, &fin_div);
        double temps_div = (fin_div.tv_sec - debut_div.tv_sec) + (fin_div.tv_nsec - debut_div.tv_nsec)*1e-9; //Convertit les ns en s
        l_div[i] = temps_div;

    }

    double somme_mul = 0;
    double somme_div = 0;

    for (int i = 0; i < M; i++) {
        somme_mul += l_mul[i];
        somme_div += l_div[i];
    }

    double moyenne_mul = somme_mul / M;
    double moyenne_div = somme_div / M;
    double moyenne_compa = moyenne_mul-moyenne_div;


    printf("Sur un total de %d comparaisons de temps d'exécution entre le calcul de %d de multiplications et de %d de divisions, cet ordinateur a en moyenne :\n", M, N, N);
    printf("-mis %f secondes à exécuter les %d multiplications\n", moyenne_mul, N);
    printf("-soit %f secondes par multiplication\n", moyenne_mul/N);
    printf("-mis %f secondes à exécuter les %d divisions\n", moyenne_div, N);
    printf("-soit %f secondes par division\n", moyenne_div/N);
    printf("\nIl y a donc %f secondes de différence en moyenne entre l'exécution d'une série de multiplications et d'une série de divisons\n", moyenne_compa);
    printf("Il y a donc %f secondes de différence en moyenne pour une unique opération\n\n", moyenne_compa/N);

    free(l_mul);
    free(l_div);
    return 0;
}