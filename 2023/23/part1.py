import sys
sys.setrecursionlimit(10000)

# read the board
board = []
with open('input.txt', 'r') as fp:
    for line in fp:
        board.append(line.strip())

pos = (0, board[0].index('.'))
goal = (len(board)-1, board[-1].index('.'))


def search(history):
    pos = history[-1]
    square = board[pos[0]][pos[1]]

    if pos == goal:
        return history

    # no options if we're on a slope
    slope_map = {'>': (0, 1), 'v': (1, 0), '<': (0, -1), '^': (-1, 0)}
    if square in '>v<^':
        new = (pos[0] + slope_map[square][0], pos[1] + slope_map[square][1])
        if new in history:
            # abort
            return [-1,]  # should catch this somewhere, but luckily works anyway (no aborted trajectories are the longest)
        history.append(new)
        return search(history)

    # check for options
    options = []
    for vel in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        new = (pos[0] + vel[0], pos[1] + vel[1])
        if new in history:
            continue
        new_square = board[new[0]][new[1]]
        if new_square != '#':
            options.append(new)

    # try them all and return the longest
    paths = [search(history + [opt,]) for opt in options]
    lengths = [len(p) for p in paths]
    ind = lengths.index(max(lengths))
    return paths[ind]

def render(history, board):
    board = board.copy()
    for p in history:
        i, j = p
        board[i] = board[i][:j] + 'O' + board[i][j+1:]
    board = '\n'.join(board)
    return board

p = search([pos,])
assert len(p) - 1 == 2042  # steps, so positions-1