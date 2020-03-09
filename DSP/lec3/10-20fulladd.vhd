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