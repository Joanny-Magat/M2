#include <stdio.h>
#include <stdlib.h> 
#include <time.h> 
#include <math.h> 

// Création d'un objet Particule
typedef struct { 
 double x;
 double y;
 double vx;
 double vy;
} Particule;

// Calcule TOUTES les forces d'un coup grâce à la 3ème loi de Newton
void Forces(int nb_particules, Particule *particules, double *Fx, double *Fy) {

 // 1. On remet toutes les forces à zéro
 for (int i = 0; i < nb_particules; i++) {
 Fx[i] = 0.0;
 Fy[i] = 0.0;
 }

 // 2. On boucle sur les paires uniques (i et j)
 for (int i = 0; i < nb_particules; i++) {
 for (int j = i + 1; j < nb_particules; j++) {
 
 // Calcul du vecteur distance
 double dx = particules[i].x - particules[j].x;
 if (dx > 50.0) { dx -= 100.0; }
 else if (dx < -50.0) { dx += 100.0; }
 
 double dy = particules[i].y - particules[j].y;
 if (dy > 50.0) { dy -= 100.0; }
 else if (dy < -50.0) { dy += 100.0; }
 
 double r2 = dx * dx + dy * dy;

 // Évite une division par zéro
 if (r2 == 0.0) { continue; }

 // Calcul de la force de Lennard-Jones
 double sr2 = 8 / r2;
 double sr6 = sr2 * sr2 * sr2;
 double coefficient = (24.0 / r2) * (2.0 * sr6 * sr6 - sr6);
 
 double force_x = coefficient * dx;
 double force_y = coefficient * dy;

 // 3ème loi de Newton : Action / Réaction
 // La force subie par 'i' est l'inverse de celle subie par 'j'
 Fx[i] += force_x;
 Fy[i] += force_y;
 
 Fx[j] -= force_x;
 Fy[j] -= force_y;
 }
 }
}

int main(int argc, char *argv[]) {

 if (argc < 3) {
 printf("Usage : %s nombre_particules nombre_frames\n", argv[0]);
 return 1;
 }

 srand(time(NULL)); // Seed aléatoire unique

 // création d'un fichier csv qui stocke les résultats pour utilisation par python
 FILE *fichier = fopen("resultats.csv", "w");

 if (fichier == NULL) {
 printf("Impossible de créer le fichier.\n");
 return 1;
 }

 fprintf(fichier, "n°particule,x,y,vx,vy\n");

 //initialisation des constantes définie par l'utilisateur
 int nb_particules = atoi(argv[1]); 
 int nb_repetition = atoi(argv[2]); 
 double dt = 0.01; 
 
 // création des n particules
 Particule *particules = malloc(nb_particules * sizeof(Particule));

 if (particules == NULL) {
 printf("Erreur d'allocation mémoire.\n");
 fclose(fichier);
 return 1;
 }

 // Initialisation des particules ordonnée
 int cote = (int)ceil(sqrt(nb_particules));
 double a = 100.0/cote;
 for (int i = 0; i < nb_particules; i++) {
 particules[i].x = (double)(a * (i % cote) + a/2);
 particules[i].y = (double)(a * (i / cote)) + a/2;
 particules[i].vx = (double)(-10 + (rand() % 21));
 particules[i].vy = (double)(-10 + (rand() % 21));
 }

 // Allocation pour les forces
 double *Fx = malloc(nb_particules * sizeof(double));
 double *Fy = malloc(nb_particules * sizeof(double));
 double *Fx_new = malloc(nb_particules * sizeof(double));
 double *Fy_new = malloc(nb_particules * sizeof(double));

 if (Fx == NULL || Fy == NULL || Fx_new == NULL || Fy_new == NULL) {
 printf("Erreur d'allocation mémoire.\n");
 free(particules); free(Fx); free(Fy); free(Fx_new); free(Fy_new);
 fclose(fichier);
 return 1;
 }

 // CALCUL DES FORCES INITIALES
 Forces(nb_particules, particules, Fx, Fy);

 // BOUCLE PRINCIPALE DE LA SIMULATION
 for (int repetition = 0; repetition < nb_repetition; repetition++) {

 printf("Frame %d : \n", repetition);

 for (int i = 0; i < nb_particules; i++) {
 printf("particule %d | x : %f, y : %f, vx : %f, vy : %f \n", i, particules[i].x, particules[i].y, particules[i].vx, particules[i].vy);
 fprintf(fichier, "%d,%f,%f,%f,%f\n", i, particules[i].x, particules[i].y, particules[i].vx, particules[i].vy);
 }

 // ÉTAPE 1 : Nouvelles positions
 for (int i = 0; i < nb_particules; i++) {
 particules[i].x += particules[i].vx * dt + Fx[i] *0.5 * dt * dt;
 if (particules[i].x > 100.0) { particules[i].x -= 100.0; }
 if (particules[i].x < 0.0) { particules[i].x += 100.0; }
 
 particules[i].y += particules[i].vy * dt + Fy[i] * 0.5 * dt * dt;
 if (particules[i].y > 100.0) { particules[i].y -= 100.0; }
 if (particules[i].y < 0.0) { particules[i].y += 100.0; }
 }

 // ÉTAPE 2 : Nouvelles forces
 Forces(nb_particules, particules, Fx_new, Fy_new);

 // ÉTAPE 3 : Nouvelles vitesses
 for (int i = 0; i < nb_particules; i++) {
 particules[i].vx += 0.5 * (Fx[i] + Fx_new[i]) * dt;
 particules[i].vy += 0.5 * (Fy[i] + Fy_new[i]) * dt;
 }

 // ÉTAPE 4 : Mise à jour des forces
 for (int i = 0; i < nb_particules; i++) {
 Fx[i] = Fx_new[i];
 Fy[i] = Fy_new[i];
 }
 }

 // Libération de la mémoire
 free(particules);
 free(Fx);
 free(Fy);
 free(Fx_new);
 free(Fy_new);
 fclose(fichier);
 
 return 0;
}