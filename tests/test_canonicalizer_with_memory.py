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
        g += [(URIRef(u's'), URIRef(u'p'), old_bnode)]
        cwm = CanonicalizerWithMemory(g)
        cg = cwm.canonical_graph()
        self.assertEqual(len(cg), 1)
        # Check map from new BNode to old_bnode
        self.assertEqual(len(cwm.bnode_map), 1)
        s, p, o = next(cg.triples((None, None, None)))
        self.assertEqual(cwm.bnode_map[o], old_bnode)

    def test03_multi_bnode_graph(self):
        """Check map for a set of bnodes."""
        g = Graph()
        ob1 = BNode('old_bnode_1')
        ob2 = BNode('old_bnode_2')
        ob3 = BNode('old_bnode_3')
        g += [(URIRef(u's'), URIRef(u'p1'), ob1),
              (ob1, URIRef(u'p2'), ob2),
              (ob1, URIRef(u'p3'), ob3)]
        cwm = CanonicalizerWithMemory(g)
        cg = cwm.canonical_graph()
        self.assertEqual(len(cg), 3)
        # Check map from new BNodes to old bnodes
        self.assertEqual(len(cwm.bnode_map), 3)
        gen = cg.triples((None, None, None))
        s, p, o = next(cg.triples((None, URIRef(u'p1'), None)))
        self.assertEqual(cwm.bnode_map[o], ob1)
        s, p, o = next(cg.triples((None, URIRef(u'p2'), None)))
        self.assertEqual(cwm.bnode_map[s], ob1)
        self.assertEqual(cwm.bnode_map[o], ob2)
        s, p, o = next(cg.triples((None, URIRef(u'p3'), None)))
        self.assertEqual(cwm.bnode_map[s], ob1)
        self.assertEqual(cwm.bnode_map[o], ob3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCanonicalizerWithMemory)
    unittest.TextTestRunner(verbosity=2).run(suite)
