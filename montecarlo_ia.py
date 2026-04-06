import math
import random
import time
import numpy as np

class NoeudMCTS:
    def __init__(self, tableau, joueur_actuel, parent=None, coup_precedent=None):
        self.tableau = tableau
        self.joueur_actuel = joueur_actuel  # Le joueur qui DOIT jouer à partir de ce noeud
        self.parent = parent
        self.coup_precedent = coup_precedent  # Le coup qui a mené à ce noeud
        self.enfants = []
        self.visites = 0
        self.victoires = 0.0  # Victoires du point de vue du joueur qui a fait le coup (le parent)
        self.mouvements_non_explores = None

class MonteCarloIA:
    def __init__(self, c_exploration=1.414):
        # Constante d'exploration (racine de 2 par défaut)
        self.c_exploration = c_exploration

    def meilleur_mouvement(self, tableau, joueur, parametre_temps, mouvements_valides, positions_capturees, score):
        """
        Trouve le meilleur mouvement en utilisant Monte Carlo Tree Search.
        Note : Contrairement à Alpha-Beta qui utilise une 'profondeur', MCTS est basé sur le temps.
        Si parametre_temps = 5, l'algorithme réfléchira pendant 5 secondes.
        """
        temps_alloue = max(1.0, float(parametre_temps)) # Minimum 1 seconde de réflexion
        racine = NoeudMCTS(np.copy(tableau), joueur)
        racine.mouvements_non_explores = mouvements_valides(racine.tableau, joueur)
        
        if not racine.mouvements_non_explores:
            return None
            
        heure_debut = time.time()
        
        # --- BOUCLE PRINCIPALE MCTS ---
        while time.time() - heure_debut < temps_alloue:
            noeud = racine
            etat_simule = np.copy(racine.tableau)
            joueur_simule = joueur
            
            # 1. SÉLECTION (Descendre l'arbre avec la formule UCB1)
            while noeud.mouvements_non_explores is not None and len(noeud.mouvements_non_explores) == 0 and len(noeud.enfants) > 0:
                noeud = self._meilleur_enfant_ucb(noeud)
                etat_simule = self._appliquer_mouvement(etat_simule, noeud.coup_precedent, 3 - noeud.joueur_actuel)
                joueur_simule = noeud.joueur_actuel
            
            # 2. EXPANSION (Ajouter un nouveau noeud à l'arbre)
            if noeud.mouvements_non_explores is None:
                noeud.mouvements_non_explores = mouvements_valides(etat_simule, joueur_simule)
            
            if len(noeud.mouvements_non_explores) > 0:
                coup = random.choice(noeud.mouvements_non_explores)
                noeud.mouvements_non_explores.remove(coup)
                etat_simule = self._appliquer_mouvement(etat_simule, coup, joueur_simule)
                joueur_simule = 3 - joueur_simule # Changement de joueur
                
                nouveau_noeud = NoeudMCTS(etat_simule, joueur_simule, parent=noeud, coup_precedent=coup)
                noeud.enfants.append(nouveau_noeud)
                noeud = nouveau_noeud
                
            # 3. SIMULATION (Jouer une partie aléatoire jusqu'à la fin)
            gagnant = self._simuler_partie(etat_simule, joueur_simule, mouvements_valides, score)
            
            # 4. RÉTROPROPAGATION (Mettre à jour les statistiques de la branche)
            while noeud is not None:
                noeud.visites += 1
                joueur_parent = 3 - noeud.joueur_actuel # Le joueur qui a pris la décision menant à ce noeud
                if gagnant == joueur_parent:
                    noeud.victoires += 1.0
                elif gagnant == 0: # Égalité
                    noeud.victoires += 0.5
                noeud = noeud.parent
                
        # Le temps est écoulé, on choisit le mouvement le plus robuste (le plus visité)
        meilleur_enfant = max(racine.enfants, key=lambda enfant: enfant.visites)
        print(f"MCTS a effectué {racine.visites} itérations en {temps_alloue} secondes.")
        return meilleur_enfant.coup_precedent

    def _meilleur_enfant_ucb(self, noeud):
        meilleur_score = -float('inf')
        meilleurs_enfants = []
        for enfant in noeud.enfants:
            if enfant.visites == 0:
                return enfant
            # Formule Upper Confidence Bound (UCB1)
            exploitation = enfant.victoires / enfant.visites
            exploration = self.c_exploration * math.sqrt(math.log(noeud.visites) / enfant.visites)
            score_ucb = exploitation + exploration
            
            if score_ucb > meilleur_score:
                meilleur_score = score_ucb
                meilleurs_enfants = [enfant]
            elif score_ucb == meilleur_score:
                meilleurs_enfants.append(enfant)
        return random.choice(meilleurs_enfants)
        
    def _appliquer_mouvement(self, tableau, coup, joueur):
        """Simule un mouvement indépendamment pour ne pas ralentir le jeu principal."""
        nouveau_tableau = np.copy(tableau)
        x, y = coup
        nouveau_tableau[y][x] = joueur
        adversaire = 3 - joueur
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            a_retourner = []
            while 0 <= nx < 8 and 0 <= ny < 8 and nouveau_tableau[ny][nx] == adversaire:
                a_retourner.append((nx, ny))
                nx += dx
                ny += dy
            if 0 <= nx < 8 and 0 <= ny < 8 and nouveau_tableau[ny][nx] == joueur:
                for rx, ry in a_retourner:
                    nouveau_tableau[ry][rx] = joueur
        return nouveau_tableau

    def _simuler_partie(self, tableau, joueur_actuel, mouvements_valides, score_func):
        """Joue des coups semi-aléatoires (Rollout) jusqu'à la fin de la partie."""
        etat = np.copy(tableau)
        joueur = joueur_actuel
        passes = 0
        
        while passes < 2:
            mouvements = mouvements_valides(etat, joueur)
            if not mouvements:
                passes += 1
                joueur = 3 - joueur
                continue
            
            passes = 0
            # Heuristique légère pour guider MCTS : s'il y a un coin, on le prend.
            coins = [(0,0), (0,7), (7,0), (7,7)]
            mouvements_coins = [m for m in mouvements if m in coins]
            if mouvements_coins:
                coup = random.choice(mouvements_coins)
            else:
                coup = random.choice(mouvements)
                
            etat = self._appliquer_mouvement(etat, coup, joueur)
            joueur = 3 - joueur
            
        # Fin de partie atteinte, calcul du score final
        whi, bla = score_func(etat)
        if whi > bla: return 1
        elif bla > whi: return 2
        return 0