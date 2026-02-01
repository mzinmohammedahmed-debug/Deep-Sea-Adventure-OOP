from bot import Bot
from aventurier import Aventurier

def tour(jeu, bot_controller, joueur):
    """Gère un tour complet pour un joueur (Humain ou Bot)"""
    
    # 1. Réduction de l'air
    jeu.reduire_air(joueur)
    
    # Si l'air est vide après la respiration, on arrête tout de suite
    if jeu.air <= 0:
        return

    # --- CAS BOT ---
    if isinstance(joueur, Bot):
        # Le bot réfléchit (rentrer ?)
        bot_controller.rentrer(jeu, joueur)
        # Le bot avance
        jeu.avancer(joueur)
        # Le bot réfléchit (action sur la case ?)
        if not joueur.revenu:
            bot_controller.chercher(jeu, joueur)

    # --- CAS HUMAIN ---
    else:
        # L'interface demande au joueur s'il veut rentrer
        jeu.rentrer(joueur)
        # Le joueur avance (animation graphique incluse dans jeu.avancer)
        jeu.avancer(joueur)
        # Si le joueur est toujours dans l'eau, l'interface lui demande quoi faire sur la case
        if not joueur.revenu:
            jeu.chercher(joueur)