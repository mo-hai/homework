import numpy as np
import matplotlib.pyplot as plt


def cubicPolynomial(X, Y):
    if len(X) != len(Y):
        print("error")
        exit(0)
    n = len(X)
    mat1 = np.zeros([4, 4], dtype=np.float)
    mat2 = np.zeros(4, dtype=np.float)
    for row in range(4):
        for col in range(4):
            sum_x = 0
            power = row + col
            for i in range(n):
                sum_x += np.power(X[i], power)
            mat1[row][col] = sum_x

    for row in range(4):
        sum_y = 0
        power = row
        for i in range(n):
            sum_y += np.power(X[i], power) * Y[i]
        mat2[row] = sum_y
    result = np.linalg.solve(mat1, mat2)
    return result


def quarticPolynomial(X, Y):
    if len(X) != len(Y):
        print("error")
        exit(0)
    n = len(X)
    mat1 = np.zeros([5, 5], dtype=np.float)
    mat2 = np.zeros(5, dtype=np.float)
    for row in range(5):
        for col in range(5):
            sum_x = 0
            power = row + col
            for i in range(n):
                sum_x += np.power(X[i], power)
            mat1[row][col] = sum_x

    for row in range(5):
        sum_y = 0
        power = row
        for i in range(n):
            sum_y += np.power(X[i], power) * Y[i]
        mat2[row] = sum_y
    result = np.linalg.solve(mat1, mat2)
    return result


def getValue(x, parameter):
    n = len(parameter)
    result = 0
    for i in range(n):
        result += parameter[i] * np.power(x, i)
    return result

if __name__ == '__main__':
    X = [0.0, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0]
    Y = [1.0, 0.41, 0.50, 0.61, 0.91, 2.02, 2.46]
    parameter1 = cubicPolynomial(X, Y)
    parameter2 = quarticPolynomial(X, Y)
    x = np.zeros(10000, dtype=np.float)
    y1 = np.zeros(10000, dtype=np.float)

    y2 = np.zeros(10000, dtype=np.float)
    for i in range(10000):
        x[i] = i / 10000
        y1[i] = getValue(x[i], parameter1)
        y2[i] = getValue(x[i], parameter2)

    plt.figure()
    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot(x, y1, c='r', label='cubicPolynomial')
    plt.plot(x, y2, c='b', label='quarticPolynomial')
    plt.legend()
    plt.show()
