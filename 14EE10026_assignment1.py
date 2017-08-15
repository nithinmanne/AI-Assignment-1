import heapq
from copy import deepcopy as copy

class State(list):
    '''Class for holding the state as a list of lists of NxN'''

    def __init__(self, *state, blank = None):
        list.__init__(self, *state)
        self.N = len(*state)
        self.level = 0
        if(blank == None):
            self.blank = self.get_blank()

    def __str__(self):
        state_str = ""
        for i in self:
            for j in i:
                    state_str += str(j)
        return state_str

    def get_blank(self):
        for i in range(self.N):
            for j in range(self.N):
                if(self[i][j]==0): return (i, j)

    def push_blank_up(self):
        if self.blank[0]==0:
            return None
        nstate = State(copy(self), blank = 1)
        nstate.level = self.level + 1
        nstate[self.blank[0]][self.blank[1]] = self[self.blank[0]-1][self.blank[1]]
        nstate.blank = (self.blank[0] - 1, self.blank[1])
        nstate[nstate.blank[0]][nstate.blank[1]] = 0
        return nstate

    def push_blank_down(self):
        if self.blank[0]==self.N-1:
            return None
        nstate = State(copy(self), blank = 1)
        nstate.level = self.level + 1
        nstate[self.blank[0]][self.blank[1]] = self[self.blank[0]+1][self.blank[1]]
        nstate.blank = (self.blank[0] + 1, self.blank[1])
        nstate[nstate.blank[0]][nstate.blank[1]] = 0
        return nstate

    def push_blank_left(self):
        if self.blank[1]==0:
            return None
        nstate = State(copy(self), blank = 1)
        nstate.level = self.level + 1
        nstate[self.blank[0]][self.blank[1]] = self[self.blank[0]][self.blank[1]-1]
        nstate.blank = (self.blank[0], self.blank[1] - 1)
        nstate[nstate.blank[0]][nstate.blank[1]] = 0
        return nstate

    def push_blank_right(self):
        if self.blank[1]==self.N-1:
            return None
        nstate = State(copy(self), blank = 1)
        nstate.level = self.level + 1
        nstate[self.blank[0]][self.blank[1]] = self[self.blank[0]][self.blank[1]+1]
        nstate.blank = (self.blank[0], self.blank[1] + 1)
        nstate[nstate.blank[0]][nstate.blank[1]] = 0
        return nstate


'''Decorator for the Heuristic Function'''

def heuristic_function(heuristic):
    def wrapper(goal):
        def h_fn(state):
            return heuristic(state, goal)
        return h_fn
    setattr(wrapper, 'heuristic_function', True)
    return wrapper

@heuristic_function
def zero(state, goal):
    return 0

@heuristic_function
def manhattan(state, goal):
    count = 0
    for i in range(state.N):
        for j in range(state.N):
            found = False
            for k in range(state.N):
                for l in range(state.N):
                    if(state[i][j]==goal[k][l]):
                        found = True
                        count += abs(i-k) + abs(j-l)
                        break
                if found:
                    break
    return count

@heuristic_function
def misplaced_tiles(state, goal):
    count = 0
    for i in range(state.N):
        for j in range(state.N):
            if(state[i][j]!=goal[i][j]):
                count += 1
    return count

@heuristic_function
def linear_conflict(state, goal):
    count = manhattan(goal)(state)
    for i in range(state.N):
        for j in range(state.N):
            if state[i][j]==0: continue
            found = False
            for k in range(state.N):
                for l in range(state.N):
                    if state[i][j]==goal[k][l]:
                        if(i==k):
                            for m in state[i][:j]:
                                if m in goal[k][l:]:
                                    count += 2
                            for m in state[i][j:]:
                                if m in goal[k][:l]:
                                    count += 2
                        if(j==l):
                            nstate = zip(*state)
                            ngoal = zip(*goal)
                            for m in nstate[i][:j]:
                                if m in ngoal[k][l:]:
                                    count += 2
                            for m in nstate[i][j:]:
                                if m in ngoal[k][:l]:
                                    count += 2
                        found = True
                        break
                if found:
                    break


def astar(start, goal, heuristic = None, f_n = 'g(state) + h(state)'):
    if heuristic == None:
        heuristic = zero
    if not(hasattr(heuristic, 'heuristic_function') and getattr(heuristic, 'heuristic_function')):
        raise ValueError("Given function needs to be decorated with @heuristic_function")
    h = heuristic(goal)
    def g(state):
        return state.level
    heap = []
    nodes = 0
    visited = set()
    state = start
    visited.add(str(state))
    heapq.heappush(heap, (eval(f_n), state))
    while(len(heap)>0):
        f_nv, ostate = heapq.heappop(heap)
        nodes += 1
        if(str(ostate) == str(goal)):
            return ostate, nodes
        state = ostate.push_blank_up()
        if (state!=None and str(state) not in visited):
            visited.add(str(state))
            heapq.heappush(heap, (eval(f_n), state))
        state = ostate.push_blank_down()
        if (state!=None and str(state) not in visited):
            visited.add(str(state))
            heapq.heappush(heap, (eval(f_n), state))
        state = ostate.push_blank_left()
        if (state!=None and str(state) not in visited):
            visited.add(str(state))
            heapq.heappush(heap, (eval(f_n), state))
        state = ostate.push_blank_right()
        if (state!=None and str(state) not in visited):
            visited.add(str(state))
            heapq.heappush(heap, (eval(f_n), state))


goal = State([[1,2,3],[4,5,6],[7,8,0]])
start = State([[1,2,3],[4,5,6],[7,0,8]])
