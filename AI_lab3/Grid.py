import random
from Cell import *


class Grid:
    def __init__(self, height, width, minP):
        self.height = height
        self.width = width
        self.grid = []
        self.mineP = minP
        self.numOfMine = 0
        self.borderHeight = self.height + 2
        self.borderWidth = self.width + 2

    def generateGrid(self):
        for i in range(self.borderHeight):
            for j in range(self.borderWidth):
                rNum = random.random()
                if i == self.borderHeight - 1 or i == 0 or j == self.borderWidth - 1 or j == 0:
                    cell = Cell(False)
                    cell.isOutside = True
                    self.grid.append(cell)
                elif 0 <= rNum < self.mineP:
                        cell = Cell(True)
                        self.grid.append(cell)
                        self.numOfMine += 1
                else:
                    cell = Cell(False)
                    self.grid.append(cell)

    def generateSpecificGrid(self):
        for i in range(self.borderHeight):
            for j in range(self.borderWidth):
                if i == self.borderHeight - 1 or i == 0 or j == self.borderWidth - 1 or j == 0:
                    cell = Cell(False)
                    cell.isOutside = True
                    self.grid.append(cell)
                else:
                    cell = Cell(False)
                    self.grid.append(cell)

        self.getCell(2, 0).isMine = True
        self.getCell(0, 2).isMine = True
        self.getCell(2, 4).isMine = True
        self.getCell(4, 2).isMine = True
        self.getCell(2, 2).numOfmines = 0
        self.getCell(1, 1).numOfmines = 1
        self.getCell(1, 2).numOfmines = 1
        self.getCell(1, 3).numOfmines = 1
        self.getCell(2, 1).numOfmines = 1
        self.getCell(2, 3).numOfmines = 1
        self.getCell(3, 1).numOfmines = 1
        self.getCell(3, 2).numOfmines = 1
        self.getCell(3, 3).numOfmines = 1

    def markMineNumber(self):
        for i in range(self.height):
            for j in range(self.width):
                cell = self.getCell(i, j)
                for ii in range(-1, 2):
                    for jj in range(-1, 2):
                        if ii == 0 and jj == 0:
                            continue
                        adj = self.getCell(i + ii, j + jj)
                        if not adj.isOutside and adj.isMine:
                            cell.numOfMines += 1

    def getCell(self, x, y):
        return self.grid[(x + 1) * self.borderWidth + (y + 1)]

    def isConsistency(self):
        for i in range(self.height):
            for j in range(self.width):
                curCell = self.getCell(i, j)
                if curCell.isCovered:
                    continue
                numOfCovered = self.numOfCoveredCell(i, j)
                numOfFlag = self.numOfFlags(i, j)
                # if the current cell shows number of mines around is 0
                # but the actual number of cells covered around > 0
                # then it is not consistency
                if curCell.numOfMines == 0 and numOfCovered > 0:
                    return False
                # if the number of mines showed by the current cells
                # is greater than the number of flags around
                # but the number of covered cells around is 0
                # then it is not consistency
                if curCell.numOfMines > numOfFlag and numOfCovered == 0:
                    return False

                if curCell.numOfMines < numOfFlag:
                    return False

        return True

    def numOfCoveredCell(self, i, j):
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                currCell = self.getCell(i + p, j + q)
                if not currCell.isOutside and currCell.isCovered and not currCell.isFlag:
                    result += 1
        return result

    def numOfFlags(self, i, j):
        result = 0
        for p in range(-1, 2):
            for q in range(-1, 2):
                if p == 0 and q == 0:
                    continue
                currCell = self.getCell(i + p, j + q)
                if not currCell.isOutside and currCell.isFlag:
                    result += 1
        return result


