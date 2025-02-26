
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

X = 0
if X > 5:
    print('X is greater than 5')
else:
    print('X is 5 or less')