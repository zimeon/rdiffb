"""Functions for mapping to and from bnodes."""

import logging
from rdflib import Graph
from rdflib.term import BNode, URIRef
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


def to_bnodes(graph, pattern):
    """Convert any URIs in graph matching pattern to bnodes.

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
    """Convert bnodes back to original URI if listed in mapping, for one triple."""
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
