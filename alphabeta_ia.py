import numpy as np
import time

value_matrix = [[500, -150, 30, 10, 10, 30, -150, 300],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [30, 0, 1, 2, 2, 1, 0, 30],
                [10, 0, 2, 16, 16, 2, 0, 10],
                [10, 0, 2, 16, 16, 2, 0, 10],
                [30, 0, 1, 2, 2, 1, 0, 30],
                [-150, -250, 0, 0, 0, 0, -250, -150],
                [500, -150, 30, 10, 10, 30, -150, 500]]

class _Timeout(Exception):
    pass

class AlphaBetaIA:
    def __init__(self):
        # Dictionnaire pour mémoriser les états déjà calculés (Table de Transposition)
        # Clé: (etat_du_tableau, tour_joueur) -> Valeur: (profondeur, score, type_de_noeud)
        self.memoire = {}

    def appliquer_mouvement(self, tableau, x, y, joueur, positions_capturees):
        nouveau = tableau.copy()
        captures = positions_capturees(nouveau, x,y, joueur)
        if not captures:
            return None
        nouveau[y][x] = joueur
        for l, c in captures:
            nouveau[c][l] = joueur  
        return nouveau
    
    def evaluation(self, tableau, joueurIA, score): # absolu
        whi, bla = score(tableau)
        if joueurIA == 2:
            return bla - whi
        else:
            return whi - bla
        
    def evaluation2(self, tableau, joueurIA): # positionnel
        score_bla = 0
        score_whi = 0
        for i in range(8):
            for j in range(8):
                if tableau[j][i] == 2:
                    score_bla += value_matrix[j][i]
                elif tableau[j][i] == 1:
                    score_whi += value_matrix[j][i]
        return score_bla-score_whi if joueurIA == 2 else score_whi-score_bla
    
    def evaluation3(self, tableau, joueurIA, mouvements_valides):
        # 1. Score positionnel (Coins et matrice)
        score_positionnel = self.evaluation2(tableau, joueurIA)

        # 2. Mobilité (Nombre de coups possibles)
        adversaire = 1 if joueurIA == 2 else 2
        
        mes_mouvements = len(mouvements_valides(tableau, joueurIA))
        ses_mouvements = len(mouvements_valides(tableau, adversaire))
        
        # Calcul de la mobilité nette
        # On veut maximiser les miens et minimiser les siens
        score_mobilite = (mes_mouvements - ses_mouvements) * 20 

        # 3. Bonus spécial pour les coins (pour renforcer l'importance)
        # Même si la matrice le fait déjà, on peut accentuer la stratégie
        bonus_coins = 0
        coins = [(0,0), (0,7), (7,0), (7,7)]
        for x, y in coins:
            if tableau[y][x] == joueurIA:
                bonus_coins += 100
            elif tableau[y][x] == adversaire:
                bonus_coins -= 100

        # Résultat final combiné
        return score_positionnel + score_mobilite + bonus_coins
    
    def alphabeta(self, tableau, profondeur, joueur, joueurIA, alpha, beta, mouvements_valides, positions_capturees, score, deadline):
        if time.time() > deadline:
            raise _Timeout()

        # --- 1. LIRE DEPUIS LA MÉMOIRE ---
        # Nous convertissons le tableau numpy en bytes pour l'utiliser comme clé
        cle = (tableau.tobytes(), joueur)

        if cle in self.memoire:
            prof_sauvegardee, valeur_sauvegardee, type_noeud = self.memoire[cle]
            # Utiliser la mémoire seulement si on cherche à une profondeur égale ou supérieure
            if prof_sauvegardee >= profondeur:
                if type_noeud == 'EXACT':
                    return valeur_sauvegardee
                elif type_noeud == 'INFERIEUR':
                    alpha = max(alpha, valeur_sauvegardee)
                elif type_noeud == 'SUPERIEUR':
                    beta = min(beta, valeur_sauvegardee)

                # Élagage immédiat (coupure) grâce à la mémoire
                if alpha >= beta:
                    return valeur_sauvegardee

        alpha_initial = alpha # Sauvegarder l'alpha initial pour classer le noeud plus tard
        # ---------------------------------

        mouvements = mouvements_valides(tableau, joueur)

        if profondeur == 0 or not mouvements:
            #val = self.evaluation2(tableau, joueurIA)
            val = self.evaluation3(tableau, joueurIA, mouvements_valides)
            # Sauvegarder les feuilles de l'arbre directement
            self.memoire[cle] = (profondeur, val, 'EXACT')
            return val

        if joueur == joueurIA:  # maximiser
            meilleur = -9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)
                val = self.alphabeta(
                    nouveau, profondeur - 1, 1 if joueur == 2 else 2,
                    joueurIA, alpha, beta, mouvements_valides,
                    positions_capturees, score, deadline
                )
                meilleur = max(meilleur, val)
                alpha = max(alpha, meilleur)
                if beta <= alpha:
                    break
            
            # --- 2. ÉCRIRE DANS LA MÉMOIRE (Max) ---
            if meilleur <= alpha_initial:
                type_noeud_final = 'SUPERIEUR' # A échoué par le bas
            elif meilleur >= beta:
                type_noeud_final = 'INFERIEUR' # A échoué par le haut (Élagage)
            else:
                type_noeud_final = 'EXACT'
            self.memoire[cle] = (profondeur, meilleur, type_noeud_final)
            # ---------------------------------------
            return meilleur

        else:  # minimiser
            pire = 9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)
                val = self.alphabeta(
                    nouveau, profondeur - 1, 1 if joueur == 2 else 2,
                    joueurIA, alpha, beta, mouvements_valides,
                    positions_capturees, score, deadline
                )
                pire = min(pire, val)
                beta = min(beta, pire)
                if beta <= alpha:
                    break
            
            # --- 3. ÉCRIRE DANS LA MÉMOIRE (Min) ---
            if pire <= alpha_initial:
                type_noeud_final = 'SUPERIEUR'
            elif pire >= beta:
                type_noeud_final = 'INFERIEUR'
            else:
                type_noeud_final = 'EXACT'
            self.memoire[cle] = (profondeur, pire, type_noeud_final)
            # ---------------------------------------
            return pire
    
    def meilleur_mouvement(self, tableau, joueurIA, profondeur, mouvements_valides, positions_capturees, score):
        mouvements = mouvements_valides(tableau, joueurIA)

        meilleur_score = -9999
        meilleur_move = None
        deadline = time.time() + 5  # timeout de 5 secondes

        for (x, y) in mouvements:
            nouveau = self.appliquer_mouvement(tableau, x, y, joueurIA, positions_capturees)

            try:
                val = self.alphabeta(
                    nouveau,
                    profondeur - 1,
                    1 if joueurIA == 2 else 2,
                    joueurIA,
                    -9999,
                    9999,
                    mouvements_valides,
                    positions_capturees,
                    score,
                    deadline
                )
            except _Timeout:
                break

            if val > meilleur_score:
                meilleur_score = val
                meilleur_move = (x, y)

        if meilleur_move is None and mouvements:
            meilleur_move = mouvements[0]
            # Corregido joueurIA para evitar errores si cae en timeout total
            meilleur_score = self.evaluation2(tableau, joueurIA)

        # Regresa los 3 valores para que tu log reciba el puntaje sin fallar
        return meilleur_move[0], meilleur_move[1], meilleur_score