#include <stdio.h>

int main() {
    long int ndim=10000;
    long int niter=10000;
 
    int a[ndim], b[ndim];

    for (long int n=0; n<niter; n++) {

        long int i;
        
        for (i=0; i<ndim; i++)
            a[i]=1;                     

        for (i=0; i<ndim; i++)
            b[i]=2;
    }
    //printf("%g", b[0]);
   return 0;
}


