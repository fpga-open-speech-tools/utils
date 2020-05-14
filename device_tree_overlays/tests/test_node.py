import unittest
import textwrap

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
        self.fail()

    def test_two_child_nodes(self):
        self.fail()

    def test_nested_child_nodes(self):
        self.fail()


if __name__ == "__main__":
    unittest.main()
