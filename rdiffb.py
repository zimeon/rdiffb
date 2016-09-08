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

import optparse
import sys

from rdiffb import __version__
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff


def dump_nt_sorted(g, prefix):
    for l in sorted(g.serialize(format='nt').splitlines()):
        if l: print(prefix + l.decode('ascii'))

def main():

    if (sys.version_info < (2,6)):
        sys.exit("This program requires python version 2.6 or later")
    
    # Options and arguments
    p = optparse.OptionParser(description='rbdiff command line client',
                              usage='usage: %prog [options] uri_path local_path  (-h for help)',
                              version='%prog '+__version__ )

    p.add_option('--verbose', '-v', action='store_true',
                   help="verbose, show additional informational messages")

    (opts, args) = p.parse_args()

    g1 = Graph().parse(format='n3', data='''
     @prefix : <http://example.org/ns#> .
     <http://example.org> :rel
        <http://example.org/same>,
         [ :label "Same" ],
         <http://example.org/a>,
         [ :label "A" ] .
         ''')
    g2 = Graph().parse(format='n3', data='''
      @prefix : <http://example.org/ns#> .
      <http://example.org> :rel
          <http://example.org/same>,
          [ :label "Same" ],
          <http://example.org/a>,
          [ :label "A" ] .
        ''')

    iso1 = to_isomorphic(g1)
    iso2 = to_isomorphic(g2)

    in_both, in_first, in_second = graph_diff(iso1, iso2)

    same = len(in_both)
    pct_same = same * 200.0 / (len(in_first) + len(in_second) + 2 * same)
    print("%d triples are shared by the two graphs (%.1f%%)" % (same,pct_same))
    print("Shared:")
    dump_nt_sorted(in_both,'= ')
    print("In first only:")
    dump_nt_sorted(in_first,'< ')
    print("In second only:")
    dump_nt_sorted(in_second,'> ')

if __name__ == '__main__':
    main()
