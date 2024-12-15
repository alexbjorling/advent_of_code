import numpy as np

# load the board as array of ascii codes and the moves as a string
board = []
moves = ""
with open("input.txt", "r") as fp:
    one, two = fp.read().split("\n\n")
    for line in one.split():
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
box = ord("O")
free = ord(".")
board[pos] = free

# helper to recursively find the next free square in a direction,
# returned as the number of steps away in that direction.
def find_free(pos, dirc):
    new_pos = (pos[0] + dirc[0], pos[1] + dirc[1])
    if board[new_pos] == wall:
        return 0
    elif board[new_pos] == box:
        rec = find_free(new_pos, dirc)
        if rec == 0:
            return 0
        else:
            return 1 + rec
    elif board[new_pos] == free:
        return 1

# helper to print the current board
def dump(board, pos):
    brd = board.copy()
    brd[pos] = ord("@")
    for row in brd:
        print("".join([chr(c) for c in row]))
    print()

# solve
for i, move in enumerate(moves):

    # number of boxes to push
    way = ways[move]
    boxes = find_free(pos, way) - 1
    if boxes == -1:
        continue

    # shift boxes
    if way == (1, 0):
        board[pos[0] + 2: pos[0] + 2 + boxes, pos[1]] = board[pos[0] + 1: pos[0] + 1 + boxes, pos[1]]
    elif way == (-1, 0):
        board[pos[0] - 1 - boxes: pos[0] - 1, pos[1]] = board[pos[0] - boxes: pos[0], pos[1]]
    if way == (0, 1):
        board[pos[0], pos[1] + 2: pos[1] + 2 + boxes] = board[pos[0], pos[1] + 1: pos[1] + 1 + boxes]
    elif way == (0, -1):
        board[pos[0], pos[1] - 1 - boxes: pos[1] - 1] = board[pos[0], pos[1] - boxes: pos[1]]

    # rewrite new position
    pos = (pos[0] + way[0], pos[1] + way[1])
    board[pos] = free

where = np.where(board == box)
tot = np.sum(where[0] * 100 + where[1])
assert tot == 1465523
