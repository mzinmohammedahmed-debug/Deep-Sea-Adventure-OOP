class DeepSeaAdventureError(Exception):
    """
    Classe de base pour toutes les exceptions spécifiques au jeu Deep Sea Adventure.
    """
    def __init__(self, message="Une erreur de logique du jeu Deep Sea Adventure s'est produite."):
        self.message = message
        super().__init__(self.message)

# ----------------------------------------------------------------------
# Exceptions de la logique de Jeu Globale
# ----------------------------------------------------------------------

class AirExhaustedError(DeepSeaAdventureError):
    """
    Exception levée lorsque l'air du sous-marin atteint zéro et que la partie
    doit s'arrêter, causant la perte de tous les trésors non-sauvés.
    """
    def __init__(self, air_restant=0):
        message = f"🚨 L'air est épuisé ({air_restant}). Fin immédiate de la manche."
        super().__init__(message)
