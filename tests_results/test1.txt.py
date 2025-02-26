
import random
def DIV(a, b):
    return a // b

def MOD(a, b):
    return a % b

def LENGTH(s):
    return len(s)

def LCASE(s):
    return s.lower()

def UCASE(s):
    return s.upper()

def SUBSTRING(s, start, length):
    return s[start:start+length]

def ROUND(n, d):
    return round(n, d)

def RANDOM():
    return random.random()

####################

Counter: int = int()
Counter = 0
Matrix: list = [[[int()] * 3] * 3]
for Index in range(1, 3):
    for Pindex in range(1, 3):
        Matrix[Index][Pindex] = Index * Pindex