"""Test rdiffb.canonicalizer_with_memory.py."""

import unittest

from rdflib import Graph
from rdiffb.canonicalizer_with_memory import CanonicalizerWithMemory


class TestCanonicalizerWithMemory(unittest.TestCase):
    """Test CanonicalizerWithMemory class."""

    def test01_create(self):
        """Creation test, check map."""
        cwm = CanonicalizerWithMemory(Graph())
        self.assertTrue(cwm)
        self.assertEqual(len(cwm.bnode_map), 0)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCanonicalizerWithMemory)
    unittest.TextTestRunner(verbosity=2).run(suite)
