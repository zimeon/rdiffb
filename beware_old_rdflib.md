# Beware old versions of rdflib -- upgrade!

When first starting to explore use of [rdflib](http://rdflib.readthedocs.io/) I foolishly didn't check the version I had installed. I read from the documentation of [rdflib.compare](http://rdflib.readthedocs.io/en/latest/apidocs/rdflib.html?highlight=compare#module-rdflib.compare) that [`rdflib.compare.to_canonical_graph`](http://rdflib.readthedocs.io/en/latest/apidocs/rdflib.html?highlight=compare#rdflib.compare.to_canonical_graph):

> Creates a canonical, read-only graph where all bnode id:s are based on deterministical SHA-256 checksums, correlated with the graph contents.

_"Great"_, I thought, that is what I need. However, it seems this works properly only with relatively new versions of `rdflib`. A very simple example program shows the problem:

``` python
# Test of rdflib graph canonicalization
from rdflib import __version__, Graph
from rdflib.compare import to_canonical_graph
print("rdflib version is "+__version__)
# Trivial one-triple graph with bnode object
g = Graph().parse(
    data='<http://example.org/s> <http://example.org/p> _:o.',
    format='turtle')
# Make canonical graph twice over
cg1 = to_canonical_graph(g)
cg2 = to_canonical_graph(g)
print(cg1.serialize(format='nt'))
print(cg2.serialize(format='nt'))
```

When I ran this with system python and whatever `rdflib` I had installed I got:

```
>python --version
Python 2.7.11
>python t1.py 
rdflib version is 4.0.1
<http://example.org/s> <http://example.org/p> _:cb4764a7a63dee9cb1adcd626b8521307f .


<http://example.org/s> <http://example.org/p> _:cbe0f34bc7d8bf2a4321b56b5e6c5c0c48 .


```

which shows that calling `to_canonical_graph` twice on the same input graph gives _different_ bnode ids. This doing a diff on 'canonical' graphs created with `to_canonical_graph` results in all bnodes being reported as different, not at all what I was hoping for.

However, all is good with a more up-to-date version of rdflib (4.2.1) using python2:

``` bash
>python t1.py 
rdflib version is 4.2.1
<http://example.org/s> <http://example.org/p> _:cb0 .


<http://example.org/s> <http://example.org/p> _:cb0 .


```

and python3:

``` bash
(py3)>python --version
Python 3.5.1 :: Continuum Analytics, Inc.
(py3)>python t1.py 
rdflib version is 4.2.1
b'<http://example.org/s> <http://example.org/p> _:cb0 .\n\n'
b'<http://example.org/s> <http://example.org/p> _:cb0 .\n\n'
```

Tests with different tagged versions from the [rdflib source repository](https://github.com/RDFLib/rdflib) show that versions prior to 4.1 show different bnode ids, 4.1.x versions give the same bnode ids, and 4.2.x give the simple `_:cb0` id (bnode ids are still long hashes in more complex graphs). So, the lesson from this story is: **use rdflib >= 4.2.0.**
