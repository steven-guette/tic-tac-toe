from typing import List, Any


class VirtualArea:
    RowsNumber = 3
    ColsNumber = 3

    def __init__(self):
        self.Area = list()
        self.SetArea()

    # region METHODS

    def AddToken(self, x, y, token):
        self.Area[x][y] = token

    def IsAvailable(self, x, y):
        return len(self.Area[x][y]) == 0

    def IsFull(self):
        for row in range(VirtualArea.RowsNumber):
            for col in range(VirtualArea.ColsNumber):
                if len(self.Area[row][col]) == 0:
                    return False

        return True

    def ResetArea(self):
        for row in range(VirtualArea.RowsNumber):
            for col in range(VirtualArea.ColsNumber):
                self.Area[row][col] = ""

    # endregion

    # region SETTERS

    def SetArea(self):
        for rows in range(VirtualArea.RowsNumber):
            c = list()

            for cols in range(VirtualArea.ColsNumber):
                c.append("")

            self.Area.append(c)

    # endregion

    # region GETTERS

    def GetArea(self):
        return self.Area

    # endregion
