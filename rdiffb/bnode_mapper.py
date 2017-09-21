"""Functions for mapping to and from bnodes."""

import logging
from rdflib import Graph
from rdflib.term import BNode, URIRef
from rdflib.plugins.serializers.nt import _nt_row
import re


def nt_sorted(g, prefix=''):
    """Linewise sort ntriples serialization, with optional prefix.

    Does not include a trailing return character.
    """
    s = ''
    for line in sorted(g.serialize(format='nt').splitlines()):
        if line:
            s += '\n' if (s) else ''
            s += prefix + line.decode('utf-8')
    return s


def serialize_equalish(in_both, mappings):
    """Return string for triples that matched.

    Although triples "match", they may not come from the same orginal
    triples so do inverse mapping for each source graph.

    WARNING - uses _nt_row() from rdflib.plugins.serializers.nt which is
    a bit naughty. However, to avoid this it is necessary either to build
    a graph for each triple to be written, or to write another copy of
    the serialization code.
    """
    s = ''
    for triple in in_both:
        triple_in_first = from_bnodes_triple(triple, mappings[0])
        triple_in_second = from_bnodes_triple(triple, mappings[1])
        if (triple_in_first == triple_in_second):
            s += '== ' + _nt_row(triple_in_first)
        else:
            s += '=< ' + _nt_row(triple_in_first)
            s += '=> ' + _nt_row(triple_in_second)
    return s


def to_bnodes(graph, pattern):
    """Convert any URIs in graph matching pattern to bnodes.

    Parameters:
        graph -- input graph to map
        pattern -- a regex to be used with regex.search() on the string
            representations of subject and predicate terms in graph
    Returns:
        new_graph -- modified graph
        subs -- number of term substitutions made
        mapping -- dict with mapping of original URIRef -> BNode
    """
    new_graph = Graph()
    mapping = dict()
    regex = re.compile(pattern)
    logging.debug("Looking for %s in graph" % (str(regex)))
    subs = 0
    for s, p, o in graph:
        if (isinstance(s, URIRef)):
            if (s in mapping):
                s = mapping[s]
                subs += 1
            elif (regex.search(str(s))):
                mapping[s] = BNode()
                s = mapping[s]
                subs += 1
        if (isinstance(o, URIRef)):
            logging.debug("node %s %s %s" % (str(s), str(p), str(o)))
            if (o in mapping):
                o = mapping[o]
                subs += 1
            elif (regex.search(str(o))):
                mapping[o] = BNode()
                o = mapping[o]
                subs += 1
        new_graph.add((s, p, o))
    logging.debug("mapping: %s, made %d subs" % (str(mapping), subs))
    return new_graph, subs, mapping


def from_bnodes_triple(triple, mapping):
    """Convert bnodes back to original URI if listed in mapping, for one triple.

    Parameters:
      triple -- a single triple as tuple (s, p, o)
      mapping -- a dictionary that maps from the current node values
    to the desired ones.

    Returns:
      (s, p, o) -- tuple of possibly modified triple
    """
    s, p, o = triple
    if (s in mapping):
        s = mapping[s]
    if (o in mapping):
        o = mapping[o]
    return((s, p, o))


def from_bnodes(graph, mapping):
    """Convert bnodes back to original URI if listed in mapping."""
    new_graph = Graph()
    for triple in graph:
        new_graph.add(from_bnodes_triple(triple, mapping))
    return new_graph
