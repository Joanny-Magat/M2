/*
Compile tous les loop-fusion.c avec les différentes optis

gcc -O3 compilateur_fusion.c -o compilateur_fusion.out
./compilateur_fusion.out
*/

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {

    for (int j = 0; j < 4; j++) {

        char bad[1000];
        char good[1000];

        snprintf(bad, sizeof(bad), "gcc -O%d loop-fusion-bad.c -o loop-fusion-bad_%d.out", j, j);
        snprintf(good, sizeof(good), "gcc -O%d loop-fusion-good.c -o loop-fusion-good_%d.out", j, j);

        system(bad);
        system(good);

    }

}