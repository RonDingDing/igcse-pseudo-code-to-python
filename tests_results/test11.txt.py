
import random

def RANDOM():
    return random.random()

def DIV(a, b):
    return a / b

def CalculateAverage():
    Total: float = float()
    Total = 0.0
    while Total < 500.0:
        for Index in range(1, 5):
            Total = Total + StudentScores[Index]
        Total = Total + RANDOM() * 10
    return Total / (5 * DIV(25, 5))
print('Average score: ', CalculateAverage())