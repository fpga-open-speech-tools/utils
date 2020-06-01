from dtogen.parser import parser
from dtogen.node import FpgaRegionNode, DeviceTreeRootNode


def main():
    """Runs the device tree generation process
    """
    nodes = parser('dtogen/de10_system.sopcinfo')
    fpga_region_node = FpgaRegionNode(
        "base_fpga_region", "de10.rbf", "base_fpga_region", nodes)
    print(fpga_region_node)
    dtroot = DeviceTreeRootNode([fpga_region_node])
    with open("de10.dts", "w") as out_file:
        out_file.write(str(dtroot))

if __name__ == "__main__":
    main()
