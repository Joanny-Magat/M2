// race.c : illustrate race condition in OpenMP
/* 
compilation:  gcc -fopenmp race.c 
*/

#include <stdio.h>
#include "omp.h"



void main() {

  int A = 0;
  omp_set_num_threads(4);

#pragma omp parallel
  {
    int ID = omp_get_thread_num();
    int Aold=A;
    A += ID;

    printf("A on rank %d: %d  -->  %d \n",ID,Aold,A);
    }

  printf("A:  %d (expected: 10)\n",A);

}
