/** @file regctl.c
Command line program to read/write register values by name.

Define registers in registers.h

@authors Trevor Vannoy, Aaron Koenigsberg

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
#include <stdio.h>
#include <sys/mman.h>   // mmap functions
#include <unistd.h>     // POSIX API
#include <errno.h>      // error numbers
#include <stdlib.h>     // exit function
#include <stdint.h>     // type definitions
#include <fcntl.h>      // file control
#include <stdbool.h>    // boolean types
#include <string.h>
#include <argp.h>

#include "regctl.h"
#include "registers.h"

#define verbose_print(fmt, ...) \
 do { if (arguments.verbose) printf(fmt, __VA_ARGS__); } while (0)

/******************************************************************************
* Argument parsing
*******************************************************************************/
// store the arguments/options given to the program
struct arguments 
{
    char *command;
    char *reg_name;
    char *reg_val;
    bool verbose;
    bool readback;
    bool list_registers;
};

// define program options/flags
static struct argp_option options[] = {
 {"verbose", 'v', 0, 0, "Produce verbose output"},
 {"readback", 'r', 0, 0, "Read back values after writing"},
 {"list-registers", 'l', 0, 0, "List available register names"},
 {0}
};

// program documentation
static char doc[] = "regctl -- read and write fpga fabric registers by name";
static char args_doc[] = "\
write register_name register_value\n \
read register_name";


/******************************************************************************
* Main program
*******************************************************************************/
int main(int argc, char **argv)
{
  struct arguments arguments;

  // create the argument parser
  struct argp argp = {options, parse_opt, args_doc, doc}; 

  // parse arguments; parse_opt will process each argument
  argp_parse(&argp, argc, argv, 0, 0, &arguments);

  // check to see if the supplied register name matches one of the registers
  int reg_idx = -1;
  for (int i=0; i < sizeof(registers)/sizeof(registers[0]); i++)
  {
    if (strcmp(registers[i].name, arguments.reg_name) == 0)
    {
      reg_idx = i;
    }
  }

  // if the register name didn't match, throw an error and exit
  if (reg_idx == -1)
  {
    fprintf(stderr, "Register name \"%s\" didn't match any registers\n", arguments.reg_name);
    list_registers(registers, sizeof(registers)/sizeof(reg_t));
    exit(EXIT_FAILURE);
  }

  // open /dev/mem so we can access the register
  int fd = open_devmem();

  // map our fpga component's registers into our program's address space
  uint32_t *base_addr = map_fpga_regs(fd, COMPONENT_BASE_ADDR, COMPONENT_SPAN);

  // compute the address for the register we are working with
  uint32_t *reg = base_addr + registers[reg_idx].offset;

  // write to the register
  if (strcmp("write", arguments.command) == 0)
  {
    // convert register value to a fixed-point integer
    uint32_t val = set_fixed_num(arguments.reg_val, registers[reg_idx].fraction_width, registers[reg_idx].is_signed);

    // write the value to memory
    verbose_print("Writing %s (0x%x) to %s at 0x%x\n", arguments.reg_val, 
      val, registers[reg_idx].name, registers[reg_idx].addr);
    *reg = val;

    if (arguments.readback)
    {
      // convert fixed-point integer to string
      char sval[100];
      fp_to_string(sval, val, registers[reg_idx].fraction_width, 
        registers[reg_idx].is_signed, NUM_PRINT_DECIMALS);

      printf("Readback: %s = %s\n", registers[reg_idx].name, sval);
      verbose_print("Readback: stored integer value = 0x%x\n", val);
    }
  }
  // read from the register
  else if (strcmp("read", arguments.command) == 0)
  {
    verbose_print("Reading %s at 0x%x\n", 
      registers[reg_idx].name, registers[reg_idx].addr);
    uint32_t val = *reg;

    // convert fixed-point integer to string
    char sval[100]; // make the buffer plenty large...
    fp_to_string(sval, val, registers[reg_idx].fraction_width,
      registers[reg_idx].is_signed, NUM_PRINT_DECIMALS);

    verbose_print("Stored integer value = 0x%x\n", val);
    printf("%s\n", sval);
  }

  // unmap our register and close /dev/mem
  cleanup(fd, base_addr);

  return 0;
}

/******************************************************************************
* Other functions...
*******************************************************************************/
/*
Print available register names
*/
static void list_registers(const reg_t *registers, const size_t num_registers)
{
  fprintf(stderr, "Available registers:\n");
  for (size_t i=0; i < num_registers; i++)
  {
    fprintf(stderr, "\t%s\n", registers[i].name);
  }
}

/*
Map the register space of our custom FPGA component
*/
static uint32_t *map_fpga_regs(
  const int fd,
  const off_t offset,
  const size_t span) 
{
  // map our custom component into virtual memory
  uint32_t *base_addr = (uint32_t *) mmap(NULL, span,
      PROT_READ | PROT_WRITE,MAP_SHARED, fd, offset);

  // check for errors
  if (base_addr == MAP_FAILED)
  {
    // capture the error number
    int err = errno;

    fprintf(stderr, "ERROR: mmap() failed\n");
    fprintf(stderr, "ERRNO: %d\n", err);

    // cleanup and exit
    close(fd);
    exit(EXIT_FAILURE);
  }

  // printf("base address = %p\n", base_addr);
  return base_addr;
}

/*
Open /dev/mem so we can access system memory
*/
static int open_devmem()
{
  int fd = open("/dev/mem", O_RDWR | O_SYNC);

  // check for errors
  if (fd < 0)
  {
    // capture the error number
    int err = errno;

    fprintf(stderr, "ERROR: couldn't open /dev/mem\n");
    fprintf(stderr, "ERRNO: %d\n", err);

    exit(EXIT_FAILURE);
  }

  return fd;
}

/*
Unmap memory and close /dev/mem
*/
static void cleanup(const int fd, uint32_t *addr) 
{
  // unmap our register at addr
  int result = munmap(addr, COMPONENT_SPAN);

  // check for errors
  if (result < 0)
  {
    // capture the error number
    int err = errno;

    fprintf(stderr, "ERROR: munmap() failed\n");
    fprintf(stderr, "ERRNO: %d\n", err);

    //cleanup and exit
    close(fd);
    exit(EXIT_FAILURE);
  }

  // close devmem
  close(fd);
}

/*
  arg option parser callback function
*/
static error_t parse_opt(int key, char *arg, struct argp_state *state)
{
  // get our arguments struct
  struct arguments *arguments = state->input;
  // printf("key=%d, arg=%s, argnum=%d\n", key, arg, state->arg_num);
  switch (key)
  {
  case 'v':
    arguments->verbose = true;
    break;

  case 'r':
    arguments->readback = true;
    break;

  case 'l':
    arguments->list_registers = true;
    list_registers(registers, sizeof(registers)/sizeof(reg_t));
    exit(EXIT_SUCCESS);

  case ARGP_KEY_INIT:
    arguments->verbose = false;
    arguments->readback = false;
    arguments->list_registers = false;
    arguments->reg_val = 0;
    break;

  // positional arguments
  case ARGP_KEY_ARG:
    if (state->arg_num == 0)
    {
      if (strcmp("write", arg) !=0 && strcmp("read", arg) != 0)
      {
        argp_error(state, "command must be either read or write");
      }
      arguments->command = arg;
    }
    else if (state->arg_num == 1)
    {
      arguments->reg_name = arg;
    }
    else if (state->arg_num == 2) 
    {
      if (strcmp("write", arguments->command) == 0)
      {
        arguments->reg_val = arg;
      }
    }
    break;

  case ARGP_KEY_END:
    // printf("argp_key_end %d\n", state->arg_num);
    if (state->arg_num <= 1) 
    {
      argp_error(state, "not enough arguments");
    }
    else if (strcmp("read", arguments->command) == 0 && state->arg_num > 2) 
    {
      argp_error(state, "too many arguments for read command");
    }
    else if (strcmp("write", arguments->command) == 0 && state->arg_num <= 2) 
    {
      argp_error(state, "not enough arguments for write command");
    } 
    else if (state-> arg_num > 3) 
    {
      argp_error(state, "too many arguments");
    }
    break;
  }

  return 0;
} 

/*
  Turns a uint32_t interpreted as a fixed point into a string.
*/
static int fp_to_string(
  char * buf, 
  uint32_t fp_num, 
  const size_t fractional_bits, 
  const bool is_signed, 
  const uint8_t num_decimals) 
{
  int buf_index = 0;
  int int_mag = 1;
  int int_part;
  int frac_part;
  int i = 0;
  int32_t int_mask = 0x00000000;  // intMask turns into a bitstring with 0's in the location of the integer part of fp_num
  for (i = 0; i < fractional_bits; i++) {
    int_mask = int_mask << 1;
    int_mask += 1;
  }
  if (is_signed) {  // if it signed, need to add '-' to the buffer as well as remove that bit from the bitstring
    if (fp_num & 0x80000000) {
      buf[buf_index++] = '-';
    }
    fp_num = fp_num & 0x7fffffff;
  }
  int_part = (fp_num >> fractional_bits);  // shift away the fractional bits
  while (int_part / int_mag > 9) {  // find the magnitude of the integer part
    int_mag *= 10;
  }
  while (int_mag > 0) {  // decrement the magnitude as we move one digit at a time from 'intPart' to the string
    // common int to ascii conversion, since ints are sequential in ascii
    buf[buf_index++] = (char)(int_part / int_mag + '0');
    int_part %= int_mag;  // remove the first digit
    int_mag /= 10;       // decrease by one order of magnitude
  }
  buf[buf_index++] = '.';
  // get rid of the integer part. Also drop the last bit, not sure why this has to happen but if it doesn't there are some errors.
  // I believe that this results in ever so slightly incorrectly translated nums, but idk
  frac_part = (fp_num & int_mask) >> 1;
  for (i = 0; i < num_decimals; ++i) {
    frac_part *= 10;  // shift the digit up, (maybe related to why dropping the last bit above?)
    buf[buf_index++] = (frac_part >> (fractional_bits - 1)) + '0'; // inspect the digit that moved past the point
    frac_part &= int_mask >> 1;  // get rid of any bits that move past the point
  }
  buf[buf_index] = '\0';
  return buf_index;
}

/*
  Converts a given string to a uint32_t representation of a fixed point number.
*/
static uint32_t set_fixed_num(
  const char * s,
  const int num_fractional_bits,
  const bool is_signed)
{
  const int ARBITRARY_CUTOFF_LEN = 9;
  int int_part_decimal = 0;
  int frac_part_decimal = 0;
  int frac_len = 0;
  int frac_comp = 1;
  int string_index = 0;
  bool seen_point = false;
  uint32_t accumulator = 0;
  int i;
  // get the info from the string
  while (s[string_index] != '\0') {
    if (s[string_index] == '.') {  // if the point is found, need to switch from int accumulating to fraction
      seen_point = true;
    }
    else if (string_index == 0 && s[0] == '-') {  // if its the first char and its a negative sign, don't sweat
      // I don't think anything needs to happen here.
    }
    else if (!seen_point) {
      int_part_decimal *= 10;  // shift digits left, then add the new digit
      // common ascii to int conversion trick, since ints are sequential in ascii
      int_part_decimal += (int)(s[string_index] - '0');
    }
    else if (frac_len < ARBITRARY_CUTOFF_LEN) {  // do not allow the len of the fraction to exceed 9.
      frac_part_decimal *= 10;  // shift digits left, then add the new digit
      frac_part_decimal += (int)(s[string_index] - '0');
      // common ascii to int conversion trick, since ints are sequential in ascii
      frac_len++;  // need to keep track of the length
      frac_comp *= 10;
    }
    else {
      break;
    }
    string_index++;
  }

  while (frac_len < ARBITRARY_CUTOFF_LEN) {  // if the fraction len < 9 we want to make it 9
    frac_part_decimal *= 10;
    frac_len++;
    frac_comp *= 10;
  }
  // convert the decimal fraction to binary info. 32 is arbitrary, it is the precision of the conversion. extra
  // precision beyond the number of fractional bits in the fixed point num will be truncated off.
  for (i = 0; i < num_fractional_bits; i++) {
    // if frac part divided by frac comp is greater than 1, a 1 should be appended to bitstring
    if (frac_part_decimal / frac_comp) {
      accumulator += 0x00000001;
      frac_part_decimal -= frac_comp;
    }
    frac_part_decimal *= 2;
    accumulator = accumulator << 1;
  }
  accumulator += int_part_decimal << num_fractional_bits;
  if (is_signed && s[0] == '-') {
    accumulator |= 0x80000000; // if its a signed int and theres a negative sign flip the first bit of accumulator
  }
  return accumulator;
}