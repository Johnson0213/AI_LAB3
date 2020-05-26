import numpy as np
import random
import itertools

# function to print a 2-D board
def printA(A):
    n = len(A)
    # m = len(A[0])
    for i in range(n):
        print(A[i])
    print()

class Board:
    B = None #board
    H = None #hint
    n, m, nmine = None, None, None
    mask = None
    
    #@staticmethod
    def inrange(self, i, j):
        # print(i, j)
        return i >= 0 and i < self.n and j >= 0 and j < self.m
    
    def __init__(self, n, m, nmine): # return a list of starting hints
        self.n = n
        self.m = m
        self.nmine = nmine
        all_coordinate = [(i, j) for j in range(self.m) for i in range(self.n)]
        # print(all_coordinate)
        mine_pos = random.sample(all_coordinate, nmine)
        self.B = [[0]*self.m for i in range(self.n)]
        self.H = [[0]*self.m for i in range(self.n)]
        for p in mine_pos:
            self.B[p[0]][p[1]] = 1
        #printA(self.B)
        for i, j in itertools.product(range(self.n), range(self.m)):
            if(self.B[i][j] == 1):
                continue
            for dx, dy in itertools.product(range(-1,2,1), range(-1,2,1)):
                if(not (dx==0 and dy==0) and self.inrange(i+dx, j+dy)):
                    self.H[i][j] += self.B[i+dx][j+dy]
        #printA(self.H)
        return
            
    def get_start(self, nstart):
        # get starting hints
        hint_coordinate = list(filter(lambda x: self.B[x[0]][x[1]]==0 ,[(i, j) for j in range(self.m) for i in range(self.n)]))
        # printA(self.B)
        # print(hint_coordinate)
        start_pos = random.sample(hint_coordinate, nstart)
        start = [[-1]*self.m for i in range(self.n)]
        for p in start_pos:
            start[p[0]][p[1]] = self.H[p[0]][p[1]]
        return start
        
        
    def q(i, j): #return -1 if is mine, return number if is hint
        return -1 if self.B[i][j] == 1 else self.H[i][j]

b = Board(3, 3, 4)
#b.get_start(3)
printA(b.get_start(3))
[2, -1, -1]
[-1, -1, 2]
[-1, 4, -1]


class LogicAgent:
    KB = [] # set
    KB0 = [] # ground truth, decided 
    def __init__(init_hint):
        pass
    def play():
        pass
    def inference():
        pass
    def solve():
        pass