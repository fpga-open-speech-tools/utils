# Register Control Program
`regctl` is a command line program that allows users to read/write registers by name, instead of by address like one would with `devmem`. This *userspace* program uses `mmap()` to access system memory, just like `devmem` does. This program is mostly useful as a slightly higher-level debugging/testing utility compared to using `devmem` (e.g. `busybox devmem` or `devmem2`). 

One nice thing about this program is that it handles conversion from human-readable numbers, like 0.34, to their fixed-point representations. 



## Usage
```
Usage: regctl [OPTION...] write register_name register_value
  or:  regctl [OPTION...]  read register_name
regctl -- read and write fpga fabric registers by name

  -l, --list-registers       List available register names
  -r, --readback             Read back values after writing
  -v, --verbose              Produce verbose output
  -?, --help                 Give this help list
      --usage                Give a short usage message
```

**Examples:**

`./regctl -v write left_gain 0.2`

`./regctl --readback --verbose write right_gain 0.732`

`./regctl -v read left_gain`

`./regctl -l`

## Customization
Define your registers and component address/span in `registers.h`. Here's an example of register definitions:
```c
static reg_t registers[] = {
  {
    .name = "left_gain",
    .width = 32,
    .fraction_width = 28,
    .is_signed = true,
    .offset = LEFT_GAIN_OFFSET
  },
  {
    .name = "right_gain",
    .width = 32,
    .fraction_width = 28,
    .is_signed = true,
    .offset = RIGHT_GAIN_OFFSET
  }
};
```

## Compiling regctl
Run the Makefile. The only prerequisite is that you're on a Linux machine and have exported `CROSS_COMPILE=arm-linux-gnueabihf-` to cross compile the executable for ARM. The Makefile will by default create executables for both x86 and ARM.
