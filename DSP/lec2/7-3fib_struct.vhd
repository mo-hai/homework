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
