/*
gcc -O0 time_div.c -o div0.out
gcc -O1 time_div.c -o div1.out
gcc -O2 time_div.c -o div2.out
gcc -O3 time_div.c -o div3.out
gcc -ffast-math time_div.c -o divmath.out

for O in 0 1 2 3; do gcc -O$O time_div.c -o div$O.out; done && gcc -ffast-math time_div.c -o divmath.out
*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main( int argc, char *argv[] )  {

    double a = 7.0;
    double b = 6.0;

    int est_entier(const char *s) {
        for (int i = 0; s[i] != '\0'; i++) {
            if (!isdigit(s[i]))
                return 0;
        }
        return 1;
    }

    if (argc < 2 || !est_entier(argv[1])) {
        printf("%s: Erreur : Argument absent ou non entier !\n", argv[0]);
        return -1;
    }

    for (int i = 0; i < atoi(argv[1]); i++); {
        double mul = a/b;
    }
    
    return 0;
}