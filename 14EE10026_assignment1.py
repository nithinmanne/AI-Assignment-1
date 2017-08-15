from copy import deepcopy as copy

class State(list):
    '''Class for holding the state as a list of lists of NxN'''

    def __init__(self, state):
        list = copy(state)
        self.N = len(state)

    def __str__(self):
        state_str = ""
        for i in self.state:
            for j in i:
                    state_str += j
        return state_str

'''Decorator for the Heuristic Function'''
def heuristic_function(heuristic):
    def wrapper(goal):
        def h_fn(state):
            return heuristic(state, goal)
        return h_fn
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
                if found:
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
