"""Test rdiffb.rdiffb.py."""

import unittest
from rdflib import Graph, URIRef, BNode
from rdiffb import RDiffB
try:  # python2
    # Must try this first as io also exists in python2
    # but is the wrong one!
    import StringIO as io
except ImportError:  # python3
    import io


class TestRDiffB(unittest.TestCase):
    """Test BRDiffB class."""

    def test01_init(self):
        """Simple init test."""
        rdb = RDiffB()
        self.assertEqual(rdb.bnodes, [])
        rdb = RDiffB(['aa', 'bb'])
        self.assertEqual(rdb.bnodes, ['aa', 'bb'])

    def test02_load_graph(self):
        """Load graph from file."""
        g = RDiffB().load_graph('examples/102063.rdf')
        self.assertEqual(len(g), 71)

    def test03_map_patterns_and_canonicalize(self):
        """Test mapping."""
        gg = Graph()
        gg += [(URIRef(u's1'), URIRef(u'p1'), URIRef(u'o1')),
               (URIRef(u's1'), URIRef(u'p2'), URIRef(u'o2')),
               (URIRef(u's2'), URIRef(u'p1'), URIRef(u'o1')),
               (URIRef(u's3'), URIRef(u'p3'), URIRef(u'o3'))]
        (g, m) = RDiffB().map_patterns_and_canonicalize(gg)
        self.assertEqual(len(g), 4)
        self.assertEqual(len(m), 0)
        (g, m) = RDiffB(['s1']).map_patterns_and_canonicalize(gg)
        self.assertEqual(len(m), 1)
        (g, m) = RDiffB(['s1', 's2']).map_patterns_and_canonicalize(gg)
        self.assertEqual(len(m), 2)
        (g, m) = RDiffB(['p1', 'p2']).map_patterns_and_canonicalize(gg)
        self.assertEqual(len(m), 0)  # don't map predicates
        (g, m) = RDiffB(['s.*']).map_patterns_and_canonicalize(gg)
        self.assertEqual(len(g), 4)

    def test04_compare_files(self):
        """Test file load and comparison."""
        rdb = RDiffB()
        num_diff = rdb.compare_files(['examples/102063.rdf', 'examples/102063.rdf'])
        self.assertEqual(num_diff, 0)
        rdb = RDiffB()
        num_diff = rdb.compare_files(['examples/102063.rdf', 'examples/102063_bad.rdf'])
        self.assertEqual(num_diff, 1)
        self.assertEqual(len(rdb.in_first), 1)
        self.assertEqual(len(rdb.in_second), 0)
        self.assertEqual(len(rdb.in_both), 70)

    def test05_compare_graphs(self):
        """Test direct graph comparison."""
        rdb = RDiffB(['o1'])
        g1 = Graph()
        bnode1 = BNode()
        g1 += [(URIRef(u'a/s1'), URIRef(u'p1'), bnode1),
               (bnode1, URIRef(u'p2'), URIRef(u'b/o2'))]
        g2 = Graph()
        g2 += [(URIRef(u'a/s1'), URIRef(u'p1'), URIRef(u'o1')),
               (URIRef(u'o1'), URIRef(u'p2'), URIRef(u'b/o2'))]
        num_diff = rdb.compare_graphs([g1, g2])
        self.assertEqual(num_diff, 0)
        self.assertEqual(len(rdb.in_first), 0)
        self.assertEqual(len(rdb.in_second), 0)
        self.assertEqual(len(rdb.in_both), 2)

    def test06_write_diff_same(self):
        """Test write_diff where graphs match."""
        rdb = RDiffB()
        rdb.filenames = ['g1', 'g2']
        g = Graph()
        g += [(URIRef(u's1'), URIRef(u'p1'), URIRef(u'o1')),
              (URIRef(u's1'), URIRef(u'p2'), URIRef(u'o2')),
              (URIRef(u's2'), URIRef(u'p1'), URIRef(u'o1'))]
        rdb.mappings = [dict(), dict()]
        rdb.in_both = g
        rdb.in_first = Graph()
        rdb.in_second = Graph()
        fh = io.StringIO()
        # Silent by default
        rdb.write_diff(fh)
        self.assertEqual(fh.getvalue(), '')
        # Note if report_isomorphic set True
        rdb.write_diff(fh, report_isomorphic=True)
        self.assertIn('Graphs g1 and g2 are isomorphic', fh.getvalue())
        self.assertNotIn('after bnode substitutions', fh.getvalue())
        # and substitution note
        fh = io.StringIO()
        rdb.num_subs = 1
        rdb.write_diff(fh, report_isomorphic=True)
        self.assertIn('Graphs g1 and g2 are isomorphic', fh.getvalue())
        self.assertIn('after bnode substitutions', fh.getvalue())

    def test06_write_diff_diff(self):
        """Test write_diff where graphs do not match."""
        rdb = RDiffB()
        rdb.filenames = ['g1', 'g2']
        gf = Graph()
        gf += [(URIRef(u's1'), URIRef(u'p1'), URIRef(u'o1'))]
        gs = Graph()
        gs += [(URIRef(u's2'), URIRef(u'p2'), URIRef(u'o2'))]
        rdb.mappings = [dict(), dict()]
        rdb.in_both = Graph()
        rdb.in_first = gf
        rdb.in_second = gs
        fh = io.StringIO()
        # No mappings
        rdb.write_diff(fh)
        self.assertIn('>  <s2> <p2> <o2> .', fh.getvalue())
        self.assertIn('<  <s1> <p1> <o1> .', fh.getvalue())
        # Now with a mapping
        # FIXME


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRDiffB)
    unittest.TextTestRunner(verbosity=2).run(suite)
