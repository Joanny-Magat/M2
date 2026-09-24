/*
Compare le temps d'exécution entre interchange-bad et interchange-good
en faisant l'expérience N fois

Toutes ces comparaisons sont elles-mêmes comparées entre elles
en fonctions du niveau d'optimisation de la compilation
allant de O0 à O3

N = argv[1]

gcc -O0 compa_interchange.c -o compa_interchange.out
./compa_interchange.out 100
perf stat -e L1-dcache-load-misses,L1-dcache-loads ./compa_interchange.out 100
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

    assert(argc == 2 && est_entier(argv[1]));

    int N = atoi(argv[1]);


    typedef struct {
        double temps[4];
    } Opti;

    Opti *l_bad = malloc(N * sizeof(Opti));
    Opti *l_good = malloc(N * sizeof(Opti));

    for (int i = 0; i < N; i++) {

        for (int j = 0; j < 4; j++) {

            char bad[100];
            char good[100];

            snprintf(bad, sizeof(bad), "./interchange-bad_%d.out", j);
            snprintf(good, sizeof(good), "./interchange-good_%d.out", j);

            struct timespec debut, fin;

            clock_gettime(CLOCK_MONOTONIC, &debut);
            system(bad);
            clock_gettime(CLOCK_MONOTONIC, &fin);

            l_bad[i].temps[j] =
                (fin.tv_sec - debut.tv_sec)
                + (fin.tv_nsec - debut.tv_nsec) * 1e-9;

            clock_gettime(CLOCK_MONOTONIC, &debut);
            system(good);
            clock_gettime(CLOCK_MONOTONIC, &fin);

            l_good[i].temps[j] =
                (fin.tv_sec - debut.tv_sec)
                + (fin.tv_nsec - debut.tv_nsec) * 1e-9;
        }
    }

    double somme_bad[4] = {0};
    double somme_good[4] = {0};

    double moyenne_bad[4];
    double moyenne_good[4];
    double moyenne_compa[4];


    // Somme des temps pour chaque niveau d'optimisation
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 4; j++) {
            somme_bad[j] += l_bad[i].temps[j];
            somme_good[j] += l_good[i].temps[j];
        }
    }


    // Moyennes
    for (int j = 0; j < 4; j++) {
        moyenne_bad[j] = somme_bad[j] / N;
        moyenne_good[j] = somme_good[j] / N;
        moyenne_compa[j] = moyenne_bad[j] - moyenne_good[j];
    }


    // Affichage
    
    system("clear");

    printf("\n");
    printf("============================================================\n");
    printf("         SYNTHÈSE DES OPTIMISATIONS DE INTERCHANGE\n");
    printf("============================================================\n");

    printf("\nTemps moyen pour %d expériences :\n\n", N);

    printf("%-15s %-18s %-18s %-18s\n",
        "Optimisation", "Bad", "Good", "Différence");

    printf("------------------------------------------------------------\n");

    for (int j = 0; j < 4; j++) {

        char nom_opti[20];

        snprintf(nom_opti, sizeof(nom_opti), "-O%d", j);
        
        printf("%-15s %-18f %-18f %-18f\n",
            nom_opti,
            moyenne_bad[j],
            moyenne_good[j],
            moyenne_compa[j]);
    }

    printf("============================================================\n");



    free(l_bad);
    free(l_good);

    return 0;
}