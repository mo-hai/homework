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
              -- if (y = '1') /= ((i mod 5) = 0) then
              --   err <= '1';
              -- end if;
              wait for 10 ns;
          end loop;
        end process;

end impl ; -- test
--pragma translate_on
