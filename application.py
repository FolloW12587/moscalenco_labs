import os
import sys

from PyQt5 import QtCore, QtWidgets, uic

from game_solver import Board, Solver, inWidthSolver, insideSolver


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

qtCreatorFile = os.path.join(BASE_DIR, "ui", "untitled.ui") 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

qtCreatorFile2 = os.path.join(BASE_DIR, "ui", "solved.ui") 
Ui_MainWindow2, QtBaseClass2 = uic.loadUiType(qtCreatorFile2)

qtCreatorFile3 = os.path.join(BASE_DIR, "ui", "waiter.ui") 
Ui_MainWindow3, QtBaseClass3 = uic.loadUiType(qtCreatorFile3)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, solved=False):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        if solved:
            self.default_2.clicked.connect(self.fillDefaultSolved)
            self.label.setText('Решенное заполнение')
        else:
            self.default_2.clicked.connect(self.fillDefault)
            self.label.setText('Начальное заполнение')
        self.solved = solved
        self.cancel.clicked.connect(exit)
        self.ok.clicked.connect(self.parseBoard)
    
    def fillDefaultSolved(self):
        Wchildren = self.findChildren(QtWidgets.QPlainTextEdit)
        #Wchildren = False
        if Wchildren:
            for i in range(len(Wchildren)):
                if i != 8:
                    Wchildren[i].setPlainText(str(i + 1))
                else:
                    Wchildren[i].setPlainText("0")
        else:
            self.btn0_0.setPlainText("1")
            self.btn0_1.setPlainText("2")
            self.btn0_2.setPlainText("3")
            self.btn1_0.setPlainText("8")
            self.btn1_1.setPlainText("0")
            self.btn1_2.setPlainText("4")
            self.btn2_0.setPlainText("7")
            self.btn2_1.setPlainText("6")
            self.btn2_2.setPlainText("5")

    def fillDefault(self):
        self.btn0_0.setPlainText("2")
        self.btn0_1.setPlainText("5")
        self.btn0_2.setPlainText("3")
        self.btn1_0.setPlainText("1")
        self.btn1_1.setPlainText("6") # 6
        self.btn1_2.setPlainText("4") # 4
        self.btn2_0.setPlainText("8")
        self.btn2_1.setPlainText("0")
        self.btn2_2.setPlainText("7")

    def parseBoard(self):
        mass = []
        temp = []
        check = []
        Wchildren = self.findChildren(QtWidgets.QPlainTextEdit)
        i = 0
        for child in Wchildren:
            num = self.checkInput(check, child)
            if num != None:
                temp.append(num)
                check.append(num)
            else:
                #print("Incorrect input data")
                child.setPlainText("")
            i += 1
            if (i%3) == 0:
                mass.append(temp)
                temp = []
        if len(check) < 9:
            print("Incorrect input data")
            self.label.setText("Неверное заполнение, заполните пустые блоки. " + self.label.text())
            return
        self.board = mass
        self.close()
        

    def checkInput(self, check, child):
        try:
            num = int(child.toPlainText())
        except ValueError:
            return None
        if num < 0 or num > 8 or num in check:
            return None
        else:
            return num


class Waiter(QtWidgets.QMainWindow, Ui_MainWindow3):
    def __init__(self, has_solution):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow3.__init__(self)
        self.setupUi(self)
        if has_solution:
            self.label.setText("Идет поиск решения...")
        else:
            self.label.setText("Решения не существует!")
            btn = QtWidgets.QPushButton('Ok', self)
            btn.move(175, 150)
            btn.clicked.connect(exit)

    def get_solver(self, start_board):
        return Solver(start_board)


class SolverPrinter(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self, solution):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow2.__init__(self)
        self.setupUi(self)
        self.solution = solution
        self.current = 0
        self.last = len(self.solution) - 1
        self.numAll.setText("Решение было найдено за " + str(len(self.solution) - 1) + " шагов!")
        self.Previous.clicked.connect(lambda: self.Paginate('Prev'))
        self.Previous.setEnabled(False)
        self.Next.clicked.connect(lambda: self.Paginate('Next'))
        self.Cancel.clicked.connect(exit)
        self.First.clicked.connect(lambda: self.Paginate('First'))
        self.Last.clicked.connect(lambda: self.Paginate('Last'))
        self.printBoard()

    def printBoard(self):
        for x in range(3):
            for y in range(3):
                qlayout = self.table.itemAtPosition(x, y)
                child = qlayout.widget()
                child.setPlainText("   " + str(self.solution[self.current].board[x][y]))
        self.moveNum.setText(str(self.current))

    def Paginate(self, where):
        if where == 'Prev':
            if self.current == self.last:
                self.Next.setEnabled(True)
            self.current -= 1
            if self.current == 0:
                self.Previous.setEnabled(False)
            self.printBoard()
        elif where == 'Next':
            if self.current == 0:
                self.Previous.setEnabled(True)
            self.current += 1
            if self.current == self.last:
                self.Next.setEnabled(False)
            self.printBoard()
        elif where == 'First':
            if self.current == self.last:
                self.Next.setEnabled(True)
            self.current = 0
            self.Previous.setEnabled(False)
            self.printBoard()
        else:
            if self.current == 0:
                self.Previous.setEnabled(True)
            self.current = self.last
            self.Next.setEnabled(False)
            self.printBoard()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    solved_window = MyApp(True)
    solved_window.show()
    app.exec_()
    window = MyApp(False)
    window.show()
    app.exec_()
    solved_board = Board(solved_window.board)
    start_board = Board(window.board, solved_board)
    
    if not start_board.has_solution():
        waiter = Waiter(False)
        waiter.show()
        sys.exit(app.exec_())
    else:
        waiter = Waiter(True)
        waiter.show()
        QtWidgets.QApplication.processEvents()
        S = waiter.get_solver(start_board)
        waiter.close()
        #app.exec_()
        SP = SolverPrinter(S.solution)
        SP.show()
        app.exec_()
    """
    if not start_board.has_solution():
        waiter = Waiter(False)
        waiter.show()
        sys.exit(app.exec_())
    else:
        #S = inWidthSolver(start_board)
        S = insideSolver(start_board).get_new_solver()
        print("Решение не найдено")
"""