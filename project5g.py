import numpy as np
from extraction import *
import math
import sys

#Extraction des données depuis le fichier test
N,M,K,p,P,R = extraction(5)

#On introduit les booléens x_k,m,n
X = np.array([[[0 for m in range(M)] for k in range(K)] for n in range(N)])

#On introduit la liste des indices possibles pour chaque n 
indices_liste = []
for n in range(N):
    ind_n = []
    for k in range(K):
        for m in range(M):
            ind_n.append((k,m))
    ind_n.sort(key = lambda x: P[n,x[0],x[1]])
    indices_liste.append(ind_n)


def question2(ind):
    """Dans la liste des indices possibles, on enlève ceux pour lequel p_k,m,n dépasse le budget p"""
    for n in range(N):
        while ind[n] != [] and P[n, ind[n][-1][0], ind[n][-1][1]] > p:
            ind[n].pop()

def removeIPdominated(ind):
    """Retire de la liste des indices possibles, les (k,m,n) qui sont IP - dominés"""
    for n in range(N):
        if len(ind[n]) > 0 : #Il faut au moins une valeur dans le tableau
            i = 1
            max_rate = R[n, ind[n][0][0], ind[n][0][1]]      
            while i < len(ind[n]): #On parcourt la liste des indices
                if R[n, ind[n][i][0], ind[n][i][1]] <= max_rate : 
                    ind[n].pop(i) #Si le r est plus faible que le max des r précédents, on ne le garde pas
                elif P[n, ind[n][i][0], ind[n][i][1]] == P[n, ind[n][i-1][0], ind[n][i-1][1]] :
                    ind[n].pop(i-1) #On ne garde pas les doublons des p
                else :
                    max_rate = R[n, ind[n][i][0], ind[n][i][1]]
                    i = i + 1



def removeLPdominated(ind):
    """Retire de la liste des indices possibles, les (k,m,n) qui sont LP - dominés"""
    for n in range(N):
        if len(ind[n]) > 1: #Il nous faut au moins deux valeurs dans la liste 
            i = 1
            pente_gauche = (R[n, ind[n][1][0], ind[n][1][1]] - R[n, ind[n][0][0], ind[n][0][1]])/(P[n, ind[n][1][0], ind[n][1][1]] - P[n, ind[n][0][0], ind[n][0][1]])
            while i < len(ind[n])-1 :
                pente_droite = (R[n, ind[n][i+1][0], ind[n][i+1][1]] - R[n, ind[n][i][0], ind[n][i][1]])/(P[n, ind[n][i+1][0], ind[n][i+1][1]] - P[n, ind[n][i][0], ind[n][i][1]])
                if pente_droite >= pente_gauche:
                    ind[n].pop(i)
                else :
                    pente_gauche = pente_droite
                    i = i + 1                

def preprocessing(ind):
    """Combine les étapes de prétraitement précédentes"""
    question2(ind)
    #print(sum(len(ind[n]) for n in range(N)))
    removeIPdominated(ind)
    #print(sum(len(ind[n]) for n in range(N)))
    removeLPdominated(ind)
    #print(sum(len(ind[n]) for n in range(N)))

preprocessing(indices_liste)

def greedy(ind):
    """Applique l'algorithme glouton de la question 6"""
    N = len(ind)
    e = [sys.float_info.max for n in range(N)]
    l = [0 for n in range(N)]
    budget_restant = p
    while max(e) > 0:
        n = e.index(max(e))
        i = l[n]
        if i >= len(ind[n]):
            e[n] = 0
        else :
            if P[n, ind[n][i][0], ind[n][i][1]] > budget_restant :
                # peut etre pb ligne suivante si i = 0
                X[n, ind[n][i][0], ind[n][i][1]] = budget_restant /(P[n, ind[n][i][0], ind[n][i][1]] - P[n, ind[n][i-1][0], ind[n][i-1][1]])
                budget_restant = 0
                return X
            else :
                budget_restant -= P[n, ind[n][i][0], ind[n][i][1]] - P[n, ind[n][i-1][0], ind[n][i-1][1]]
                e[n] = (R[n, ind[n][i+1][0], ind[n][i+1][1]] - R[n, ind[n][i][0], ind[n][i][1]]) / (P[n, ind[n][i+1][0], ind[n][i+1][1]] - P[n, ind[n][i][0], ind[n][i][1]])

                l[n] = i + 1




        






