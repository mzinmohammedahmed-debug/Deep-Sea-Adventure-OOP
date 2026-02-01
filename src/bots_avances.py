from bot import Bot

class BotPrudent(Bot):
    """
    Stratégie : Sécurité maximale.
    - Prend le premier trésor qu'il trouve.
    - Rentre immédiatement dès qu'il possède au moins 1 ruine.
    """
    def decide_rentrer(self, jeu):
        # Rentre s'il a le moindre trésor
        return len(self.tresors_par_manche) >= 1

    def decide_prendre_ruine(self, jeu, case_contenu):
        # Ne prend une ruine que s'il n'en a pas déjà (pour ne pas être ralenti)
        return len(self.tresors_par_manche) == 0

    def decide_deposer_ruine(self, jeu):
        # Ne dépose jamais, car il ne prend qu'un seul trésor et rentre avec.
        return False
    


class BotGourmand(Bot):
    """
    Stratégie : Risque élevé.
    - Ignore les niveaux 1 et 2.
    - Ne rentre que s'il est très chargé ou si l'air est critique.
    """
    def decide_rentrer(self, jeu):
        # Rentre seulement si l'air est critique (< 10) OU s'il porte beaucoup (> 2 ruines)
        if jeu.air < 10:
            return True
        return len(self.tresors_par_manche) > 2

    def decide_prendre_ruine(self, jeu, case_contenu):
        # Regarde ce qu'il y a sur la case
        niveau_moyen = sum(r.niveau for r in case_contenu) / len(case_contenu)
        
        # Prend seulement si c'est intéressant (Niveau >= 2) ou s'il est déjà sur le retour
        if self.sens == "remonter":
            return True # Sur le retour, on ramasse tout ce qui traîne
        
        return niveau_moyen >= 2

    def decide_deposer_ruine(self, jeu):
        # Ne dépose que si l'air est vraiment bas (< 5) pour se sauver
        return jeu.air < 5
    

class BotCalculateur(Bot):
    """
    Stratégie : Probabiliste.
    - Estime le nombre de tours pour rentrer selon son poids.
    - Rentre si (Air Restant) < (Distance / Vitesse Moyenne) + Marge de sécurité.
    """
    def decide_rentrer(self, jeu):
        if self.position == 0:
            return False
            
        # Vitesse moyenne d'un dé (2 à 6) est 4. 
        # On soustrait le poids (nombre de trésors). Minimum 1 case/tour.
        vitesse_estimee = max(1, 4 - self.poids())
        
        # Combien de tours pour rentrer ?
        tours_necessaires = self.position / vitesse_estimee#temps nécessaire pour aller au sous-marin
        
        # Combien d'air sera consommé par TOUS les joueurs par tour ?
        # (C'est une estimation, on suppose que le nombre de trésors des autres reste constant)
        conso_air_tour = 0
        for j in jeu.dico_joueurs.keys():
            if not j.revenu:
                conso_air_tour += j.poids()
        
        conso_air_tour = max(1, conso_air_tour) # Au minimum 1 si quelqu'un prend un truc
        
        # Air nécessaire pour que JE rentre
        air_necessaire = tours_necessaires * conso_air_tour
        
        # On rentre si l'air restant est proche de ce qui est nécessaire (avec marge de 2 d'erreur)
        return jeu.air <= (air_necessaire + 2)

    def decide_prendre_ruine(self, jeu, case_contenu):
        # Ne prend pas si ça le rend trop lent pour rentrer vu l'air actuel
        futur_poids = self.poids() + 1
        vitesse_estimee = max(1, 4 - futur_poids)
        tours_necessaires = self.position / vitesse_estimee
        
        if (tours_necessaires * futur_poids) > jeu.air:
            return False # Ça serait du suicide
        return True

    def decide_deposer_ruine(self, jeu):
        # Si l'air chute drastiquement, il lâche du lest
        return jeu.air < 8 and self.poids() > 1