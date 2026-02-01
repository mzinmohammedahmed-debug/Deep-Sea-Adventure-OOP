import tkinter as tk
from tkinter import messagebox
import threading
from jeu import Jeu, StopRequested
from jeu_bot import JeuBotController
from interface_graphique import DeepSeaGUI
import traceback

def thread_jeu(gui):
    """Fonction qui fait tourner le jeu en parallèle"""
    try:
        # On initialise le jeu
        jeu = Jeu(gui=gui) 
        bot_controller = JeuBotController()
        # On lance la partie
        jeu.commencer_jeu(bot_controller)
    except StopRequested:
        print("Jeu arrêté par l'utilisateur.")
        return
    except Exception as e:
        # EN CAS D'ERREUR : On affiche une popup explicite
        err_msg = f"Une erreur est survenue :\n{str(e)}\n\n{traceback.format_exc()}"
        print(err_msg) # Affiche aussi dans la console
        gui.root.after(0, lambda: messagebox.showerror("Erreur Fatale", err_msg))

if __name__ == "__main__":
    root = tk.Tk()

    gui = DeepSeaGUI(root)
    # Activer le mode intégré : choix et lancer de dé via boutons dans la colonne de droite
    gui.inline_choices_enabled = True

    t = threading.Thread(target=thread_jeu, args=(gui,), daemon=True)
    t.start()

    # Gestion de la fermeture propre : signale l'arrêt, attend le thread, puis détruit la fenêtre
    def on_close():
        gui.request_stop()
        try:
            root.destroy()
        except Exception:
            pass

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()