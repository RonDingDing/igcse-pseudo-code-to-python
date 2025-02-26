
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

def ProcessGrades(FileName):
    FileName = open(FileName, 'write')
    Grade: str = str()
    for Index in range(1, 5):
        if StudentScores[Index] >= PassMark:
            Grade = 'O'
            __case = MOD(Index, 3)
            if __case == 0:
                Grade = 'A'
            elif __case == 1:
                Grade = 'B'
            elif __case == 2:
                Grade = 'C'
            else:
                Grade = 'X'
        else:
            Grade = 'F'
        OutputLine: str = str()
        OutputLine = SUBSTRING(StudentNames[Index], 1, 3) + ': ' + StudentScores[Index] + ' (' + Grade + ')'
        FileName.write({'type': 'Identifier', 'name': 'OutputLine'})
    FileName.close()