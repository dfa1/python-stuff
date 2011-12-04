"""
x^2 + x + 41 generates a list of primes where 0 < x < q-2
q must be a prime
"""

def euler(q):
    for x in range(0, q - 2):
        yield x*x + x + q

for p in euler(41):
    print p
