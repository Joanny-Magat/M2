/*

@author: magat-j
joanny.magat@etu.umontpellier.fr

Crée N particules initialement alignées verticalement et ayant des vitesses de même norme et de directions aléatoires.
Ces particules évoluent dans une boîte périodique.
On utilise les coordonnées cartésiennes en 2D.
La simulation dure T tours.
Ensuite, simule à chaque instant leurs évolutions grâce au potentiel de lenard-Jones.
Tous les x tours, x étant calculé de sorte à avoir Nb_lignes dans le csv,
la position,la vitesse et l'accélération de chaque particule est sauvegardée et le tout est au final exporté dans un csv.

N = argv[1] (entier)
T = argv[2] (entier)
Nb_lignes = argv[3] (entier)

Compilation :
gcc -O0 Pot_Lenard-Jones_perio.c -o Pot_Lenard-Jones_perio.out -lm
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
#include <assert.h>

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

    assert(
        argc <= 4 &&
        (argc < 2 || est_entier(argv[1])) &&
        (argc < 3 || est_entier(argv[2])) &&
        (argc < 4 || est_entier(argv[3]))
    );


    // Constantes //

    int N = atoi(argv[1]);
    int T = atoi(argv[2]);
    int nombre_lignes_csv = atoi(argv[3]);

    double dt = 0.0001;
    int L = (int) (2*sqrt(N)); // Longueur de la boite
    double d_min_carre = 1; // Carré de la distance minimum initiale entre deux particules

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
    snprintf(nom_csv, sizeof(nom_csv), "data/PotLJ_perio_date=%s_N=%d_T=%d_NbLignes=%d_L=%d.csv", buffer, N, T, nombre_lignes_csv, L);

    FILE *fichier = fopen(nom_csv, "w");

    if (fichier == NULL) {
        printf("Erreur : Impossible de créer le fichier.\n");
        return 1;
    }

    fprintf(fichier, "//////////////////////////////////////////////////////\n");
    fprintf(fichier, "// Potentiel de Lenard-Jones dans une boîte périodique %d x %d.\n", L, L);
    fprintf(fichier, "// Simulation de N = %d particules pendant T = %d tours.\n", N, T);
    fprintf(fichier, "// Ce CSV contient %d tours sur les %d.\n", nombre_lignes_csv, T);
    fprintf(fichier, "// Constantes : sigma^2 = 10, espilon = 1, m = 1.\n");
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
        double ax1; // ax en t+1
        double ay1; // ay en t+1
    } Particule;
    
    Particule *l_particules = malloc(N*sizeof(Particule));

    fprintf(fichier, "###### Tour 0 ######\n");


    // Création de la particule 0 :
    l_particules[0].x = (double)(-L/2 + rand() % L); // Nombre aléatoire entre -L/2 et L/2
    l_particules[0].y = (double)(-L/2 + rand() % L); // Nombre aléatoire entre -L/2 et L/2
    l_particules[0].vx = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
    l_particules[0].vy = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
    l_particules[0].ax = 0;
    l_particules[0].ay = 0;
    l_particules[0].ax1 = 0;
    l_particules[0].ay1 = 0;
    fprintf(fichier, "0,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", l_particules[0].x, l_particules[0].y, l_particules[0].vx, l_particules[0].vy, l_particules[0].ax, l_particules[0].ay);
    

    for (int i = 1; i < N; i++) {

        int i_trop_proche = 0; // Par défaut ne fait la boucle do while que une fois

        do {

            i_trop_proche = 0;

            l_particules[i].x = (double)(-L/2 + rand() % L); // Nombre aléatoire entre -L/2 et L/2
            l_particules[i].y = (double)(-L/2 + rand() % L); // Nombre aléatoire entre -L/2 et L/2
            l_particules[i].vx = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
            l_particules[i].vy = (double)(-1 + rand() % 3); // Nombre aléatoire entre -1 et 1
            l_particules[i].ax = 0;
            l_particules[i].ay = 0;
            l_particules[i].ax1 = 0;
            l_particules[i].ay1 = 0; 

            double xi = l_particules[i].x;
            double yi = l_particules[i].y;

            for (int j = 0; j < i; j++) {
                
                double xj = l_particules[j].x;
                double yj = l_particules[j].y;
                double dx = xj - xi;
                double dy = yj - yi;

                // Périodicité :
                if (dx > L/2)  dx-= L/2;
                if (dx < -L/2) dx+= L/2;
                if (dy > L/2)  dy-= L/2;
                if (dy < -L/2) dy+= L/2;


                double r_carre = dx*dx+dy*dy;


                // Test si trop proche
                if (r_carre < d_min_carre) {
                    i_trop_proche = 1; // Les deux particules sont trop proches donc on régénère les positions de i
                    break;
                }

                /*
                double F_ij_x = 
                ( 24 / r_carre )
                * ( 2*pow(1/r_carre,6)
                - pow(1/r_carre,3) ) * dx;
                
                double F_ij_y = 
                ( 24 / r_carre )
                * ( 2*pow(1/r_carre,6)
                - pow(1/r_carre,3) ) * dy;


                // Symétrie et masse normalisée
                l_particules[i].ax += F_ij_x;
                l_particules[i].ay += F_ij_y;
                l_particules[j].ax -= F_ij_x;
                l_particules[j].ay -= F_ij_y;
                */
            }

        } while (i_trop_proche);

        

        fprintf(fichier, "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy, l_particules[i].ax, l_particules[i].ay);
    }



    
    // Calcul de la simulation //



    int numero_ligne_actuelle_csv = 1;
    int prochain_tour_csv = (int) ( ((long long)numero_ligne_actuelle_csv * T) / nombre_lignes_csv );
    //Numéro du prochain tour où il faudra enregistrer les données dans le csv


    for (int t = 1; t < T; t++) { // à chaque tour
    
        for (int i = 0; i < N; i++) { // pour chaque particule i 
            
            double axi1 = 0;
            double ayi1 = 0;

            for (int j = 0; j < N; j++) { // pour chaque couple i-j, symétrie NON prise en compte (sinon faire j < i)

                if ( i == j ) {continue;}
 
                double dx = l_particules[j].x - l_particules[i].x;
                double dy = l_particules[j].y - l_particules[i].y;

                // Périodicité :
                if (dx > L/2) {dx-= L/2;}
                if (dx < -L/2){dx+= L/2;}
                if (dy > L/2) {dy-= L/2;}
                if (dy < -L/2) {dy+= L/2;}


                double r_carre = dx*dx + dy*dy;
                if (r_carre == 0) {continue;}

                double un_sur_r_carre = 10 / r_carre; // sigma*sigma = 10
                double un_sur_r_6 = un_sur_r_carre * un_sur_r_carre * un_sur_r_carre;

                double F_ij_x = 
                ( 24 * un_sur_r_carre )
                * ( 2 * un_sur_r_6 * un_sur_r_6
                - un_sur_r_6 ) * dx;
                
                double F_ij_y = 
                ( 24 * un_sur_r_carre )
                * ( 2 * un_sur_r_6 * un_sur_r_6
                - un_sur_r_6 ) * dy;


                axi1 += F_ij_x; // Masse normalisée
                ayi1 += F_ij_y;

                /*
                // Symétrie
                l_particules[j].ax1 -= F_ij_x;
                l_particules[j].ay1 -= F_ij_y;
                */
            }

            l_particules[i].ax1 = axi1;
            l_particules[i].ay1 = ayi1;

        }

        for (int i = 0; i < N; i++) {

            // Algorithme de Verlet à un pas
            l_particules[i].x = fmod( (l_particules[i].x + dt*l_particules[i].vx + 0.5 * dt*dt * l_particules[i].ax), L ); // Périodicité :
            l_particules[i].y = fmod( (l_particules[i].y + dt*l_particules[i].vy + 0.5 * dt*dt * l_particules[i].ay), L ); // On replie les positions dans [0, L] avec fmod (modulo)
            l_particules[i].vx = l_particules[i].vx + 0.5 * dt * (l_particules[i].ax + l_particules[i].ax1);
            l_particules[i].vy = l_particules[i].vy + 0.5 * dt * (l_particules[i].ay + l_particules[i].ay1);
        
            l_particules[i].ax = l_particules[i].ax1;
            l_particules[i].ay = l_particules[i].ay1; 
        }

        if (t == prochain_tour_csv) { // Si on doit écrire les données durant ce tour

            fprintf(fichier, "###### Tour %d ######\n", t);

            for(int i = 0; i<N; i++){
                fprintf(fichier, "%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy, l_particules[i].ax, l_particules[i].ay);
                //printf("%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy, l_particules[i].ax, l_particules[i].ay);
            }

            numero_ligne_actuelle_csv++;
            if ( numero_ligne_actuelle_csv < nombre_lignes_csv ) { // Calcule le prochain tour où il faudra écrire (sauf si ça dépasse le nombre max de tour)
                prochain_tour_csv = (int) ( ((long long)numero_ligne_actuelle_csv * T) / nombre_lignes_csv );
            }

        }
    }

    fclose(fichier);
    free(l_particules);
    return 0;
}