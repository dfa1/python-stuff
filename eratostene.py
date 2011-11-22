from functools import reduce

def eratostene(n):
    def multiples(i):  
        return set(range(i + i, n + 1, i))
    return reduce(set.difference, map(multiples, range(1, n)))

print(sorted(eratostene(1000)))

