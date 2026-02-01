from bot import Bot

class JeuBotController:
    def rentrer(self, jeu, joueur):
        if not isinstance(joueur, Bot): return
        if joueur.sens == "plonger" and joueur.position != 0:
            if joueur.decide_rentrer(jeu):
                joueur.sens = "remonter"
                jeu.log(f"🤖 {joueur.nom} décide de remonter")

    def chercher(self, jeu, joueur):
        if not isinstance(joueur, Bot): return
        
        case = joueur.position
        if case == 0: return

        # Case vide : Déposer ?
        if jeu.plateau[case] == []:
            if joueur.decide_deposer_ruine(jeu):
                r = joueur.choisir_ruine_a_deposer(jeu)
                if r:
                    jeu.plateau[case] = [r]
                    joueur.retirer_tresor(r)
                    jeu.log(f"🤖 {joueur.nom} dépose une ruine")
                    jeu.update_ui()
        
        # Case pleine : Prendre ?
        else:
            if joueur.decide_prendre_ruine(jeu, jeu.plateau[case]):
                jeu.prendre(case, joueur)
            else:
                jeu.log(f"🤖 {joueur.nom} ignore le trésor")