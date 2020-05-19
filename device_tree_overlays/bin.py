from dtogen.parser import parser
import os
def main():
    print(os.getcwd())
    nodes = parser('dtogen/arria10_system.sopcinfo', 'arria10_hps_0_bridges', 'h2f_lw')
    for node in nodes:
        print(node)
    pass

if __name__ == "__main__":
    main()