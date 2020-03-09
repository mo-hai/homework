# lec3 VHDL第三次作业

## chapter 10

**10.16. 二进制加法。实现两个十六进制数相加 2A + 3C**

2A + 3C == 66<sub>Hex</sub> = 102<sub>Dec</sub>



**1.18. 位计数电路。用全加器设计一个电路，接受一个7位输入，输出一个表示输入中1的个数的3位二进制数。**

设计思路：从输入的低位开始扫描序列，设计的全加器为3位，将输入的每一位的高2位补0，并与上一次输入的结果一同输入到一个新的全加器中，若该位为1则结果加1，若该位为0则结果不变，这样最终累加的结果将保存再ypp（6）中，ypp是一个二维数组。

仿真结果图所示，当输入为9时，即 0001001，其中1的个数为2，输出结果y也为2，符合设计要求，其他的输入也同样符合要求，可知设计正确。

![10-18-465464658](https://homework-image.oss-cn-beijing.aliyuncs.com/image/10-18-465464658.png)

代码如下所示。其中FA是加法器，count1是技术电路，count_test是计数电路。

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity FA is
    generic(n: integer := 8);
    port (
        a,b: in std_logic_vector(n-1 downto 0);
        cin: in std_logic;
        cout: out std_logic;
        s:out std_logic_vector(n -1 downto 0)

    ) ;
end FA;

architecture impl of FA is

    signal sum: std_logic_vector(n downto 0);

begin
    sum <= ('0' & a) + ('0' & b) + cin;
    cout <= sum(n);
    s <= sum(n-1 downto 0);
end impl ; -- impl


library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity count1 is
  port (
    a: in std_logic_vector(6 downto 0);
    y: out std_logic_vector(2 downto 0)
  ) ;
end count1;

architecture impl of count1 is
    type PartialP is array(6 downto 0) of std_logic_vector ( 2 downto 0);
    signal ypp : PartialP;
    signal cout: std_logic;
    signal xin: PartialP;

begin
    xin(0) <= "00" & a(0);
    d0: entity work.FA generic map(3) port map(xin(0), "000", '0',cout, ypp(0));
    xin(1) <= "00" & a(1);
    d1: entity work.FA generic map(3) port map(xin(1), ypp(0), '0',cout, ypp(1));
    xin(2) <= "00" & a(2);
    d2: entity work.FA generic map(3) port map(xin(2), ypp(1), '0',cout, ypp(2));
    xin(3) <= "00" & a(3);
    d3: entity work.FA generic map(3) port map(xin(3), ypp(2), '0',cout, ypp(3));
    xin(4) <= "00" & a(4);
    d4: entity work.FA generic map(3) port map(xin(4), ypp(3), '0',cout, ypp(4));
    xin(5) <= "00" & a(5);
    d5: entity work.FA generic map(3) port map(xin(5), ypp(4), '0',cout, ypp(5));
    xin(6) <= "00" & a(6);
    d6: entity work.FA generic map(3) port map(xin(6), ypp(5), '0',cout, ypp(6));
    y <= ypp(6);
end impl ; -- impl


--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;


entity count_test is
end count_test;

architecture impl of count_test is
    signal a: std_logic_vector(6 downto 0);
    signal y: std_logic_vector(2 downto 0);
    
    begin

        p1: entity work.count1 port map(a, y);
        process begin
          for i in 0 to 2**7 - 1 loop
              a <= std_logic_vector(to_unsigned(i, 7));
              wait for 10 ns;
          end loop;
        end process;

end impl ; -- test
--pragma translate_on
```



**10.20. 饱和加法器设计。在一些应用中，特别是信号处理中，希望加法器饱和，再溢出状态下产生2<sup>n-1</sup> 的结果，而不是模运算后的结果。设计一个饱和加法器，可以使用n位加法器和n位多路复用器作为基本器件**

饱和加法器，当正向溢出的时候输出输出最大正数，当负向溢出的时候输出最小负数。分析可知，当符号位进位为’1‘，数据最高位进位为‘0‘时发生负向溢出，即两个负数相加超出最小负数表示范围，当符号进位为’0‘且数据最高位进位为’1‘时，发生正向溢出，即两个正数相加超过最大正数表示范围。

因此可以改造全加器，当发生正向溢出时符号位设置为’0‘，数据位全设置为‘1’，表示最大正数；当发生负向溢出时，符号位设置为‘1’，数据位全设置为‘0’表示最小负数

仿真结果如下所示，设计的前20ns位两组特殊的数据，前10ns为 1000 + 1010 发生负向溢出，应该输出1000，仿真结果符合预期，10-20ns输入为0111+ 0010，为正向溢出，输出结果为0111，符合预期，之后输入a从0010开始每隔40ns加1，输入b从0001开始每隔10ns加1，通过观察发现，输出的结果也是符合预期，说明设计正确。

![10-20](https://homework-image.oss-cn-beijing.aliyuncs.com/image/10-20.png)

代码如下所示

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity fulladd is
    generic(N: integer := 8);
    port (
        a,b: in std_logic_vector(n-1 downto 0);
        sub: in std_logic;
        s: out std_logic_vector(n-1 downto 0);
        ovf: out std_logic
    ) ;
end fulladd;

architecture impl of fulladd is

    signal c1, c2: std_logic;
    signal c1n: std_logic_vector(n-1 downto 0);
    signal c2s: std_logic_vector(1 downto 0);

begin
    ovf <= c1 xor c2;
    c1n <= ('0' & a(n-2 downto 0)) + ('0' & (b(n -2 downto 0) xor (n-2 downto 0 => sub))) + sub;
    -- s(n-2 downto 0) <= c1n(n-2 downto 0);
    c1 <= c1n(n - 1);
    c2s <= ('0' & a(n-1)) + ('0' & (b(n - 1) xor sub)) + c1;
    -- s(n - 1) <= c2s(0);
    c2 <= c2s(1);
    s(n - 2 downto 0) <= (n-2 downto 0 => '1') when c1 = '1' and c2 = '0'  
    else (n-2 downto 0 => '0') when c2 = '1' and c1 = '0'
    else c1n(n -2 downto 0);

    s(n - 1) <= '0' when c1 = '1' and c2 = '0' 
    else '1' when c2 = '1' and c1 = '0'
    else c2s(0);
end impl ; -- impl


--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;


entity fulladd_test is
end fulladd_test;

architecture impl of fulladd_test is
    signal a: std_logic_vector(3 downto 0);
    signal b: std_logic_vector(3 downto 0);
    signal y: std_logic_vector(3 downto 0);
    signal ovf: std_logic;
    
    begin

        p1: entity work.fulladd generic map(4) port map(a, b, '0', y, ovf);
        process begin
            a <= "1000";
            b <= "1010";
            wait for 10 ns;
            a <= "0111";
            b <= "0010";
            wait for 10 ns;
            for i in 2 to 2**4 -1 loop
                a <= std_logic_vector(to_unsigned(i, 4));
                for j in 1 to 2**4 -1 loop
                    b <= std_logic_vector(to_unsigned(j, 4));
                    wait for 10 ns;
                end loop;
            end loop;
        end process;

end impl ; -- test
--pragma translate_on
```





**10.44. 倍5电路。使用加法器，组合构建块和门，设计一个接收4位基2补码二进制输入a（3 downto 0）的电路，并输入一个7位基2补码输出b（6 downto 0），输出是输入的5倍。不能使用乘法器，使用尽可能少的加法器。**

设计思路：将输入左移两位，得到原输入的四倍，在使用一个加法器加上原来输入元素，得到原输入的五倍，需要注意的是，输入的是基2的补码，最高位表示符号位，在左移两位后需要对原数据进行符号扩展。

如下所示，当输入由0000-0111时，输入为正数，输出直接扩大五倍，当输入为1000时，表示的时-8，输出为58<sub>Hex</sub> 转换为十进制的数为-40，符合题意，同理验证其他复数也符合5倍的要求，可知电路设计正确。

![10-44](https://homework-image.oss-cn-beijing.aliyuncs.com/image/10-44.png)

设计代码如下所示

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity addsub is
    generic(N: integer := 8);
    port (
        a,b: in std_logic_vector(n-1 downto 0);
        sub: in std_logic;
        s: out std_logic_vector(n-1 downto 0);
        ovf: out std_logic
    ) ;
end addsub;

architecture impl of addsub is

    signal c1, c2: std_logic;
    signal c1n: std_logic_vector(n-1 downto 0);
    signal c2s: std_logic_vector(1 downto 0);

begin
    ovf <= c1 xor c2;
    c1n <= ('0' & a(n-2 downto 0)) + ('0' & (b(n -2 downto 0) xor (n-2 downto 0 => sub))) + sub;
    s(n-2 downto 0) <= c1n(n-2 downto 0);
    c1 <= c1n(n - 1);
    c2s <= ('0' & a(n-1)) + ('0' & (b(n - 1) xor sub)) + c1;
    s(n - 1) <= c2s(0);
    c2 <= c2s(1);
end impl ; -- impl


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity fives is
  port (
    num: in std_logic_vector(3 downto 0);
    y: out std_logic_vector(6 downto 0)
  ) ;
end fives;

architecture impl of fives is

    signal num_sll_2, num_temp: std_logic_vector(6 downto 0) := "0000000";
    signal ovf: std_logic;

begin
num_temp <= "111" & num when num(3) = '1' else "000" & num ;
num_sll_2(5 downto 0) <= num & "00";
num_sll_2(6) <= '1' when num(3) = '1' else '0';

e0: entity work.addsub generic map(7) port map(num_temp, num_sll_2, '0', y, ovf);
end impl ; -- impl


--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;


entity fives_test is
end fives_test;

architecture impl of fives_test is
    signal a: std_logic_vector(3 downto 0);
    signal y: std_logic_vector(6 downto 0);
    
    begin

        p1: entity work.fives  port map(a, y);
        process begin
          for i in 0 to 2**4 - 1 loop
              a <= std_logic_vector(to_unsigned(i, 4));
              wait for 10 ns;
          end loop;
        end process;

end impl ; -- test
--pragma translate_on
```



## chapter 11

**11.6. 定点数表示。将0.3775转化到最近的s1.5格式定点数表示，给出绝对跟相对误差**

0.3775 * 2<sup>5</sup> = 12.08 ≈ 12 = 01100

转为s1.5的形式为0.01100 = 0.375

绝对误差 = | 0.375 - 0.3775 | = 0.0025

相对误差为<span>(0.3775 - 0.375)  / 0.3775 = 0.0066</span>



**11.11. 选择定点表示方案。以0.1PSI的精度表示一个范围从-10PSI到10PSI的相对压力信号。选择一个指定精度的并且以最少位数覆盖此范围的定点表示方法**

由于2<sup>-4</sup> < 0.1 所以小数部分可以用四位二进制表示，由于要表示正负数，需要一位符号位，整数位可以用4位二进制数表示，因此最终表示格式位9位：s4.4



**11.18. 浮点表示。将100 000转化成偏移量为8，格式为s3E5的浮点数，并给出相对误差跟绝对误差**

s3E5从左到右为1位符号，5位指数，3位小数，将（100,000）<sub>10</sub> 转化为2进制数位 ‭1 1000 0110 1010 0000‬ = 0.‭11000011010100000‬ * 2<sup>‭1 0001‬</sup> 

由于偏移量位8，指数部分需要加上1000，最终得到指数位1 1001

要求保留三位小数，可得小数部分为110

最终得到的s3E5浮点数为 0 11001 110，表示为十进制数为98,304

绝对误差 = 100,000 - 98,000 = 2,000

相对误差为(100,000 - 98,000)  / 100,000 = 0.02