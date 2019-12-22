import numpy as np

res = -1.4260247563462665


def f(x):
    return np.power(10 / x, 2) * np.sin(10 / x)


def gaussL():
    XX = [-0.9061798459, -0.5384693101, 0, 0.5384693101, 0.9061798459]
    AA = [0.2369268851, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268851]
    x = []
    h = (3 - 1) / 10
    for i in range(11):
        x.append(1 + i * h)
    result_t = []
    for i in range(10):
        a = x[i]
        b = x[i + 1]
        sum_t = 0
        for j in range(5):
            tt = (b - a) / 2 * XX[j] + (a + b) / 2
            sum_t += AA[j] * np.power(10 / tt, 2) * np.sin(10 / tt)
        result_t.append((b - a) / 2 * sum_t)

    result = sum(result_t)
    return result


def T(n):
    a = 1
    b = 3
    h = (b - a) / n
    sum_t = 0
    for i in range(1, n, 1):
        x = a + h * i
        temp = 2 * f(x)
        sum_t += temp
    return (sum_t + f(1) + f(3)) * h / 2


def romgberg():
    print("romberg")
    size = 10
    temp = np.zeros([size, size], dtype=np.float)
    for j in range(size):
        print()
        for k in range(j + 1):
            if k == 0:
                temp[j][k] = T(np.power(2, j))
            else:
                temp[j][k] = (np.power(4, k) * temp[j][k - 1] - temp[j - 1][k - 1]) / (np.power(4, k) - 1)
            print("%.6f" % temp[j][k], end=" ")
            if np.abs(temp[j][k] - res) < 1.0 / np.power(10, 4):
                print()
                return temp[j][k]


if __name__ == '__main__':
    result = gaussL()
    print(result)
    result = romgberg()
    print(result)
