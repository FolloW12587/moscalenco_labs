from math import inf

'''
board = [
    [0,1,0,0,1,1,0,1,0,1],
    [0,0,1,0,1,0,1,1,1,0],
    [1,1,0,1,0,1,1,0,0,1],
    [0,0,1,0,1,0,0,1,1,0],
    [0,1,0,0,1,1,0,1,0,1],
    [1,1,1,1,0,1,1,0,0,1]
]'''
board = [[1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
[0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
[0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
[1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]]

def generateMatrix(L):
    outer = []
    for i in range(L):
        outer.append([0]*L)
    return outer
    # return [
    #     [0]*L,
    #     [0]*L,
    #     [0]*L,
    #     [0]*L,
    #     [0]*L,
    #     [0]*L
    #     ]

def get_num(row1, row2):
    out = 0
    for i in range(len(row1)):
        if row1[i] != row2[i]:
            out += 1
    return out

def delCol(matrix, col):
    for i in range(len(matrix)):
        matrix[i][col] = inf
    return matrix

def delRow(matrix, row):
    matrix[row] = [inf] * len(matrix)
    return matrix

def newMatrix(matrix, i):
    matrix = delCol(matrix, i)
    return delRow(matrix, i)

def getMin(row, j):
    m = min(row)
    i = row.index(m)
    if i == j:
        row[i] = inf
        return getMin(row, len(row) + 1)
    else:
        return i

def check_matrix(num):
    for m in board:
        for n in m:
            if n != num:
                return False
    return True                

if __name__ == "__main__":
    if check_matrix(0):
        print("Невозможно выполнить задание, все значения равны 0")
        exit()
    if check_matrix(1):
        print("Невозможно выполнить задание, все значения равны 1")
        exit()
    L = len(board)
    matrix = generateMatrix(L)
    for i in range(L):
        for j in range(L):
            num = get_num(board[i], board[j])
            matrix[i][j] = num
            matrix[i % L][j % L]
    for m in matrix:
        print(m)
    deleted = []
    i = 0
    while len(deleted) < len(matrix):
        deleted.append(i + 1)
        m = getMin(matrix[i], i)
        matrix = newMatrix(matrix, i)
        i = m
    print('Решение')
    for i in range(0 ,len(deleted), 2):
        print("(", deleted[i], ", ",deleted[i+1], ")", sep='')
