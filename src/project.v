/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

(* blackbox *) (* keep *)
module my_logo (
    input  wire       clk,      // clock (unused but present)
    input  wire       rst_n     // reset (unused but present)
);
  // This is a silicon art module - no functional logic needed
  // The (* blackbox *) attribute tells the tools this is a physical macro
  
  // Add some dummy logic to make it look like a proper module
  reg [1:0] dummy_reg;
  
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      dummy_reg <= 2'b00;
    end else begin
      dummy_reg <= dummy_reg + 1'b1;
    end
  end
  
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
  my_logo logo(
    .clk(clk),
    .rst_n(rst_n)
  );

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
