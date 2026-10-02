// vectorisation-loops-check.c

/* 
README : illustrate caveats when trying to vectorise loops
 gcc -O3 -fopt-info-vec -fopt-info-vec-missed vectorisation-loops-check-exo.c -o loops.out
 time ./loops.out  
*/

#include <stdio.h>
#include <assert.h>

int f(int i,int imax) {
  return (i<imax)*27;
}
    

int main() {	  

  const int dim=100000;
  int x[dim];
  int y[dim];

  // loop #0: 
  for (int i=0; i<dim; i++)
    x[i]=dim-i-1;
  
  // loop #1: 
  for (int i=0; i<dim; i++)
    x[i] *=i;
  
  // loop #2:
  const int k=10;
  assert(k>=0);
  assert(k<dim/2);
  for (int i=dim/2; i<dim; i++)
    x[i]=x[i-2]; // dummy operation
  
  // loop #3:
  for (int i=0; f(i,dim)>0; i++)
    x[i]+=2;  

  // loop #4:
  for (int i=0; i<dim; i++) {
    if (i>0)
      x[i]+=2;
  }

  // loop #5: 
  for (int i=0; i<dim; i++)
    x[i]+=f(x[i],dim);  

  // loop #5: 
  for (int i=0; i<dim; i++)
    x[i]+=y[i];  


  // loop #6: 
  for (int i=0; i<dim; i++)
    x[i]+=x[y[i]];  

  printf("k: %d",k); // dummy print
}
