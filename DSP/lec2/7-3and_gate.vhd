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
