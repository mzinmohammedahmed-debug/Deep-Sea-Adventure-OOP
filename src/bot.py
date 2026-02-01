import random
from aventurier import Aventurier

class Bot(Aventurier):
    """
    Joueur contrôlé par l'ordinateur.
    Prend toutes ses décisions automatiquement.
    """

    def __init__(self, nom, position=0, sens="plonger"):
        super().__init__(nom, position, sens)

    # --- Décision de rentrer vers le sous-marin ---
    def decide_rentrer(self,jeu):
        # Rentre si lourd ou 50% des cas
        if self.poids() > 3:
            return True
        return random.random() < 0.5

    # --- Décision de ramasser une ruine ---
    def decide_prendre_ruine(self,jeu, case_contenu):
        return random.random() < 0.5

    # --- Décision de déposer une ruine sur case blanche ---
    def decide_deposer_ruine(self,jeu):
        if not self.tresors_par_manche:
            return False
        return random.random() < 0.5

    # --- Choisit automatiquement une ruine à déposer ---
    def choisir_ruine_a_deposer(self,jeu):
        if not self.tresors_par_manche:
            return None
        return random.choice(self.tresors_par_manche)
