from copy import deepcopy
import sys
sys.setrecursionlimit(10**4)


class Board():
    def __init__(self, board=None, x_0=None, y_0=None, solved=False):
        if board:
            self.board = board
            self.x_0 = x_0
            self.y_0 = y_0
            if not self.x_0 or not self.y_0:
                self.x_0, self.y_0 = self.get_zero_coords()
        elif solved: # верное решение
            self.board = [
                [1, 2, 3],
                [8, 0, 4],
                [7, 6, 5]
            ]
            self.x_0, self.y_0 = self.get_zero_coords()
        else: # Начальное заполнение
            self.board = [
                [2, 5, 3],
                [1, 6, 4],
                [8, 0, 7]
            ]
            self.x_0, self.y_0 = self.get_zero_coords()

    def get_zero_coords(self):
        for i in range(len(self.board)):
            if 0 in self.board[i]:
                x = i
                y = self.board[i].index(0)
                break
        return x, y
                
    def get_h(self):
        # Рассчет h
        h = 0
        for i in range(len(solved_board.board)):
            for j in range(len(solved_board.board[i])):
                if solved_board.board[i][j] != self.board[i][j]:
                    h += 1
        return h

    def get_neighbours(self):
        List = []
        side = self.move("left")
        if side:
            List.append(side)
        side = self.move("right")
        if side:
            List.append(side)
        side = self.move("up")
        if side:
            List.append(side)
        side = self.move("down")
        if side:
            List.append(side)
        return List

    def move(self, where):
        # moving zero to the different sides
        if where == "left":
            if self.y_0 == 0:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0][self.y_0 - 1]
                new[self.x_0][self.y_0 - 1] = 0
                return Board(new, self.x_0, self.y_0 - 1)
        if where == "right":
            if self.y_0 == 2:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0][self.y_0 + 1]
                new[self.x_0][self.y_0 + 1] = 0
                return Board(new, self.x_0, self.y_0 + 1)
        if where == "up":
            if self.x_0 == 0:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0 - 1][self.y_0]
                new[self.x_0 - 1][self.y_0] = 0
                return Board(new, self.x_0 - 1, self.y_0)
        if where == "down":
            if self.x_0 == 2:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0 + 1][self.y_0]
                new[self.x_0 + 1][self.y_0] = 0
                return Board(new, self.x_0 + 1, self.y_0)

    def has_solution(self):
        summ = self.x_0
        flat = []
        for b in self.board:
            flat += b
        for i in range(len(flat)):
            if i != len(flat) - 1 and flat[i] != 0:
                for j in range(i + 1, len(flat)):
                    if flat[j] != 0 and flat[i] > flat[j]:
                        summ += 1
        return summ

    def Print_board(self):
        print("\n", end='')
        for x in self.board:
            print(str(x))


solved_board = Board(solved=True)


class Iter():
    def __init__(self, board=Board(), prev_iter=None, g=0):
        self.board = board
        self.prev_iter = prev_iter
        self.g = g
        

    def get_f(self):
        return self.g + self.board.get_h()

    def get_neighbours(self):
        return self.board.get_neighbours()


class Solver():
    def __init__(self):
        self.history = []
        self.first = Iter()
        self.queue = [self.first,]
        self.f_mass = [self.first.get_f(),]
        while len(self.queue) > 0:
            index_min = self.get_min_index()
            self.f_mass.pop(index_min)
            iter1 = self.queue.pop(index_min)
            neighbours = iter1.get_neighbours()
            neighbours = self.check_neighbours(neighbours)
            for neighbour in neighbours:
                if neighbour.board in self.history:
                    continue
                self.history.append(neighbour.board)                    
                if self.isRight(neighbour):
                    print("Решение найдено! На это потребовалось ходов:", iter1.g + 1)
                    neighbour.Print_board()
                    self.print_question(iter1)
                    neighbour.Print_board()
                    exit()
                new_iter = Iter(neighbour, iter1, iter1.g+1)
                self.queue.append(new_iter)
                self.f_mass.append(new_iter.get_f())
        print("Решение не найдено")
    
    def print_question(self, iter1):
        print("Решение может быть большим, вы действительно хотите его вывести? (Y - да, Иначе - нет) ", end='')
        if input() == 'Y':
            self.Print_solution(iter1)
        else:
            print("bye")

    def Print_solution(self, iter1):
        solution = []
        while True:
            if iter1:
                solution.append(iter1.board)
                iter1 = iter1.prev_iter
            else:
                break
        solution.reverse()
        for board in solution:
            board.Print_board()

    def check_neighbours(self, neighbours):
        output = []
        for neighbour in neighbours:
            if neighbour.board not in self.history:
                output.append(neighbour)
        return output
    
    def isRight(self, board):
        if board.get_h() == 0:
            return True
        else:
            return False
        
    def get_min_index(self):
        if len(self.f_mass) == 0:
            return None
        m = self.f_mass.copy()
        m.sort()
        return self.f_mass.index(m[0])

        
if __name__ == "__main__":
    S = Solver()
    print("Решение не найдено")
