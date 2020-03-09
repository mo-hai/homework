# lec3 流水线与并行处理

**3.2. 考虑如图所示的滤波器框图，假定乘法操作的时间为2 u.t ，加法操作的时间为1 u.t**

![3-21resource](https://homework-image.oss-cn-beijing.aliyuncs.com/image/3-21resource.svg)

* 计算滤波器的关键路径

  由图可知，关键路径为A2 -> M2 -> A1 -> M3 -> A3 -> A4

  关键路径延时= 1 u.t + 2 u.t + 1 u.t + 2 u.t + 1 u.t + 1 u.t = 8 u.t   

  

* 在适当的前馈割集中插入寄存器，使得IRR滤波器变成流水结构，其关键路径要是下降为3 u.t

  要求关键路径的延时为3 u.t ，可得电路结构如图所示，其关键路径为3 u.t(A2 -> M2 | A1 -> M3)

![3-21result](https://homework-image.oss-cn-beijing.aliyuncs.com/image/3-21result.svg)

**3.5. 考察FIR滤波器一个直接实现形式 y(n) = ax(x) + bx(n-2) + cx(n-3) 假设一次乘加操作需要的时间为T**

由表达式可以可出电路的结构如图所示

![5sdasdasda](https://homework-image.oss-cn-beijing.aliyuncs.com/image/5sdasdasda.svg)

* 在该滤波器中加入流水线，使得时钟周期约等于T

  由题意可得，关键路径的延时为T，可在如下图所示的前馈割集的交点处加入寄存器，使得关键路径的延时为T，关键路径为M2 -> A1。

  ![5-1aaa](https://homework-image.oss-cn-beijing.aliyuncs.com/image/5-1aaa.svg)

* 取分组尺寸为3，画出分组滤波器的结构。用流水线实现该分组滤波器，使得时钟周期约为T，问系统采样的速率是多少。

  y(3k) = ax(3k) + bx(3k - 2) + cx(3k - 3)

  y(3k + 1) = ax(3k + 1) + bx(3k - 1) + cx(3k - 2)

  y(3k + 2) = ax(3k + 2) + bx(3k) + cx(3k - 1)

  T<sub>sample</sub> =  1 /(LM) * T<sub>clk</sub> = T / 3

  采样速率为3 / T

  只考虑并行结构，如下图所示。

  ![3-5b 4578](https://homework-image.oss-cn-beijing.aliyuncs.com/image/3-5b 4578.svg)

  考虑并行流水线结构，如下图所示。

  ![3-4578979](https://homework-image.oss-cn-beijing.aliyuncs.com/image/3-4578979.svg)

* 用流水线实现(b)中的分组滤波器，使得时钟周期为T/2，指出适当的切割集合，并标出。假设乘法器运算时间是0.75T，加法器运算时间是0.25T，乘法器可拆分成两部分，其中一部分运算时间是0.5T，另一部分运算时间是0.25T。

  

  如下图所示，将所有的乘法器一分为二，靠近加法器的部分划分为0.25T，另外一部分为0.5T，这样关键路径的长度就为0.5T，每个时钟周期采样6次。

  T<sub>sample</sub> =  1 /(LM) * T<sub>clk</sub> = T / 6

  采样速率为6 / T
  
  这里只画出了一个分割，其他的分割也类似，将乘法器分割成两部分，由于每一个支路的运算都经过加法器，因此，运算之间的相对时序不会改变，输出依然正确。
  
  ![5-cccc](https://homework-image.oss-cn-beijing.aliyuncs.com/image/5-cccc.svg)