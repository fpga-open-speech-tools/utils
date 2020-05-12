class DeviceTreeNode():
    def __init__(self, name, label=None, parent=None, children=None, compatible=None):
        self.name = name
        self.label = label
        self.parent = parent


        if children is None:
            self._children = []
        else:
            # TODO: check if children are valid objects then add to the list
            #       it'd be nice to not repeat this type checking code everywhere
            pass

        # TODO: compatible should be a list of strings
        self.compatible = compatible
        

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        # we are overwriting the children list, so start with an empty list
        self._children = []

        # TODO: a single DeviceTreeNode isn't iterable, so this raises an exception unless we explicitly pass in children as a list
        for child in children:
            if isinstance(child, DeviceTreeNode):
                child.parent = self
                self._children.append(child)
            else:
                raise TypeError("child is not a DeviceTreeNode")

    # NOTE: instead of having this method, we could instead make users call device_tree_node.children.append(); I'm not sure which way is preferable. 
    def add_children(self, children):
        for child in children:
            if isinstance(child, DeviceTreeNode):
                child.parent = self
                self._children.append(child)
            else:
                raise TypeError("child is not a DeviceTreeNode")
            
    
    def __str__(self):
        s = ''
        if self.label is not None:
            s += self.label + ': '
        s += self.name + ' {\n'
        if self.compatible is not None:
            # TODO: make tab size a variable
            s += 4*' ' + 'compatible = "{}";\n'.format(self.compatible)

        for child in self._children:
            s += 4*' ' + str(child).replace('\n', '\n' + 4*' ') + '\n'

        # TODO: From a subclass, I'd like to call the base class' __str__ method first, then the subclass' __str__ method would fill in the rest of the details that the base class doesn't know about. However, this ending brace will mess that up...
        s += '};'


        return s
        

    
    