field = [
    '#############################',
    '#   S #            ##       #',
    '#     #            ##       #',
    '#     #            ##       #',
    '#     #            ##       #',
    '#     # ########   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#     #       ##   ##  ##   #',
    '#  #######    ##   ##  ## X #',
    '#             ##       ##   #',
    '#############################',
]

def find_char(field, char):
    start_row = ([char in row for row in field]).index(True)
    start_column = field[start_row].index(char)
    return (start_row, start_column)

start = find_char(field, 'S')
target = find_char(field, 'X')
