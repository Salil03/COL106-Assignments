import random
import math

# To generate random prime less than N


def randPrime(N):
    primes = []
    for q in range(2, N+1):
        if (isPrime(q)):
            primes.append(q)
    return primes[random.randint(0, len(primes)-1)]

# To check if a number is prime


def isPrime(q):
    if (q > 1):
        for i in range(2, int(math.sqrt(q)) + 1):
            if (q % i == 0):
                return False
        return True
    else:
        return False

# pattern matching


def randPatternMatch(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatch(q, p, x)

# pattern matching with wildcard


def randPatternMatchWildcard(eps, p, x):
    N = findN(eps, len(p))
    q = randPrime(N)
    return modPatternMatchWildcard(q, p, x)

# return appropriate N that satisfies the error bounds


def findN(eps, m):
    '''We want to pick N such that N/ln(N) >= 2*m*log(26)/eps = k(say). This will ensure (number of primes which divide f(A)-f(B))/(total number of primes) <= eps

    It can be proved that if we have m >=1 and eps <1 then choosing N = 2*k*log(2*k) will satisfy the above condition.
    '''
    k = math.ceil(2*m * math.log2(26)/eps)
    return int(math.ceil(2*k*math.log2(2*k)))


# Return sorted list of starting indices where p matches x
def modPatternMatch(q, p, x):
    pattern = 0  # holds the number for pattern
    roll = 0  # holds the number for m digits of x
    power = 1
    for i in range(len(p)):
        pattern = (pattern * 26 + ord(p[i]) - 65) % q
        roll = (roll * 26 + ord(x[i]) - 65) % q
        power = (power * 26) % q
    L = []
    for i in range(len(x) - len(p) + 1):
        if pattern == roll:
            L.append(i)
        if i < len(x) - len(p):
            # remove the first digit and add next digit
            roll = (roll * 26) % q
            roll = (roll - power * (ord(x[i]) - 65)) % q
            roll = (roll + ord(x[i + len(p)]) - 65) % q
    return L


# Return sorted list of starting indices where p matches x
def modPatternMatchWildcard(q, p, x):
    pattern = 0
    wildcard = 0  # position of wildcard
    roll = 0
    power = 1
    for i in range(len(p)):
        power = (power * 26) % q
        if p[i] == '?':
            pattern = (pattern * 26) % q
            wildcard = i
            roll = (roll*26) % q
        else:
            pattern = (pattern * 26 + ord(p[i]) - 65) % q
            roll = (roll * 26 + ord(x[i]) - 65) % q

    power_wild = 1
    for i in range(len(p) - wildcard-1):
        power_wild = (power_wild*26) % q
    L = []
    for i in range(len(x) - len(p)+1):
        if pattern == roll:
            L.append(i)
        if i+len(p) < len(x):
            roll = (roll + power_wild*(ord(x[i + wildcard]) - 65)) % q  # add digit at wildcard
            # remove first digit and add next digit
            roll = (roll * 26) % q
            roll = (roll - power * (ord(x[i]) - 65)) % q
            roll = (roll + ord(x[i + len(p)]) - 65) % q
            roll = (roll - power_wild*(ord(x[i+wildcard+1]) - 65)) % q  # remove digit at wildcard
    return L
