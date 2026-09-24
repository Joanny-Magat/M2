/*
Compare le temps d'exécution entre N multiplications et N divisions
en faisant l'expérience M fois

Toutes ces comparaisons sont elles-mêmes comparées entre elles
en fonctions du niveau d'optimisation de la compilation
allant de O0 à O3 en faisant aussi ffast-math

N = argv[1]
M = argv[2]

gcc -O0 time_compa_opti.c -o compa_opti.out
./compa_opti.out 1000000 10
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include <assert.h>

int main(int argc, char *argv[]) {


    int est_entier(const char *s) {
        for (int i = 0; s[i] != '\0'; i++) {
            if (!isdigit(s[i]))
                return 0;
        }
        return 1;
    }

    assert(argc == 3 && est_entier(argv[1]) && est_entier(argv[2]));

    int N = atoi(argv[1]);
    int M = atoi(argv[2]);



    typedef struct {
        double temps[5];
    } Opti;

    Opti *l_mul = malloc(M * sizeof(Opti));
    Opti *l_div = malloc(M * sizeof(Opti));

    for (int i = 0; i < M; i++) {

        for (int j = 0; j < 5; j++) {

            char mul[100];
            char div[100];

            if (j < 4) {
                snprintf(mul, sizeof(mul), "./mul%d.out %d", j, N);
                snprintf(div, sizeof(div), "./div%d.out %d", j, N);
            } else {
                snprintf(mul, sizeof(mul), "./mulmath.out %d", N);
                snprintf(div, sizeof(div), "./divmath.out %d", N);
            }

            struct timespec debut, fin;

            clock_gettime(CLOCK_MONOTONIC, &debut);
            system(mul);
            clock_gettime(CLOCK_MONOTONIC, &fin);

            l_mul[i].temps[j] =
                (fin.tv_sec - debut.tv_sec)
                + (fin.tv_nsec - debut.tv_nsec) * 1e-9;

            clock_gettime(CLOCK_MONOTONIC, &debut);
            system(div);
            clock_gettime(CLOCK_MONOTONIC, &fin);

            l_div[i].temps[j] =
                (fin.tv_sec - debut.tv_sec)
                + (fin.tv_nsec - debut.tv_nsec) * 1e-9;
        }
    }

    double somme_mul[5] = {0};
    double somme_div[5] = {0};

    double moyenne_mul[5];
    double moyenne_div[5];
    double moyenne_compa[5];


    // Somme des temps pour chaque niveau d'optimisation
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < 5; j++) {
            somme_mul[j] += l_mul[i].temps[j];
            somme_div[j] += l_div[i].temps[j];
        }
    }


    // Moyennes
    for (int j = 0; j < 5; j++) {
        moyenne_mul[j] = somme_mul[j] / M;
        moyenne_div[j] = somme_div[j] / M;
        moyenne_compa[j] = moyenne_mul[j] - moyenne_div[j];
    }


    // Affichage
    printf("\nRésultats sur %d expériences avec N = %d :\n\n", M, N);

    for (int j = 0; j < 5; j++) {

        if (j < 4) {
            printf("========== Niveau -O%d ==========\n", j);
        } else {
            printf("========== -ffast-math ==========\n");
        }

        printf("Multiplications : %f secondes\n", moyenne_mul[j]);
        printf("                 %f secondes par multiplication\n",
            moyenne_mul[j] / N);

        printf("Divisions       : %f secondes\n", moyenne_div[j]);
        printf("                 %f secondes par division\n",
            moyenne_div[j] / N);

        printf("Différence totale : %f secondes\n", moyenne_compa[j]);
        printf("Différence par opération : %f secondes\n\n",
            moyenne_compa[j] / N);
    }

    printf("\n");
    printf("============================================================\n");
    printf("                 SYNTHÈSE DES OPTIMISATIONS\n");
    printf("============================================================\n");

    printf("\nTemps moyen pour %d opérations, sur %d expériences :\n\n", N, M);

    printf("%-15s %-18s %-18s %-18s\n",
        "Optimisation", "Multiplications", "Divisions", "Différence");

    printf("------------------------------------------------------------\n");

    for (int j = 0; j < 5; j++) {

        char nom_opti[20];

        if (j < 4)
            snprintf(nom_opti, sizeof(nom_opti), "-O%d", j);
        else
            snprintf(nom_opti, sizeof(nom_opti), "-ffast-math");

        printf("%-15s %-18f %-18f %-18f\n",
            nom_opti,
            moyenne_mul[j],
            moyenne_div[j],
            moyenne_compa[j]);
    }

    printf("============================================================\n");



    free(l_mul);
    free(l_div);

    return 0;
}