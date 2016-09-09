# rdiffb - RDF diff with convenient bnode treatment

[![Build Status](https://travis-ci.org/zimeon/rdiffb.svg?branch=master)](https://travis-ci.org/zimeon/rdiffb)

## Problem statement

As part of the [LD4L](http://ld4l.org/) Labs project we want a continuous integration environment for conversion of MARC21 bibliographic records into BIBFRAME or LD4L Ontology RDF data. To test against hand-crafted test cases we want an RDF comparison that will handle isomorphism of graphs both with bnodes and with certain other URIs that may be generated in conversion but should be treated like bnodes. This could be handled by doing a URI -> bnode conversion for certain patterns beforehand but we might hope for more useful debigging output if the understanding is integrated.

## Existing work

  * [https://www.w3.org/2001/sw/wiki/How_to_diff_RDF]
  * [https://groups.google.com/forum/#!topic/thosch/SR902daW0LI]
  * [https://sourceforge.net/projects/knobot/files/rdf-utils/] 
  * [http://rdflib3.readthedocs.io/en/latest/apidocs/rdflib.html#module-rdflib.compare]

## Notes

  * [Beware old versions of rdflib -- upgrade!](beware_old_rdflib.md)