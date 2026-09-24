/*
Compile tous les interchange.c avec les différentes optis

gcc -O3 compilateur_interchange.c -o compilateur_interchange.out
./compilateur_interchange.out
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    for (int j = 0; j < 4; j++) {

        char bad[1000];
        char good[1000];

        snprintf(bad, sizeof(bad), "gcc -O%d interchange-bad.c -o interchange-bad_%d.out", j, j);
        snprintf(good, sizeof(good), "gcc -O%d interchange-good.c -o interchange-good_%d.out", j, j);

        system(bad);
        system(good);

    }

}