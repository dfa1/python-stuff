"""
Fermat polygonal number theorem

That is, every positive number can be written as the sum of three or
fewer triangular numbers, and as the sum of four or fewer square
numbers, and as the sum of five or fewer pentagonal numbers, and so on.

Sample data for triangular numbers:
1    1
2    1+1
3    3 
4    3+1
5    3+1+1
6    6
7    6+1
8    6+1+1
9    6+3
10   6+3+1
11   10+1
12   6+5+1
13   10+3
14   10+3+1
15   15
16   15+1
17   10+6+1
18   15+3
19   15+3+1
20   10+10
21   15+6 21
22   15+6+1 6+6+10 21+1
23   15+3+3 21+1+1
24   21+3
25   21+3+1
26   21+5
27   21+5+1
28   21+6+1 28
"""

def triangulars():
    """yields 1, 3, 6, 10, 15, ..."""
    n = s = 1
    while True:
        yield s 
        n += 1
        s += n

def len_1(n, base):
    return [[x] for x in base if x == n]

def len_2(n, base):
    return [[x, y] for x in base for y in base if x >= y and x + y == n]

def len_3(n, base):
    return [[x, y, z] for x in base for y in base for z in base if x >= y >= z and x + y + z == n]

def fermat(n):
    import itertools
    less_than_n = lambda x: x <= n
    gen = triangulars()
    base = list(itertools.takewhile(less_than_n, gen))
    return itertools.chain(
        len_1(n, base),
        len_2(n, base),
        len_3(n, base)
        )

for i in range(1, 50):
    print i, "->", ", ".join(map(str, fermat(i)))

# def take(n, generator):
#     """simplified itertools.take_while()"""
#     i = 1
#     while i < n:
#         yield next(generator)
#         i += 1

# def squares():
#     """1, 4, 9, 16, 25"""
#     n  = 1
#     while True:
#         yield n * n
#         n += 1

# def pentagonals():
#     pass
