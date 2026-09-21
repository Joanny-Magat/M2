#include <stdio.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>

    /*
    ICI sigma   = 1
    et  epsilon = 1
    */

//macros pour cstes globales
#define Rc   2.5
#define Rc2  (Rc*Rc)
#define src2 (1.0/Rc2)
#define src6 (src2*src2*src2)
#define uc   (4*(src6*src6 - src6))

//const double epsilon = 1;
//const double sigma = 1;

const double m = 1;         // masse des particules, on se fixe same masse
const double dmin2 = 1.0;   // carré de la distance mini autorisée entre deux particules

double dx;
double dy;
double r2;

//double sr2,sr6,sr12;

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//           FONCTIONS
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


void interactions(double dx, double dy, double r2,
                  double *u12, double *f12x, double *f12y) {
    if (r2 > Rc2) { *u12 = *f12x = *f12y = 0; return; }
    double sr2  = 1.0/r2;          // ← r2 = le PARAMÈTRE, la vraie distance²
    double sr6  = sr2*sr2*sr2;
    double sr12 = sr6*sr6;
    *u12  = 4*(sr12 - sr6) - uc;
    double f_temp = -24.0/r2*(sr6 - 2*sr12);
    *f12x = f_temp*dx;
    *f12y = f_temp*dy;
}

// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//             MAIN
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 


int main(int argc, char *argv[]) {
    //srand(time(NULL));

    if( argc < 2 ) { // au cas ou pas de arg
        printf("%s: oops - no command line argument given\n", argv[0]);
        return -1; /* error */
    }

    // VARIABLES 
    int arg = atoi(argv[1]); // nb Particules
    // INFO PARTICULES
    double x[arg];  // x des particules
    double y[arg];  // y des particules
    double vx[arg]; // vitesse en x des particules
    double vy[arg]; // vitesse en y des particules
    // accel useless pr linstant voir en bas
    //double ax[arg]; // accélération en x des particles   
    //double ay[arg]; // accélération en y des particles
    double axold[arg]; //meme si pas de ax et ay il faut ça 
    double ayold[arg]; 

    double **r = malloc(arg * sizeof(double*)); // mat des distances MTN CE SERA LES DIST AU CARRE
    for (int i = 0; i < arg; i++){
        r[i] = malloc(arg * sizeof(double));
    }

    for(int i=0;i<arg;i++){ //vitesse init random
        vx[i]=(float)(-1 + (rand() % 3));   // 0,1,2 -> -1,0,+1
        vy[i]=(float)(-1 + (rand() % 3));
    }
    //
    double **u = malloc(arg * sizeof(double*));
    for (int i = 0; i < arg; i++){
        u[i] = malloc(arg * sizeof(double));
    }

    // FORCSE
    double fx[arg]; // tab des forces qui agissent en x sur chq particle
    double fy[arg]; // tab des forces qui agissent en y sur chq particle

    // TEMPS
    double nbpas = 1000;
    double dt = 0.01;

//------------------------------------
// boucle initiale
//------------------------------------
    for(int i=0;i<arg;i++){
        r[i][i]=0;
        int ok = 0; // booleen

        fx[i]=0;fy[i]=0;
        while(!ok){ // gen positions initiales random
            x[i]=(float)((rand() % 20));
            y[i]=(float)((rand() % 20));
            ok = 1;
            for(int j=0;j<i;j++){
                if(i==j) continue;
                
                dx = x[i]-x[j];
                dy = y[i]-y[j];
                
                // POUR LA PERIODICITE
                if (dx > 20/2)  dx-= 20;
                if (dx < -20/2) dx+= 20;
                if (dy > 20/2)  dy-= 20;
                if (dy < -20/2) dy+= 20;
                
                r[i][j] = dx*dx + dy*dy;
                if(r[i][j] < dmin2){ ok = 0; break; } // cond pr pas qu'elles spawnent trop proches
                r[j][i] = r[i][j];

                //SI C OK ON CONTINUE : 
                double u12, f12x, f12y; //temp pr add après 
                //sr2  = 1/r2;
                //sr6  = sr2*sr2*sr2; // sigma puissance 6
                //sr12 = sr6*sr6;

                interactions(dx, dy,r[i][j], &u12, &f12x, &f12y);
                
                u[i][j]=u12;
                fx[i] += f12x;
                fy[i] += f12y;
                fx[j] -= f12x;
                fy[j] -= f12y;
                
            }
            // accel useless ici car enft on use juste le tab des fx et fy vu que m=1
            //ax[i] = fx[i]; // c'est f / m ici mais comme m=1 on met pas
            //ay[i] = fy[i];
        }   
    }


//------------------------------------
// Boucle temporelle
//------------------------------------



    for(int t=0;t<nbpas;t++){
        // nouvelles pos
        ////////////////////
        for(int i=0;i<arg;i++){
            x[i] += vx[i]*dt + 0.5*fx[i]*dt*dt;
            y[i] += vy[i]*dt + 0.5*fy[i]*dt*dt;
            // 2. on replie dans [0, L] avec fmod
            x[i] = fmod(x[i], 20);  if (x[i] < 0) x[i] += 20;
            y[i] = fmod(y[i], 20);  if (y[i] < 0) y[i] += 20;
            // et on stock old accel :
            axold[i] = fx[i];
            ayold[i] = fy[i];

            fx[i]=0;fy[i]=0;
            for(int j=0;j<i;j++){
                if(i==j) continue;
                dx = x[i]-x[j];
                dy = y[i]-y[j];

                // POUR LA PERIODICITE :
                if (dx > 20/2)  dx-= 20;
                if (dx < -20/2) dx+= 20;
                if (dy > 20/2)  dy-= 20;
                if (dy < -20/2) dy+= 20;

                r[i][j] = dx*dx + dy*dy;
                r[j][i] = r[i][j];

                //SI C OK ON CONTINUE : 
                double u12, f12x, f12y; //temp pr add après 
                //sr2  = 1/r2;
                //sr6  = sr2*sr2*sr2; // sigma puissance 6
                //sr12 = sr6*sr6;

                interactions(dx, dy,r[i][j], &u12, &f12x, &f12y);

                u[i][j]=u12;
                fx[i] += f12x;
                fy[i] += f12y;
                fx[j] -= f12x;
                fy[j] -= f12y;
            }
            // NOUVELLES VITESSES ET ACCELERATIONS : 

            // accel useless ici car enft on use juste le tab des fx et fy vu que m=1
            //ax[i] = fx[i]; // c'est f / m ici mais comme m=1 on met pas
            //ay[i] = fy[i];
            vx[i] += 0.5*(axold[i] + fx[i])*dt;
            vy[i] += 0.5*(ayold[i] + fy[i])*dt;

     
        }
        

        char nom[256];
        sprintf(nom, "data/etat_%d.csv", t);
        FILE *f = fopen(nom, "w");
        if (f == NULL) {printf("Erreur %s\n", nom); return 1;}
        
        fprintf(f, "i,x,y,vx,vy,ax,ay,fx,fy\n");
        for(int i = 0; i<arg; i++){
            fprintf(f,"%d,%f,%f,%f,%f,%f,%f,%f,%f\n",
            i,x[i],y[i],vx[i],vy[i],fx[i],fy[i],fx[i],fy[i]);
        }
        fclose(f);
    } 

    for (int i = 0; i < arg; i++) { free(r[i]); free(u[i]); }
    free(r); free(u);


}