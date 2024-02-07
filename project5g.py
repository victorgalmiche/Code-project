import numpy as np
from extraction import *
import math
import sys

#Extraction des données depuis le fichier test
N,M,K,p,P,R = extraction(1)

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
print(indices_liste)

def greedy(ind):
    """Applique l'algorithme glouton de la question 6"""
    N = len(ind)
    e = []
    l = [0 for n in range(N)]
    budget_restant = p

    #Phase d'initialisation
    for n in range(N):
        if len(ind[n]) == 0:
            return "pas de solution"
        elif len(ind[n]) == 1:
            e.append(0)
        else :
            e.append((R[n, ind[n][1][0], ind[n][1][1]] - R[n, ind[n][0][0], ind[n][0][1]])/(P[n, ind[n][1][0], ind[n][1][1]] - P[n, ind[n][0][0], ind[n][0][1]]))
        budget_restant -= P[n, ind[n][0][0], ind[n][0][1]]
        X[n, ind[n][0][0], ind[n][0][1]] = 1
    
    while budget_restant > 0 and max(e) > 0: #On vérifie qu'il reste du budget, et que l'on peut encore avancer
        n = e.index(max(e))
        i = l[n]
        delta_P = P[n, ind[n][i+1][0], ind[n][i+1][1]] - P[n, ind[n][i][0], ind[n][i][1]]
        #delta_R = R[n, ind[n][i+1][0], ind[n][i+1][1]] - R[n, ind[n][i][0], ind[n][i][1]]
        if  delta_P > budget_restant : 
            #On a deux x qui sont fractionnaires dans ce cas
            X[n, ind[n][i+1][0], ind[n][i+1][1]] = (budget_restant - P[n, ind[n][i][0], ind[n][i][1]])/delta_P
            X[n, ind[n][i][0], ind[n][i][1]] -= X[n, ind[n][i+1][0], ind[n][i+1][1]] #Somme = 1
            budget_restant = 0
        else :
            X[n, ind[n][i][0], ind[n][i][1]] = 0
            X[n, ind[n][i+1][0], ind[n][i+1][1]] = 1
            l[n] = i+1
            budget_restant -= delta_P
            if i == len(ind[n]) - 2:
                e[n] = 0 #On est arrivé au bout de la liste des indices possibles pour la fréquence n
            else : 
                e[n] = (R[n, ind[n][i+2][0], ind[n][i+2][1]] - R[n, ind[n][i+1][0], ind[n][i+1][1]])/(P[n, ind[n][i+2][0], ind[n][i+2][1]] - P[n, ind[n][i+1][0], ind[n][i+1][1]])
    #on renvoie le tableau des x 
    return X

print(greedy(indices_liste))



        






