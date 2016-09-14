"""Test rdiffb.bnode_mapper.py."""

import unittest

from rdflib import Graph, URIRef, BNode
from rdiffb.bnode_mapper import to_bnodes, from_bnodes_triple, from_bnodes


class TestBNodeMapper(unittest.TestCase):
    """Test BNodeMapper class."""

    def test01_to_bnode(self):
        """BNode mapping loadTestsFromTestCase."""
        g = Graph()
        g += [(URIRef(u'http://example.org/a/s'),
               URIRef(u'http://example.org/a/p'),
               URIRef(u'http://example.org/a/o')),
              (URIRef(u'http://example.org/b/s'),
               URIRef(u'http://example.org/b/p'),
               URIRef(u'http://example.org/b/o'))]
        gb, subs, mapping = to_bnodes(g, 'http://example.org/a/')
        self.assertEqual(len(gb), 2)
        self.assertEqual(subs, 2)
        self.assertEqual(len(mapping), 2)
        self.assertTrue(URIRef(u'http://example.org/a/s') in mapping)
        self.assertTrue(URIRef(u'http://example.org/a/o') in mapping)
        for s,p,o in gb.triples((None, URIRef(u'http://example.org/a/p'), None)):
            self.assertTrue(isinstance(s, BNode))
            self.assertTrue(isinstance(o, BNode))

    def test02_from_bnodes_triple(self):
        """Test mapping of single triple with BNode."""
        b1 = BNode()
        b2 = BNode()
        mapping = dict()
        mapping[b1] = URIRef(u'sss')
        mapping[b2] = URIRef(u'ooo')
        s, p, o = from_bnodes_triple((b1, b2, b2), mapping)
        self.assertEqual(s, URIRef(u'sss'))
        self.assertEqual(p, b2)  # no change
        self.assertEqual(o, URIRef(u'ooo'))


    def test03_from_bnodes(self):
        """Test mapping of graph with BNodes."""
        b1 = BNode()
        b2 = BNode()
        mapping = dict()
        mapping[b1] = URIRef(u'http://example.org/e/s')
        mapping[b2] = URIRef(u'http://example.org/f/o')
        g = Graph()
        g += [(b1,
               URIRef(u'http://example.org/e/p'),
               URIRef(u'http://example.org/e/o')),
              (URIRef(u'http://example.org/f/s'),
               URIRef(u'http://example.org/f/p'),
               b2)]
        g2 = from_bnodes(g, mapping)
        self.assertEqual(len(g2), 2)
        for s,p,o in g2.triples((None, URIRef(u'http://example.org/e/p'), None)):
            self.assertEqual(s, URIRef(u'http://example.org/e/s'))
            self.assertEqual(o, URIRef(u'http://example.org/e/o'))
        for s,p,o in g2.triples((None, URIRef(u'http://example.org/f/p'), None)):
            self.assertEqual(s, URIRef(u'http://example.org/f/s'))
            self.assertEqual(o, URIRef(u'http://example.org/f/o'))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBNodeMapper)
    unittest.TextTestRunner(verbosity=2).run(suite)
