import tkinter.messagebox
from random import randint


class IA:
    GameArea = list()

    def __init__(self, name, token, level):
        self.Name = name
        self.Token = token
        self.Level = level

    def Play(self, gameArea):
        IA.GameArea = gameArea

        if self.Level == 3:
            return IA.GetTacticalSelect()
        elif self.Level == 2:
            return IA.GetRandomChoice()
        else:
            return IA.GetRandomSelect()

    def CanWin(line):
        if len(line[0]) > 0 and (line[0] == line[1] or line[0] == line[2]):
            return True
        elif len(line[1]) > 0 and line[1] == line[2]:
            return True

        return False

    CanWin = staticmethod(CanWin)

    def GetRandomChoice():
        if randint(0, 1) == 0:
            return IA.GetRandomSelect()
        else:
            return IA.GetTacticalSelect()

    GetRandomChoice = staticmethod(GetRandomChoice)

    def GetRandomSelect():
        freeSquares = IA.GetFreeSquares()
        return freeSquares[randint(0, len(freeSquares)-1)]

    GetRandomSelect = staticmethod(GetRandomSelect)

    def GetTacticalSelect():
        fault = []

        diag1 = (IA.GameArea[0][2], IA.GameArea[1][1], IA.GameArea[2][0])
        diag2 = (IA.GameArea[0][0], IA.GameArea[1][1], IA.GameArea[2][2])

        if IA.CanWin(diag1):
            f = 2
            for i in range(3):
                if len(IA.GameArea[i][f]) == 0:
                    fault = [i, f]
                    break
                f -= 1
        elif IA.CanWin(diag2):
            for i in range(3):
                if len(IA.GameArea[i][i]) == 0:
                    fault = [i, i]
                    break
        else:
            for i in range(3):
                row = (IA.GameArea[i][0], IA.GameArea[i][1], IA.GameArea[i][2])
                col = (IA.GameArea[0][i], IA.GameArea[1][i], IA.GameArea[2][i])

                if IA.CanWin(row):
                    for j in range(3):
                        if len(IA.GameArea[i][j]) == 0:
                            fault = [i, j]
                            break
                elif IA.CanWin(col):
                    for j in range(3):
                        if len(IA.GameArea[j][i]) == 0:
                            fault = [j, i]
                            break

                if len(fault) > 0:
                    break

        if len(fault) == 0:
            fault = IA.GetRandomSelect()

        return fault

    GetTacticalSelect = staticmethod(GetTacticalSelect)

    def GetFreeSquares():
        squares = list()

        for row in range(len(IA.GameArea)):
            for col in range(len(IA.GameArea)):
                if len(IA.GameArea[row][col]) == 0:
                    squares.append((row, col))

        return squares

    GetFreeSquares = staticmethod(GetFreeSquares)
