# lec2 迭代边界

**2.1. 使用LPM算法i计算如图所示的迭代边界**

![2-1](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-1.jpg)

程序验证结果如下所示：

![2-1-1](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-1-1.png)

验证程序如下所示

```pyth
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
        print(L[i])

    result = 0.0
    for i in range(1, n):
        for j in range(n):
            result = np.max([result, L[i][j][j] / (i + 1)])
    print(result)

```

**2.3 使用LPM算法计算DFG的迭代边界**

设计延时标记如下图所示

![2-3](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3.jpg)

可得L1矩阵如下图所示

![2-3-1](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-1.jpg)

| ![2-3-2](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-2.png)L2 | ![2-3-3](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-3.png)L3 |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
| ![2-3-4](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-4.png)L4 | ![2-3-5](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-5.png)L5 |
| ![2-3-6](https://homework-image.oss-cn-beijing.aliyuncs.com/image/2-3-6.png)L6 |                                                              |

通过2.1的验证程序可以求得迭代边界为4