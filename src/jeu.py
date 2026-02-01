import numpy.random as npr
import random as rd
from ruine import creation_des_ruines
from aventurier import Aventurier
from bot import Bot
from gestions_des_erreurs import AirExhaustedError, DeepSeaAdventureError
from manche import jouer_manche
from bots_avances import BotPrudent, BotGourmand, BotCalculateur
import time


class StopRequested(Exception):
    """Exception interne utilisée pour interrompre proprement le jeu quand l'utilisateur ferme la GUI."""
    pass

class Jeu :
    def __init__(self, gui=None) :
        self.gui = gui
        self._air = 25
        self._plateau = creation_des_ruines()
        
        # Configuration
        if self.gui:
            self.gui.afficher("Bienvenue dans Deep Sea Adventure !")
            self._nb_aventuriers = self.gui.demander_nombre(" Combien de Joueurs humains ?", 1, 6)
            self._nb_bot = self.gui.demander_nombre(" Combien de Bots ?", 0, 6 - self._nb_aventuriers)
        else:
            self._nb_aventuriers = 1
            self._nb_bot = 1

        self._dico_aventurier = {}
        self._dico_bots = {}
        self._nb_joueurs = self._nb_aventuriers + self._nb_bot
        self._dico_joueurs = {}
        self._dico_joueurs_revenu = {}

    # --- UI Helpers ---
    def log(self, msg):
        if self.gui: self.gui.afficher(msg)
        else: print(msg)
        
    def update_ui(self):
        if self.gui:
            # Si une demande d'arrêt a été émise depuis la GUI, on interrompt.
            if getattr(self.gui, "_closing", False):
                raise StopRequested()
            self.gui.dessiner_plateau(self)
            try:
                # Met à jour uniquement les scores en temps réel
                self.gui.actualiser_scores(self)
            except Exception:
                pass
            time.sleep(0.1)

    # --- Properties ---
    @property
    def air(self): return self._air
    @property
    def plateau(self): return self._plateau
    @property
    def dico_joueurs(self): return self._dico_joueurs
    @property
    def dico_joueurs_revenu(self): return self._dico_joueurs_revenu

    # --- Setup ---
    def creer_aventuriers(self):
        for i in range(1, self._nb_aventuriers + 1):
            default = f"Joueur {i}"
            if self.gui:
                try:
                    nom = self.gui.demander_texte(f"Nom du joueur {i} ?", default)
                except Exception:
                    nom = default
            else:
                nom = default

            if not nom:
                nom = default

            j = Aventurier(nom)
            self._dico_aventurier[j] = [j.tresors_par_manche, j.score]

    def creer_bots(self):
        classes_bots = [BotPrudent, BotGourmand, BotCalculateur, Bot]
        for i in range(self._nb_bot):
            ClasseChoisie = rd.choice(classes_bots)
            nom = f"Bot {i+1} ({ClasseChoisie.__name__})"
            j = ClasseChoisie(nom)
            self._dico_bots[j] = [j.tresors_par_manche, j.score]

    def dico_complet(self):
        self._dico_joueurs.update(self._dico_aventurier)
        self._dico_joueurs.update(self._dico_bots)

    # --- Actions ---
    def reduire_air(self, joueur):
        conso = len(joueur.tresors_par_manche)
        if conso > 0:
            self.log(f"📉 Air -{conso} ({joueur.nom})")
        self._air -= conso
        self.update_ui()

    def rentrer(self, joueur):
        """Action Humain : Demander via GUI"""
        if joueur.sens == "plonger" and joueur.position != 0:
            choix = self.gui.demander_choix(f"{joueur.nom}, remonter ?", ["oui", "non"])
            if choix == "oui":
                joueur.sens = "remonter"
                self.log(f"{joueur.nom} décide de remonter !")

    def lancer_de(self, joueur=None):
        # Si la GUI propose un mode de lancer via bouton, l'utiliser (bloquant jusqu'au clic)
        if self.gui and hasattr(self.gui, 'demander_lancer_de'):
            try:
                is_bot = isinstance(joueur, Bot)
                res = self.gui.demander_lancer_de(is_bot=is_bot)
                self.log(f"🎲 Dés : {res}")
                return res
            except Exception:
                pass

        res = npr.randint(1,3) + npr.randint(1,3)
        self.log(f"🎲 Dés : {res}")
        return res

    def tous_revenus(self):
        return len(self._dico_joueurs_revenu) == len(self._dico_joueurs)
    
    def caseblanche(self) :
        # Enlève les cases vides (sauf le sous-marin index 0)
        self._plateau = [case for i, case in enumerate(self._plateau) if i == 0 or case != []]
        self.update_ui()

    def avancer(self, joueur):
        mouvement = max(0, self.lancer_de(joueur) - joueur.poids())
        self.log(f"Avance de {mouvement} cases")
        direction = 1 if joueur.sens == "plonger" else -1
        
        while mouvement > 0:
            joueur.position += direction
            self.update_ui() # Animation
            
            # Bornes
            if joueur.position >= 32:
                joueur.position = 32
                joueur.sens = "remonter"
                break 
            if joueur.position <= 0:
                joueur.position = 0
                joueur.revenu = True
                self._dico_joueurs_revenu[joueur] = joueur
                self.log(f"⚓ {joueur.nom} est rentré !")
                break
            
            # Saute-mouton ?
            case_occupee = False
            for autre in self._dico_joueurs:
                if (autre is not joueur) and (not autre.revenu) and (autre.position == joueur.position):
                    case_occupee = True
            
            if not case_occupee:
                mouvement -= 1
            else:
                time.sleep(0.1) # Petit effet visuel pour le saut

    def prendre(self, case, joueur):
        liste_ruine = list(self._plateau[case])
        for r in liste_ruine: joueur.ajouter_tresor(r)
        self._plateau[case] = []
        self.log(f"💰 {joueur.nom} prend {len(liste_ruine)} trésor(s)")
        self.update_ui()

    def chercher(self, joueur):
        """Action Humain : Interaction GUI"""
        case = joueur.position
        if case == 0: return

        # Case vide
        if self._plateau[case] == []:
            if len(joueur.tresors_par_manche) > 0:
                if self.gui.demander_choix(f"{joueur.nom}, poser une ruine ?", ["oui", "non"]) == "oui":
                    # Demander à la GUI laquelle déposer (n'affiche que le niveau)
                    try:
                        r = self.gui.choisir_ruine_a_deposer(joueur)
                    except Exception:
                        r = None
                    if r:
                        # Retirer du joueur et déposer
                        joueur.retirer_tresor(r)
                        self._plateau[case] = [r]
                        self.log(f"👇 {joueur.nom} pose un trésor (Niv {getattr(r, 'niveau', '?')})")
                        self.update_ui()
        # Case pleine
        else:
            if self.gui.demander_choix(f"{joueur.nom}, prendre trésor(s) ?", ["oui", "non"]) == "oui":
                self.prendre(case, joueur)

    def perdants(self):
        self.log("💀 Fin de manche : trésors perdus !")
        for j in self._dico_joueurs:
            if not j.revenu:
                j.vider_tresors_manche()
        self.update_ui()

    def reinitialiser(self):
        self._air = 25
        self._dico_joueurs_revenu = {}
        for j in self._dico_joueurs:
            j.revenu = False
            j.position = 0
            j.tresors_par_manche = []
            j.sens = "plonger"
            j.nb_tresor_manche = 0
        self.update_ui()

    def determiner_ordre_joueurs(self):
        return sorted(list(self._dico_joueurs.keys()), key=lambda x: x.position, reverse=True)

    def commencer_jeu(self, jeu_bot):
        self.creer_aventuriers()
        self.creer_bots()
        self.dico_complet()
        self.update_ui()
        
        ordre = list(self._dico_joueurs.keys())

        for manche in range(1, 4):
            self.log(f"\n=== MANCHE {manche} ===")
            try:
                jouer_manche(self, jeu_bot, ordre)
                self.log("✅ Tout le monde est rentré !")
            except AirExhaustedError:
                self.log("🚨 PLUS D'AIR !")
            
            # Fin de manche
            for j in self._dico_joueurs_revenu: j.ajouter_score()
            self.perdants()
            self.caseblanche()
            
            if manche < 3:
                self.reinitialiser()
                ordre = self.determiner_ordre_joueurs()
                time.sleep(2)

        # Fin de partie
        self.log("\n=== CLASSEMENT ===")
        gagnants = sorted(self._dico_joueurs.keys(), key=lambda j: j.score, reverse=True)
        for i, j in enumerate(gagnants, 1):
            self.log(f"{i}. {j.nom} : {j.score} pts")