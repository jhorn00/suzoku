def validate(board):
    # first thing we need to do is validate the board
    # validate rows:
    for i in board:
        dup_set = set()
        compare = []
        for j in i:
            if j != 0:
                dup_set.add(j)
                compare.append(j)
        if len(dup_set) != len(compare):
            return "invalid board"
    # validate columns:
    for x in range(0, len(board)):
        dup_set = set()
        compare = []
        for i in board:
            if i[x] != 0:
                dup_set.add(i[x])
                compare.append(i[x])
        if len(dup_set) != len(compare):
            return "invalid board"
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
            return "invalid board"
    return "valid board"
