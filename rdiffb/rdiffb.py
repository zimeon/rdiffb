"""RDF diff with bnode handling command line utility."""

import logging
import sys

from rdflib import __version__ as rdflib_version, Graph
from rdflib.compare import isomorphic, to_isomorphic, graph_diff, to_canonical_graph
from rdflib.util import guess_format
from rdflib.term import BNode, URIRef

from .canonicalizer_with_memory import CanonicalizerWithMemory
from .bnode_mapper import nt_sorted, serialize_equalish, to_bnodes, from_bnodes_triple, from_bnodes


class RDiffB(object):
    """RDiffB class implements RDF diff functions with bnode mapping."""

    def __init__(self, bnodes=None):
        """Initialize, optionally with set of bnode patterns."""
        self.bnodes = bnodes if bnodes else []
        self._initialize()

    def _initialize(self):
        # Clear internal data
        self.filenames = []
        self.graphs = []
        self.mappings = []
        self.num_subs = 0
        # results
        self.in_both = None
        self.in_first = None
        self.in_second = None

    @property
    def num_diff(self):
        """Number of triples in difference."""
        return(len(self.in_first) + len(self.in_second))

    def load_graph(self, filename):
        """Load RDF from file to get graph."""
        fmt = guess_format(filename)
        logging.info("Reading %s as %s..." % (filename, fmt))
        graph = Graph().parse(filename, format=fmt)
        logging.debug("... got %d triples" % (len(graph)))
        return(graph)

    def map_patterns_and_canonicalize(self, graph):
        """Map nodes matching patterns in self.bnodes and canonicalize.

        Records the mappings applied, including following changes made
        during the canonicalization process. Returns the modified graph
        and the mapping.
        """
        mapping = dict()
        for pattern in self.bnodes:
            logging.debug("Looking for pattern %s" % (pattern))
            graph, subs, this_mapping = to_bnodes(graph, pattern)
            self.num_subs += subs
            mapping.update(this_mapping)
        logging.debug("Complete mapping: " + str(mapping))
        cwm = CanonicalizerWithMemory(graph)
        graph = cwm.canonical_graph()
        # Merge mapping from patterns with mapping from canonicalization
        mapping = dict((v, k) for k, v in mapping.items())  # invert: bnode -> original URI
        for (new_bnode, old_bnode) in cwm.bnode_map.items():
            if (old_bnode in mapping):
                # We mapped twice, make make from new_bnode -> original
                mapping[new_bnode] = mapping[old_bnode]
                del mapping[old_bnode]
            else:
                # Original was a bnode, just canonicalization mapping
                mapping[new_bnode] = old_bnode
        return(graph, mapping)

    def compare_files(self, filenames):
        """Compare graphs from two RDF files in the filenames list.

        Returns the number of triples that are different after matching
        up bnodes.
        """
        graphs = []
        for filename in filenames:
            graphs.append(self.load_graph(filename))
        return(self.compare_graphs(graphs, filenames))

    def compare_graphs(self, graphs, names=None):
        """Compare two Graph objects given in the graphs list.

        Returns the number of triples that are different after matching
        up bnodes.
        """
        self._initialize()
        if (names is None):
            self.filenames = ['graph1', 'graph2']
        else:
            self.filenames = names
        for g in graphs:
            (graph, mapping) = self.map_patterns_and_canonicalize(g)
            self.graphs.append(graph)
            self.mappings.append(mapping)
        self.in_both, self.in_first, self.in_second = \
            graph_diff(self.graphs[0], self.graphs[1])
        return(self.num_diff)

    def write_diff(self, fh, report_isomorphic=False):
        """Write diff results in human-readable form to fh."""
        num_same = len(self.in_both)
        pct_same = num_same * 200.0 / (self.num_diff + 2 * num_same)
        if (self.num_diff == 0):
            if (report_isomorphic):
                sub_note = ' after bnode substitutions' if (self.num_subs > 0) else ''
                fh.write("Graphs %s and %s are isomorphic%s\n" %
                         (self.filenames[0], self.filenames[1], sub_note))
        else:
            logging.info(
                "%d triples are shared by the two graphs (%.1f%%)" %
                (num_same, pct_same))
            logging.info(serialize_equalish(self.in_both, self.mappings))
            # Normal diff outout for < and >
            if (len(self.in_first) > 0):
                logging.debug("In first only:")
                fh.write(nt_sorted(from_bnodes(self.in_first, self.mappings[0]), '<  ') + "\n")
            if (len(self.in_second) > 0):
                logging.debug("In second only:")
                fh.write(nt_sorted(from_bnodes(self.in_second, self.mappings[1]), '>  ') + "\n")
