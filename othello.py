# Rules of the Othello game :
# Dans le tableau 1 = blanc 2 = noir

import numpy

def positions_capturees(tableau, ligne, col, joueur):
    if tableau[ligne][col] != 0:
        return []
    rival = 1 if joueur == 2 else 2
    toutes_captures = []

    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for dl, dc in directions:
        chemin = []
        l, c = ligne + dl, col + dc

        while 0 <= l < 8 and 0 <= c < 8 and tableau[l][c] == rival:
            chemin.append((l,c))
            l+=dl
            c+=dc
        if 0 <= l < 8 and 0 <= c < 8 and tableau[l][c] == joueur:
            toutes_captures.extend(chemin)
    return toutes_captures

def mouvements_valides(tableau, joueur):
    valides = []
    for i in range(8):
        for j in range(8):
            if positions_capturees(tableau, i, j, joueur):
                valides.append((i,j))
    return valides

othello_base = numpy.zeros((8, 8), dtype=int)
othello_base[3][3] = 1
othello_base[3][4] = 2
othello_base[4][3] = 2
othello_base[4][4] = 1

joueur = 2

while True:
    print(othello_base)
    mouvements = mouvements_valides(othello_base, joueur)

    if not mouvements:
        print(f"The player {'Black' if joueur == 2 else 'White'} has no movements")
        autre_joueur = 1 if joueur == 2 else 2
        if not mouvements_valides(othello_base, autre_joueur):
            print("End")
            break
        joueur = autre_joueur
        continue
    
    print(f"Turn of the: {'Blacks (2)' if joueur == 2 else 'Whites (1)'}")
    x = int(input("Enter the x coordinate: "))
    y = int(input("Enter the y coordinate: "))
    catchs = positions_capturees(othello_base, x, y, joueur)
    if catchs:
        othello_base[x][y] = joueur
        for rl, rc in catchs:
            othello_base[rl][rc] = joueur
        joueur = 1 if joueur == 2 else 2 # change le turn
    else: 
        print("bad movement")
