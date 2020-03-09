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
