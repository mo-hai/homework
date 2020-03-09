--pragma translate_off

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
use std.textio.all;
use ieee.std_logic_textio.all;


entity fib_test is
end fib_test;

architecture test of fib_test is

    signal num: std_logic_vector(3 downto 0);
    signal isfib_con, isfib_logic, isfib_struct,is_eq: std_logic;
    
    begin
        fib_con: entity work.fib_condition(fib_condition_impl) port map(num, isfib_con);
        fib_logi: entity work.fib_logic(fib_logic_impl) port map(num, isfib_logic);
        fib_str: entity work.fib_struct(fib_struct_impl) port map(num, isfib_struct);
        
        process is
            variable temp: integer:=0;
            variable buf1: line;
        begin
            for i in 0 to 15 loop
                num <= std_logic_vector(to_unsigned(i, 4));
                if isfib_logic = isfib_con and isfib_con = isfib_struct then is_eq <= '1';
                else is_eq <= '0';
                end if;
                wait for 10 ns;
                write(buf1, temp);
                writeline(output, buf1);

            end loop;
        end process;

end test ; -- test
--pragma translate_on
