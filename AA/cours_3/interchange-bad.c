#include <stdio.h>

int main (int argc, char * argv[]) {

  long int i, j, m, ndim=100, niter=10000;
  //long int i, j, m, ndim=1000, niter=100;

  float a[ndim][ndim], b[ndim][ndim];

   for (m=0; m<niter; m++) {
     
    for (i=0; i<ndim; i++){
      for (j=0; j<ndim; j++) {
	b[j][i] = a[j][i];
      }
    }
    
   }
   
   printf("%g", b[1][1]); // sans ce printf, gcc v 4.8 optimise trop !
   return 0;
}
