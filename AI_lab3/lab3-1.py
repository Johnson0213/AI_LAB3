#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import random
import itertools
from copy import deepcopy
import math


# In[2]:


# hyper params
MATCH_ITER_LIMIT = 3 # n => n^2 => n^4 => n^8 => n^16, or can use CLS_LIMIT
MATCH_SIZE_LIMIT =2 # subset with size <= limit can match wih other
GLOBAL_LIMIT = 5000 # when to add global limit, when C(n,m) is less than gloal limit
CLS_LIMIT = 1000


# In[3]:


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
    
    # for printing
    def __repr__(self):
        n = self.n
        m = self.m
        ret = ""
        for i in range(n):
            ret += str(self.B[i])
            ret += "\n"
        return ret
            
    def get_start(self, nstart = None):
        # get starting hints(starting safe positions)
        if(nstart == None):
            nstart = int(np.sqrt(self.n*self.m))
        hint_coordinate = list(filter(lambda x: self.B[x[0]][x[1]]==0 ,[(i, j) for j in range(self.m) for i in range(self.n)]))
        # printA(self.B)
        # print(hint_coordinate)
        start_pos = random.sample(hint_coordinate, nstart)
        #start = [[-1]*self.m for i in range(self.n)]
        #for p in start_pos:
        #    start[p[0]][p[1]] = self.H[p[0]][p[1]]
        return start_pos
        
    # query
    def q(self, i, j): #return -1 if is mine, return number if is hint
        return -1 if self.B[i][j] == 1 else self.H[i][j]
    def q(self, p): #return -1 if is mine, return number if is hint
        return -1 if self.B[p[0]][p[1]] == 1 else self.H[p[0]][p[1]]
                                            
    


# In[4]:


class VAR:
    pos = None
    T = None # true / false, Mine/ Safe
    
    def __init__(self, pos, T):
        self.pos = pos
        self.T = T
    def __repr__(self):
        if self.T :
            return "M(%d,%d)"%(self.pos[0], self.pos[1])
        else:
            return "S(%d,%d)"%(self.pos[0], self.pos[1])
    
    def __eq__(self, rhs):
        if(isinstance(rhs, VAR)):
            return (self.pos == rhs.pos and self.T == rhs.T)
        else:
            return False
    # collision? 
    def __hash__(self):
        return hash(self.__repr__())
    
    def neg(self):
        return VAR(self.pos, not self.T)

class CLS: # Or of Variables
    # use set of variable is enough
    def formatch(self):
        # 2 literal
        pass
        
    pass


# In[5]:


# Treat as an ADT(abstact data structure) that support desired op.s
class KB: # And of Variables
    kb = list()  # list of cls(set of variable)
    #cls is set, set is unhashable, can define cls but
    kb0 = set() # set of variable
    def __init__(self):
        self.kb = list()
        self.kb0 = set()
    
    # return kb0's size
    def atom(self):
        return len(self.kb0)
    def pos_atom(self):
        ret = 0
        for var in self.kb0: 
            ret += var.T
        return ret
    
    # pop 1 len(1) from kb 
    def get_single(self):
        for cls in self.kb:
            if len(cls) == 1:
                return deepcopy(cls) 
        return None
    
    # add to kb0 
    def add_kb0(self, var):
        #assert(len(cls) == 1)
        assert(var not in self.kb0)
        assert(var.neg() not in self.kb0)
        self.kb0.add(var) # kb0 is a set
        return
    
    # remove cls from kb
    def remove(self, cls):
        assert(cls in self.kb)
        self.kb.remove(cls)
        return
    # remove cls and add to kb0
    def transfer_to_kb0(self, var):
        self.remove({var})
        self.add_kb0(var)
        # resolution
        kb_tmp = []
        for cls in self.kb:
            if var in cls:
                #tautology
                continue
            elif var.neg() in cls:
                cls.remove(var.neg())
                assert(len(cls) != 0)
                kb_tmp.append(cls)
            else:
                kb_tmp.append(cls)
        self.kb = kb_tmp
            
    
    # insert cls to kb
    # resolution with kb0 and check is not supperset(or eq) to other
    # assert not negative tautology
    def insert(self, cls):
        # resolutions with kb0
        assert(isinstance(cls, set))
        #cls_0 = deepcopy(cls)
        for truth in self.kb0:
            if truth in cls:
                # tautology
                return 
            elif truth.neg() in self.kb0:
                # this part is never True
                cls.remove(truth) # error handling should be redundunt
        
        # should not be negative tautology
        if(len(cls) == 0):
            #print(cls_0)
            assert(len(cls) != 0)
            # should not be negative tautology
        
        # check not supper set or equal to other
        flag = True
        for cls2 in self.kb:
            if(cls2.issubset(cls)):
                flag = False
                break
        if flag:
            self.kb.append(cls)
        return
    
    # do pair wise match for cls with size 2
    def match(self):
        self.deal_sub()
        kb2 = [cls for cls in self.kb if len(cls) <= 2]
        n = len(kb2)
        
        def get_match(cls1, cls2):
            if(cls1.issubset(cls2)):
                return cls1
            comp = []
            for var in cls1:
                if var.neg in cls2:
                    comp.append(var)
            if(len(comp) > 1):
                return []
            elif (len(comp) == 1):
                var = comp[0]
                resolution_cls = cls1.union(cls2)
                if(var in resolution_cls):
                    resolution_cls.remove(var)
                if(var.neg() in resolution_cls):
                    resolution_cls.remove(var.neg())
                return [resolution_cls]
            else :
                return []
            
        for i in range(n):
            for j in range(i+1, n):
                a = kb2[i]
                b = kb2[j]
                for match_cls in get_match(a,b):
                    assert(isinstance(match_cls, set))
                    self.insert(match_cls)
        return
    
    # check pairwise subsumpltion and remove the less restricting ones
    #O(n^2)
    def deal_sub(self):
        kb_tmp = []
        n = len(self.kb)
        for i in range(n):
            cls1 = self.kb[i]
            flag = True
            for j in range(n):
                cls2 = self.kb[j]
                if(i != j and cls2.issubset(cls1)):
                    if(cls2.issuperset(cls1)): # eq case
                        print("BAD THING")
                        if(j > i):
                            flag = False
                            break
                    flag = False
                    break
            if(flag):
                kb_tmp.append(self.kb[i]) #type 
                
        self.kb = kb_tmp
        return
    


# In[9]:


class LogicAgent:
    b = None # game board in agent's hand
    B = None # solution, not used, will declare in solve as answer and return
    kb = None # current kowledge, include kb0(marked)
    
    def __init__(self):
        pass
    
    def solve(self, b, MATCH_ITER_LIMIT = MATCH_ITER_LIMIT, PRINT=False):
        # initializing solver
        self.b = b # game engine
        self.kb = KB() # KB
        B = [[-1]*b.m for i in range(b.n)]# answer, -1 not decided, 0 no mine, 1 mine
        kb = self.kb # sugar
        #b = self.b
        
        # get init positions
        start_pos = self.b.get_start()
        # add inital safe position to KB
        for p in start_pos:
            kb.insert({VAR(p, 0)})
        
        # start solving
        iteration = 0
        while(1):
            # is done
            if(kb.atom() == b.n*b.m):
                # B = [[-1]*b.m for i in range(b.n)]
                # for var in kb0:
                #     B[var.pos[0]][var.pos[1]] = var.T
                return B, (kb.atom(), b.n*b.m)
            
            if PRINT:
                iteration += 1
                print("ith iteration, i = ", iteration)
                printA(B)
                print(b)
            
            # check whether add global constraint now
            
            def comb(n, r):
                return math.factorial(n) // math.factorial(r) // math.factorial(n-r)
                
            if(comb(b.n*b.m - kb.atom(), b.nmine - kb.pos_atom()) < GLOBAL_LIMIT):
                undecided = []
                V0 = []
                V1 = []
                for i in range(b.n):
                    for j in range(b.m):
                        if(B[i][j] == -1):
                            undecided.append((i,j))
                            V0.append(VAR((i,j), 0))
                            V1.append(VAR((i,j), 1))
                assert(b.n*b.m - kb.atom() == len(V0))
                m = len(V0)
                n = b.nmine - kb.pos_atom()
                for cmb in itertools.combinations(V1, m-n+1):
                    kb.insert(set(cmb))
                for cmb in itertools.combinations(V0, n+1):
                    kb.insert(set(cmb))
        
            # get singleton
            cnt = 0
            while(kb.get_single() == None and cnt < MATCH_ITER_LIMIT):
                kb.match()
                cnt += 1
            if(kb.get_single() == None): # no any sigleton after matching limit
                print("Matching Limit Exceed!")
                # B = [[-1]*b.m for i in range(b.n)]
                # for var in kb0:
                #    B[var.pos[0]][var.pos[1]] = var.T
                return B, (kb.atom(), b.n*b.m)
                # break
                
            ## deal with sigleton
            a = kb.get_single() # a singleton cls's only var
            ad = deepcopy(a)
            a = ad.pop()
            hint = b.q(a.pos)
            assert((hint == -1 and a.T == 1) or (hint != -1 and a.T == 0))
            ## common
            # 1. move to kb0
            # 2. matching of new kb0 to remainning cls
            i = a.pos[0]
            j = a.pos[1]
            kb.transfer_to_kb0(a)
            B[i][j] = a.T
            if(a.T == 0): # is safe and with hint res
                i = a.pos[0]
                j = a.pos[1]
                # undecided = []
                V0 = []
                V1 = []
                n = hint # should - positive B
                for dx, dy in itertools.product(range(-1,2,1), range(-1,2,1)):
                    nx, ny = i+dx, j+dy
                    if(not (dx==0 and dy==0) and b.inrange(nx, ny)):
                        if(B[nx][ny] == -1):
                            # undecided.append((nx, ny))
                            V0.append(VAR((nx,ny), 0))
                            V1.append(VAR((nx,ny), 1))
                        if(B[nx][ny] == 1):
                            n -= 1
                m = len(V0)
                # clause type, C m choose n, now at i, used array
                # use iter tool for higher performance
                for cmb in itertools.combinations(V1, m-n+1):
                    kb.insert(set(cmb))
                for cmb in itertools.combinations(V0, n+1):
                    kb.insert(set(cmb))
    
    def do(self, a): # deal with a singleton
        pass
                
             
        
        


# In[12]:


b = Board(16,16,25)
agent = LogicAgent()
B, rate = agent.solve(b)
printA(B)


# In[13]:


print(b)


# In[ ]:





# In[ ]:




