import numpy as np

def lpm(src):
    src = np.array(src)
    n = np.size(src, 0)
    L = np.zeros((n, n, n), dtype=np.int)
    L[0] = src

    for i in range(1, n):
        for row in range(n):
            for col in range(n):
                result = -1
                for j in range(n):
                    if L[0][row][j] == -1:
                        continue
                    if L[i - 1][j][col] == -1:
                        continue
                    temp = L[0][row][j] + L[i - 1][j][col]
                    result = np.max([result, temp])
                L[i][row][col] = result

    for i in range(n):
        print(L[i], end='\n \n')

    result = 0.0
    for i in range(1, n):
        for j in range(n):
            result = np.max([result, L[i][j][j] / (i + 1)])
    print(result)



if __name__ == '__main__':
    source1 = [[-1, 0, -1],
              [7, -1, 3],
              [3, -1, -1]]
    print("source1")
    lpm(source1)
    source2 = [[4, 4, 4, -1, 4, -1],
               [-1, -1, -1, -1, -1, -1],
               [-1, -1, -1, 0, -1, -1],
               [4, 4, 4, -1, 4, -1],
               [-1, -1, -1, -1, -1, 0],
               [-1, -1, -1, -1, -1, -1]]
    source2 = np.array(source2)
    print("source2")
    lpm(source2)
