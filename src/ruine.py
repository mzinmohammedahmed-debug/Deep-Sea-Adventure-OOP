import random

class Ruine:
    def __init__(self, niveau):
        self.niveau = niveau
        # Points en fonction du niveau (règles classiques)
        if niveau == 1:
            self.nombre_de_points = random.randint(0, 3)
        elif niveau == 2:
            self.nombre_de_points = random.randint(4, 7)
        elif niveau == 3:
            self.nombre_de_points = random.randint(8, 11)
        else: # Niveau 4
            self.nombre_de_points = random.randint(12, 15)

    def __repr__(self):
        return f"[Niv {self.niveau}|{self.nombre_de_points}pts]"

def creation_des_ruines():
    """Crée la liste des 32 ruines du plateau"""
    plateau = [0] # Case 0 = Sous-marin
    # 8 ruines de chaque niveau (1 à 4)
    for niv in range(1, 5):
        for _ in range(8):
            plateau.append([Ruine(niv)])
    return plateau


