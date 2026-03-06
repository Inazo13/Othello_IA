# Rules of the Othello game :
# Dans le tableau 1 = blanc 2 = noir

import numpy as np
from minmax_ia import meilleur_mouvement

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

othello_base = np.zeros((8, 8), dtype=int)
othello_base[3][3] = 1
othello_base[3][4] = 2
othello_base[4][3] = 2
othello_base[4][4] = 1

joueur = 2

while True:
    print(othello_base)
    mouvements = mouvements_valides(othello_base, joueur)
    whi, bla = score(othello_base)

    if not mouvements:
        print(f"The player {'Black' if joueur == 2 else 'White'} has no movements")
        autre_joueur = 1 if joueur == 2 else 2
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
    if joueur == 2:
        x,y = meilleur_mouvement(othello_base, 2, 3, mouvements_valides, positions_capturees, score)
        print(f"AI plays at position ({x}, {y})")
    else:
        x = int(input("Enter the x coordinate: "))
        y = int(input("Enter the y coordinate: "))
    catchs = positions_capturees(othello_base, x, y, joueur)
    if catchs:
        othello_base[y][x] = joueur
        for rl, rc in catchs:
            othello_base[rc][rl] = joueur
        joueur = 1 if joueur == 2 else 2 # change le turn
    else: 
        print("bad movement")

