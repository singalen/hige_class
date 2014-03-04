
def is_crosses(a):
    hash_count = sum([s.count('#') for s in a])
    return hash_count % 5 == 0