import math
import numpy as np
from collections import defaultdict


def get_squares_table(p: int) -> defaultdict:
    if p == 1:
        d = defaultdict(list)
        d[0].append(0)
        return d
    elif p == 2:
        d = defaultdict(list)
        d[0].append(0)
        d[1].append(1)
        return d
    else:
        table = np.arange(p // 2 + 1)
        table = table * table
        table = list(table % p)
        table = table + table[::-1][:-1]
        reversed_table = defaultdict(list)
        x = np.arange(p)
        for elem, v in zip(table, x):
            reversed_table[elem].append(v)
        return reversed_table


def get_points(y_2: list, p: int) -> list:
    squares_to_roots = get_squares_table(p)
    possible_y_2 = list(set(squares_to_roots.keys()) & set(y_2))
    x = np.arange(p)
    x_to_y_2 = dict(zip(x, y_2))
    x_to_y = defaultdict(list)
    points = []
    for k, v in x_to_y_2.items():
        if v in possible_y_2:
            for v_i in squares_to_roots[v]:
                x_to_y[k].append(v_i)
                points.append((k, v_i))
    return points


if __name__ == '__main__':
    print(get_squares_table(13))
