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
