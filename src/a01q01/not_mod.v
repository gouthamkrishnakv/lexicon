// LEXICON: Generated file
// Project: assignment_01
// Subproject: a01q01
// MODULE not
// Type: MODULE FILE

// TIMESCALE: <time_unit>/<time_precision>
`timescale 1ps/1ps

module not_mod(
    y,
    x
);
    output y;
    input x;
    nand(y,x,x);

endmodule