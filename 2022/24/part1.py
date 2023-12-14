import re
import numpy as np
import copy

MAX_STEPS = 30


class State:
    def __init__(self, pos, blizzards, board):
        self.v_pos, self.h_pos = pos
        self.blizzards = blizzards
        self.board = board

    def validate(self):
        # wall collision
        on_rim = ((self.v_pos == 0) or (self.v_pos == self.board.height - 1) or (self.h_pos == 0) or (self.h_pos == self.board.width - 1))
        at_start = (self.v_pos, self.h_pos) == board.start_pos
        at_finish = (self.v_pos, self.h_pos) == board.finish_pos
        if on_rim and not (at_start or at_finish):
            return False

        # blizzard collision
        for b in self.blizzards:
            if (self.v_pos == b.v_pos) and (self.h_pos == b.h_pos):
                return False

        return True

    def possible_next_states(self, strategy='all'):
        # propagate the blizzards
        blizzards = copy.deepcopy(self.blizzards)
        for b in blizzards:
            b.step_forward()

        # find possible futures
        opts = {'blizzards':blizzards, 'board':self.board}
        all_states = {
            'v': State(pos=(self.v_pos+1, self.h_pos), **opts),
            '>': State(pos=(self.v_pos, self.h_pos+1), **opts),
            '^': State(pos=(self.v_pos-1, self.h_pos), **opts),
            '<': State(pos=(self.v_pos, self.h_pos-1), **opts),
            'o': State(pos=(self.v_pos, self.h_pos), **opts),
        }

        # remove invalid states
        valid_states = {}
        for k, v in all_states.items():
            if v.validate():
                valid_states[k] = v

        # choose which to return
        if strategy == 'all':
            # allow all moves
            ret = list(valid_states.values())
        elif strategy == 'strict':
            # only allow moves v and >
            ret = [valid_states[k] for k in valid_states.keys() if k in '>v']
        elif strategy == 'conservative':
            # only allow moves ^ or < when necessary
            poss = valid_states.keys()
            if 'v' in poss or '>' in poss or 'o' in poss:
                ret = [valid_states[k] for k in valid_states.keys() if k in '>vo']
            else:
                ret = list(valid_states.values())
        elif strategy == 'more_conservative':
            # only allow moves ^ or < or o when necessary
            poss = valid_states.keys()
            if 'v' in poss or '>' in poss:
                ret = [valid_states[k] for k in valid_states.keys() if k in '>v']
            else:
                ret = list(valid_states.values())
        else:
            raise ValueError('invalid strategy "%s"' % strategy)

        return ret


class Blizzard:
    def __init__(self, pos, direction, board):
        self.v_pos, self.h_pos = pos
        self.direction = direction
        self.board = board

    def step_forward(self):
        # step according to direction and apply periodic boundaries
        if self.direction == '>':
            self.h_pos += 1
            if self.h_pos == self.board.width - 1:
                self.h_pos = 1
        elif self.direction == 'v':
            self.v_pos += 1
            if self.v_pos == self.board.height - 1:
                self.v_pos = 1
        elif self.direction == '<':
            self.h_pos -= 1
            if self.h_pos == 0:
                self.h_pos = self.board.width - 2
        elif self.direction == '^':
            self.v_pos -= 1
            if self.h_pos == self.board.width - 1:
                self.h_pos = 1


class Board():
    def __init__(self, filename):
        with open(filename, 'r') as fp:
            data = fp.read().split('\n')
        if not len(data[-1]):
            data.pop()

        self.width = len(data[0])
        self.height = len(data)

        # find start and finish positions
        self.start_pos = (0, re.search('\.', data[0]).span()[0])
        self.finish_pos = (len(data)-1, re.search('\.', data[-1]).span()[0])

        # save text input
        self.text = data


# board and initial state
board = Board('input.txt')
blizzards = []
for i, line in enumerate(board.text):
    for hit in re.finditer('([v|\<|\^|\>])', line):
        blizzards.append(Blizzard((i, hit.span()[0]), hit.group(), board))
initial = State(board.start_pos, blizzards, board)


# recursive search by going deep first - solves the example but not the real problem
density_of_states = np.zeros(MAX_STEPS + 1, dtype=int)
def eval_state(state, steps_taken):
    density_of_states[steps_taken] += 1
    print(density_of_states)
    if (state.v_pos, state.h_pos) == board.finish_pos:
        return steps_taken
    if steps_taken >= MAX_STEPS:
        return None
    solutions = []
    for st in state.possible_next_states(strategy='conservative'):
        solutions.append(eval_state(st, steps_taken + 1))
    working_solutions = [i for i in solutions if i is not None]
    return min(working_solutions) if working_solutions else None
## r = eval_state(initial, steps_taken=0)


# recurseve search by going wide first, evaluating all the states that
# are reachable after a given number of steps, then going deeper.
def eval_level(state_list, steps_taken):
    print('level %d, list of %d states' % (steps_taken, len(state_list)))

    # no solution with this strategy?
    if not len(state_list):
        return None

    # generate next level of states
    next_level = []
    for st in state_list:
        next_level += st.possible_next_states(strategy='conservative')

    # are any of them winners?
    for st in next_level:
        if (st.v_pos, st.h_pos) == board.finish_pos:
            return steps_taken

    # otherwise go one level deeper    
    eval_level(next_level, steps_taken+1)
r = eval_level([initial], steps_taken=0)
