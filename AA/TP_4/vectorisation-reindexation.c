// vectorisation-loops-check.c

/* 
README : vectorise a non-vectorisable loop via a temporary array with re-indexing

gcc -O3 -fopt-info-vec -fopt-info-vec-missed vectorisation-reindexation.c -o reindex.out
time ./reindex.out  
 */

#include <stdio.h>
#include <assert.h>


int main() {	  

  const int dim=100000;
  double A[dim];

  // initialise array
  for (int i=0; i<dim; i++)
    A[i] = 1./(i+1);

  // calculate required sum
  double S=0;
  for (int i=0; i<dim; i++)
    S += (i+1)*A[i] +1./(i+1)*A[dim-i-1]; 
  

  printf("S: %lf",S); // dummy print
}
