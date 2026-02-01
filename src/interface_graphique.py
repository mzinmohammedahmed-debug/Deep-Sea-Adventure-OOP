import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import math
import datetime
import random

# --- PALETTE DE COULEURS & THEME ---
THEME = {
    "bg_main": "#0f172a",       # Bleu nuit très sombre (Fond)
    "bg_panel": "#1e293b",      # Bleu gris foncé pour le panneau de droite
    "text_main": "#e2e8f0",     # Blanc cassé
    "text_dim": "#94a3b8",      # Gris clair
    "accent": "#38bdf8",        # Bleu ciel (cyan)
    "gold": "#f59e0b",          # Jaune trésor
    "danger": "#ef4444",        # Rouge alerte
    "success": "#22c55e",       # Vert succès
    "sub_hull": "#334155",      # Gris métallique
    "sub_light": "#fbbf24",     # Lumière jaune
    
    # Couleurs des vagues (Dégradé vertical)
    "wave_1": "#172554",        # Bleu profond
    "wave_2": "#1e3a8a",        # Bleu royal
    "wave_3": "#1e40af",        # Bleu électrique sombre
    "wave_4": "#1d4ed8"         # Bleu plus clair
}

FONTS = {
    "title": ("Helvetica", 16, "bold"),
    "subtitle": ("Helvetica", 12, "bold"),
    "body": ("Segoe UI", 10),
    "mono": ("Consolas", 10),
    "big_score": ("Helvetica", 28, "bold")
}

class ModernButton(tk.Button):
    """Un bouton stylisé 'Flat Design' avec effet de survol."""
    def __init__(self, master, **kwargs):
        bg_color = kwargs.pop("bg", THEME["bg_panel"])
        fg_color = kwargs.pop("fg", THEME["text_main"])
        active_bg = kwargs.pop("activebackground", THEME["accent"])
        
        super().__init__(master, **kwargs)
        self.config(
            bg=bg_color, fg=fg_color, 
            activebackground=active_bg, activeforeground="white",
            relief=tk.FLAT, borderwidth=0, 
            padx=15, pady=8, font=FONTS["body"], cursor="hand2"
        )
        self.default_bg = bg_color
        self.hover_bg = "#334155" 
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e): self.config(bg=self.hover_bg)
    def on_leave(self, e): self.config(bg=self.default_bg)

class DeepSeaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Deep Sea Adventure")
        self.root.geometry("1100x750")
        self.root.configure(bg=THEME["bg_main"])
        self._closing = False
        self.inline_choices_enabled = False

        # --- LAYOUT PRINCIPAL ---
        self.left_frame = tk.Frame(self.root, bg=THEME["bg_main"])
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0) # Marges supprimées pour immersion

        self.canvas = tk.Canvas(self.left_frame, bg="#0b1120", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.config(bd=0)

        # Ecouteur pour redimensionnement (Plein écran)
        self.canvas.bind("<Configure>", self._on_resize)

        # Conteneur droite (Infos)
        self.right_frame = tk.Frame(self.root, bg=THEME["bg_panel"], width=350)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.right_frame.pack_propagate(False)

        # --- WIDGETS DU PANNEAU DE DROITE ---
        self.frame_air = tk.Frame(self.right_frame, bg=THEME["bg_panel"])
        self.frame_air.pack(fill=tk.X, pady=20, padx=20)
        
        tk.Label(self.frame_air, text="RÉSERVE D'AIR", font=FONTS["subtitle"], 
                 bg=THEME["bg_panel"], fg=THEME["text_dim"]).pack(anchor="w")
        
        self.lbl_air_val = tk.Label(self.frame_air, text="25", font=FONTS["big_score"], 
                                    bg=THEME["bg_panel"], fg=THEME["success"])
        self.lbl_air_val.pack(anchor="e")
        
        self.air_bar_canvas = tk.Canvas(self.frame_air, height=6, bg="#334155", highlightthickness=0)
        self.air_bar_canvas.pack(fill=tk.X, pady=(5,0))
        self.air_bar_rect = self.air_bar_canvas.create_rectangle(0, 0, 310, 6, fill=THEME["success"], width=0)

        tk.Frame(self.right_frame, height=1, bg="#334155").pack(fill=tk.X, padx=20, pady=10)

        self.inline_frame = tk.Frame(self.right_frame, bg=THEME["bg_panel"])
        self.inline_frame.pack(fill=tk.X, padx=20, pady=10)
        self._inline_widgets = []

        tk.Frame(self.right_frame, height=1, bg="#334155").pack(fill=tk.X, padx=20, pady=10)

        self.lbl_scores_title = tk.Label(self.right_frame, text="PLONGEURS", font=FONTS["subtitle"], 
                                         bg=THEME["bg_panel"], fg=THEME["text_dim"])
        self.lbl_scores_title.pack(anchor="w", padx=20)

        self.scores_label = tk.Label(self.right_frame, text="En attente...", font=FONTS["body"], 
                                     bg=THEME["bg_panel"], fg=THEME["text_main"], justify=tk.LEFT, anchor="nw")
        self.scores_label.pack(fill=tk.BOTH, padx=20, pady=(5, 10))

        self.log_container = tk.Frame(self.right_frame, bg="#0f172a", highlightthickness=1, highlightbackground="#334155")
        self.log_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.log_text = tk.Text(self.log_container, height=10, bg="#0f172a", fg=THEME["text_main"], 
                                font=("Consolas", 9), bd=0, relief=tk.FLAT, state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll = tk.Scrollbar(self.log_container, command=self.log_text.yview, bg="#0f172a")
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scroll.set)

        self.log_text.tag_config("err", foreground=THEME["danger"])
        self.log_text.tag_config("warn", foreground=THEME["gold"])
        self.log_text.tag_config("info", foreground=THEME["text_dim"])
        self.log_text.tag_config("action", foreground=THEME["accent"])

        # --- CONFIGURATION GRAPHIQUE ---
        self.couleurs_ruines = {1: "#fbbf24", 2: "#f97316", 3: "#ef4444", 4: "#a855f7"}
        self.couleurs_joueurs = ["#38bdf8", "#4ade80", "#f472b6", "#fbbf24", "#a78bfa", "#94a3b8"]
        self._bubbles = []
        self._bubble_after_id = None
        self._last_game = None
        
        # --- CONFIGURATION VAGUES VERTICALES ---
        self._waves_data = []
        # On crée des couches de vagues verticales
        for i in range(5):
            # chaque couche a une petite sous-oscillation pour plus de richesse
            base_color = THEME[f"wave_{min(i+1, 4)}"]
            self._waves_data.append({
                "phase": random.uniform(0, math.pi * 2),
                "phase2": random.uniform(0, math.pi * 2),
                "speed": random.uniform(0.008, 0.035), 
                "amp": random.randint(18, 60),    # Amplitude principale
                "amp2": random.randint(6, 20),    # Petite turbulence
                "freq": random.randint(120, 420), # Fréquence principale
                "freq2": random.randint(40, 160), # Fréquence secondaire
                "x_base_pct": 0.12 + (i * 0.19),  # Position en % de la largeur
                "width": random.randint(80, 320), # Largeur de la bande
                "color": base_color,
                "obj_id": None
            })
        self._wave_after_id = None
        
        self._start_bubble_animation()
        self._start_wave_animation()
        
        self.root.protocol("WM_DELETE_WINDOW", self.request_stop)

    # --- EVENEMENTS RESPONSIVE ---
    def _on_resize(self, event):
        """Appelé quand la fenêtre change de taille."""
        if self._last_game:
            # On redessine le jeu pour s'adapter à la nouvelle taille
            self.dessiner_plateau(self._last_game)

    # --- LOGIQUE D'AFFICHAGE TEXTE ---
    def afficher(self, message):
        def _write():
            if self._closing: return
            self.log_text.config(state=tk.NORMAL)
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            msg = str(message)
            tag = "info"
            if "Erreur" in msg or "🚨" in msg: tag = "err"
            elif "Avance" in msg or "🎲" in msg: tag = "action"
            elif "💰" in msg or "pose" in msg: tag = "warn"
            
            self.log_text.insert(tk.END, f"[{ts}] ", "info")
            self.log_text.insert(tk.END, f"{msg}\n", tag)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        self.root.after(0, _write)

    # --- INPUTS ---
    def demander_nombre(self, question, min_val, max_val):
        result = {"val": min_val}
        event = threading.Event()
        def popup():
            res = simpledialog.askinteger("Configuration", question, minvalue=min_val, maxvalue=max_val, parent=self.root)
            result["val"] = res if res is not None else min_val
            event.set()
        self.root.after(0, popup)
        while not event.is_set() and not self._closing: event.wait(0.1)
        return result["val"]

    def demander_texte(self, question, default=""):
        result = {"val": default}
        event = threading.Event()
        def popup():
            res = simpledialog.askstring("Identité", question, initialvalue=default, parent=self.root)
            result["val"] = res if res else default
            event.set()
        self.root.after(0, popup)
        while not event.is_set() and not self._closing: event.wait(0.1)
        return result["val"]

    def demander_choix(self, question, options=["Oui", "Non"]):
        if self.inline_choices_enabled:
            return self._inline_interaction(question, options)
        return options[0] 

    def demander_lancer_de(self, is_bot: bool = False):
        """Renvoie la valeur du lancer de dés.

        Si `is_bot` est True, le lancer est automatique (retour immédiat),
        sinon si `inline_choices_enabled` est activé on propose un bouton.
        """
        import numpy.random as npr
        # Si c'est un bot, on retourne immédiatement un lancer aléatoire
        if is_bot:
            return int(npr.randint(1,3) + npr.randint(1,3))

        # Pour un humain, on peut proposer un bouton inline si activé
        if self.inline_choices_enabled:
            res_dict = self._inline_interaction("À vous de jouer !", ["🎲 Lancer les dés"])
            return int(npr.randint(1,3) + npr.randint(1,3))

        return int(npr.randint(1,3) + npr.randint(1,3))

    def _inline_interaction(self, text, buttons):
        event = threading.Event()
        result = {"val": None}
        def _setup():
            for w in self._inline_widgets: w.destroy()
            self._inline_widgets.clear()
            lbl = tk.Label(self.inline_frame, text=text, wraplength=300, 
                           bg=THEME["bg_panel"], fg="white", font=FONTS["subtitle"])
            lbl.pack(pady=(0, 10))
            self._inline_widgets.append(lbl)
            btn_frame = tk.Frame(self.inline_frame, bg=THEME["bg_panel"])
            btn_frame.pack()
            self._inline_widgets.append(btn_frame)
            for opt in buttons:
                def _click(o=opt):
                    result["val"] = o.lower() if isinstance(o, str) else o
                    for w in self._inline_widgets: w.destroy()
                    self._inline_widgets.clear()
                    event.set()
                bg_btn = THEME["sub_hull"] if "non" in opt.lower() else THEME["accent"]
                btn = ModernButton(btn_frame, text=opt, command=_click, bg=bg_btn)
                btn.pack(side=tk.LEFT, padx=5)
                self._inline_widgets.append(btn)
        self.root.after(0, _setup)
        while not event.is_set():
            if self._closing: return buttons[0]
            event.wait(0.1)
        return result["val"]

    # --- ANIMATION VAGUES VERTICALES ---
    def _start_wave_animation(self):
        self._animate_waves()

    def _animate_waves(self):
        if self._closing: return

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 10: w, h = 800, 600

        # Pour chaque couche de vague
        for i, wave in enumerate(self._waves_data):
            # avancer les phases (chacune à sa vitesse pour plus de naturel)
            wave['phase'] += wave['speed']
            wave['phase2'] += wave['speed'] * 0.9

            points = []
            # Points selon une grille adaptée à la taille pour plus de fluidité
            samples = max(24, int(h / 12))
            dy = h / samples

            base_x = w * wave['x_base_pct']

            # point de départ (haut gauche de la bande)
            points.extend([base_x - wave['width'], 0])

            # Courbe composée (sin principal + petite turbulence)
            for s in range(samples + 1):
                y = int(s * dy)
                a1 = (y / wave['freq']) + wave['phase']
                a2 = (y / wave['freq2']) + wave['phase2']
                x = base_x + wave['amp'] * math.sin(a1) + wave['amp2'] * math.sin(a2)
                points.extend([x, y])

            # Fermeture du polygone (bas gauche)
            points.extend([base_x - wave['width'], h])

            # Calculer une légère variation de couleur pour donner de la profondeur
            def _tint_hex(hexcol, factor=1.0):
                hexcol = hexcol.lstrip('#')
                r = int(hexcol[0:2], 16)
                g = int(hexcol[2:4], 16)
                b = int(hexcol[4:6], 16)
                r = max(0, min(255, int(r * factor)))
                g = max(0, min(255, int(g * factor)))
                b = max(0, min(255, int(b * factor)))
                return f"#{r:02x}{g:02x}{b:02x}"

            # facteur selon la couche et la phase pour un léger scintillement
            depth_factor = 0.82 + (i * 0.04) + 0.03 * math.sin(wave['phase'] * 1.5)
            fill_color = _tint_hex(wave['color'], depth_factor)

            # Mise à jour graphique
            try:
                if wave['obj_id'] and self.canvas.type(wave['obj_id']):
                    self.canvas.coords(wave['obj_id'], points)
                    self.canvas.itemconfig(wave['obj_id'], fill=fill_color)
                    self.canvas.tag_lower(wave['obj_id'])
                else:
                    # Création avec smooth et splinesteps pour courbes douces
                    stipple_val = "gray25" if i % 2 == 0 else "gray12"
                    wave['obj_id'] = self.canvas.create_polygon(
                        points,
                        fill=fill_color,
                        outline="",
                        smooth=True,
                        splinesteps=36,
                        tags="wave",
                        stipple=stipple_val
                    )
                    self.canvas.tag_lower(wave['obj_id'])
            except Exception:
                pass

        self._wave_after_id = self.root.after(50, self._animate_waves)


    # --- DESSIN DU JEU ---
    def dessiner_plateau(self, jeu):
        self._last_game = jeu
        # Utiliser after_idle pour éviter le spam de redessin lors du resize
        self.root.after_idle(lambda: self._render(jeu))

    def _render(self, jeu):
        # On ne touche pas aux tags "wave"
        items = self.canvas.find_all()
        for item in items:
            tags = self.canvas.gettags(item)
            if "wave" not in tags:
                self.canvas.delete(item)

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        # Fallback si fenêtre pas encore affichée
        if w < 50: w = 800
        if h < 50: h = 600

        self._update_right_panel(jeu)

        # Chemin du jeu (Serpent qui s'adapte à w/h)
        coords = self._calculate_path_coords(jeu, w, h)

        if len(coords) > 1:
            points = []
            for i in sorted(coords.keys()):
                points.extend(coords[i])
            self.canvas.create_line(points, fill="#475569", width=3, smooth=True, splinesteps=36)

        # Cases
        for i, (cx, cy) in coords.items():
            if i == 0: continue
            
            contenu = jeu.plateau[i]
            tag = f"case_{i}"
            
            self.canvas.create_oval(cx-18, cy-18+4, cx+18, cy+18+4, fill="#020617", outline="", tags=tag)
            
            if contenu == []:
                self.canvas.create_oval(cx-6, cy-6, cx+6, cy+6, fill="#334155", outline="", tags=tag)
            else:
                niveau = sum(r.niveau for r in contenu)
                niv_base = contenu[0].niveau
                color = self.couleurs_ruines.get(niv_base, "#94a3b8")
                
                self.canvas.create_oval(cx-16, cy-16, cx+16, cy+16, fill=color, outline="white", width=2, tags=tag)
                
                txt = "★" if len(contenu) > 1 else str(niveau)
                self.canvas.create_text(cx, cy, text=txt, font=("Segoe UI", 11, "bold"), fill="white")
                
                if len(contenu) > 1:
                    self.canvas.create_text(cx+12, cy-12, text=f"x{len(contenu)}", font=("Arial", 8, "bold"), fill="white")

            def _handler(idx=i): self._show_case_info(idx)
            self.canvas.tag_bind(tag, "<Button-1>", lambda e: _handler())

        # Sous-marin
        sub_x, sub_y = coords[0]
        self._draw_submarine(sub_x, sub_y)

        # Joueurs
        self._draw_players(jeu, coords)

        # Bulles (re-raise pour être au dessus)
        self._draw_bubbles()

    def _calculate_path_coords(self, jeu, w, h):
        coords = {}
        nb_cases = len(jeu.plateau)
        
        # Adaptation dynamique des marges
        margin_x = w * 0.1 # 10% de marge
        
        coords[0] = (w * 0.15, h * 0.15) # Sous-marin en haut gauche proportionnel
        
        for i in range(1, nb_cases):
            # Le serpent occupe 80% de la hauteur
            available_h = h * 0.8
            start_y = h * 0.2
            
            rows = 4
            row_height = available_h / rows
            items_per_row = max(5, math.ceil(nb_cases / rows))
            
            row_idx = (i-1) // items_per_row
            col_idx = (i-1) % items_per_row
            
            y = start_y + row_idx * row_height
            available_w = w - 2 * margin_x
            
            if row_idx % 2 == 0:
                x = margin_x + col_idx * (available_w / items_per_row)
            else:
                x = w - margin_x - col_idx * (available_w / items_per_row)
                
            coords[i] = (x, y)
        return coords

    def _draw_submarine(self, x, y):
        self.canvas.create_oval(x-50, y-25, x+70, y+25, fill=THEME["sub_hull"], outline="#cbd5e1", width=2)
        self.canvas.create_rectangle(x-10, y-40, x+20, y-20, fill=THEME["sub_hull"], outline="#cbd5e1", width=2)
        self.canvas.create_line(x+5, y-40, x+5, y-50, x+15, y-50, fill="#cbd5e1", width=3)
        self.canvas.create_oval(x+30, y-10, x+50, y+10, fill=THEME["sub_light"], outline="#f59e0b", width=2)
        self.canvas.create_polygon(x-55, y-10, x-55, y+10, x-65, y, fill="#94a3b8")
        self.canvas.create_text(x, y+5, text="NAUTILUS", font=("Arial", 8), fill="#94a3b8")

    def _draw_players(self, jeu, coords):
        map_pos = {}
        for j in jeu.dico_joueurs.keys():
            if j.position not in map_pos: map_pos[j.position] = []
            map_pos[j.position].append(j)
            
        for pos, players in map_pos.items():
            cx, cy = coords.get(pos, (0,0))
            count = len(players)
            offset_step = 25
            start_x = cx - ((count-1)*offset_step)/2
            
            for idx, p in enumerate(players):
                px = start_x + idx * offset_step
                py = cy - 35 if pos > 0 else cy + 40
                
                p_idx = abs(hash(p.nom)) % len(self.couleurs_joueurs)
                color = self.couleurs_joueurs[p_idx]
                
                self.canvas.create_oval(px-8, py-18, px+8, py-2, fill=color, outline="white")
                points = [px-10, py, px+10, py, px, py+15]
                self.canvas.create_polygon(points, fill=color, outline="white")
                
                initial = p.nom[0].upper()
                self.canvas.create_text(px, py-10, text=initial, font=("Arial", 8, "bold"), fill="#1e293b")
                
                if pos > 0:
                    arrow = "↓" if p.sens == "plonger" else "↑"
                    acolor = THEME["danger"] if p.sens == "plonger" else THEME["success"]
                    self.canvas.create_text(px+12, py, text=arrow, fill=acolor, font=("Arial", 12, "bold"))

                if len(p.tresors_par_manche) > 0:
                    self.canvas.create_oval(px-6, py+2, px+6, py+14, fill=THEME["gold"], outline="white")
                    self.canvas.create_text(px, py+8, text=str(len(p.tresors_par_manche)), font=("Arial", 7), fill="black")

    def _update_right_panel(self, jeu):
        color = THEME["success"] if jeu.air > 15 else THEME["gold"] if jeu.air > 5 else THEME["danger"]
        self.lbl_air_val.config(text=f"{jeu.air}", fg=color)
        
        width_max = 310
        pct = max(0, min(1, jeu.air / 25))
        self.air_bar_canvas.coords(self.air_bar_rect, 0, 0, width_max * pct, 6)
        self.air_bar_canvas.itemconfig(self.air_bar_rect, fill=color)

        txt = ""
        joueurs_sorted = sorted(jeu.dico_joueurs.keys(), key=lambda x: x.score, reverse=True)
        for j in joueurs_sorted:
            status = "✅" if j.revenu else "🌊"
            txt += f"{status} {j.nom:<12} {j.score:>3} pts"
            if j.tresors_par_manche:
                txt += f" 🎒{len(j.tresors_par_manche)}"
            txt += "\n"
        self.scores_label.config(text=txt)

    def _show_case_info(self, idx):
        jeu = self._last_game
        if not jeu: return
        content = jeu.plateau[idx]
        if not content:
            msg = "Cette zone a été pillée ! Il ne reste rien."
        else:
            pts = [f"Niv {r.niveau}" for r in content]
            msg = f"Contenu : {', '.join(pts)}"
            if len(content) > 1:
                msg += "\n(Pile de trésors)"
        messagebox.showinfo(f"Zone de recherche {idx}", msg)

    # --- ANIMATION BULLES ---
    def _create_bubble(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100: return
        x = random.randint(20, w-20)
        y = h + 20
        size = random.randint(2, 8)
        bid = self.canvas.create_oval(x, y, x+size, y+size, outline="#bae6fd", width=1)
        self._bubbles.append({"id": bid, "speed": random.uniform(1, 3), "drift": random.uniform(-0.5, 0.5)})

    def _animate_bubbles(self):
        if self._closing: return
        for b in list(self._bubbles):
            self.canvas.move(b['id'], b['drift'], -b['speed'])
            coords = self.canvas.coords(b['id'])
            if not coords or coords[1] < -20:
                self.canvas.delete(b['id'])
                self._bubbles.remove(b)
        if random.random() < 0.3: self._create_bubble()
        self._bubble_after_id = self.root.after(50, self._animate_bubbles)

    def _draw_bubbles(self):
        # S'assurer que les bulles restent au-dessus du fond (vagues)
        try:
            for b in list(self._bubbles):
                try:
                    if b.get('id') and self.canvas.type(b['id']):
                        self.canvas.tag_raise(b['id'])
                except Exception:
                    pass
        except Exception:
            pass

    def _start_bubble_animation(self):
        self._animate_bubbles()

    def request_stop(self):
        self._closing = True
        if self._bubble_after_id: self.root.after_cancel(self._bubble_after_id)
        if self._wave_after_id: self.root.after_cancel(self._wave_after_id)
        self.root.destroy()

    # --- Choix ruine ---
    def choisir_ruine_a_deposer(self, joueur):
        tresors = list(joueur.tresors_par_manche)
        if not tresors: return None

        def _clear_inline():
            for w in getattr(self, '_inline_widgets', []):
                try: w.destroy()
                except Exception: pass
            try: self._inline_widgets.clear()
            except Exception: pass

        if getattr(self, 'inline_choices_enabled', False):
            event = threading.Event()
            result = {'val': None}
            def _render_inline():
                _clear_inline()
                lbl = tk.Label(self.inline_frame, text=f"Choisir une ruine ({len(tresors)}):", bg="#2c3e50", fg="white")
                lbl.pack(pady=(4,2))
                self._inline_widgets.append(lbl)
                btn_frame = tk.Frame(self.inline_frame, bg="#2c3e50")
                btn_frame.pack(pady=(2,6))
                self._inline_widgets.append(btn_frame)
                for r in tresors:
                    txt = f"Niv {getattr(r, 'niveau', '?')}"
                    def _cmd(chosen=r):
                        result['val'] = chosen
                        _clear_inline()
                        event.set()
                    b = tk.Button(btn_frame, text=txt, command=_cmd)
                    b.pack(side=tk.LEFT, padx=4, pady=2)
                    self._inline_widgets.append(b)
                btn_cancel = tk.Button(self.inline_frame, text="Annuler", command=lambda: ( _clear_inline(), event.set() ))
                btn_cancel.pack(pady=(2,4))
                self._inline_widgets.append(btn_cancel)
            self.root.after(0, _render_inline)
            while not event.is_set():
                if getattr(self, '_closing', False): return None
                event.wait(0.1)
            return result['val']

        event = threading.Event()
        result = {'val': None}
        def popup():
            top = tk.Toplevel(self.root)
            top.title("Choisir une ruine")
            top.geometry("320x220")
            tk.Label(top, text="Sélectionnez une ruine:", wraplength=300).pack(pady=8)
            list_frame = tk.Frame(top)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=8)
            lb = tk.Listbox(list_frame)
            for r in tresors: lb.insert(tk.END, f"Niv {getattr(r, 'niveau', '?')}")
            lb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scr = tk.Scrollbar(list_frame, command=lb.yview)
            scr.pack(side=tk.RIGHT, fill=tk.Y)
            lb.config(yscrollcommand=scr.set)
            def _ok():
                sel = lb.curselection()
                if sel: result['val'] = tresors[sel[0]]
                try: top.destroy()
                except Exception: pass
                event.set()
            def _cancel():
                try: top.destroy()
                except Exception: pass
                event.set()
            btns = tk.Frame(top)
            btns.pack(pady=6)
            tk.Button(btns, text="Choisir", command=_ok).pack(side=tk.LEFT, padx=8)
            tk.Button(btns, text="Annuler", command=_cancel).pack(side=tk.LEFT, padx=8)
            top.protocol("WM_DELETE_WINDOW", _cancel)
            top.transient(self.root)
            top.grab_set()
        self.root.after(0, popup)
        while not event.is_set():
            if getattr(self, '_closing', False): return None
            event.wait(0.1)
        return result['val']

    def actualiser_scores(self, jeu): pass
    def clear_log(self): 
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
    def afficher_scores_finaux(self, jeu):
        self.afficher("--- FIN DE PARTIE ---")
        gagnant = max(jeu.dico_joueurs.keys(), key=lambda x: x.score)
        messagebox.showinfo("Victoire !", f"Le gagnant est {gagnant.nom} avec {gagnant.score} points !")