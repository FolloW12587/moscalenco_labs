class Solver():
    def __init__(self, element):
        self.query = [element,]

    def solve(self):
        OK = False
        while len(self.query) != 0:
            element = self.query.pop()
            first, second = element.get_next()
            if second == None:
                if first:
                    print('Формула доказана!')
                    element.print_history()
                    OK = True
                    break
                else:
                    continue
            self.query += [first, second]
        if not OK:
            print('Формула не доказана!')


class solverElement():
    def __init__(self, left, right, prev = None):
        self.left = left
        self.right = right
        self.prev = prev
        self.get_left_right()

    def print_history(self):
        if self.prev != None:
            self.prev.print_history()
        print(self.left, '=', self.right)

    def get_next(self):
        for i in range(len(self.left)):
            if len(self.left[i]) > 1:
                split = self.left[i].split('V')
                left = self.left[:]
                del left[i]
                left_first = left + split[0:1]
                left_second = left + split[1:2]
                return solverElement(left_first, self.right, self), solverElement(left_second, self.right, self)
        for i in range(len(self.right)):
            if len(self.right[i]) > 1:
                split = self.right[i].split('&')
                right = self.right[:]
                del right[i]
                right_first = right + split[0:1]
                right_second = right + split[1:2]
                return solverElement(self.left, right_first, self), solverElement(self.left, right_second, self)
        self.left = list(set(self.left))
        self.right = list(set(self.right))
        if len(self.left) == len(self.right):
            for i in self.left:
                if i not in self.right or self.left.count(i) != self.right.count(i):
                    return False, None
            return True, None
        return False, None
        

    def get_elements(self, side, sign):
        elements = []
        elem = ''
        big = False
        for i in range(len(side)):
            if side[i] == sign and not big:
                if '|' in elem and '(' not in elem:
                    elems = elem.split('|')
                    elem = '!('+elems[0] + 'V' + elems[1] +')'
                elif r'/' in elem and '(' not in elem:
                    elems = elem.split(r'/')
                    elem = '!('+elems[0] + '&' + elems[1] +')'
                elif '-' in elem and '(' not in elem:
                    elems = elem.split('-')
                    elem = '(!'+ elems[0] + 'V'+ elems[1]+')'
                elements.append(elem)
                elem = ''
            elif side[i] == '(':
                elem += '('
                big = True
            elif side[i] == ')':
                elem += ')'
                if i == len(side) - 1:
                    elements.append(elem)
                big = False
            elif i == len(side) - 1:
                elem += side[i]
                if '|' in elem and '(' not in elem:
                    elems = elem.split('|')
                    elem = '!('+elems[0] + 'V' + elems[1] +')'
                elif r'/' in elem and '(' not in elem:
                    elems = elem.split(r'/')
                    elem = '!('+elems[0] + '&' + elems[1] +')'
                elif '-' in elem and '(' not in elem:
                    elems = elem.split('-')
                    elem = '(!'+ elems[0] + 'V'+ elems[1]+')'
                elements.append(elem)
            else:
                elem += side[i]
        return elements
        
    def reflection_remove(self, left, right):
        from_left = []
        from_right = []
        for i in range(len(left)):
            if left[i][0] == '!' and (len(left[i]) == 2 or left[i][1] == '('):
                from_left.append(i)
                right.append(left[i][1:])
        from_left.sort(reverse=True)
        for i in from_left:
            del left[i]
        for i in range(len(right)):
            if right[i][0] == '!' and (len(right[i]) == 2 or right[i][1] == '('):
                from_right.append(i)
                left.append(right[i][1:])
        from_right.sort(reverse=True)
        for i in from_right:
            del right[i]
        return left, right
        
    def remove_brackets(self, left, right):
        from_left = []
        from_right = []
        for i in range(len(left)):
            if left[i][0] == '(':
                from_left.append(i)
                left.append(left[i][1:-1])
        from_left.sort(reverse=True)
        for i in from_left:
            del left[i]
        for i in range(len(right)):
            if right[i][0] == '(':
                from_right.append(i)
                right.append(right[i][1:-1])
        from_right.sort(reverse=True)
        for i in from_right:
            del right[i]
        return left, right

    def get_left_right(self):
        left = self.left
        right = self.right
        while True:
            l = []
            for i in range(len(left)):
                left_new = self.get_elements(left[i], '&')
                l += left_new
            r = []
            for i in range(len(right)):
                right_new = self.get_elements(right[i], 'V')
                r += right_new
            l, r = self.reflection_remove(l, r)
            l, r = self.remove_brackets(l, r)
            if left == l and right == r:
                break
            else:
                left = l
                right = r
        self.left = left
        self.right = right


def get_elements(side, sign):
    elements = []
    elem = ''
    big = False
    for i in range(len(side)):
        if side[i] == sign and not big:
            if '|' in elem and '(' not in elem:
                elems = elem.split('|')
                elem = '!('+elems[0] + 'V' + elems[1] +')'
            elif r'/' in elem and '(' not in elem:
                elems = elem.split(r'/')
                elem = '!('+elems[0] + '&' + elems[1] +')'
            elif '-' in elem and '(' not in elem:
                elems = elem.split('-')
                elem = '(!'+ elems[0] + 'V'+ elems[1]+')'
            elements.append(elem)
            elem = ''
        elif side[i] == '(':
            elem += '('
            big = True
        elif side[i] == ')':
            elem += ')'
            if i == len(side) - 1:
                elements.append(elem)
            big = False
        elif i == len(side) - 1:
            elem += side[i]
            if '|' in elem and '(' not in elem:
                elems = elem.split('|')
                elem = '!('+elems[0] + 'V' + elems[1] +')'
            elif r'/' in elem and '(' not in elem:
                elems = elem.split(r'/')
                elem = '!('+elems[0] + '&' + elems[1] +')'
            elif '-' in elem and '(' not in elem:
                elems = elem.split('-')
                elem = '(!'+ elems[0] + 'V'+ elems[1]+')'
            elements.append(elem)
        else:
            elem += side[i]
    return elements


if __name__ == "__main__":
    print("! - отрицание", "& - конъюнкция", "V - дизъюнкция", r"/ - операция Шеффера", "| - стрелка Пирса", "= - импликация, разделяющая части выражения", "- - импликация", "Используйте круглые скобки () для группировки", sep="\n")
    data = input("Введите предложение: ")
    data = data.replace(' ', '')
    if data.count('(') != data.count(')'):
        print("Введенно неверное выражение")
        exit()
    sides = data.split('=')
    if len(sides) != 2:
        print("Введенно неверное выражение")
        exit()
    left = get_elements(sides[0], '&')
    right = get_elements(sides[1], 'V')
    element = solverElement(left, right)
    Solver(element).solve()
