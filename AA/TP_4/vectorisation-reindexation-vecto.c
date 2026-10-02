// vectorisation-loops-check.c

/* 
README : vectorise a non-vectorisable loop via a temporary array with re-indexing

gcc -O3 -fopt-info-vec -fopt-info-vec-missed vectorisation-reindexation-vecto.c -o reindex-vecto.out
time ./reindex-vecto.out  
 */

#include <stdio.h>
#include <assert.h>

int main() {	  

  const int dim=100000;
  double A[dim];
  double A_inv[dim];

  // initialise array
  for (int i=0; i<dim; i++) {
    A[i] = 1./(i+1);
    
  }
  for (int i=0; i<dim; i++) {
    A_inv[dim-i-1] = A[i];
  }

  // calculate required sum
  double S[dim];
  for (int i=0; i<dim; i++)
    S[i] = (i+1)*A[i] +1./(i+1)*A_inv[i]; 
  
  double sum = 0;
  for (int i=0; i<dim; i++)
    sum += S[i];
  printf("S: %lf",sum); // dummy print
}
