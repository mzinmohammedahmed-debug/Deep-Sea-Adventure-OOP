# 🌊 Deep Sea Adventure - Master 1 Data Science

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Completed-success)
![Context](https://img.shields.io/badge/Context-Master_1_Univ_Angers-orange)

Une implémentation complète en **Programmation Orientée Objet (POO)** du jeu de société "Deep Sea Adventure", réalisée dans le cadre du Master 1 Data Science à l'**Université d'Angers** (2025-2026).

> ⚠️ **Note sur le projet :** Ce dépôt contient une version évoluée du projet universitaire. L'interface graphique (GUI) a été développée post-soutenance pour remplacer l'affichage ASCII initial présenté dans le rapport.

## 🎮 Aperçu du Projet
Ce logiciel simule une plongée sous-marine où des aventuriers doivent rapporter des trésors sans épuiser la réserve d'air commune. Il met en œuvre des concepts avancés de développement :
* **Architecture Modulaire :** Séparation stricte entre la logique métier, les données et l'affichage.
* **Intelligences Artificielles :** Plusieurs stratégies de Bots (Prudent, Gourmand, Calculateur) utilisant des probabilités.
* **Interface Graphique Moderne :** Développement d'une GUI en `Tkinter` avec animations (vagues, bulles) et gestion multithread.

## 🛠️ Fonctionnalités Techniques
* **POO & Héritage :** Les Bots héritent de la classe `Aventurier`, permettant un polymorphisme complet dans le moteur de jeu.
* **Algorithmes de Décision :** Le *Bot Calculateur* estime le nombre de tours nécessaires pour rentrer en fonction de son poids et de l'air restant.
* **Gestion des Erreurs :** Utilisation d'exceptions personnalisées (`AirExhaustedError`) pour gérer la fin de manche de manière robuste.

## 👥 Équipe et Contributions
Ce projet a été initié en groupe.
* **Membres du groupe :** MZIN Mohammed Ahmed, BAPTISTE PYRYT, GASPARD TESTON, CARMEL AWANDE.
* **Contribution spécifique de ce dépôt :**
    * Conception de l'architecture POO centrale (Ruine, Plateau).
    * Développement de Bots avancées (`bots_avances.py`).
    * Rédaction du rapport en **LaTeX**.
    * **Conception intégrale de l'Interface Graphique (post-projet)** pour remplacer la vue console.

## 📄 Documentation
Le dossier `/docs` contient :
* [`Rapport_Projet_POO.pdf`](docs/Rapport_Projet_POO.pdf) : Le rapport académique officiel (LaTeX) détaillant la structure du code et la version ASCII originale.
* [`Regles_du_jeu.md`](docs/Regles_du_jeu.md) : Explication détaillée des règles.

## 🚀 Installation et Lancement
1.  Cloner le dépôt :
    ```bash
    git clone [https://github.com/mzinmohammedahmed-debug/Deep-Sea-Adventure-OOP.git](https://github.com/mzinmohammedahmed-debug/Deep-Sea-Adventure-OOP.git)
    ```
2.  Lancer le jeu :
    ```bash
    python src/main.py
    ```
    *(Aucune installation complexe requise, utilise `tkinter` natif et `numpy`)*
