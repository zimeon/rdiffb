"""Test rdiffb.canonicalizer_with_memory.py."""

import unittest

from rdflib import Graph, URIRef, BNode
from rdiffb.canonicalizer_with_memory import CanonicalizerWithMemory


class TestCanonicalizerWithMemory(unittest.TestCase):
    """Test CanonicalizerWithMemory class."""

    def test01_create(self):
        """Creation test, check map."""
        cwm = CanonicalizerWithMemory(Graph())
        self.assertTrue(cwm)
        self.assertEqual(len(cwm.bnode_map), 0)

    def test02_one_triple_graph(self):
        """Check map of one bnode."""
        g = Graph()
        old_bnode = BNode('12345')
        g += [ (URIRef(u's'), URIRef(u'p'), old_bnode) ]
        cwm = CanonicalizerWithMemory(g)
        cg = cwm.canonical_graph()
        self.assertEqual(len(cg), 1)
        # Check map from new BNode to old_bnode
        self.assertEqual(len(cwm.bnode_map), 1)
        s, p, o = next(cg.triples((None, None, None)))
        self.assertEqual(cwm.bnode_map[o], old_bnode)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCanonicalizerWithMemory)
    unittest.TextTestRunner(verbosity=2).run(suite)
