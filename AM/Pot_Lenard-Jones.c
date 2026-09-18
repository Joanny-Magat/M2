/*

@author: magat-j
joanny.magat@etu.umontpellier.fr

Crée N particules initialement alignées verticalement et ayant des vitesses de même norme et de directions aléatoires.
Ces particules évoluent dans un espace infini (à terme il faudra faire une boite carré sans bord ie si on atteint le haut, renvoie en bas).
On utilise les coordonnées cartésiennes en 2D.
La simulation dure T tours.
Ensuite, simule à chaque instant leurs évolutions grâce au potentiel de lenard-Jones.
Tous les x tours, x étant calculé de sorte d'avoir Nb_lignes dans le csv, la position et la vitesse de chaque particule est sauvegardée et le tout est au final exporté dans un csv.

N = argv[1] (entier)
T = argv[2] (entier)
Nb_lignes = argv[3] (entier)

gcc -O0 Pot_Lenard-Jones.c -o Pot_Lenard-Jones.out -lm
(-lm est important pour faire fonctionner pow)

Windows : .\Pot_Lenard-Jones.out 5 1000 10
Linux : ./Pot_Lenard-Jones.out 5 1000 10

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

    double epsilon = 1.0;
    double sigma = 1.0;
    double m = 1.0;
    double dt = 0.01;



    // Création du dossier data s'il n'existe pas //

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
    snprintf(nom_csv, sizeof(nom_csv), "Pot_LJ_N=%d_T=%d_NbLignes=%d_date=%s.csv", N, T, nombre_lignes_csv, buffer);

    FILE *fichier = fopen(nom_csv, "w");

    if (fichier == NULL) {
        printf("Erreur : Impossible de créer le fichier.\n");
        return 1;
    }



    // Initialisation des N particules et du csv //

    typedef struct {
        double x;
        double y;
        double vx;
        double vy;
    } Particule;
    
    Particule *l_particules = malloc(N*sizeof(Particule));

    FILE *fichier0 = fopen("data/tour_0.csv", "w");

    if (fichier0 == NULL) {
        printf("Erreur : Impossible de créer le fichier.\n");
        return 1;
    }

    fprintf(fichier0, "particule,x,y,vx,vy\n");

    for(int i = 0; i<N; i++){
        
    }


    for (int i = 0; i < N; i++) {

        l_particules[i].x = (double)(-100 + rand() % 201); // Nombre aléatoire entre -100 et 100
        l_particules[i].y = (double)(-100 + rand() % 201); // Nombre aléatoire entre -100 et 100
        l_particules[i].vx = (double)(-1 + rand() % 2); // Nombre aléatoire entre -1 et 1
        l_particules[i].vy = (double)(-1 + rand() % 2); // Nombre aléatoire entre -1 et 1

        fprintf(fichier0, "%d,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy);
    }

    fclose(fichier0);



   


    // Fonction force //

    double force(double epsilon, double sigma, double xi, double yi, double xj, double yj) {
        // Calcul de la norme de la force F_ij

        // AMELIORATION : Prendre en compte le cas où les particules sont très proches

        double r_carre = (xj-xi)*(xj-xi)+(yj-yi)*(yj-yi);

        return 
            ( (24*epsilon) / r_carre )
            * ( 2*pow((sigma*sigma)/r_carre,6)
            - pow((sigma*sigma)/r_carre,3) );
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
            
            double axi = 0.0; // composante x de l'accélération de la particule i
            double ayi = 0.0; // composante y de l'accélération de la particule i

            double xi = l_particules[i].x;
            double yi = l_particules[i].y;
            double vxi = l_particules[i].vx;
            double vyi = l_particules[i].vy;

            for (int j = 0; j < N; j++) { // pour chaque couple i-j

                if ( i == j ) {
                    continue;
                }
 
                double xj = l_particules[j].x;
                double yj = l_particules[j].y;

                F_ij[i][j].x = force(epsilon,sigma,xi,yi,xj,yj) * ( xj - xi );
                F_ij[i][j].y = force(epsilon,sigma,xi,yi,xj,yj) * ( yj - yi );
                axi = axi + F_ij[i][j].x;
                ayi = ayi + F_ij[i][j].y;

            }

            axi = axi/m;
            ayi = ayi/m;
            // On applique Euler
            l_particules[i].x = vxi + xi*dt;
            l_particules[i].y = vyi + yi*dt;
            l_particules[i].vx = axi + vxi*dt;
            l_particules[i].vy = ayi + vyi*dt;
            
        }

        if (t == prochain_tour_csv) { // Si on doit écrire les données durant ce tour
            
            char nom_csv[100];
            snprintf(nom_csv, sizeof(nom_csv), "data/tour_%d.csv", t);

            FILE *fichier = fopen(nom_csv, "w");

            if (fichier == NULL) {
                printf("Erreur : Impossible de créer le fichier.\n");
                return 1;
            }

            fprintf(fichier, "particule,x,y,vx,vy\n");

            for(int i = 0; i<N; i++){
                fprintf(fichier, "%d,%.2f,%.2f,%.2f,%.2f\n", i,l_particules[i].x, l_particules[i].y, l_particules[i].vx, l_particules[i].vy);
            }

            fclose(fichier);

            numero_ligne_actuelle_csv++;
            if ( numero_ligne_actuelle_csv < nombre_lignes_csv ) { // Calcule le prochain tour où il faudra écrire (sauf si ça dépasse le nombre max de tour)
                prochain_tour_csv = (int) ( ((long long)numero_ligne_actuelle_csv * T) / nombre_lignes_csv );
            }

        }
    }

    free(F_ij);
    free(F_i);
    free(l_particules);
    
    return 0;
}