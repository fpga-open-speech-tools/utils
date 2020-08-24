from dtogen.parser import parser
from dtogen.node import FpgaRegionNode, DeviceTreeRootNode

import argparse
import pathlib

def generate_device_tree_overlay(sopcinfo_file, rbf_file, output_dir = ""):
    """Runs the device tree generation process
    """
    sopcinfo_file = sopcinfo_file.replace("\\\\", "\\")
    output_dir = pathlib.Path(output_dir)
    rbf_file = str(pathlib.Path(rbf_file).with_suffix(".rbf"))
    dts_file = pathlib.Path(rbf_file).with_suffix(".dts")

    nodes = parser(sopcinfo_file)
    fpga_region_node = FpgaRegionNode(
        "base_fpga_region", rbf_file, "base_fpga_region", nodes)
    dtroot = DeviceTreeRootNode([fpga_region_node])

    with open(str(output_dir.joinpath(dts_file)), "w") as out_file:
        out_file.write(str(dtroot))

def parseargs():

    parser = argparse.ArgumentParser(
        description="Generates a device tree overlay file")
    parser.add_argument('-s', '--sopcinfo',
                        help="Path to sopcinfo file containing description of Platform Designer system")
    parser.add_argument('-r', '--rbf',
                        help="Name of programming file for the fpga")
    parser.add_argument('-o', '--output-dir', default="", required=False,
                        help="Output directory for the dts file")
    args = parser.parse_args()
    return (args.sopcinfo, args.rbf, args.output_dir)

if __name__ == "__main__":
    (sopcinfo, rbf, output_dir) = parseargs()
    generate_device_tree_overlay(sopcinfo, rbf, output_dir)
