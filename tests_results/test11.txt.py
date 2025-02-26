
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

def CalculateAverage():
    Total: float = float()
    Total = 0.0
    while Total < 500.0:
        for Index in range(1, 5):
            Total = Total + StudentScores[Index]
        Total = Total + RANDOM() * 10
    return Total / 5 * DIV(25, 5)
print('Average score: ', CalculateAverage())