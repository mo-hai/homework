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