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