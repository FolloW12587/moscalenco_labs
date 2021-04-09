import numpy as np
import pandas as pd
from sympy import Symbol, simplify


x1 = Symbol('x1')
x2 = Symbol('x2')
x3 = Symbol('x3')
x4 = Symbol('x4')
x5 = Symbol('x5')
x6 = Symbol('x6')
x7 = Symbol('x7')
x8 = Symbol('x8')
x9 = Symbol('x9')

data = pd.DataFrame([
    ['0', 1, 1, 1, 1, 1, 1, 1],
    ['0', 0, 0, 1, 0, 0, 1, 0],
    ['0', 1, 1, 0, 1, 0, 0, 1],
    ['1', 0, 0, 1, 1, 0, 1, 1],
    ['1', 0, 1, 0, 1, 1, 1, 0],
    ['1', 1, 0, 1, 0, 1, 0, 0]
], columns=['class', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])


if __name__ == "__main__":

    ### xoring classes ###
    classes = data['class'].unique()
    temp = data.copy()
    outer = pd.DataFrame(columns=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])
    for i in range(len(classes)):
        curr = temp[temp['class'] == classes[i]]
        temp = temp[temp['class'] != classes[i]]
        if len(temp) != 0:
            for n in range(len(curr)):
                for m in range(len(temp)):
                    row = np.bitwise_xor(curr.iloc[n][['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']], temp.iloc[m][['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7']])
                    row = pd.DataFrame([row.values,], columns=list(row.index))
                    outer = pd.concat([outer, row])

    print('After XOR operation:')
    print(outer)

    ### counting ones ###
    ones = pd.Series()
    for i in range(len(outer)):
        ones.set_value(i, outer.iloc[i].sum())
    ones.sort_values(inplace=True)
    print('counting ones')
    print(ones)

    ### sort in order of ones ascending ###
    data_sorted = pd.DataFrame(columns=['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7'])
    for i in list(ones.index):
        data_sorted = pd.concat([data_sorted, pd.DataFrame([outer.iloc[i].values,], columns=outer.iloc[i].index)])
    data_sorted.reset_index(inplace=True, drop=True)
    print('sort in order of ones ascending')
    print(data_sorted)
    
    ### deleting rows by masks ###
    columns = list(data_sorted.columns)
    index_list = list(data_sorted.index)
    for i in range(len(data_sorted)):
        if i not in index_list:
            continue
        cols = []
        for c in columns:
            if data_sorted.iloc[i][c] == 1:
                cols.append(c)
        temp = data_sorted.copy()
        for c in cols:
            temp = temp[temp[c] == 1]
        for ind in list(temp.index):
            if ind == i or ind not in index_list:
                continue
            if ind in index_list:
                index_list.remove(ind)
    data_sorted = data_sorted.filter(items=index_list, axis=0)
    print('deleting rows by masks')
    print(data_sorted)


    ### creating expressions ###
    temp_str = ''

    for i in range(len(data_sorted)):
        temp_str += '('
        for col in columns:
            if data_sorted.iloc[i][col] == 1:
                temp_str += col + '|'
        temp_str = temp_str[:-1]
        if len(temp_str) == 0:
            continue
        temp_str += ')'
        if i != len(data_sorted) -1:
            temp_str += '&'

    print('creating expressions')
    ev = eval(temp_str)
    print(ev)


    ### simplification ###
    print('simplification')
    simple = simplify(ev)
    print('simple = ', simple)
    
    print("Тупиковые тесты: ")
    for i in range(len(simple.args)):
        print(i+1, simple.args[i].args)
