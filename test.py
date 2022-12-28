row = 7
col = 7

for i in range(row - 1, -1, -1):
    # osea para arriba y izquierda
    for j in range(col - 1, -1, -1):
        print(i, j)
        col -=1
        break

