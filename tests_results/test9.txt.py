
def UCASE(s):
    return s.upper()


def ROUND(n, d):
    return round(n, d)

def InputStudentData():
    TempName: str = str()
    TempScore: float = float()
    print('Enter student data:')
    for Index in range(1, 5):
        print('Student ', Index, ' name:')
        TempName = str(input())
        StudentNames[Index] = UCASE(TempName)
        while True:
            print('Score (0-100):')
            TempScore = float(input())
            if TempScore >= 0 and TempScore <= 100:
                break
        StudentScores[Index] = ROUND(TempScore, 1)