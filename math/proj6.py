import numpy as np
import matplotlib.pyplot as plt


def L5(value, x):
    l0 = (x - value[1][0])*(x - value[2][0])*(x - value[3][0])*(x - value[4][0])*(x - value[5][0]) / \
         ((value[0][0] - value[1][0])*(value[0][0] - value[2][0])*(value[0][0] - value[3][0])*(value[0][0] - value[4][0])*(value[0][0] - value[5][0]))

    l1 = (x - value[0][0])*(x - value[2][0])*(x - value[3][0])*(x - value[4][0])*(x - value[5][0]) / \
         ((value[1][0] - value[0][0])*(value[1][0] - value[2][0])*(value[1][0] - value[3][0])*(value[1][0] - value[4][0])*(value[1][0] - value[5][0]))

    l2 = (x - value[0][0])*(x - value[1][0])*(x - value[3][0])*(x - value[4][0])*(x - value[5][0]) / \
         ((value[2][0] - value[0][0])*(value[2][0] - value[1][0])*(value[2][0] - value[3][0])*(value[2][0] - value[4][0])*(value[2][0] - value[5][0]))

    l3 = (x - value[1][0])*(x - value[2][0])*(x - value[0][0])*(x - value[4][0])*(x - value[5][0]) / \
         ((value[3][0] - value[1][0])*(value[3][0] - value[2][0])*(value[3][0] - value[0][0])*(value[3][0] - value[4][0])*(value[3][0] - value[5][0]))

    l4 = (x - value[1][0])*(x - value[2][0])*(x - value[3][0])*(x - value[0][0])*(x - value[5][0]) / \
         ((value[4][0] - value[1][0])*(value[4][0] - value[2][0])*(value[4][0] - value[3][0])*(value[4][0] - value[0][0])*(value[4][0] - value[5][0]))

    l5 = (x - value[1][0])*(x - value[2][0])*(x - value[3][0])*(x - value[4][0])*(x - value[5][0]) / \
         ((value[5][0] - value[1][0])*(value[5][0] - value[2][0])*(value[5][0] - value[3][0])*(value[5][0] - value[4][0])*(value[5][0] - value[0][0]))

    result = l0 * value[0][1] + l1 * value[1][1] + l2 * value[2][1] + l3 * value[3][1] + l4 * value[4][1] + l5 * value[5][1]

    return result



def s(value, x):
    x0 = value[0][0]
    y0 = value[0][1]

    x1 = value[2][0]
    y1 = value[2][1]

    x2 = value[4][0]
    y2 = value[4][1]

    x3 = value[5][0]
    y3 = value[5][1]

    h0 = 1
    h1 = 6
    h2 = 2

    M0 = 0
    M1 = -0.1749409
    M2 = 0.06097321
    M3 = 0
    reuslt = 0
    if x >= 0 and x < 1:
        reuslt = M0*(x1 - x)**3 / (6 * h0) + M1 * (x - x0)**3 / (6 * h0) + (y0 - M0 * h0**2 / 6)*(x1 - x) / h0 +\
                 (y1 - M1 * h0**2 / 6)*(x - x0) / h0
    elif x >= 1 and x < 7:
        reuslt = M1*(x2 - x)**3 / (6 * h1) + M2 * (x - x1)**3 / (6 * h1) + (y1 - M1 * h1**2 / 6)*(x2 - x) / h1 +\
                 (y2 - M2 * h1**2 / 6)*(x - x1) / h1
    elif x >= 7 and x <= 9:
        reuslt = M2*(x3 - x)**3 / (6 * h2) + M3 * (x - x2)**3 / (6 * h2) + (y2 - M2 * h2**2 / 6)*(x3 - x) / h2 +\
                 (y3 - M3 * h2**2 / 6)*(x - x2) / h2
    return reuslt




if __name__ == '__main__':
    value = [[0.0, 0.0], [0.5, 1.6], [1.0, 2.0], [6.0, 1.5], [7.0, 1.5], [9.0, 0.0]]
    value = np.array(value)

    list1 = []
    list2 = []
    count = 0.0
    while count < 9:
        list1.append([count, L5(value, count)])
        list2.append([count, s(value, count)])
        count += 1
    plt.figure()
    plt.title("Matplotlib demo")
    plt.xlabel("x axis caption")
    plt.ylabel("y axis caption")
    plt.plot([list1[i][0] for i in range(len(list1))], [list1[i][1] for i in range(len(list1))], c='r', label='L5')
    plt.plot([list2[i][0] for i in range(len(list2))], [list2[i][1] for i in range(len(list2))], c='b', label='s')
    plt.legend()
    plt.show()
    # print(L5(value, 2))


