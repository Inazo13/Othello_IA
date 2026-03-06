# Rules of the Othello game :
# Dans le tableau 1 = blanc 2 = noir

import numpy as np
from minmax_ia import MinMaxIA
from alphabeta_ia import AlphaBetaIA

def score(tableau):
    return int(np.sum(tableau == 1)), int(np.sum(tableau == 2))

def positions_capturees(tableau, ligne, col, joueur):
    if tableau[col][ligne] != 0:
        return []
    rival = 1 if joueur == 2 else 2
    toutes_captures = []

    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for dl, dc in directions:
        chemin = []
        l, c = ligne + dl, col + dc

        while 0 <= l < 8 and 0 <= c < 8 and tableau[c][l] == rival:
            chemin.append((l,c))
            l+=dl
            c+=dc
        if 0 <= l < 8 and 0 <= c < 8 and tableau[c][l] == joueur:
            toutes_captures.extend(chemin)
    return toutes_captures

def mouvements_valides(tableau, joueur):
    valides = []
    for i in range(8):
        for j in range(8):
            if positions_capturees(tableau, i, j, joueur):
                valides.append((i,j))
    return valides

def matrice_base():
    othello_base = np.zeros((8, 8), dtype=int)
    othello_base[3][3] = 1
    othello_base[3][4] = 2
    othello_base[4][3] = 2
    othello_base[4][4] = 1
    return othello_base

def partie():
    print("OTHELLO — Mode Console\n")
    print("1 : Joueur vs Joueur")
    print("2 : Joueur (Noir) vs IA (Blanc)")
    print("3 : IA (Noir) vs Joueur (Blanc)")
    print("4 : IA (Noir) vs IA (Blanc)")
    while True:
        try:
            choix = int(input("Mode : "))
            if choix in (1, 2, 3, 4):
                break
        except ValueError:
            pass
        print("Entrer 1, 2, 3 ou 4.")

    othello_base = matrice_base()
    # ia_blanc = MinMaxIA() if choix in (2, 4) else None
    # ia_noir = MinMaxIA() if choix in (3, 4) else None
    ia_blanc = AlphaBetaIA() if choix in (2, 4) else None
    ia_noir = AlphaBetaIA() if choix in (3, 4) else None
    joueur = 2

    while True:
        print(othello_base)
        mouvements = mouvements_valides(othello_base, joueur)
        autre_joueur = 1 if joueur == 2 else 2
        whi, bla = score(othello_base)

        if not mouvements:
            print(f"The player {'Black' if joueur == 2 else 'White'} has no movements")
            if not mouvements_valides(othello_base, autre_joueur):
                print("End of the game")
                if whi > bla:
                    print(f"White wins : {whi} - {bla}")
                elif bla > whi:
                    print(f"Black wins : {bla} - {whi}")
                else:
                    print(f"It's a tie : {whi} - {bla}")
                break
            joueur = autre_joueur
            continue
        
        print(f"Turn of the: {'Blacks (2)' if joueur == 2 else 'Whites (1)'}")
        print(f"Score : Whites {whi} - Blacks {bla}\n")
        print(f"Possible moves : {mouvements}\n")


        ia = ia_noir if joueur == 2 else ia_blanc
        if ia:
            x,y = ia.meilleur_mouvement(othello_base, joueur, 5, mouvements_valides, positions_capturees, score)            
            print(f"AI plays at position ({x}, {y})")
        else:
            while True: 
                try:
                    x = int(input("Enter the x coordinate: "))
                    y = int(input("Enter the y coordinate: "))
                    if (x, y) in mouvements:
                        break
                    print("Coup invalide")
                except ValueError:
                    print("Entrez des coordonées")
        catchs = positions_capturees(othello_base, x, y, joueur)
        if catchs:
            othello_base[y][x] = joueur
            for rl, rc in catchs:
                othello_base[rc][rl] = joueur
            joueur = autre_joueur # change le turn
        else: 
            print("bad movement")



if __name__ == "__main__" :
    partie()