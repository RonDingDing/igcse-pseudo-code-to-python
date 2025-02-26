
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

Size: int = int()
Size = 10
Matrix: list = [[[int()] * ((2 + Size + 2 * 2) - (2 + Size + 2 * 2) + 1)] * ((Size + 2 * 2) - (1) + 1)]
if Matrix[1][2] > 100:
    print('Large number')
else:
    print('Normal')