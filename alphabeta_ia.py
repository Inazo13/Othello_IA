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

# value_matrix2 = [[100, -20, 10, 5, 5, 10, -20, 100],
#                  [-20, -50, -2, -2, -2, -2, -50, -20],
#                  [10, -2, -1, -1, -1, -1, -2, 10],
#                  [5, -2, -1, -1, -1, -1, -2, 5],
#                  [5, -2, -1, -1, -1, -1, -2, 5],
#                  [10, -2, -1, -1, -1, -1, -2, 10],
#                  [-20, -50, -2, -2, -2, -2, -50, -20],
#                  [100, -20, 10, 5, 5, 10, -20, 100]]

class _Timeout(Exception):
    pass

class AlphaBetaIA:
    def appliquer_mouvement(self, tableau, x, y, joueur, positions_capturees):
        nouveau = tableau.copy()
        captures = positions_capturees(nouveau, x,y, joueur)
        if not captures:
            return None
        nouveau[y][x] = joueur
        for l, c in captures:
            nouveau[c][l] = joueur  
        return nouveau
    
    def evaluation(self, tableau, joueurIA, score):
        whi, bla = score(tableau)
        if joueurIA == 2:
            return bla - whi
        else:
            return whi - bla
        
    def evaluation2(self, tableau, joueurIA):
        score_bla = 0
        score_whi = 0
        for i in range(8):
            for j in range(8):
                if tableau[j][i] == 2:
                    score_bla += value_matrix[j][i]
                elif tableau[j][i] == 1:
                    score_whi += value_matrix[j][i]
        return score_bla-score_whi if joueurIA == 2 else score_whi-score_bla
    
    def alphabeta(self, tableau, profondeur, joueur, joueurIA, alpha, beta, mouvements_valides, positions_capturees, score, deadline):
        if time.time() > deadline:
            raise _Timeout()

        mouvements = mouvements_valides(tableau, joueur)

        if profondeur == 0 or not mouvements:
            #return self.evaluation(tableau, joueurIA, score)
            return self.evaluation2(tableau, joueurIA)

        if joueur == joueurIA:  # maximiser
            meilleur = -9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)
                val = self.alphabeta(
                    nouveau,
                    profondeur - 1,
                    1 if joueur == 2 else 2,
                    joueurIA,
                    alpha,
                    beta,
                    mouvements_valides,
                    positions_capturees,
                    score,
                    deadline
                )
                meilleur = max(meilleur, val)
                alpha = max(alpha, meilleur)
                if beta <= alpha:
                    break
            return meilleur

        else:  # minimiser
            pire = 9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)
                val = self.alphabeta(
                    nouveau,
                    profondeur - 1,
                    1 if joueur == 2 else 2,
                    joueurIA,
                    alpha,
                    beta,
                    mouvements_valides,
                    positions_capturees,
                    score,
                    deadline
                )
                pire = min(pire, val)
                beta = min(beta, pire)
                if beta <= alpha:
                    break
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

        return meilleur_move