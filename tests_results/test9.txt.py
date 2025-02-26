
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

def InputStudentData():
    TempName: str = str()
    TempScore: float = float()
    print('Enter student data:')
    for Index in range(1, 5):
        print('Student ', Index, ' name:')
        TempName = input()
        StudentNames[Index] = UCASE(TempName)
        while True:
            print('Score (0-100):')
            TempScore = input()
            if TempScore >= 0 and TempScore <= 100:
                break
        StudentScores[Index] = ROUND(TempScore, 1)