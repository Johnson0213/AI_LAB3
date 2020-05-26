#!/usr/bin/env python
# coding: utf-8

# In[241]:


import numpy as np
import random
import itertools
from copy import deepcopy


# In[224]:


# hyper params
MATCH_INTER_LIMIT = 3 # n => n^2 => n^4 => n^8 => n^16, or can use CLS_LIMIT
MATCH_SIZE_LIMIT =2 # subset with size <= limit can match wih other
CLS_LIMIT = 1000


# In[225]:


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
    def q(i, j): #return -1 if is mine, return number if is hint
        return -1 if self.B[i][j] == 1 else self.H[i][j]
    def q(p): #return -1 if is mine, return number if is hint
        return -1 if self.B[p[0]][p[1]] == 1 else self.H[p[0]][p[1]]
                                            
    


# In[226]:


b = Board(3, 3, 4)
#b.get_start(3)
printA(b.get_start())
printA(b.B)
print(b)


# In[227]:


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


# In[256]:


# Treat as an ADT(abstact data structure) that support desired op.s
class KB: # And of Variables
    kb = list()  # list of cls(set of variable)
    #cls is set, set is unhashable, can define cls but
    kb0 = set() # set of variable
    def __init__(self):
        pass
    
    # return kb0's size
    def atom(self):
        return len(self.kb0)
    
    # pop 1 len(1) from kb 
    def get_single(self):
        for cls in self.kb:
            if len(cls) == 1:
                return cls 
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
    def transfet_to_kb0(self, var):
        self.remove(set(var))
        self.add_kb0(var)
        # resolution
        kb_tmp = []
        for cls in self.kb:
            if var in cls:
                #tautology
                continue
            elif var.neg() in cls:
                cls.remove(var.neg())
                kb_tmp.append(cls)
            else:
                kb_tmp.append(cls)
        self.kb = kb_tmp
            
    
    # insert cls to kb
    # resolution with kb0 and check is not supperset(or eq) to other
    # assert not negative tautology
    def insert(self, cls):
        # resolutions with kb0
        for truth in self.kb0:
            if truth in cls:
                # tautology
                return 
            elif truth.neg() in self.kb0:
                # this part is never True
                cls.remove(truth) # error handling should be redundunt
        
        # should not be negative tautology
        assert(len(cls) != 0)
        
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
        self.check_sub()
        kb2 = [cls for cls in kb if len(cls) <= 2]
        kbm = []
        n = len(kb2)
        for i in range(n):
            for j in range(i+1, n):
                a = kb2[i]
                b = kb2[i]
                
                kbm.append(get_match(a,b))
        pass
    
    # check pairwise subsumpltion and remove the less restricting ones
    #O(n^2)
    def check_sub(self):
        pass
    


# In[257]:


class LogicAgent:
    b = None # game board in agent's hand
    B = None # solution, not used, will declare in solve as answer and return
    solved = None # cnt of solved cells
    kb = None # current kowledge, include kb0(marked)
    MATCH_INTER_LIMIT = None # for matching
    
    def __init__(self):
        pass
    
    def solve(self, b, MATCH_INTER_LIMIT = MATCH_INTER_LIMIT):
        # initializing solver
        self.b = b # game engine
        self.kb = KB() # KB
        B = [[-1]*b.m for i in range(b.n)]# answer
        kb = self.kb # sugar
        #b = self.b
        
        # get init positions
        start_pos = self.b.get_start()
        # add inital safe position to KB
        for p in start_pos:
            kb.insert(set({VAR(p, 0)}))
        
        # start solving
        while(1):
            # done 
            if(kb.atom() == b.n*b.m):
                # B = [[-1]*b.m for i in range(b.n)]
                # for var in kb0:
                #     B[var.pos[0]][var.pos[1]] = var.T
                return B, (kb.atom(), b.n*n.m)
            # get singleton
            cnt = 0
            while(kb.get_single() == None and cnt < self.MATCH_INTER_LIMIT):
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
            a = kb.get_single()[0] # a singleton cls's only var
            hint = b.q(a.pos)
            assert((hint == -1 and a.T == 1) or (hint != -1 and a.T == 0))
            ## common
            # 1. move to kb0
            # 2. matching of new kb0 to remainning cls
            i = a.pos[0]
            j = a.pos[1]
            kb.trasfer_to_kb0(a)
            B[i][j] = a.T
            if(a.T == 0): # is safe and with hint res
                i = a.pos[0]
                j = a.pos[1]
                undecided = []
                for dx, dy in itertools.product(range(-1,2,1), range(-1,2,1)):
                    nx, ny = i+dx, j+dy
                    if(not (dx==0 and dy==0) and self.inrange(nx, ny)):
                        if(B[nx][ny] == -1):
                            undecided.append((nx, ny))
                m = len(undecided)
                n = hint
                #clause type, C m choose n, now at i, used array
                def generate_C(T, m, n, i, A, ans, cur):
                    if(n > m-i): # required > left
                        return 
                    if(n == 0): # done one case
                        ans.append(cur) # add cur to ans
                        return 
                    if(i == m): # end of arrat
                        return
                    use = deepcopy(cur)
                    nouse = deepcopy(cur)
                    use.add(VAR(A[i], T))
                    generate_C(T, m, n-1, i+1, A, ans, cur)
                    nouse.remove(VAR(A[i], T))
                    generate_C(T, m, n, i+1, A, ans, cur)
                    return
                
                pos = []
                neg = []
                generate_C(0, m, m-n+1, 0, undecided, pos, set()) # T, n, m, i, A
                generate_C(1, m, n+1, 0, undecided, neg, set()) # T, n, m, i, A
                    
                
    
    def do(self, a): # deal with a singleton
        pass
                
             
        
        


# In[258]:


agent = LogicAgent()
agent.solve(b)


# In[281]:


exp = 0
def generate_C(T, m, n, i, A, ans, cur):
    global exp
    exp += 1
    if(n > m-i): # required > left
        return 
    if(n == 0): # done one case
        ans.append(cur) # add cur to ans
        return 
    if(i == m): # end of arrat
        return
    use = deepcopy(cur)
    nouse = deepcopy(cur)
    use.add(VAR(A[i], T))
    generate_C(T, m, n-1, i+1, A, ans, use)
    generate_C(T, m, n, i+1, A, ans, nouse)
    return


# In[288]:


print(len(list(itertools.combinations([(i,i) for i in range(15)], 8))))


# In[284]:


ans = []
exp = 0
generate_C(1, 15, 8, 0, [(i,i) for i in range(15)], ans,  set())
print(exp)
print(ans)


# In[236]:


# test correctness of implementation
v1 = VAR((0, 0), 0)
v2 = VAR((0, 0), 1)
v3 = v2.neg()
s1 = {v1, v3, VAR((0, 0), 0)} # hash ok
s2 = {v1}


# In[204]:


a1 = [s1, s2]
a1.sort()
print(a1)


# In[205]:


x = {"a", "b", "c"}
y = {"c", "b", "a"}
print(x.issubset(y))
print(y.issubset(x))


# In[206]:


a1.remove(s1)
a1


# In[291]:


a = []
a.append(None)
print(a)


# In[ ]:




