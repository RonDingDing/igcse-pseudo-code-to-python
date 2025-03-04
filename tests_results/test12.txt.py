
def DIV(a, b):
    return a / b

def ProcessGrades(a: int):
    return a / (5 * DIV(25, 5))
def Plus(a: int, b: int):
    return a + b
print('Average score: ', ProcessGrades())
print('Average score: ', Plus(4, 8))