/*

@author: magat-j
joanny.magat@etu.umontpellier.fr

Crée N particules initialement alignées verticalement et ayant des vitesses de même norme et de directions aléatoires.
Ces particules évoluent dans un espace infini (cd Pot_Lenard-Jones_perio.c pour une boîte périodique).
On utilise les coordonnées cartésiennes en 2D.
La simulation dure T tours.
Ensuite, simule à chaque instant leurs évolutions grâce au potentiel de lenard-Jones.
Tous les x tours, x étant calculé de sorte à avoir Nb_lignes dans le csv,
la position,la vitesse et l'accélération de chaque particule est sauvegardée et le tout est au final exporté dans un csv.

N = argv[1] (entier)
T = argv[2] (entier)
Nb_lignes = argv[3] (entier)

Compilation :
gcc -O0 Pot_Lenard-Jones.c -o Pot_Lenard-Jones.out -lm
(-lm est important pour faire fonctionner pow)

Windows : .\Pot_Lenard-Jones_perio.out 100 10000 1000
Linux : ./Pot_Lenard-Jones_perio.out 100 10000 1000

*/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <sys/stat.h>
#include <sys/types.h>

int main(int argc, char *argv[]) {

    srand(time(NULL));

    // Vérification des arguments d'entrées //

    int est_entier(const char *s) {
        for (int i = 0; s[i] != '\0'; i++) {
            if (!isdigit(s[i]))
                return 0;
        }
        return 1;
    }

    if (argc < 4 || !est_entier(argv[1]) || !est_entier(argv[2]) || !est_entier(argv[3]) ) {
        printf("Erreur : Arguments absents ou non entiers !\n");
        return 1;
    }


    // Constantes //

    int N = atoi(argv[1]);
    int T = atoi(argv[2]);
    int nombre_lignes_csv = atoi(argv[3]);

    double dt = 0.01;

    /* Constantes normalisées => on ne les def meme pas vu que tout vaut 1
    double epsilon = 1.0;
    double sigma = 1.0;
    double m = 1.0;
    */



    // Création csv et du dossier data s'il n'existe pas //

    struct stat st;

    if (stat("./data", &st) != 0 || !S_ISDIR(st.st_mode))
    {
        mkdir("./data", 0755);
    }


    time_t now = time(NULL);
    struct tm *date = localtime(&now);
    
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Hh_%Mmin_%Ss_%d_%m_%Y", date);

    char nom_csv[100];
    snprintf(nom_csv, sizeof(nom_csv), "data/PotLJ_date=%s_N=%d_T=%d_NbLignes=%d.csv", buffer, N, T, nombre_lignes_csv);

    FILE *fichier = fopen(nom_csv, "w");

    if (fichier == NULL) {
        printf("Erreur : Impossible de créer le fichier.\n");
        return 1;
    }

    fprintf(fichier, "//////////////////////////////////////////////////////\n");
    fprintf(fichier, "// Potentiel de Lenard-Jones.\n");
    fprintf(fichier, "// Simulation de N = %d particules pendant T = %d tours.\n", N, T);
    fprintf(fichier, "// Ce CSV contient %d tours sur les %d.\n", nombre_lignes_csv, T);
    fprintf(fichier, "// Les constantes sont normalisées ; espilon = 1, sigma = 1, m = 1.\n");
    fprintf(fichier, "// Description des colonnes : particule_i,x,y,vx,vy,ax,ay\n");
    fprintf(fichier, "//////////////////////////////////////////////////////\n");





    // Initialisation des N particules et du csv //

    typedef struct {
        double x;
        double y;
        double vx;
        double vy;
        double ax;
        double ay;
    } Particule;
    
    Particule *l_particules = malloc(N*sizeof(Particule));

    fprintf(fichier, "###### Tour 0 ######\n");

    for (int i = 0; i < N; i++) {

        l_particules[i].x = (double)(-100 + rand() % 201); // Nombre aléatoire entre -100 et 100
        l_particules[i].y = (double)(-100 + rand() % 201); // Nombre aléatoire entre -100 et 100
        l_particules[i].vx = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
        l_particules[i].vy = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
        l_particules[i].ax = 0; // Nombre aléatoire entre -1 et 1
        l_particules[i].ay = 0; 

        fprintf(fichier, "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy, l_particules[i].ax, l_particules[i].ay);
    }


    // Fonction force //

    double force(double xi, double yi, double xj, double yj) {
        // Calcul de la norme de la force F_ij

        // AMELIORATION : Prendre en compte le cas où les particules sont très proches

        double r_carre = (xj-xi)*(xj-xi)+(yj-yi)*(yj-yi);

        return 
            ( 24 / r_carre )
            * ( 2*pow(1/r_carre,6)
            - pow(1/r_carre,3) );
    }


    
    // Calcul de la simulation //


    typedef struct {
        double x;
        double y;
    } Force;
    

    Force **F_ij = malloc(N*sizeof(Force *)); // Liste de tous les F_ij
    Force *F_i = malloc(N*N*sizeof(Force)); // Liste permettant de créer F_ij
    for (int i=0; i<N; i++) {
        F_ij[i] = F_i + i*N;
    }
    
    // OPTIMISATION : On pourrait ne calculer que la moitié des forces,
    // les symétriques étant des opposées


    // Calcul des numéros de tour où on save dans le csv //

    int numero_ligne_actuelle_csv = 1;
    int prochain_tour_csv = (int) ( ((long long)numero_ligne_actuelle_csv * T) / nombre_lignes_csv );
    //Numéro du prochain tour où il faudra enregistrer les données dans le csv



    for (int t = 1; t < T; t++) { // à chaque tour
    
        for (int i = 0; i < N; i++) { // pour chaque particule i 
            
            double xi = l_particules[i].x;
            double yi = l_particules[i].y;
            double vxi = l_particules[i].vx;
            double vyi = l_particules[i].vy;
            double axi = l_particules[i].ax;
            double ayi = l_particules[i].ay;
            double axi1 = 0; // ax i+1
            double ayi1 = 0; // ay i+1

            for (int j = 0; j < N; j++) { // pour chaque couple i-j

                if ( i == j ) {
                    continue;
                }
 
                double xj = l_particules[j].x;
                double yj = l_particules[j].y;

                F_ij[i][j].x = force(xi,yi,xj,yj) * ( xj - xi );
                F_ij[i][j].y = force(xi,yi,xj,yj) * ( yj - yi );
                axi1 = axi1 + F_ij[i][j].x;
                ayi1 = ayi1 + F_ij[i][j].y;
            }

            /* m normalisé
            axi1 = axi1/m;
            ayi1 = ayi1/m;
            */

            l_particules[i].ax = axi1;
            l_particules[i].ay = ayi1;

            /* Euler :
            l_particules[i].x = vxi + xi*dt;
            l_particules[i].y = vyi + yi*dt;
            l_particules[i].vx = axi + vxi*dt;
            l_particules[i].vy = ayi + vyi*dt;
            */

            // Algorithme de Verlet à un pas
            l_particules[i].x = xi + dt*vxi + ( (dt*dt)/2 ) * axi;
            l_particules[i].y = yi + dt*vyi + ( (dt*dt)/2 ) * ayi;
            l_particules[i].vx = vxi + (dt/2) * (axi + axi1);
            l_particules[i].vy = vyi + (dt/2) * (ayi + ayi1);   
        }

        if (t == prochain_tour_csv) { // Si on doit écrire les données durant ce tour

            fprintf(fichier, "###### Tour %d ######\n", t);

            for(int i = 0; i<N; i++){
                fprintf(fichier, "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy, l_particules[i].ax, l_particules[i].ay);
            }

            numero_ligne_actuelle_csv++;
            if ( numero_ligne_actuelle_csv < nombre_lignes_csv ) { // Calcule le prochain tour où il faudra écrire (sauf si ça dépasse le nombre max de tour)
                prochain_tour_csv = (int) ( ((long long)numero_ligne_actuelle_csv * T) / nombre_lignes_csv );
            }

        }
    }

    fclose(fichier);
    free(F_ij);
    free(F_i);
    free(l_particules);
    
    return 0;
}