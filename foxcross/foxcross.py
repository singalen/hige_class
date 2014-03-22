# -*- coding: utf-8 -*-


def _is_cross_at(a, x, y):
    if x <= 0 or x >= len(a)-1:
        raise IndexError(x)
    if y <= 0 or y >= len(a[0])-1:
        raise IndexError(y)

    return a[x][y] == '#' and a[x][y-1] == '#' and a[x][y+1] == '#' and a[x-1][y] == '#' and a[x+1][y] == '#'


def is_crosses(a):
    n = len(a)

    # Предусматриваем случай, когда в a[] сидят str-ы.
    for x in range(0, n):
        if isinstance(a[x], str):
            a[x] = list(a[x])

    for x in range(1, n-1):
        for y in range(1, n-1):
            if _is_cross_at(a, x, y):
                a[x][y] = '!'
                a[x][y-1] = '!'
                a[x][y+1] = '!'
                a[x-1][y] = '!'
                a[x+1][y] = '!'

    hash_count = sum([s.count('#') for s in a])

    return hash_count == 0

if __name__ == '__main__':
    n = int(input())
    a = []
    for i in range(0, n):
        line = input()
        a.append(line)

    if is_crosses(a):
        print('TRUE')
    else:
        print('FALSE')
