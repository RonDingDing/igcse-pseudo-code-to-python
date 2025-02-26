
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

def ProcessGrades(a):
    return a / 5 * DIV(25, 5)
def Plus(a, b):
    return a + b
print('Average score: ', ProcessGrades())
print('Average score: ', Plus(4, 8))