# rdiffb - RDF diff with convenient bnode treatment

[![Build Status](https://travis-ci.org/zimeon/rdiffb.svg?branch=master)](https://travis-ci.org/zimeon/rdiffb)
[![Coverage Status](https://coveralls.io/repos/github/zimeon/rdiffb/badge.svg?branch=master)](https://coveralls.io/github/zimeon/rdiffb?branch=master)

## Problem statement

As part of the [LD4L](http://ld4l.org/) Labs project we want a continuous integration environment for conversion of MARC21 bibliographic records into BIBFRAME or LD4L Ontology RDF data. To test against hand-crafted test cases we want an RDF comparison that will handle isomorphism of graphs both with bnodes and with certain other URIs that may be generated in conversion where the exact URI isn't known. It thus seems best to treat some generated URIs like bnodes for testing. This problem could be handled using a two stage process: URI -> bnode conversion for certain patterns, then graph comparison accounting for bnodes (isomorphism). Combining these two stages to keep track of id changes has the promise of more useful debugging information.

## Other work on RDF graph diffs

  * [https://www.w3.org/2001/sw/wiki/How_to_diff_RDF]
  * [https://groups.google.com/forum/#!topic/thosch/SR902daW0LI]
  * [https://sourceforge.net/projects/knobot/files/rdf-utils/] 
  * [http://rdflib3.readthedocs.io/en/latest/apidocs/rdflib.html#module-rdflib.compare]

## Notes

  * [LD4L RDF `diff` Use Case](ld4l_use_case.md) in detail with examples using `rdfdiffb.py`
  * [Beware old versions of rdflib -- upgrade!](beware_old_rdflib.md)