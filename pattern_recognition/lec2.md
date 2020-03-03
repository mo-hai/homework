# lec2 统计决策方法

## bayes

**1.1  By explicit integration, check that the distributions are indeed normalized.**

求函数积分是否为1

![b1-1](https://homework-image.oss-cn-beijing.aliyuncs.com/image/b1-1.jpg)



**1.2. Assuming P(ω1) = P(ω2), show that P(ω1|x) = P(ω2|x) if x = (a1 + a2)/2, i.e., the minimum error decision boundary is a point midway between the peaks of the two distributions, regardless of b.**

![b1-2](https://homework-image.oss-cn-beijing.aliyuncs.com/image/b1-2.jpg)



**1.3 Plot P(ω1|x) for the case a1 = 3, a2 = 5 and b = 1.**

图形如下所示：

![image-20200302230955464](https://homework-image.oss-cn-beijing.aliyuncs.com/image/image-20200302230955464.png)

```pyth
import numpy as np
import matplotlib.pyplot as plt



def dd(x, a):
    """
    计算函数值
    :param x: 自变量
    :param a: 给定参数
    :return: 计算出函数值
    """
    return (1 / np.pi) * (1 / (1 + (x - a) ** 2)) * (1 / 2)


if __name__ == '__main__':
    y = []
    x = []
    for i in range(-10000, 10000, 1):
        y.append(dd(i / 100, 3) / (dd(i / 100, 3) + dd(i / 100, 5)))
        x.append(i / 100)
    plt.figure()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.plot(x, y, c="r")
    plt.show()
```



**1.4. How do P(ω1|x) and P(ω2|x) behave as x → −∞? x → +∞? Explain.**

![b1-4](https://homework-image.oss-cn-beijing.aliyuncs.com/image/b1-4.jpg)





**3. where λr is the loss incurred for choosing the (c + 1)th action, rejection, and λs is the loss incurred for making a substitution error. Show that the minimum risk is obtained if we decide ωi if P(ωi |x) ≥ P(ωj |x) for all j and if P(ωi |x) ≥ 1 − λr/λs, and reject otherwise. What happens if λr = 0? What happens if λr > λs?**

![b3](https://homework-image.oss-cn-beijing.aliyuncs.com/image/b3.jpg)



**4. Consider a two-category classification problem in two dimensions with p(x|ω1) ∼ N(0, I), p(x|ω2) ∼ N (1, 1)T , I  and P(ω1) = P(ω2) = 0.5. Calculate the Bayes decision boundar**

计算决策边界

![b4](https://homework-image.oss-cn-beijing.aliyuncs.com/image/b4.jpg)



## Navie bayes

**1.1. Assume Sunny and Windy are truly independent given Hike. Write down the Naive Bayes decision rule for this problem using both attributes Sunny and Windy.**



![n1-1](https://homework-image.oss-cn-beijing.aliyuncs.com/image/n1-1.jpg)



**1.2. Given the decision rule above, what is the expected error rate of the Naive Bayes classifier? (The expected error rate is the probability that each class generates an observation where the decision rule is incorrect.)**



![n1-2](https://homework-image.oss-cn-beijing.aliyuncs.com/image/n1-2.jpg)



**1.3. What is the joint probability that Alice and Bob go to hiking and the weather is sunny and windy, that is P(Sunny, W indy, Hike)?**



![n1-3](https://homework-image.oss-cn-beijing.aliyuncs.com/image/n1-3.jpg)



**1.4. Next, suppose that we gather more information about weather conditions and introduce a new feature denoting whether the weather is X3: Rainy or not. Assume that each day the weather in CA can be either Rainy or Sunny. That is, it can not be both Sunny and Rainy (similarly, it can not be ¬Sunny and ¬Rainy). In the above new case, are any of the Naive Bayes assumptions violated? Why (not)? What is the joint probability that Alice and Bob go to hiking and the weather is sunny, windy and not rainy, that is P(Sunny, W indy, ¬Rainy, Hike)?**



![n1-4](https://homework-image.oss-cn-beijing.aliyuncs.com/image/n1-4.jpg)



**1.5. What is the expected error rate when the Naive Bayes classier uses all three attributes? Will the performance of Naive Bayes be improved by observing the new attribute Rainy? Explain why**



![n1-5](https://homework-image.oss-cn-beijing.aliyuncs.com/image/n1-5.jpg)



## ROC Analysis

grand truth: Sid = [1 0 1 1 1 0 0 0]

source1 : [0.5 0.3 0.6 0.22 0.4 0.51 0.2 0.33]

source2: SC2 = [0.04 0.1 0.68 0.22 0.4 0.11 0.8 0.53]

利用**ROC**算法画出roc曲线，并求曲线下的面积

图形如下所示，最后求解得到的c1的面积为：0.6875；c2的面积为0.4375

![image-20200302220640162](https://homework-image.oss-cn-beijing.aliyuncs.com/image/image-20200302220640162.png)

```pyth
import numpy as np
import matplotlib.pyplot as plt


def getTPR_FPR(grand_truth, score):
    """
    计算roc图中的点
    :param grand_truth: 训练集
    :param score: 预测概率数组
    :return:roc曲线的点集
    """
    n = len(grand_truth)
    pos_num = sum(grand_truth)
    neg_num = n - pos_num
    tp_num = 0
    fp_num = 0
    points = []
    lable = [[]]
    pre_sc = -float('inf')
    index = sorted(range(len(grand_truth)), key=lambda x: score[x], reverse=True)
    for i in index:
        if pre_sc != score[i]:
            points.append((fp_num / neg_num, tp_num / pos_num))
            pre_sc = score[i]
        if grand_truth[i] == 1:
            tp_num += 1
        else:
            fp_num += 1
    points.append((fp_num / neg_num, tp_num / pos_num))
    return points


def getAUC(source):
    """
    计算曲线下的面积
    :param source: 曲线点对
    :return: 曲线下的面积
    """
    area = 0
    pre_index = 0
    n = len(source)
    for i in range(n - 1):
        if i == n-2:
            break
        if source[i][1] == source[i + 1][1]:
            continue
        area += source[i][1] * (source[i][0] - source[pre_index][0])
        pre_index = i
    if source[n-1][1] == source[n-2][1]:
        area += source[n - 1][1] * (source[n-1][0] - source[pre_index][0])
    else:
        area += source[n - 2][1] * (source[n-2][0] - source[pre_index][0])
    return area


def getOptimalPoint(source):
    """
    得到最佳的阈值，纵向上提升最大的点
    :param source: roc点集
    :return: 最佳阈值
    """
    pre_index = 0
    optimal_point = 0
    max_temp = 0
    n = len(source)
    for i in range(n):
        if i == n -2:
            break
        if source[i][1] != source[i + 1][1]:
            continue
        temp = source[i][1] - source[pre_index][1]
        if temp > max_temp:
            optimal_point = i
            max_temp = temp
        pre_index = i + 1

    if source[n - 1][1] != source[n - 1][1]:
        temp = source[n - 1][1] = source[n - 2][1]
        if temp > max_temp:
            optimal_point = n - 1
    return source[optimal_point]




if __name__ == '__main__':
    sid = [1, 0, 1, 1, 1, 0, 0, 0]
    sc1 = [0.5, 0.3, 0.6, 0.22, 0.4, 0.51, 0.2, 0.33]
    sc2 = [0.04, 0.1, 0.68, 0.22, 0.4, 0.11, 0.8, 0.53]

    a = getTPR_FPR(sid, sc1)
    b = getTPR_FPR(sid, sc2)

    print(a)
    print(b)

    a_p = getOptimalPoint(a)
    b_p = getOptimalPoint(b)

    plt.figure()
    plt.plot([a[i][0] for i in range(len(a))], [a[i][1] for i in range(len(a))], c="r", label='c1')
    plt.plot([b[i][0] for i in range(len(b))], [b[i][1] for i in range(len(b))], c="b", label='c2')
    plt.plot(a_p[0], a_p[1], c="y", marker="o", label="pa", markersize=13)
    plt.plot(b_p[0], b_p[1], c="g", marker="x", label="pb", markersize=13)

    plt.legend()
    plt.show()
    print(getAUC(a))
    print(getAUC(b))




```



