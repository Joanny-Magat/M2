#include <stdio.h>

int main( int argc, char *argv[] )  {

   if( argc < 2 ) {
      printf("%s: oops - no command line argument given\n", argv[0]);
     return -1; /* error */
   }

   printf("argument supplied is: %s\n", argv[1]);
   return 0;
}