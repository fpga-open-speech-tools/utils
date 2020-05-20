from dtogen.parser import parser

def main():
    """Runs the device tree generation process
    """
    nodes = parser('dtogen/arria10_system.sopcinfo')
    for node in nodes:
        print(node)
    pass

if __name__ == "__main__":
    main()