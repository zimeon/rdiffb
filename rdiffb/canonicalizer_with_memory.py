"""Create canonical graph and remember bnode id canonicalization.

This code subclasses rdflib.compare._TripleCanonicalizer in order
add storage for the bnode id changes, and to store each change.

WARNING - This code is critically dependent upon the internal
structure of the base class rdflib.compare._TripleCanonicalizer
and this is not a published interface --- IT MAY BREAK WITH A 
NEW VERSION OF rdflib (created with v4.2.1 2016-09-09).
"""

from rdflib.graph import Graph, ConjunctiveGraph, ReadOnlyGraphAggregate
from rdflib.term import BNode, Node
from rdflib.compare import _TripleCanonicalizer

class CanonicalizerWithMemory(_TripleCanonicalizer):

    def __init__(self, graph, **kwargs):
        """Initialize instance, add bnode_map."""
        super(CanonicalizerWithMemory, self).__init__(graph, **kwargs)
        self.bnode_map = dict()

    def _canonicalize_bnodes(self, triple, labels):
        """Assign new bnode ids based on canonical labels.

        WARNING - This method overrides the method of the same name
        in rdflib.compare._TripleCanonicalizer --- IT MAY BREAK WITH
        A NEW VERSION OF rdflib (created with v4.2.1).

        For each bnode id change, the map from new_id to old_id is
        recorded in self.bnode_map.
        """
        for term in triple:
            if isinstance(term, BNode):
                # FIXME - it is a bit inefficient to do this here as we
                # FIXME - set the value in the bnode_map dict() every time
                # FIXME - the mapping is used. However, since this is where
                # FIXME - in the code the full id is generated it seems the
                # FIXME - cleanest place to put it. Otherwise we'd have to 
                # FIXME - duplicate the id construction from label[..]
                old_id = str(term)
                new_id = "cb%s" % labels[term]
                self.bnode_map[new_id] = old_id
                #print(old_id + ' --> ' + new_id)
                yield BNode(value=new_id)
            else:
                yield term

    def canonical_graph(self, g1):
        """Creates a canonical, read-only graph.

        Modification of rdflib.compare.to_canonical_graph that is instead
        made as a method of CanonicalizerWithMemory so that we can access
        the store of bnode relabelings made during the canonicalization.

        Creates a canonical, read-only graph where all bnode id's are based on
        deterministical SHA-256 checksums, correlated with the graph contents.

        As a side-effect, self.bnode_map will be populated with a mapping
        from new bnode ids to old bnode ids (see _canonicalize_bnodes).
        """
        graph = Graph()
        graph += self.canonical_triples()
        return ReadOnlyGraphAggregate([graph])