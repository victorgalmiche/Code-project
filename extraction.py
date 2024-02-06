import numpy as np

def extraction(i):
    #On commence par ouvrir un objet file
    fichier = open(r'C:\Users\victo\Desktop\POLYTECHNIQUE\2A\P2\INF421\Programming Project\Code project\testfiles\test'+str(i)+'.txt','r', encoding='utf-8')
    #fichier = open('.\testfiles\test' + str(i) + '.txt', 'r', encoding = 'utf-8')

    #On lit les premières lignes qui nous donnennt N, M, K et p
    ligne = fichier.readline().strip()
    N = int(float(ligne))

    ligne = fichier.readline().strip()
    M = int(float(ligne))

    ligne = fichier.readline().strip()
    K = int(float(ligne))

    ligne = fichier.readline().strip()
    p = int(float(ligne))

    #On lit ensuite les matrices p_k,m,n pour tout n
    #Ici l'extraction se fait de telle sorte que le tableau est organisé selon P[n][k][m]
    P = []
    for n in range(N):
        p_n = []
        for k in range(K): 
            ligne = fichier.readline().strip().split('   ')
            for m in range(M):
                ligne[m] = int(float(ligne[m]))
            p_n.append(ligne)
        P.append(p_n)

    P =np.array(P)

    #Comme pour P avec les r_k,m,n
    R = []
    for n in range(N):
        r_n = []
        for k in range(K):
            ligne = fichier.readline().strip().split('   ')
            for m in range(M):
                ligne[m] = int(float(ligne[m]))
            r_n.append(ligne)
        R.append(r_n)
    R = np.array(R)

    return (N, M, K, p, P, R)