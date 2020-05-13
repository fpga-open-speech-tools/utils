from .node import Node

class FpgaRegionNode(Node):
    def __init__(self, name, firmware_name, label=None, children=None, compatible=None, status=None):
        super().__init__(name, label=label, children=children, compatible=compatible)
        self.firmware_name = firmware_name
        self.status = status

    def _print_properties(self):
        s = ''
        s += super()._print_properties()
        s += 4*' ' + 'firmware-name = "{}";\n'.format(self.firmware_name)
        if self.status is not None:
            s += 4*' ' + 'status = "{}";\n'.format(self.status)
        
        return s