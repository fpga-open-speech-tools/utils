from .abstractnode import AbstractNode

class Node(AbstractNode):
    def __init__(self, name, label=None, parent=None, children=None, compatible=None):
           super().__init__(name=name, label=label, parent=parent, children=children)

           self.compatible = compatible
    
    def _print_properties(self):
        s = ''
        if self.compatible is not None:
            # TODO: make tab size a variable
            s += 4*' ' + 'compatible = "{}";\n'.format(self.compatible)

        return s
        

    
    