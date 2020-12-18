/** @file regctl.h
FPGA component register defintions. 

This file contains addresses and information for registers in a custom FPGA 
component. Change the definitions in this file to reflect your component. 

@author Trevor Vannoy

Copyright 2020 Trevor Vannoy

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
IN THE SOFTWARE.
*/
#ifndef REGISTERS_H
#define REGISTERS_H

#include "regctl.h"

/******************************************************************************
* Bus and component addresses
*******************************************************************************/
// base address for the hps-to-fpga lightweight bridge
// this is the bus that our custom component is connected to
#define H2F_LW_BASE_ADDR 0xff200000

// offset from h2f_lw base as reported by Platform Designer
#define COMPONENT_OFFSET 0x0

// component base address as seen by the HPS
#define COMPONENT_BASE_ADDR (H2F_LW_BASE_ADDR + COMPONENT_OFFSET)

// span of our custom component as reported by Platform Designer.
// this is computed as: last address - first address + 1
#define COMPONENT_SPAN 0x8


/******************************************************************************
* Register definitions
*******************************************************************************/
/* 
  Remember that each register is offset from each other by 4 bytes;
  this is different from the vhdl view where each register is offset by 1 word
  when we do the addressing on the avalon bus!

  Here we specify the offsets in words rather than bytes because we type cast
  the base address returned by mmap to a uint32_t*. Thus when we increment that
  pointer by 1, the memory address increments by 4 bytes since that's the size
  of the type the pointer points to.

  See regctl.h for documentation on reg_t fields
*/
#define LEFT_GAIN_OFFSET 0x0
#define RIGHT_GAIN_OFFSET 0x1


static reg_t registers[] = {
  {
    .name = "left_gain",
    .width = 32,
    .fraction_width = 28,
    .is_signed = true,
    .offset = LEFT_GAIN_OFFSET,
    .addr = COMPONENT_BASE_ADDR + 4*LEFT_GAIN_OFFSET
  },
  {
    .name = "right_gain",
    .width = 32,
    .fraction_width = 28,
    .is_signed = true,
    .offset = RIGHT_GAIN_OFFSET,
    .addr = COMPONENT_BASE_ADDR + 4*RIGHT_GAIN_OFFSET
  }
};

#endif // REGISTERS_H