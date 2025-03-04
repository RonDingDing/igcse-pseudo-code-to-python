Size: int = int()
Size = 10
Matrix: list = [[int()] * 2] * ((Size + 2 * 2) - (1))
if Matrix[1][2] > 100:
    print('Large number')
else:
    print('Normal')