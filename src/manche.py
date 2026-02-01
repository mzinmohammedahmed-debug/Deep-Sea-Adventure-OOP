from tour import tour
from gestions_des_erreurs import AirExhaustedError
import time

def jouer_manche(jeu, bot_controller, ordre):
    j = 0
    # La manche continue tant que :
    # 1. Tout le monde n'est pas rentré
    # 2. Il reste de l'air (vérifié dans tour et ici)
    
    while not jeu.tous_revenus():
        
        if jeu.air <= 0:
            raise AirExhaustedError(jeu.air)

        joueur = ordre[j]

        if not joueur.revenu:
            # On surligne le joueur actuel dans les logs
            jeu.log(f"\n--- Tour de {joueur.nom} ---")
            
            tour(jeu, bot_controller, joueur)
            
            # Vérification après le tour
            if jeu.air <= 0:
                raise AirExhaustedError(jeu.air)
                
            time.sleep(0.5) # Petite pause entre les joueurs

        # Joueur suivant
        j = (j + 1) % len(ordre)