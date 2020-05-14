from abc import ABC, abstractmethod


class AbstractNode(ABC):
    def __init__(self, name, label=None, parent=None, children=[]):
        self.name = name
        self.label = label
        self.parent = parent

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
            if self.label is not None:
                s += self.label + ': '
            s += self.name + ' {\n'

        s += self._print_properties()

        for child in self._children:
            s += 4*' ' + str(child).replace('\n', '\n' + 4*' ') + '\n'

        s += '};'

        return s


class Node(AbstractNode):
    def __init__(self, name, label=None, parent=None,
                 children=None, compatible=None):
        super().__init__(name=name, label=label, parent=parent, children=children)

        self.compatible = compatible

    def _print_properties(self):
        s = ''
        if self.compatible is not None:
            # TODO: make tab size a variable
            s += 4*' ' + 'compatible = "{}";\n'.format(self.compatible)

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
        s += 4*' ' + 'firmware-name = "{}";\n'.format(self.firmware_name)
        if self.status is not None:
            s += 4*' ' + 'status = "{}";\n'.format(self.status)

        return s
