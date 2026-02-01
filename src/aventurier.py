from ruine import Ruine

class Aventurier:
    def __init__(self, nom, position=0, sens="plonger"):
        # SUPPRESSION DU INPUT BLOQUANT ICI
        self._nom = nom
        self._position = position
        self._tresors_par_manche = []
        self._nb_tresor_manche = 0
        self._score = 0
        self._sens = sens.lower()
        self._revenu = False

    @property
    def nom(self): return self._nom
    @property
    def position(self): return self._position
    @position.setter
    def position(self, val): self._position = val
    @property
    def nb_tresor_manche(self): return self._nb_tresor_manche
    @nb_tresor_manche.setter
    def nb_tresor_manche(self, val): self._nb_tresor_manche = val
    @property
    def score(self): return self._score
    @property
    def tresors_par_manche(self): return self._tresors_par_manche
    @tresors_par_manche.setter
    def tresors_par_manche(self, value) : self._tresors_par_manche = value
    @property
    def sens(self): return self._sens
    @sens.setter
    def sens(self, value): self._sens = value
    @property
    def revenu(self): return self._revenu
    @revenu.setter
    def revenu(self, val): self._revenu = val

    def ajouter_tresor(self, r: Ruine):
        self._tresors_par_manche.append(r)

    def retirer_tresor(self, r: Ruine):
        try:
            self._tresors_par_manche.remove(r)
            return True
        except ValueError:
            return False

    def ajouter_score(self):
        for tresor in self._tresors_par_manche :
            self._nb_tresor_manche += 1
            self._score += tresor.nombre_de_points
    
    def vider_tresors_manche(self):
        self._tresors_par_manche.clear() 

    def poids(self)-> int:
        return len(self._tresors_par_manche)   

    def __repr__(self):
        return f"{self._nom} (pos={self._position})"