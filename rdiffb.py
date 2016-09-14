#!/usr/bin/env python
"""
rbdiff: RDF diff with bnode handling command line utility.

Copyright 2016

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License
"""

import logging
import optparse
import sys

from rdflib import __version__ as rdflib_version, Graph
from rdflib.compare import isomorphic, to_isomorphic, graph_diff, to_canonical_graph
from rdflib.util import guess_format
from rdflib.term import BNode, URIRef

import rdiffb
from rdiffb.canonicalizer_with_memory import CanonicalizerWithMemory
from rdiffb.bnode_mapper import nt_sorted, serialize_equalish, to_bnodes, from_bnodes_triple, from_bnodes


def main():
    """Command line client."""
    if (sys.version_info < (2, 6)):
        sys.exit("This program requires python version 2.6 or later")
    if (rdflib_version < "4.2.0"):
        sys.exit("This program requires rdflib >= 4.2.0 for correct "
                 "rdflib.compare using the RDGA1 algorithm")

    # Options and arguments
    p = optparse.OptionParser(description='rbdiff command line client',
                              usage='usage: %prog [options] uri_path local_path  (-h for help)',
                              version='%prog ' + rdiffb.__version__)

    p.add_option('--bnode', '-b', action='append', default=[],
                 help="add a regex for URIs that should be treated like bnodes "
                      "in diffs (repeatable)")
    p.add_option('--report-isomorphic-graphs', '-s', action='store_true',
                 help="report if the input RDF graphs are isomorphic (after any bnode substitution)")
    p.add_option('--verbose', '-v', action='store_true',
                 help="verbose, show additional informational messages")
    p.add_option('--debug', '-d', action='store_true',
                 help="very verbose output")

    (opt, args) = p.parse_args()

    # use --verbose & --debug to set up logging level
    level = logging.DEBUG if opt.debug else logging.INFO if opt.verbose else logging.WARN
    logging.basicConfig(level=level, format='%(message)s')

    if (len(args) != 2):
        sys.exit("Two arguments required")

    graphs = []
    mappings = []
    num_subs = 0
    for filename in args:
        fmt = guess_format(filename)
        logging.info("Reading %s as %s..." % (filename, fmt))
        graph = Graph().parse(filename, format=fmt)
        logging.debug("... got %d triples" % (len(graph)))
        mapping = dict()
        for pattern in opt.bnode:
            logging.debug("Looking for pattern %s" % (pattern))
            graph, subs, this_mapping = to_bnodes(graph, pattern)
            num_subs += subs
            mapping.update(this_mapping)
        logging.debug("Complete mapping: " + str(mapping))
        cwm = CanonicalizerWithMemory(graph)
        graph = cwm.canonical_graph()
        graphs.append(graph)
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
        mappings.append(mapping)

    in_both, in_first, in_second = graph_diff(graphs[0], graphs[1])

    num_same = len(in_both)
    num_diff = len(in_first) + len(in_second)
    pct_same = num_same * 200.0 / (num_diff + 2 * num_same)
    if (num_diff == 0):
        if (opt.report_isomorphic_graphs):
            sub_note = ' after bnode substitutions' if (num_subs > 0) else ''
            sys.stdout.write("Graphs %s and %s are isomorphic%s\n" % (args[0], args[1], sub_note))
    else:
        logging.info(
            "%d triples are shared by the two graphs (%.1f%%)" %
            (num_same, pct_same))
        logging.info(serialize_equalish(in_both, mappings))
    # Normal diff outout for < and >
    if (len(in_first) > 0):
        logging.debug("In first only:")
        sys.stdout.write(nt_sorted(from_bnodes(in_first, mappings[0]), '<  ') + "\n")
    if (len(in_second) > 0):
        logging.debug("In second only:")
        sys.stdout.write(nt_sorted(from_bnodes(in_second, mappings[1]), '>  ') + "\n")

    # Exit status: 0 if same, 1 if different
    sys.exit(1 if (num_diff > 0) else 0)

if __name__ == '__main__':
    main()
