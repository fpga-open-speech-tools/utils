from dtogen.parser import parser
from dtogen.node import FpgaRegionNode

def main():
    """Runs the device tree generation process
    """
    nodes = parser('dtogen/arria10_system.sopcinfo')
    fpga_region_node = FpgaRegionNode("base_fpga_region", "echo.rbf", "base_fpga_region", nodes, status= "echo rbf loaded")
    print(fpga_region_node)

if __name__ == "__main__":
    main()