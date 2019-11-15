import numpy


def question1(x):
    return 20 / (x ** 2 + 2 * x + 10)


def question2(x):
    return (20 - 2 * x ** 2 - x ** 3) / 10


def question3(x):
    return (x * question1(question1(x)) - question1(x) ** 2) / (question1(question1(x)) - 2 * question1(x) + x)


def question4(x):
    return (x * question2(question2(x)) - question2(x) ** 2) / (question2(question2(x)) - 2 * question2(x) + x)


def question5(x):
    return x - (x ** 3 + 2 * x ** 2 + 10 * x - 20) / (3 * x ** 2 + 4 * x + 10)


if __name__ == '__main__':
    x = 1
    accuracy = 1.368808107
    solve = question1
    n = input("请输入需要解答的小题号\n1:执行第1小题\n2:执行第2小题\n3:执行第3小题\n4:执行第4小题\n5:执行第5小题\n")
    if n == '1':
        solve = question1
    elif n == '2':
        solve = question2
    elif n == '3':
        solve = question3
    elif n == '4':
        solve = question4
    elif n == '5':
        solve = question5
    else:
        print("输入错误")
        exit(0)
    count = 0
    for count in range(10000):
        temp = solve(x)
        if abs(temp - x) < 10 ** -9:  # 准确到小数点后8位
            x = temp
            break
        x = temp
    print(x, count, abs(x - accuracy))

# 1.3688081075681298 25 5.681297654547279e-10
# 0.548946478054766 9999 0.819861628945234
# 1.3688081119266895 12 4.926689500805992e-09
# 1.3688081082034376 187 1.2034375718172896e-09
# 1.3688081078213727 4 8.213727475947508e-10
