# Rules of the Othello game :
# Dans le tableau 1 = blanc 2 = noir

import numpy

def cases_adjacentes_prises(x, y):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if othello_base[x+i][y+j]!=0 and othello_base[x+i][y+j]!=joueur:
                return True
    return False

def position_valide(x, y, joueur):
    if x < 0 or x > 7 and y < 0 or y > 7:
        return False
    elif othello_base[x][y] != 0:
        return False
    elif not cases_adjacentes_prises(x, y, joueur):
        return False
    return True

othello_base = numpy.zeros((8, 8), dtype=int)
othello_base[3][3] = 1
othello_base[3][4] = 2
othello_base[4][3] = 2
othello_base[4][4] = 1

joueur = 2

while True:
    print(othello_base)
    x = int(input("Enter the x coordinate"))
    y = int(input("Enter the y coordinate"))
    if position_valide(x, y, joueur):
        othello_base[x][y] = joueur
        if joueur == 1:
            joueur = 2
        else:
            joueur = 1
    else:
        print("Position non valide, re-essayez")

    