// hello world : see OpenMP hands on tutorial
// compilation: gcc -fopenmp hello.c
#include <stdio.h>
#include "omp.h"
void main() {
#pragma omp parallel
{
int ID = omp_get_thread_num();
printf("hello world (%d) \n", ID);
}
}