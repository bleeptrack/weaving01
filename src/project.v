/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

(* blackbox *) (* keep *)
module my_logo ();
endmodule

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  (* keep *)
  my_logo logo();

  // Use all inputs to ensure proper pin connections
  wire [7:0] ui_sum = ui_in + uio_in;
  
  // Connect control signals to outputs to prevent optimization
  wire [7:0] ctrl_signals = {5'b0, ena, clk, rst_n};

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_sum + ctrl_signals;  // Sum plus control signals
  assign uio_out = 8'b0;  // Set all bits to 0
  assign uio_oe  = 8'b0;  // Set all bits to 0 (all pins as inputs)

endmodule
