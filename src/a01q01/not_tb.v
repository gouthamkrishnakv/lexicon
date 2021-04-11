// LEXICON: Generated file
// Project: ${project}
// Subproject: ${subproject}
// MODULE ${name}
// Type: TEST BENCH FILE

// TIMESCALE: <time_unit>/<time_precision>
`timescale 1ps/1ps

module ${name}_tb;
    reg x;
    wire y;

    not not1(y, x);

    initial begin
        $dumpfile("not.vcd");
        $dumpvars(0, x, y)
        x = 1;
    #10;x = 0;
    #10;x = 1;
    #10;x = 0;
    #10;
    end
    
endmodule