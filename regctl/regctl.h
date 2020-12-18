/** @file regctl.h

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
#ifndef REGCTL_H
#define REGCTL_H

// number of decimal places to print when converting fixed-point to string
#define NUM_PRINT_DECIMALS 12

/******************************************************************************
* Type definitions
*******************************************************************************/
/** @struct reg_t 
@brief structure containing register information (e.g. name, datatype, etc.)

@var name, register name

@var width, register width in bits

@var fraction_width, number of fractional bits

@var is_signed, whether the register is signed or unsigned

@var offset, register address offset, in words, from the component base

@var addr, physical register address, only used for diagnostics
*/

struct reg 
{
  const char *name;
  const uint8_t width;
  const uint8_t fraction_width;
  const bool is_signed;
  const uint32_t offset;
  const uint32_t addr;
} typedef reg_t;

/******************************************************************************
* Function prototypes
*******************************************************************************/
/** parse_opt: argp option parser callback function.
This function gets called for every argument provided to the program. 
See the argp documentation for more information.

@param key, option key

@param arg, the command line argument

@param state, internal argp parser state

@returns parser error code
*/
static error_t parse_opt(int key, char *arg, struct argp_state *state);

/** fp_to_string: Turns a uint32_t interpreted as a fixed point into a string.

@param buf, buffer in which to fill the string. It is assumed to have enough space. If a buflen parameter were passed it would
be simple to add a check to make sure that no writing goes past the bound of the array.

@param fp_num, the uint32_t to be interpreted as a fixed point to be translated into a string

@param fractional_bits, the number of fractional bits for the interpretation. No consideration is made to check that it
is a sensible number. i.e. less than 32, more than 0.

@param is_signed, whether or not to interpret the first bit as a sign. If true, the first bit is inspected then dumped.

@param num_decimals, number of decimals to write to the string.

@returns the length of the buffered string.
*/
static int fp_to_string(
  char * buf, 
  uint32_t fp_num, 
  const size_t fractional_bits, 
  const bool is_signed, 
  const uint8_t num_decimals
);

/** set_fixed_num: Converts a given string to a uint32_t interpreted as a fixed point.

@param s, the string to be converted.

@param num_fractional_bits, the number of fractional bits in the fixed point. No consideration is made to validate.

@param is_signed, whether or not to interpret the string as a signed or not.

@returns returns a uint32_t that is a fixed point representation based on the num_fractional_bits and is_signed params.
*/
static uint32_t set_fixed_num(
  const char * s, 
  const int num_fractional_bits, 
  const bool is_signed
);

/** open_devmem: Opens /dev/mem/ so we can access system memory.

@returns a file descriptor pointing to /dev/mem
*/
static int open_devmem();

/** cleanup: Unmap memory and close /dev/mem.

@param fd, file descriptor pointing to /dev/mem

@param addr, pointer to the memory to unmap
*/
static void cleanup(const int fd, uint32_t *addr);

/** map_fpga_regs: Map the register space of our custom FPGA component.

@param fd, file descriptor to /dev/mem

@param offset, base address of the custom FPGA component

@param span, memory span of the custom FPGA component

@returns pointer to the base address of the custom FPGA component
*/
static uint32_t *map_fpga_regs(
  const int fd,
  const off_t base_addr,
  const size_t span
);

/** list_registers: Print available register names.

@param registers, pointer to an array of register structs

@param num_registers, number of registers in the array
*/
static void list_registers(const reg_t *registers, const size_t num_registers);

#endif // REGCTL_H