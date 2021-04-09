from copy import deepcopy


class Board():
    def __init__(self, board, solved_board=None, x_0=None, y_0=None):
        self.board = board
        self.solved_board = solved_board
        self.x_0 = x_0
        self.y_0 = y_0
        if not self.x_0 or not self.y_0:
            self.x_0, self.y_0 = self.get_zero_coords()

    def get_zero_coords(self):
        for i in range(len(self.board)):
            if 0 in self.board[i]:
                x = i
                y = self.board[i].index(0)
                break
        return x, y
                
    def get_h(self):
        h = 0
        for i in range(len(self.solved_board.board)):
            for j in range(len(self.solved_board.board[i])):
                if self.solved_board.board[i][j] != self.board[i][j]:
                    for k in range(len(self.solved_board.board)):
                        if self.solved_board.board[i][j] in self.board[k]:
                            h += abs(k - i)
                            ind = self.board[k].index(self.solved_board.board[i][j])
                            h += abs(ind - j)
        return h

    def get_neighbours(self):
        List = []
        side = self.move("left")
        if side:
            List.append(side)
        side = self.move("up")
        if side:
            List.append(side)
        side = self.move("right")
        if side:
            List.append(side)
        side = self.move("down")
        if side:
            List.append(side)
        return List

    def move(self, where):
        if where == "left":
            if self.y_0 == 0:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0][self.y_0 - 1]
                new[self.x_0][self.y_0 - 1] = 0
                return Board(new, self.solved_board, self.x_0, self.y_0 - 1)
        if where == "right":
            if self.y_0 == 2:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0][self.y_0 + 1]
                new[self.x_0][self.y_0 + 1] = 0
                return Board(new, self.solved_board, self.x_0, self.y_0 + 1)
        if where == "up":
            if self.x_0 == 0:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0 - 1][self.y_0]
                new[self.x_0 - 1][self.y_0] = 0
                return Board(new, self.solved_board, self.x_0 - 1, self.y_0)
        if where == "down":
            if self.x_0 == 2:
                return None
            else:
                new = deepcopy(self.board)
                new[self.x_0][self.y_0] = new[self.x_0 + 1][self.y_0]
                new[self.x_0 + 1][self.y_0] = 0
                return Board(new, self.solved_board, self.x_0 + 1, self.y_0)

    def has_solution(self):
        this_loops = self.get_loops(deepcopy(self.board))
        this_decr = self.get_decr(this_loops)
        solved_loops = self.get_loops(deepcopy(self.solved_board.board))
        solved_decr = self.get_decr(solved_loops)
        this_parity = self.get_parity(self.x_0, self.y_0)
        solved_parity = self.get_parity(self.solved_board.x_0, self.solved_board.y_0)
        if (this_decr + solved_decr + this_parity + solved_parity) % 2 == 0:
            return True
        else:
            return False

    def get_decr(self, loops):
        decr = - len(loops)
        for loop in loops:
            decr += len(loop)
        return decr % 2


    def get_parity(self, x, y):
        if (x == 0 and y == 0) or (x == 0 and y == 2) or (x == 1 and y == 1) or (x == 2 and y == 0) or (x == 2 and y == 2):
            return 1
        else:
            return 0

    def get_loops(self, board):
        loops = []
        used = []
        flat = []
        for b in board:
            flat += b
        for i in range(1, len(flat) + 1):
            loop = []
            index = i
            if index in used:
                continue
            used.append(index)
            loop.append(index)
            while True:
                index = flat[index - 1]
                if index == 0:
                    index = 9
                if index not in loop:
                    loop.append(index)
                    used.append(index)
                else:
                    loops.append(loop)
                    break
        return loops

    def Print_board(self):
        print("\n", end='')
        for x in self.board:
            print(str(x))

class Iter():
    def __init__(self, board, prev_iter=None, g=0):
        self.board = board
        self.prev_iter = prev_iter
        self.g = g
        
    def get_f(self):
        return self.g + self.board.get_h()

    def get_neighbours(self):
        return self.board.get_neighbours()


class Solver():
    def __init__(self, board):
        self.history = []
        self.first = Iter(board=board)
        self.queue = [self.first,]
        self.f_mass = [self.first.get_f(),]
        self.solution = None
        while len(self.queue) > 0:
            index_min = self.get_min_index()
            self.f_mass.pop(index_min)
            iter1 = self.queue.pop(index_min)
            neighbours = iter1.get_neighbours()
            neighbours = self.check_neighbours(neighbours)
            for neighbour in neighbours:                    
                if self.isRight(neighbour):
                    print("Решение найдено! На это потребовалось ходов:", iter1.g + 1)
                    self.solution = self.get_solution(iter1, neighbour)
                    break
                new_iter = Iter(neighbour, iter1, iter1.g+1)
                self.queue.append(new_iter)
                self.f_mass.append(new_iter.get_f())
            if self.solution:
                break
        if not self.solution:
            print("Решение не найдено")
            exit()

    def get_solution(self, iter1, neighbour):
        solution = []
        while True:
            if iter1:
                solution.append(iter1.board)
                iter1 = iter1.prev_iter
            else:
                break
        solution.reverse()
        solution.append(neighbour)
        return solution

    def check_neighbours(self, neighbours):
        output = []
        for neighbour in neighbours:
            if neighbour.board not in self.history:
                output.append(neighbour)
                self.history.append(neighbour.board)
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


class inWidthSolver(Solver):
    def __init__(self, board):
        self.history = []
        self.first = Iter(board=board)
        self.queue = [self.first,]
        self.current = 0
        self.cur_neighbours = []
        while True:
            for iter1 in self.queue:
                self.current += 1
                neighbours = iter1.get_neighbours()
                neighbours = self.check_neighbours(neighbours)
                for neighbour in neighbours:
                    if self.isRight(neighbour):
                        print("Решение найдено, вершин раскрыто: ", self.current)
                        exit()
                self.cur_neighbours += neighbours
            self.queue = self.cur_neighbours
            self.cur_neighbours = []
            if self.queue == []:
                print("Решение не найдено")
                exit()


class insideSolver(Solver):
    def __init__(self, board, history=[], g=0, count = 0):
        self.g = g + 1
        self.count = count + 1
        self.history = history
        self.board = board
        self.neighbours = self.board.get_neighbours()
        self.neighbours = self.check_neighbours(self.neighbours)

    def get_new_solver(self):
        while len(self.neighbours) > 0:
            neighbour = self.neighbours.pop()
            if self.isRight(neighbour):
                print("Вершин раскрыто: ", self.count)
                exit()
            if self.g == 5:
                continue
            self.count = insideSolver(neighbour, self.history, self.g, self.count).get_new_solver()
        return self.count
        