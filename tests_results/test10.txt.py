
def MOD(a, b):
    return a % b


def SUBSTRING(s, start, length):
    return s[start:start+length]

def ProcessGrades():
    with open("1.txt", 'w') as __fp:
        pass
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
        with open("1.txt", 'w') as __fp:
            __fp.write(OutputLine)
    