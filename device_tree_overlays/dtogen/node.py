from abc import ABC, abstractmethod


class AbstractNode(ABC):
    def __init__(self, name, label=None, parent=None, children=[]):
        self.name = name
        self.label = label
        self.parent = parent
        self._default_format = True
        self.tab_amount = 4
        self._children = []
        if children:
            # make sure children is a list
            if not isinstance(children, list):
                children = [children]

            self.add_children(*children)

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        # we are overwriting the children list, so start with an empty list
        self._children = []

        # make sure children is a list
        if not isinstance(children, list):
            children = [children]

        self.add_children(*children)

    # NOTE: instead of having this method, we could instead make users call device_tree_node.children.append(); I'm not sure which way is preferable.
    def add_children(self, *args):
        for child in args:
            if isinstance(child, AbstractNode):
                child.parent = self
                self._children.append(child)
            else:
                raise TypeError("child is not a device tree node object")

    @abstractmethod
    def _print_properties(self):
        return NotImplemented

    def __str__(self):
        s = ''

        # XXX: maybe we could handle the base device tree references in a cleaner way than just checking if the node doesn't have a parent. Just because a node doesn't have a parent doesn't mean that the node is being inserted at a label in the base device tree. The node could need to be inserted into the root of the base device tree, for example.
        if self.parent is None:
            # if the node doesn't have a parent, reference a base device tree label for tree insertion

            # TODO: name is a required argument, so I'm using it for the label here, but maybe it would make more sense to use label instead? But labels aren't required in general.
            s += '&' + self.name + ' {\n'
        else:
            # if the node has a parent, we don't need to reference a label in the base device tree
            if self._default_format:
                if self.label is not None:
                    s += self.label + ': '
                s += self.name + ' {\n'

        s += self._print_properties()
        for child in self._children:
            s += child.tab_amount*' ' + str(child).replace('\n', '\n' + child.tab_amount*' ') + '\n'
        if self._default_format:
            s += '};'

        return s
    @staticmethod
    def hex(__i, length = 8):
        hex_str = hex(__i)[2:]
        padding = (8-len(hex_str)) * '0'
        return f"0x{padding}{hex_str}"


class Node(AbstractNode):
    def __init__(self, name, label=None, parent=None,
                 children=None, compatible=None):
        super().__init__(name=name, label=label, parent=parent, children=children)

        self.compatible = compatible

    def _print_properties(self):
        s = ''
        if self.compatible is not None:
            # TODO: make tab size a variable
            s += self.tab_amount *' ' + 'compatible = "{}";\n'.format(self.compatible)

        return s


class FpgaRegionNode(Node):
    def __init__(self, name, firmware_name, label=None,
                 children=None, compatible=None, status=None):
        super().__init__(name, label=label, children=children, compatible=compatible)
        self.firmware_name = firmware_name
        self.status = status

    def _print_properties(self):
        s = ''
        s += super()._print_properties()
        s += self.tab_amount *' ' + 'firmware-name = "{}";\n'.format(self.firmware_name)
        if self.status is not None:
            s += self.tab_amount *' ' + 'status = "{}";\n'.format(self.status)

        return s

class MemoryMappedNode(Node):
    def __init__(self, name, base_addr, span, label=None, parent=None,
                 children=None, compatible=None):
        super().__init__(name, label=label, parent=parent, children=children, compatible=compatible)
        self.base_addr = base_addr
        self.span = span

class MemoryBridgeNode(MemoryMappedNode):
    def __init__(self, name, base_addr, span, index=None, label=None, parent=None,
                 children=None, compatible=None):
        super().__init__(name, base_addr, span, label=label, parent=parent, children=children, compatible=compatible)
        self.index = index
        self._default_format = False
        self.tab_amount = 0

    def _print_properties(self):
        return ''

class MemoryMappedSlaveNode(MemoryMappedNode):
    def __init__(self, name, base_addr, span, index=None, label=None, parent=None,
                 children=None, compatible=''):
        super().__init__('', base_addr, span, label=label, parent=parent, children=children, compatible=compatible)
        self.index = index

        base_addr_str = self.hex(self.base_addr)[2:]
        self._name = name
        self.name = f"{self._name}@0x{self.index or ''}{base_addr_str}"
    def _print_properties(self):
        s = ""
        s += f"{self.tab_amount*' '}compatible = {self.compatible};\n"
        s += f"{self.tab_amount*' '}reg = <{self.hex(self.index)} {self.hex(self.base_addr)} {self.hex(self.span)}>;\n"
        return s
class BridgeRootNode(Node):
    def __init__(self, name, label=None, parent=None, children=None, compatible=None):
        super().__init__(name, label=label, children=children, compatible=compatible)
    def _print_properties(self):
        s = ''
        # This specifies reg values in children will be with the bridge number
        # and the untranslated base address 
        s += self.tab_amount*' ' +'#address-cells = <2>;\n'
        # A single value will be given for the span of the register on children
        s += self.tab_amount*' ' +'#size-cells = <1>;\n'

        s += self.tab_amount*' ' +'ranges = '
        for i in range(len(self.children)):
            bridge = self.children[i]
            if len(bridge.children) == 0:
                s += f"< {self.hex(bridge.index)} {self.hex(0)} {self.hex(bridge.base_addr)} {self.hex(bridge.span)}>"
                if (i == len(self.children) - 1):
                    s += ';\n'
                else:
                    s += ',\n' + self.tab_amount * 2 * ' '
            for j in range(len(bridge.children)):
                child = bridge.children[j]
                s += '<' + self.hex(bridge.index) + ' '
                s += self.hex(child.base_addr) + ' '
                s += self.hex(child.base_addr + bridge.base_addr) + ' '
                s += self.hex(child.span) + '>'
                if (i == len(self.children) - 1) and (j == len(bridge.children) - 1):
                    s += ';\n'
                else:
                    s += ',\n' + self.tab_amount * 2 * ' '
        return s
       