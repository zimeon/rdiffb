#!/usr/bin/env python
"""
rdfdiffb.py: RDF diff with bnode handling command line utility.

Copyright 2016--2017

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

from rdiffb import __version__ as rdiffb_version, RDiffB
from rdiffb.bnode_mapper import nt_sorted, serialize_equalish, from_bnodes


def main():
    """Command line client."""
    if (sys.version_info < (2, 7)):
        sys.exit("This program requires python version 2.7 or later")
    if (rdflib_version < "4.2.0"):
        sys.exit("This program requires rdflib >= 4.2.0 for correct "
                 "rdflib.compare using the RDGA1 algorithm")

    # Options and arguments
    p = optparse.OptionParser(description='rdfdiffb command line client',
                              usage='usage: %prog [options] uri_path local_path  (-h for help)',
                              version='%prog ' + rdiffb_version)

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
        sys.exit("Two file name arguments required")

    rdb = RDiffB(opt.bnode)
    num_diff = rdb.compare_files(args)
    rdb.write_diff(sys.stdout, opt.report_isomorphic_graphs)

    # Exit status: 0 if same, 1 if different
    sys.exit(1 if (num_diff > 0) else 0)

if __name__ == '__main__':
    main()
