Counter: int = int()
Counter = 0
Matrix: list = [[int()] * 2] * 2
for Index in range(1, 3):
    for Pindex in range(1, 3):
        Matrix[Index][Pindex] = Index * Pindex