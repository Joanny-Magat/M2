#include <stdio.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>

/*

Script de Théo

gcc -O0 LJperiod_Theo.c -o Pot_Lenard-Jones_Theo.out -lm
./Pot_Lenard-Jones_Theo.out 100

*/

/////////////////////////////////////////////////
//
//  A FAIRE  : LA BOITE A DES BORDS PERIODIQUES DONC FAUT IMPLEMENTER ÇA.
// dcp faut faire gaffe aussi pr les interactions 
//
/////////////////////////////////////////////////



//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//      FONCTIONS
//
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


//distance
double distance(double x1, double x2, double y1, double y2){
    double dx = x1 - x2;
    double dy = y1 - y2;
    return sqrt(dx*dx + dy*dy);
}





int main(int argc, char *argv[]) {

    //srand(time(NULL));


   if( argc < 2 ) { // au cas ou pas de arg
      printf("%s: oops - no command line argument given\n", argv[0]);
     return -1; /* error */
   }


    double epsilon = 1;
    double sigma = 1;


   int arg = atoi(argv[1]); // nb Particules

    double x[arg]; // x des particules
    double y[arg]; // y des particules.


    double **r = malloc(arg * sizeof(double*));
    for (int i = 0; i < arg; i++){
        r[i] = malloc(arg * sizeof(double));
}

    double vx[arg]; // vitesse en x des particules
    double vy[arg]; // vitesse en y des particules
    
/*
    for(int i=0;i<arg;i++){ //vitesse init random
        vx[i]=(float)(-10 + (rand() % 21));
        vy[i]=(float)(-10 + (rand() % 21));
    }
*/
    for(int i=0;i<arg;i++){ //vitesse init random
        vx[i]=(float)(-1 + (rand() % 3));   // 0,1,2 -> -1,0,+1
        vy[i]=(float)(-1 + (rand() % 3));
    }


    double m = 1; // masse des particules, on se fixe same masse
//------------------------------------
// Calcul des distances r
//------------------------------------
/*
    double a = 1.2;                       // espacement : dans la portée de LJ
    int cote = (int)ceil(sqrt(arg));      // nb de colonnes
    for(int i = 0; i < arg; i++){
        x[i] = a * (i % cote);
        y[i] = a * (i / cote);
    }
*/
    double dmin = 1.0;   // distance mini autorisée entre deux particules



    

    for(int i=0;i<arg;i++){
        int ok = 0;
        while(!ok){
            x[i]=(float)((rand() % 20));
            y[i]=(float)((rand() % 20));
            ok = 1;
            for(int j=0;j<i;j++){
                double dx = x[i]-x[j], dy = y[i]-y[j];
                if(sqrt(dx*dx + dy*dy) < dmin){ ok = 0; break; }
            }
        }
        r[i][i]=0;
        for(int j=0;j<i;j++){
            double dx = x[i] - x[j];
            double dy = y[i] - y[j];
            r[i][j]=sqrt(dx*dx + dy*dy);
            r[j][i]=r[i][j];
        }
    }

    /*
    printf("FIN : \n");
    for(int i = 0;i<arg;i++){
        for(int j = 0;j<arg;j++){
            printf("%6.2f", r[i][j]);
        printf("\n");
        }
    }
    */

    double **u = malloc(arg * sizeof(double*));
    for (int i = 0; i < arg; i++){
        u[i] = malloc(arg * sizeof(double));
    }
//------------------------------------
// Calcul des u(r) 
//------------------------------------

//    double sr[arg][arg];
//    double sr6[arg][arg];

    for(int i=0;i<arg;i++){
        for(int j=0;j<i;j++){

            double sr = sigma/r[i][j];
            double sr6 = sr*sr*sr*sr*sr*sr; // sigma puissance 6
            //printf("\n sr et sr6");
            //printf("%6f ", sigma);
            //printf("%6f ", r[i][j]);
            //printf("%6f ", sr);
            //printf("%6f ", sr6);

            u[i][j] = 4*epsilon * ( sr6*sr6 - sr6 ); // formle de LJ
            //u[j][i] = 0;
            u[j][i] = u[i][j]; // val entre 1-2 = celle entre 2-1
        }
    }

    /*
    printf("u : \n");
    for(int i = 0;i<arg;i++){
        for(int j = 0;j<arg;j++){
            printf("%6f ", u[i][j]);
        }
        printf("\n");
    }
    */

//------------------------------------
// Calcul des forces Fi (somme des u des r)
//------------------------------------


    /*
    pour avoir Fi : 
    faire grad(u_i)
    sommer les grad
    */



    double fx[arg]; // tab des forces qui agissent en x sur chq particle
    double fy[arg]; // tab des forces qui agissent en y sur chq particle

/*
    for(int i = 0; i < arg;i++){
        fx[i] = -(24*epsilon / (r*r)*(sr6-2*sr6*sr6)*x[i]);
        fy[i] = -(24*epsilon / (r*r)*(sr6-2*sr6*sr6)*y[i]);
    }
        ^ ça pas bon du tout
*/

    for(int i = 0; i<arg; i++){
        fx[i]=0;fy[i]=0;
        for(int j = 0; j<arg; j++){
            if(j==i) continue;
            double sr = sigma/r[i][j];
            double sr6 = sr*sr*sr*sr*sr*sr; // sigma puissance 6

            double dx = x[i] - x[j];
            if (dx > 20/2)  dx-= 20;
            if (dx < -20/2) dx+= 20;
            double dy = y[i] - y[j];
            if (dy > 20/2)  dy-= 20;
            if (dy < -20/2) dy+= 20;
            fx[i] += -(24*epsilon / (r[i][j]*r[i][j])*(sr6-2*sr6*sr6)*dx);
            fy[i] += -(24*epsilon / (r[i][j]*r[i][j])*(sr6-2*sr6*sr6)*dy);
        
        }
    }
    


    // mtn les a(t=0) : 
    
    double ax[arg];    
    double ay[arg];
    for(int i=0;i<arg;i++){
        ax[i] = fx[i] / m;
        ay[i] = fy[i] / m;
    }





//------------------------------------
// Boucle temporelle
//------------------------------------


    double nbpas = 1000;
    double dt = 0.01;



    double axold[arg];
    double ayold[arg]; 

    for(int t=0;t<nbpas;t++){
        // nouvelles pos
        ////////////////////
        for(int i=0;i<arg;i++){
            x[i] += vx[i]*dt + 0.5*ax[i]*dt*dt;
            y[i] += vy[i]*dt + 0.5*ay[i]*dt*dt;

            // 2. on replie dans [0, L] avec fmod
            x[i] = fmod(x[i], 20);  if (x[i] < 0) x[i] += 20;
            y[i] = fmod(y[i], 20);  if (y[i] < 0) y[i] += 20;
            // et on stock old accel :
            axold[i] = ax[i];
            ayold[i] = ay[i];
        }

        // nouvelles dist
        ////////////////////
    for(int i=0;i<arg;i++){
            for(int j=0;j<i;j++){
                if(j==i) continue;
                //dx
                double dx = x[i] - x[j];
                if (dx > 20/2)  dx-= 20;
                if (dx < -20/2) dx+= 20;
                double dy = y[i] - y[j];
                if (dy > 20/2)  dy-= 20;
                if (dy < -20/2) dy+= 20;
                r[i][j]=sqrt(dx*dx + dy*dy); // assignation r
                r[j][i]=r[i][j];
            }
        }

        // nouveaux u
        ////////////////////
        for(int i=0;i<arg;i++){
            for(int j=0;j<i;j++){
                double sr = sigma/r[i][j];
                double sr6 = sr*sr*sr*sr*sr*sr; // sigma puissance 6
                u[i][j] = 4*epsilon * ( sr6*sr6 - sr6 ); // formle de LJ
                u[j][i] = u[i][j]; // val entre 1-2 = celle entre 2-1
            }
        }

        
        // nouvelles forces
        /////////////////////
            for(int i = 0; i<arg; i++){
            fx[i]=0;fy[i]=0;
            for(int j = 0; j<arg; j++){
                if(j==i) continue;
                double sr = sigma/r[i][j];
                double sr6 = sr*sr*sr*sr*sr*sr; // sigma puissance 6

                double dx = x[i] - x[j];
                if (dx > 20/2)  dx-= 20;
                if (dx < -20/2) dx+= 20;
                double dy = y[i] - y[j];
                if (dy > 20/2)  dy-= 20;
                if (dy < -20/2) dy+= 20;

                fx[i] += -(24*epsilon / (r[i][j]*r[i][j])*(sr6-2*sr6*sr6)*dx);
                fy[i] += -(24*epsilon / (r[i][j]*r[i][j])*(sr6-2*sr6*sr6)*dy);
            }
        }

        // nouvelles accel
        /////////////////////
        for(int i=0;i<arg;i++){
            ax[i] = fx[i] / m;
            ay[i] = fy[i] / m;
        }

        // nouvelles vitesses
        for(int i=0;i<arg;i++){
            vx[i] += 0.5*(axold[i] + ax[i])*dt;
            vy[i] += 0.5*(ayold[i] + ay[i])*dt;
        }
        
    char nom[256];
    sprintf(nom, "data/etat_%d.csv", t);
    FILE *f = fopen(nom, "w");
    if (f == NULL) {printf("Erreur %s\n", nom); return 1;}
    
    fprintf(f, "i,x,y,vx,vy,ax,ay,fx,fy\n");
    for(int i = 0; i<arg; i++){
        fprintf(f,"%d,%f,%f,%f,%f,%f,%f,%f,%f\n",
        i,x[i],y[i],vx[i],vy[i],ax[i],ay[i],fx[i],fy[i]);
    }
    fclose(f);





    }

    for (int i = 0; i < arg; i++) { free(r[i]); free(u[i]); }
    free(r); free(u);


}