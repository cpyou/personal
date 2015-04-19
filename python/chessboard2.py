# -*- coding: utf-8 -*-

up_to_right_up = (1, 2)
up_to_left_up = (-1, 2)
down_to_right_down = (1, -2)
down_to_left_down = (-1, -2)
left_to_left_up = (-2, 1)
left_to_left_down = (-2, -1)
right_to_right_up = (2, 1)
right_to_right_down = (2, -1)

actions = [
    up_to_right_up, up_to_left_up,
    down_to_right_down, down_to_left_down,
    left_to_left_up, left_to_left_down,
    right_to_right_up, right_to_right_down
]


def generate_chessboard():
    res = []
    for x in xrange(1, 9):
        for y in xrange(1, 9):
            res.append((x, y))
    return res


def generate_lower_list(points, new_chessboards):
    res = []
    chessboards = generate_chessboard()
    for point in points:
        for action in actions:
            lower_point = (point[0] + action[0], point[1] + action[1])
            if lower_point in chessboards and lower_point not in res and lower_point not in new_chessboards:
                res.append(lower_point)
    return res


def generate_lists(end_point):
    res = []
    chessboards = generate_chessboard()
    new_chessboards = [end_point]
    lower_list = [end_point]
    while set(new_chessboards) != set(chessboards):
        lower_list = generate_lower_list(lower_list, new_chessboards)
        new_chessboards.extend(lower_list)
        res.append(lower_list)
        print lower_list, '数量', len(lower_list)

    return res

end_point = (3, 3)
steps = generate_lists(end_point)

