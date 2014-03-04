
def is_crosses(a):
    hash_count = sum([s.count('#') for s in a])
    return hash_count % 5 == 0

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
