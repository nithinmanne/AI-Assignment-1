
class State(list):
    '''Class for holding the state as a list of lists of NxN'''

    def __init__(self, *state):
        list.__init__(self, *state)
        self.N = len(*state)

    def __str__(self):
        state_str = ""
        for i in self:
            for j in i:
                    state_str += str(j)
        return state_str

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


hasattr(zero, 'heuristic_function') and getattr(zero, 'heuristic_function')
