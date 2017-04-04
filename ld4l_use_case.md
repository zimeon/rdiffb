# LD4L RDF `diff` Use Case

Consider an example from the Cornell University Library catalog, say the very exciting [_Clinical cardiopulmonary physiology_](https://newcatalog.library.cornell.edu/catalog/102063) from 1957. I'm going to use this as an example for how we might think about using `rdiffb` to testing [LD4L Labs](https://www.ld4l.org/ld4l-labs/) conversion of the MARC record to the BIBFRAME-based LD4L Labs ontology.

> I'm working with this example because the [LD4All Ontology Working Groups](https://github.com/cul-it/onto-working-docs) have hand-transformed the MARC into the prototype LD4All Target Ontology. The original MARC and transformed data files are at <https://github.com/cul-it/onto-working-docs/tree/master/SampleData/102063>.
>
> All the examples shown here show work when run from the root of a cloned copy of this github repository.

So, starting from the Cornell catalog, we have for this item:

   * [Human readable page](https://newcatalog.library.cornell.edu/catalog/102063)
   * [MARC21](https://newcatalog.library.cornell.edu/catalog/102063.marc)
   * [MARCXML](https://newcatalog.library.cornell.edu/catalog/102063.marcxml)

Let's imagine that we have a MARCXML-to-LD4LAll ontology converter `marcxml_to_ld4lall` that we can run as follows:

``` sh
NOT-REAL> cat examples/102063.marc.xml | marcxml_to_ld4lall > examples/102063.rdf
```

This doesn't exist yet but there is a mockup of possible output [102063.rdf](examples/102063.rdf), which includes a number of generated URIs (no bnodes) of the form `http://example.org/cornell/xx/########` (where `########` is some hex string). 

Let's say we have some beautifully hand-crafted RDF that we are expecting the converter to produce [102063_simple.ttl](examples/102063_simple.ttl) and we now want to see whether the converter output matched (perhaps as part of an acceptance test).

A first attempt might be to convert each output to ntriples (I use `rapper` from the [`raptor`](http://librdf.org/raptor/rapper.html) suite for conversion below), sort the triples and use Unix `diff`. This is pretty ugly:

``` sh
(py3)simeon@RottenApple rdiffb>rapper -i rdfxml -o ntriples examples/102063.rdf | sort > /tmp/in.nt
rapper: Parsing URI file:examples/102063.rdf with parser rdfxml
rapper: Serializing with serializer ntriples
rapper: Parsing returned 71 triples
(py3)simeon@RottenApple rdiffb>rapper -i turtle -o ntriples examples/102063_simple.ttl | sort > /tmp/out.nt
rapper: Parsing URI file:examples/102063_simple.ttl with parser turtle
rapper: Serializing with serializer ntriples
rapper: Parsing returned 71 triples
(py3)simeon@RottenApple rdiffb>diff /tmp/in.nt /tmp/out.nt 
1,71c1,71
< <http://example.org/cornell/xx/0caa0837> <http://bibframe.org/vocab/source> "CStRLIN"^^<http://bib.ld4l.org/ontology/MARCOrgCode> .
< <http://example.org/cornell/xx/0caa0837> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
.... 130 lines omitted ...
> _:genid5 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
> _:genid5 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "notisAAL3258" .
> _:genid6 <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n85179829> .
> _:genid6 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/LocalIlsIdentifier> .
> _:genid6 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "102063" .
> _:genid7 <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n92026228> .
> _:genid7 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/EditingActivity> .
> _:genid8 <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n50060120> .
> _:genid8 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/ContributingActivity> .
> _:genid9 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.loc.gov/mads/rdf/v1#MainTitleElement> .
> _:genid9 <http://www.w3.org/2000/01/rdf-schema#label> "Clinical cardiopulmonary physiology." .
```

Without lots of eyestrain we don't learn very much. The `rdfdiffb.py` program is designed to do two things: First, it can treat URIs matching certain patterns like bnodes. In the examples here, we want to treat any URI starting `http://example.org/` as a bnode. Second, it uses a deterministic relabeling of bnodes to match-up bnodes from isomorphic graphs. Thus if the two graphs are the same up to bnodes and the specified URI patterms, we will see no diff:

``` sh
(py3)simeon@RottenApple rdiffb>python rdfdiffb.py -s -b http://example.org/ examples/102063.rdf examples/102063_simple.ttl
Graphs examples/102063.rdf and examples/102063_simple.ttl are isomorphic after bnode substitutions
```

(`-s` flag says report same, rather then being silent like default `diff` behavior, `-b http://example.org/` says theat URIs matching like bnodes.)

What if the converter were not perfect, but the outout instead contained an error? The example [102063_bad.rdf](examples/102063_bad.rdf) is missing the dimensions of the book (one triple). Comparison with our handcrafted version is then:

``` sh
(py3)simeon@RottenApple rdiffb>python rdfdiffb.py -s -b http://example.org/ examples/102063_bad.rdf examples/102063_simple.ttl
<  <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/hasInstance> <http://example.org/cornell/xx/60ed19e4> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bib.ld4l.org/ontology/hasActivity> <http://example.org/cornell/xx/c3767171> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/classification> <http://example.org/cornell/xx/217f63bb> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/extent> <http://example.org/cornell/xx/d2eef25f> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/instanceOf> <http://example.org/cornell/xx/102063> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
<  <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
<  <http://example.org/cornell/xx/60ed19e4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
>  <http://example.org/bib/102063> <http://bibframe.org/vocab/hasInstance> <http://example.org/bib/102063instance1> .
>  <http://example.org/bib/102063instance1> <http://bib.ld4l.org/ontology/hasActivity> _:ub1bL85C22 .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/classification> _:ub1bL66C23 .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/dimensions> "27 cm" .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/extent> _:ub1bL75C15 .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/instanceOf> <http://example.org/bib/102063> .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
>  <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
>  <http://example.org/bib/102063instance1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
```

Sadly, the output is rather more than one triple. This is because the deterministic assignment of canonical bnode labels depends upon the environment of the bnode which is changed because of the missing triple. In this case we see in the output all triples involving the `bf:Instance` that should have had the dimensions. Ideally, a helpful tool would have output just:

```
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/dimensions> "27 cm" .
```

But at least one can tell a match from a mismatch, and output in the mismatching case is somewhat helpful.
