import unittest

from dtogen.node import Node


class TestNode(unittest.TestCase):
    def test_top_level_node(self):
        expected = (
            '&name {\n'
            '    compatible = "dev,test";\n'
            '};'
        )

        n = Node(name='name', label='label', compatible='dev,test')

        self.assertEqual(expected, str(n))

    def test_one_child_node(self):
        expected = (
            '&i2c {\n'
            '    compatible = "dev,i2c";\n'
            '    adc0: adc {\n'
            '        compatible = "dev,adc";\n'
            '    };\n'
            '};'
        )

        i2c = Node(name='i2c', compatible='dev,i2c')
        adc0 = Node(name='adc', label='adc0', compatible='dev,adc')

        i2c.children = adc0

        self.assertEqual(expected, str(i2c))

    def test_two_child_nodes(self):
        expected = (
            '&i2c {\n'
            '    compatible = "dev,i2c";\n'
            '    adc0: adc {\n'
            '        compatible = "dev,adc";\n'
            '    };\n'
            '    eeprom0: eeprom {\n'
            '        compatible = "dev,eeprom";\n'
            '    };\n'
            '};'
        )

        i2c = Node(name='i2c', compatible='dev,i2c')
        adc0 = Node(name='adc', label='adc0', compatible='dev,adc')
        eeprom0 = Node(name='eeprom', label='eeprom0', compatible='dev,eeprom')

        i2c.children = [adc0, eeprom0]

        self.assertEqual(expected, str(i2c))

    def test_nested_child_nodes(self):
        expected = (
            '&parent {\n'
            '    compatible = "parent";\n'
            '    child0: child {\n'
            '        compatible = "child";\n'
            '        child1: child {\n'
            '            compatible = "child";\n'
            '        };\n'
            '    };\n'
            '};'
        )

        parent = Node(name='parent', compatible='parent')
        child0 = Node(name='child', label='child0', compatible='child')
        child1 = Node(name='child', label='child1', compatible='child')

        parent.children = [child0]
        child0.children = [child1]

        self.assertEqual(expected, str(parent))


if __name__ == "__main__":
    unittest.main()
