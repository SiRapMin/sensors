def LCSLength(X, Y):
    C=[[0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0]]
    for i in range(0,len(X)):
       C[i][0] = 0
    for j in range(0,len(Y)):
       C[0][j] = 0
    for i in range(1,len(X)):
        for j in range(1,len(Y)):
            if X[i] == Y[j]:
                C[i][j] = C[i-1][j-1] + 1
            else:
                C[i][j] = max(C[i][j-1], C[i-1][j])
    return C
def PRINT_LCS(b, X, i, j)
    if i = 0 or j = 0
          then return
    If b[i, j] = “     ”
          then PRINT-LCS(b, X, i-1,j-1)
                   print xi
    Else if b[i, j] = “    ”
           then PRINT-LCS(b, X, i-1, j)
    Else Print-LCS(b, X, I, j, -1)


print(LCSLength(['A','B','C','B','D','A','B'],['B','D','C','A','B','A']),end='/n')