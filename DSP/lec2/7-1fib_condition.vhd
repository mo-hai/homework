
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