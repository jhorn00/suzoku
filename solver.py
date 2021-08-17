# This function validates the board and returns the result of the analysis.
# Efficiency may be revised later, I am aware there are optimizations to be made.
# Currently it should support the validation of any sudoku board size, assuming only ints are used.
def validate(board):
    # validate rows:
    for i in board:
        dup_set = set()
        compare = []
        for j in i:
            if j != 0:
                dup_set.add(j)
                compare.append(j)
        if len(dup_set) != len(compare):
            return False
    # validate columns:
    for x in range(0, len(board)):
        dup_set = set()
        compare = []
        for i in board:
            if i[x] != 0:
                dup_set.add(i[x])
                compare.append(i[x])
        if len(dup_set) != len(compare):
            return False
    # validate grids:
    # calculate how many grids there are
    num_grids = int((len(board) / 3) * (len(board) / 3))
    # create a list of grids so we can compare the same way as before
    grid_list = [[] for i in range(num_grids)]
    # for each grid
    offset = 0
    for i in board:
        for x in range(0, len(board)):
            grid_list[int(int(x) / 3) + int(offset / 3) * 3].append(i[x])
        offset = offset + 1
    for i in grid_list:
        dup_set = set()
        compare = []
        for j in i:
            if j != 0:
                dup_set.add(j)
                compare.append(j)
        if len(dup_set) != len(compare):
            return False
    return True


# Possible error for larger boards here, but we will not allow for those.
def check(board, row, col, num):
    for x in range(0, len(board)):
        if board[row][x] == num:
            return False
    for x in range(0, len(board)):
        if board[x][col] == num:
            return False
    startY = row - row % 3
    startX = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + startY][j + startX] == num:
                return False
    return True


# Solves a valid board using backtracking, returns true when finished.
# I opted to use the detected board dimensions rather than hard-code it
# because I *might* add larger board solving later. It appears there is no standard
# implementation or rules for 16x16 and larger boards. The problem this causes for me
# is implementing solutions for integer and character puzzle types. I feel it provides
# negligible educational benefit to go through the trouble of adding such a feature.
def solve(board, row, col):
    # if we reach the end return
    if row == len(board) - 1 and col == len(board):
        print("finishes")
        return True
    # move to next row when necessary
    if col == len(board):
        row += 1
        col = 0
    # skip non-empty cells
    if board[row][col] != 0:
        return solve(board, row, col + 1)
    for num in range(1, len(board) + 1):
        if check(board, row, col, num):
            board[row][col] = num
            if solve(board, row, col + 1):
                return True
        board[row][col] = 0
    return False
