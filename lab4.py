'''matrix = [
    [1,1,0,0,1,1,1,0,0,1,0,1,0],
    [0,0,1,1,0,0,0,0,1,0,1,0,1],
    [0,1,0,1,0,1,0,1,0,1,0,1,1],
    [1,1,0,0,1,0,1,0,0,1,0,1,1],
    [0,0,1,1,0,0,0,1,1,0,1,0,0],
    [0,1,0,1,0,1,0,1,0,0,1,1,1]
]'''

matrix = [
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,0,1,0,1,0,1,0,1,0,1],
    [0,1,0,1,0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]
'''

matrix = [[1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1],
[0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
[0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
[0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0],
[1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1],
[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1]]
'''


if __name__ == "__main__":
    # R1 = int(input("Введите R1 (Рекомендуется {}): ".format(round(len(matrix[0])/2 + len(matrix[0])/4)))) #маска - должна отличаться от последней найденной маски на R1 и не совпадает со всеми масками по R2
    # R2 = int(input("Введите R2: (Рекомендуется {}) ".format(round(len(matrix[0])/2 + len(matrix[0])/4))))
    R1 = round(len(matrix[0])/2 + len(matrix[0])/4)
    R2 = round(len(matrix[0])/2 + len(matrix[0])/4)
    masks = [0,]

    for i in range(1, len(matrix)):
        mask = masks[-1]
        if i == mask:
            continue
        for m in masks:
            a = True
            div = 0
            for k in range(len(matrix[i])):
                if matrix[i][k] != matrix[m][k]:
                    div += 1
            if div < R2:
                a = False
                break
        if not a:
            continue
        div = 0
        for j in range(len(matrix[i])):
            if matrix[i][j] != matrix[mask][j]:
                div += 1
        if div >= R1:
            masks.append(i)
    print("Маски: ", list(map(lambda x: x+1, masks)))
    codes = []
    for i in range(len(matrix)):
        code = []
        for j in range(len(masks)):
            if i == masks[j]:
                code.append(1)
                continue
            comp = 0
            for k in range(len(matrix[i])):
                if matrix[i][k] == matrix[masks[j]][k]:
                    comp += 1
            if comp >= 9:
                code.append(1)
            else:
                code.append(0)
        codes.append(code)
    print("Коды строк:")
    vectors = []
    used = []
    for code in codes:
        print(code)
        if code in used:
            continue
        used.append(code)
        c = codes.count(code)
        vector = []
        prev = -1
        for i in range(c):
            ind = codes.index(code, prev+1)
            vector.append(ind+1)
            prev = ind
        vectors.append(tuple(vector))
    print("Кластеры: " + str(vectors)[1:-1])