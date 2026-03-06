import numpy as np

class MinMaxIA:
    def appliquer_mouvement(self, tableau, x, y, joueur, positions_capturees):  # Simuler le mouvement
        nouveau = tableau.copy()  # copier le tableau
        captures = positions_capturees(nouveau, x, y, joueur)  # pions capturees

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

    def minimax(self, tableau, profondeur, joueur, joueurIA, mouvements_valides, positions_capturees, score):
        mouvements = mouvements_valides(tableau, joueur)

        if profondeur == 0 or not mouvements:
            return self.evaluation(tableau, joueurIA, score)

        if joueur == joueurIA:  # maximiser
            meilleur = -9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)  # simuler le mouvement
                val = self.minimax(
                    nouveau,
                    profondeur - 1,
                    1 if joueur == 2 else 2,
                    joueurIA,
                    mouvements_valides,
                    positions_capturees,
                    score
                )
                meilleur = max(meilleur, val)
            return meilleur

        else:  # minimiser
            pire = 9999
            for (x, y) in mouvements:
                nouveau = self.appliquer_mouvement(tableau, x, y, joueur, positions_capturees)
                val = self.minimax(
                    nouveau,
                    profondeur - 1,
                    1 if joueur == 2 else 2,
                    joueurIA,
                    mouvements_valides,
                    positions_capturees,
                    score
                )
                pire = min(pire, val)
            return pire

    def meilleur_mouvement(self, tableau, joueurIA, profondeur, mouvements_valides, positions_capturees, score):
        mouvements = mouvements_valides(tableau, joueurIA)

        meilleur_score = -9999
        meilleur_move = None

        for (x, y) in mouvements:
            nouveau = self.appliquer_mouvement(tableau, x, y, joueurIA, positions_capturees)

            val = self.minimax(
                nouveau,
                profondeur - 1,
                1 if joueurIA == 2 else 2,
                joueurIA,
                mouvements_valides,
                positions_capturees,
                score
            )

            if val > meilleur_score:
                meilleur_score = val
                meilleur_move = (x, y)

        return meilleur_move