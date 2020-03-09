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