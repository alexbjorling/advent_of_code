import numpy as np

# load the board as array of ascii codes and the moves as a string
board = []
moves = ""
with open("input.txt", "r") as fp:
    one, two = fp.read().split("\n\n")
    for line in one.split():
        line = line.replace("#", "##").replace(".", "..").replace("O", "[]").replace("@", "@.")
        board.append([ord(c) for c in line.strip()])
    for line in two.splitlines():
        moves = moves + line.strip()
board = np.array(board)

# definitions and starting position
pos = tuple(np.array(np.where(board == ord("@"))).T[0])
ways = {
    "v": (1, 0),
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
}
wall = ord("#")
lbox = ord("[")
rbox = ord("]")
free = ord(".")
board[pos] = free

# helper to recursively find the next free square horizontally,
# returned as the number of steps away in that direction
def find_free(pos, dirc):
    new_pos = (pos[0] + dirc[0], pos[1] + dirc[1])
    if board[new_pos] == wall:
        return 0
    elif board[new_pos] in (lbox, rbox):
        rec = find_free(new_pos, dirc)
        if rec == 0:
            return 0
        else:
            return 1 + rec
    elif board[new_pos] == free:
        return 1

# helper to recusively find the indices on subsequent lines to move
# returns [[row 1 indices], [row 2 indices], ...] or None if nothing
# can be shifted.
def boxes_to_shift(inds, row, dirc):
    if wall in board[row + dirc, inds[-1]]:
        return None  # dead end!

    # work out which positions on row (row+dirc) will be pushed by stuff on row (row)
    new_inds = []
    for ind in inds[-1]:
        if board[row, ind] == board[row+dirc, ind] and board[row, ind] in (lbox+dirc, rbox):
            new_inds.append(ind) # boxes directly above each other
        elif board[row + dirc, ind] == rbox:
            new_inds.append(ind)
            new_inds.append(ind - 1)
        elif board[row + dirc, ind] == lbox:
            new_inds.append(ind)
            new_inds.append(ind + 1)

    new_inds = sorted(list(set(new_inds)))

    if new_inds == []:
        # we're done, there's nothing to shift on row (row + dirc)
        return inds
    else:
        updated_inds = boxes_to_shift(inds + [new_inds,], row + dirc, dirc)
        if updated_inds == None:
            return None
        else:
            return updated_inds

# helper to print the current board
def dump(board, pos):
    brd = board.copy()
    brd[pos] = ord("@")
    for row in brd:
        print("".join([chr(c) for c in row]))
    print()

# solve
for i, move in enumerate(moves):

    if move in "<>":

        # number of boxes to push
        way = ways[move]
        boxes = find_free(pos, way) - 1
        if boxes == -1:
            continue

        # shift boxes
        if way == (0, 1):
            board[pos[0], pos[1] + 2: pos[1] + 2 + boxes] = board[pos[0], pos[1] + 1: pos[1] + 1 + boxes]
        elif way == (0, -1):
            board[pos[0], pos[1] - 1 - boxes: pos[1] - 1] = board[pos[0], pos[1] - boxes: pos[1]]

        # rewrite new position
        pos = (pos[0] + way[0], pos[1] + way[1])
        board[pos] = free

    elif move in "v^":
        way = -1 if move == "^" else 1

        # find which boxes on adjacent rows to shift
        shift = boxes_to_shift([[pos[1],]], pos[0], way)
        if shift is None:
            continue

        # loop over the rows and do the shifting
        N = len(shift)
        for i in range(N - 1):
            row = pos[0] + way * (N - i)
            inds = shift[N - i - 1]
            board[row, inds] = board[row - way, inds]
            board[row - way, inds] = free

        # rewrite new position
        pos = (pos[0] + way, pos[1])
        board[pos] = free

where = np.where(board == lbox)
tot = np.sum(where[0] * 100 + where[1])
assert tot == 1471049
