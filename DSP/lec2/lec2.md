# lec2 VHDL第二次作业

## chapter 6

**6.15. 为7段解码器的第一段设计一个积之和电路**

真值表如下所示。

| 输入（dcba） | 输出 | 1段输出 |
| :----------: | :--: | :-----: |
|     0000     |  0   |    0    |
|     0001     |  1   |    0    |
|     0010     |  2   |    0    |
|     0011     |  3   |    0    |
|     0100     |  4   |    0    |
|     0101     |  5   |    1    |
|     0110     |  6   |    1    |
|     0111     |  7   |    0    |
|     1000     |  8   |    0    |
|     1001     |  9   |    0    |
|    others    |  -   |    -    |

| BA/DC |  00  |  01  |  11  |  10  |
| :---: | :--: | :--: | :--: | :--: |
|  00   |  0   |  0   |  0   |  0   |
|  01   |  0   |  1   |  0   |  1   |
|  11   |  X   |  X   |  X   |  X   |
|  10   |  0   |  0   |  X   |  X   |

![6-15 4564](https://homework-image.oss-cn-beijing.aliyuncs.com/image/6-15 4564.png)

电路图如下所示

![787914653](https://homework-image.oss-cn-beijing.aliyuncs.com/image/787914653.png)

**6.44. 修复电路图中的冒险**

保持原电路的结构的情况下，新增一个b与c的逻辑门。

![image-20200303002553676](https://homework-image.oss-cn-beijing.aliyuncs.com/image/image-20200303002553676.png)

简化后的电路如下图所示

![6-44 13214654](https://homework-image.oss-cn-beijing.aliyuncs.com/image/6-44 13214654.png)



## chapter 7

**7.1. 条件语句斐波那契vhdl实现**

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity fib_condition is
  port (
    num : in std_logic_vector(3 downto 0);
    is_fib: out std_logic);
end fib_condition;

architecture fib_condition_impl of fib_condition is
begin
  process( num )
  begin
    case num is
      when "0000" | "0001" | "0010" | "0011" | "0101" | "1000" | "1101"
       => is_fib <= '1';
      when others => is_fib <= '0';
    end case;
  end process ;
end fib_condition_impl;

```



**7.2 最小逻辑斐波那契实现**

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity fib_logic is
  port (
    num : in std_logic_vector(3 downto 0);
    is_fib: out std_logic);
end fib_logic;

architecture fib_logic_impl of fib_logic is
begin
    is_fib <= ((not num(0) and not num(1) and not num(2)) or 
            (num(0) and not num(1) and num(2)) or 
            (num(0) and not num(1) and not num(3)) or 
            (not num(2) and not num(3)));
end fib_logic_impl;

```



**7.3. 结构化斐波那契数列实现**

```vhdl
--Fib_struct.vhd
library ieee;
use ieee.std_logic_1164.all;

entity fib_struct is
  port (
    num : in std_logic_vector(3 downto 0);
    is_fib: out std_logic);
end fib_struct;


architecture fib_struct_impl of fib_struct is
    component and_gate is
        port(a,b,c: in std_logic; y : out std_logic);
    end component;
    signal a0, a1, a2, a3, n1, n2, n3 : std_logic;

begin
    a0 <= not num(0);
    a1 <= not num(1);
    a2 <= not num(2);
    a3 <= not num(3);
    is_fib <= n1 or n2 or n3;

    and1: entity work.and_gate(logic_impl) port map(a => a0, b=> a1, c=> a2, y=> n1);
    and2: entity work.and_gate(logic_impl) port map(a => num(0), b => a1, c => num(2), y =>n2);
    and3: entity work.and_gate(logic_impl) port map(c => a2, d => a3, y => n3);

end fib_struct_impl ; -- fib_struct_impl

--and_gate.vhd

library ieee;
use ieee.std_logic_1164.all;

entity and_gate is
    port (a,b,c,d : in std_logic := '1'; y :out std_logic) ;
  end and_gate;
  
  architecture logic_impl of and_gate is
  
  begin
      y <= a and b and c and d;
  end logic_impl ; -- and_gate_impl
  architecture alt_impl of and_gate is
  
  begin
      y <= not( not a and not b and not c and not d);
  end alt_impl ; -- alt_impl




```



**7.4. 斐波那契数列测试**

仿真结果如下图所示，num为4位输如，从0循环到15，每隔10ns加1，其中isfib_con，isfib_logic，isfib_struct分别指示7.1、7.2、7.3的结果，即是否为斐波那契数，is_eq指示三者的结果是否相等。

由途中可以看出，当输入num为0、1、2、3、5、8、13时三者输出为1，其余结果输出为0。is_eq的结果一直为1，结果符合预期，由此可知电路设计正确。

![image-20200303003054797](https://homework-image.oss-cn-beijing.aliyuncs.com/image/image-20200303003054797.png)

测试代码如下

```vhdl
--Fib_test.vhd
--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;


entity fib_test is
end fib_test;

architecture test of fib_test is

    signal num: std_logic_vector(3 downto 0);
    signal isfib_con, isfib_logic, isfib_struct,is_eq: std_logic;
    
    begin
        fib_con: entity work.fib_condition(fib_condition_impl) port map(num, isfib_con);
        fib_logi: entity work.fib_logic(fib_logic_impl) port map(num, isfib_logic);
        fib_str: entity work.fib_struct(fib_struct_impl) port map(num, isfib_struct);
        
        process is
            variable temp: integer:=0;
            variable buf1: line;
        begin
            for i in 0 to 15 loop
                num <= std_logic_vector(to_unsigned(i, 4));
                if (isfib_logic = isfib_con) and (isfib_con = isfib_struct) then is_eq <= '1';
                else is_eq <= '0';
                end if;
                wait for 10 ns;
                write(buf1, temp);
                writeline(output, buf1);

```

# chapter8

**4-16译码器跟或门实现七段译码器**

仿真电路如下图所示，num为4位输入，从0循环到15，每隔10ns加1，y为电路7位输出。

![7-56565465](https://homework-image.oss-cn-beijing.aliyuncs.com/image/7-56565465.png)



```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity Dec is
    generic(n: integer:= 2; m: integer := 4);
    port (
        a: in std_logic_vector(n-1 downto 0);
        b: out std_logic_vector(m-1 downto 0)
    ) ;
end Dec;

architecture impl of Dec is

    signal one: unsigned(m-1 downto 0);
    signal shift: integer;

begin
    one <= to_unsigned(1, m);
    shift <= to_integer(unsigned(a));
    b <= std_logic_vector(one sll shift);
end impl ; --Dec impl


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Dec4to16 is
    port (
        a: in std_logic_vector(3 downto 0);
        b: out std_logic_vector(15 downto 0)
    ) ;   
end Dec4to16;  

architecture impl4to16 of Dec4to16 is

    signal x, y :std_logic_vector(3 downto 0);

begin

    d0: entity work.Dec port map(a(1 downto 0), x);
    d1: entity work.Dec port map(a(3 downto 2), y);

    b(3 downto 0) <= x and (3 downto 0 => y(0));
    b(7 downto 4) <= x and (3 downto 0 => y(1));
    b(11 downto 8) <= x and (3 downto 0 => y(2));
    b(15 downto 12) <= x and (3 downto 0 => y(3));

end impl4to16 ; -- impl



library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity sevenSeg is
  port (
    a: in std_logic_vector(3 downto 0);
    b: out std_logic_vector(6 downto 0)
  ) ;
end sevenSeg;

architecture impl of sevenSeg is

    signal one_hot: std_logic_vector(15 downto 0) := "0000000000000000";

begin
    d1: entity work.Dec4to16 port map(a, one_hot);
    process(one_hot)
    begin
        case(one_hot) is
            when "0000000000000001" => b <="1000000"; --0
            when "0000000000000010" => b <="1111001"; --1
            when "0000000000000100" => b <="0100100"; --2
            when "0000000000001000" => b <="0110000"; --3
            when "0000000000010000" => b <="0011001"; --4
            when "0000000000100000" => b <="0010010"; --5
            when "0000000001000000" => b <="0000010"; --6
            when "0000000010000000" => b <="1111000"; --7
            when "0000000100000000" => b <="0000000"; --8
            when "0000001000000000" => b <="0010000"; --9

            when "0000010000000000" => b <="0001000"; --A
            when "0000100000000000" => b <="0000011"; --b
            when "0001000000000000" => b <="1000110"; --C
            when "0010000000000000" => b <="0100001"; --d
            when "0100000000000000" => b <="0000110"; --E
            when "1000000000000000" => b <="0001110"; --F
            when others => b <=  (others => '-');
        end case;
    end process ;
end impl ; -- impl




--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;


entity segTest is
end segTest;

architecture test of segTest is

    signal num: std_logic_vector(3 downto 0);
    signal y: std_logic_vector(6 downto 0);
    
    begin
        p1: entity work.sevenSeg port map(num, y);
        process is

        begin
            for i in 0 to 15 loop
                num <= std_logic_vector(to_unsigned(i, 4));
                wait for 10 ns;
            end loop;
        end process;

end test ; -- test
--pragma translate_on

```



**8.14. 比较器实现**

仿真结果如下图所示，其中a、b为两位输入，b每隔10ns循环加1，a每隔40ns循环加1，y为输出，a>b输出1，非则输出0。

前40ns，a输入为0，一直不大于b，所以y输出为0，50ns-80ns，a输入为1，只有在第50ns的时候大于b，输出为1，由图中的结果可知，电路设计符合预期。

![dasdasd ](https://homework-image.oss-cn-beijing.aliyuncs.com/image/dasdasd .png)

代码如下所示

```vhdl
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_misc.all;

entity magComp is
    generic(k: integer := 8);
    port (
        a,b: in std_logic_vector(k-1 downto 0);
        gt: out std_logic
    ) ;
end magComp;

architecture impl of magComp is

    signal eqi, gti: std_logic_vector(k-1 downto 0);
    signal gta, eqa: std_logic_vector(k downto 0);


begin
    eqi <= a xnor b;
    gti <= a and not b;
    gta <= '0' & (gta(k downto 1) or (gti and eqa(k downto 1)));
    eqa <= '1' & (eqa(k downto 1) and eqi);
    gt <= or_reduce(gta);
end impl ; -- impl


--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;


entity comptest is
end comptest;

architecture test of comptest is
    signal k: integer :=2;
    signal a: std_logic_vector(k-1 downto 0);
    signal b: std_logic_vector(k-1 downto 0);
    signal y: std_logic;
    
    begin

        p1: entity work.magComp generic map(k) port map(a, b, y);
        process is

        begin
            for i in 0 to 2**k - 1 loop
                a <= std_logic_vector(to_unsigned(i, k));
                for j in 0 to 2**k -1 loop
                    b <= std_logic_vector(to_unsigned(j, k));
                    wait for 10 ns;
                end loop;
            end loop;
        end process;

end test ; -- test
--pragma translate_on

```

## chapter9

**9.3. 设计倍5电路**

其中a为8位输入.

y为1位输出，若a为5的倍数，则输出1，否则输出0.

err为1位出去，与直接使用amod5的输出进行比较，若不相同则输出1.

由下图可以看出，在a输入0以及5时，y跳变位1，其余情况为0，说明符合逻辑，err输出一直为0，说明设计的电路与直接使用mod函数计算出的结果一致，符合预期.

![dafqwerw](https://homework-image.oss-cn-beijing.aliyuncs.com/image/dafqwerw.png)

代码如下所示

```vhdl
library ieee;
use ieee.std_logic_1164.all;

entity multiple_of_5_bit is
  port (
    a: in std_logic;
    remin: in std_logic_vector(2 downto 0);
    remout: out std_logic_vector(2 downto 0)
  ) ;
end multiple_of_5_bit;

architecture impl of multiple_of_5_bit is

begin
  process(a, remin) begin
    case remin & a is
        when "0000" => remout <= "000";
        when "0001" => remout <= "001";
        when "0010" => remout <= "010";
        when "0011" => remout <= "011";
        when "0100" => remout <= "100";
        when "0101" => remout <= "000";
        when "0110" => remout <= "001";
        when "0111" => remout <= "010";
        when "1000" => remout <= "011";
        when "1001" => remout <= "100";
        when others => remout <= (others => '-');
    end case;
end process;

end impl ; -- impl


library ieee;
use ieee.std_logic_1164.all;

entity multiple_of_5 is
  port (
  num: in std_logic_vector(7 downto 0);
  y: out std_logic
  );
end multiple_of_5;

architecture impl of multiple_of_5 is

  signal re: std_logic_vector(23 downto 0);

begin
b7: entity work.multiple_of_5_bit port map(num(7), "000", re(23 downto 21));
b6: entity work.multiple_of_5_bit port map(num(6), re(23 downto 21), re(20 downto 18));
b5: entity work.multiple_of_5_bit port map(num(5), re(20 downto 18), re(17 downto 15));
b4: entity work.multiple_of_5_bit port map(num(4), re(17 downto 15), re(14 downto 12));
b3: entity work.multiple_of_5_bit port map(num(3), re(14 downto 12), re(11 downto 9));
b2: entity work.multiple_of_5_bit port map(num(2), re(11 downto 9), re(8 downto 6));
b1: entity work.multiple_of_5_bit port map(num(1), re(8 downto 6), re(5 downto 3));
b0: entity work.multiple_of_5_bit port map(num(0), re(5 downto 3), re(2 downto 0));

y <= '1' when re(2 downto 0) = "000" else '0';
end impl ; -- impl



--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;


entity multiple_of_5_test is
end multiple_of_5_test;

architecture impl of multiple_of_5_test is
    signal a: std_logic_vector(7 downto 0);
    signal y, err: std_logic;
    
    begin

        p1: entity work.multiple_of_5 port map(a, y);
        process begin
          err <= '0';
          for i in 0 to 2**8 - 1 loop
              a <= std_logic_vector(to_unsigned(i, 8));
              if (y = '1') /= ((i mod 5) = 0) then
                err <= '1';
              end if;
              wait for 10 ns;
          end loop;
        end process;

end impl ; -- test
--pragma translate_on

```

