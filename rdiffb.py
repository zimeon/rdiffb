#!/usr/bin/env python
"""
rbdiff: RDF diff with bnode handling command line utility

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

import rdiffb

def nt_sorted(g, prefix=''):
    """Linewise sort ntriples serialization, with optional prefix."""
    s = ''
    for line in sorted(g.serialize(format='nt').splitlines()):
        if line:
            s += prefix + line.decode('utf-8') + "\n"
    return s

def main():

    if (sys.version_info < (2,6)):
        sys.exit("This program requires python version 2.6 or later")
    if (rdflib_version < "4.2.0"):
        sys.exit("This program requires rdflib >= 4.2.0 for correct "
                 "rdflib.compare using the RDGA1 algorithm")
    
    # Options and arguments
    p = optparse.OptionParser(description='rbdiff command line client',
                              usage='usage: %prog [options] uri_path local_path  (-h for help)',
                              version='%prog '+rdiffb.__version__ )

    p.add_option('--bnode', '-b', action='append', default=[],
                 help="add a regex for URIs that should be treated like bnodes "
                      "in diffs (repeatable)")
    p.add_option('--verbose', '-v', action='store_true',
                 help="verbose, show additional informational messages")
    p.add_option('--debug', '-d', action='store_true',
                 help="very verbose output")

    (opt, args) = p.parse_args()

    # use --verbose & --debug to set up logging level
    level = logging.DEBUG if opt.debug else logging.INFO if opt.verbose else logging.WARN
    logging.basicConfig(level=level, format='%(message)s')

    if (len(args)!=2):
        sys.exit("Two arguments required")

    graphs = []
    for filename in args:
        fmt = guess_format(filename)
        logging.info("Reading %s as %s..." % (filename, fmt))
        graph = Graph().parse(filename, format=fmt)
        logging.debug("... got %d triples" % (len(graph)))
        graph = to_canonical_graph(graph)
        graphs.append(graph)

    in_both, in_first, in_second = graph_diff(graphs[0], graphs[1])

    same = len(in_both)
    diff = len(in_first) + len(in_second)
    pct_same = same * 200.0 / ( diff + 2 * same)
    logging.info("%d triples are shared by the two graphs (%.1f%%)" % (same, pct_same))
    logging.info("Shared:")
    logging.info(nt_sorted(in_both, '= '))
    if (len(in_first)>0):
        logging.info("In first only:")
        sys.stdout.write(nt_sorted(in_first, '< '))
    if (len(in_second)>0):
        logging.info("In second only:")
        sys.stdout.write(nt_sorted(in_second, '> '))

    # Exit status: 0 if same, 1 if different
    sys.exit(1 if (diff>0) else 0)

if __name__ == '__main__':
    main()
