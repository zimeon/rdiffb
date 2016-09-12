# LD4L RDF `diff` Use Case

Consider an example from the Cornell University Library catalog, say the very exciting [_Clinical cardiopulmonary physiology_](https://newcatalog.library.cornell.edu/catalog/102063) from 1957. I'm going to use this as an example for how we might think about using `rdiffb` to testing [LD4L Labs](https://www.ld4l.org/ld4l-labs/) conversion of the MARC record to the BIBFRAME-based LD4L Labs ontology.

> I'm working with this example because the [LD4All Ontology Working Groups](https://github.com/cul-it/onto-working-docs) have hand-transformed the MARC into the prototype LD4All Target Ontology. The original MARC and transformed data files are at <https://github.com/cul-it/onto-working-docs/tree/master/SampleData/102063>.
>
> All the examples shown here show work when run from the root of a cloned copy of this github repository.

So, starting from the Cornell catalog, we have for this item:

   * [Human readable page](https://newcatalog.library.cornell.edu/catalog/102063)
   * [MARC21](https://newcatalog.library.cornell.edu/catalog/102063.marc)
   * [MARCXML](https://newcatalog.library.cornell.edu/catalog/102063.marcxml)

Let's imagine that we have a MARCXML-to-LD4LAll ontology that we can run as follows:

``` sh
NOT-REAL> cat examples/102063.marc.xml | marcxml_to_ld4lall > examples/102063.rdf

This doesn't exist yet but there is a mockup of possible output [102063.rdf](examples/102063.rdf), which includes a number of generated URIs (no bnodes) of the form `http://example.org/cornell/xx/########` (where `########` is some hex string). 

Let's say we have some beautifully hand-crafted RDF that we are expecting the converter to produce [102063_simple.ttl](examples/102063_simple.ttl) and we now want to see whether the converter output matched (perhaps as part of an acceptance test).

A first attempt might be to convert each output to ntriples (I use `rapper` from the [`raptor`](http://librdf.org/raptor/rapper.html) for conversion below), sort the triples and use Unix `diff`. This is pretty ugly:

``` sh
(py3)simeon@RottenApple rdiffb>rapper -i rdfxml -o ntriples examples/102063.rdf | sort > /tmp/in.nt
rapper: Parsing URI file:///Users/simeon/src/rdiffb/examples/102063.rdf with parser rdfxml
rapper: Serializing with serializer ntriples
rapper: Parsing returned 71 triples
(py3)simeon@RottenApple rdiffb>rapper -i turtle -o ntriples examples/102063_simple.ttl | sort > /tmp/out.nt
rapper: Parsing URI file:///Users/simeon/src/rdiffb/examples/102063_simple.ttl with parser turtle
rapper: Serializing with serializer ntriples
rapper: Parsing returned 71 triples
(py3)simeon@RottenApple rdiffb>diff /tmp/in.nt /tmp/out.nt 
1,71c1,71
< <http://example.org/cornell/xx/0caa0837> <http://bibframe.org/vocab/source> "CStRLIN"^^<http://bib.ld4l.org/ontology/MARCOrgCode> .
< <http://example.org/cornell/xx/0caa0837> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
< <http://example.org/cornell/xx/0caa0837> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "NYCX86B63464" .
< <http://example.org/cornell/xx/0e8bfd42> <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n92026228> .
< <http://example.org/cornell/xx/0e8bfd42> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/EditingActivity> .
< <http://example.org/cornell/xx/102063> <http://bib.ld4l.org/ontology/hasActivity> <http://example.org/cornell/xx/0e8bfd42> .
< <http://example.org/cornell/xx/102063> <http://bib.ld4l.org/ontology/hasActivity> <http://example.org/cornell/xx/383ba728> .
< <http://example.org/cornell/xx/102063> <http://bib.ld4l.org/ontology/hasPreferredTitle> <http://example.org/cornell/xx/cd468cc8> .
< <http://example.org/cornell/xx/102063> <http://bib.ld4l.org/ontology/illustrativeContent> <http://bib.ld4l.org/ontology/IllustrationsContent> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/classification> <http://example.org/cornell/xx/ca846954> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/classification> <http://example.org/cornell/xx/f6109249> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/hasInstance> <http://example.org/cornell/xx/60ed19e4> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/identifiedBy> <http://example.org/cornell/xx/0caa0837> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/identifiedBy> <http://example.org/cornell/xx/35ca771e> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/identifiedBy> <http://example.org/cornell/xx/9d987592> .
< <http://example.org/cornell/xx/102063> <http://bibframe.org/vocab/identifiedBy> <http://example.org/cornell/xx/fd6f3927> .
< <http://example.org/cornell/xx/102063> <http://purl.org/dc/terms/language> <http://lexvo.org/id/iso639-3/eng> .
< <http://example.org/cornell/xx/102063> <http://purl.org/dc/terms/subject> <http://id.loc.gov/authorities/subjects/sh85023137> .
< <http://example.org/cornell/xx/102063> <http://purl.org/dc/terms/subject> <http://id.worldcat.org/fast/853831> .
< <http://example.org/cornell/xx/102063> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Text> .
< <http://example.org/cornell/xx/102063> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Work> .
< <http://example.org/cornell/xx/102063> <http://www.w3.org/2002/07/owl#sameAs> <http://lccn.loc.gov/56010158/L> .
< <http://example.org/cornell/xx/217f63bb> <http://bibframe.org/vocab/classificationPortion> "RC941" .
< <http://example.org/cornell/xx/217f63bb> <http://bibframe.org/vocab/itemPortion> ".C6" .
< <http://example.org/cornell/xx/217f63bb> <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78089035> .
< <http://example.org/cornell/xx/217f63bb> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationLcc> .
< <http://example.org/cornell/xx/35ca771e> <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n85179829> .
< <http://example.org/cornell/xx/35ca771e> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
< <http://example.org/cornell/xx/35ca771e> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "notisAAL3258" .
< <http://example.org/cornell/xx/383ba728> <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n50060120> .
< <http://example.org/cornell/xx/383ba728> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/ContributingActivity> .
< <http://example.org/cornell/xx/44e6bc1d> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.loc.gov/mads/rdf/v1#MainTitleElement> .
< <http://example.org/cornell/xx/44e6bc1d> <http://www.w3.org/2000/01/rdf-schema#label> "Clinical cardiopulmonary physiology." .
< <http://example.org/cornell/xx/60ed19e4> <http://bib.ld4l.org/ontology/hasActivity> <http://example.org/cornell/xx/c3767171> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/classification> <http://example.org/cornell/xx/217f63bb> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/dimensions> "27 cm" .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/extent> <http://example.org/cornell/xx/d2eef25f> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/instanceOf> <http://example.org/cornell/xx/102063> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
< <http://example.org/cornell/xx/60ed19e4> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
< <http://example.org/cornell/xx/60ed19e4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
< <http://example.org/cornell/xx/6ef0d391> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Unit> .
< <http://example.org/cornell/xx/6ef0d391> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "page" .
< <http://example.org/cornell/xx/6f41da78> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Location> .
< <http://example.org/cornell/xx/6f41da78> <http://www.w3.org/2000/01/rdf-schema#label> "New York" .
< <http://example.org/cornell/xx/6f41da78> <http://www.w3.org/2002/07/owl#sameAs> <http://sws.geonames.org/5128581/> .
< <http://example.org/cornell/xx/9d987592> <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78015294> .
< <http://example.org/cornell/xx/9d987592> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
< <http://example.org/cornell/xx/9d987592> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "1345399" .
< <http://example.org/cornell/xx/c3767171> <http://bib.ld4l.org/ontology/hasActivityStatement> "New York, Grune & Stratton, 1957." .
< <http://example.org/cornell/xx/c3767171> <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n83008217> .
< <http://example.org/cornell/xx/c3767171> <http://bibframe.org/vocab/place> <http://example.org/cornell/xx/6f41da78> .
< <http://example.org/cornell/xx/c3767171> <http://purl.org/dc/terms/date> "1957"^^<http://id.loc.gov/datatypes/edtf/EDTF> .
< <http://example.org/cornell/xx/c3767171> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/PublicationActivity> .
< <http://example.org/cornell/xx/ca846954> <http://bibframe.org/vocab/classificationPortion> "RC941" .
< <http://example.org/cornell/xx/ca846954> <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78089035> .
< <http://example.org/cornell/xx/ca846954> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationLcc> .
< <http://example.org/cornell/xx/cd468cc8> <http://purl.org/dc/terms/hasPart> <http://example.org/cornell/xx/44e6bc1d> .
< <http://example.org/cornell/xx/cd468cc8> <http://purl.org/dc/terms/language> <http://lexvo.org/id/iso639-3/eng> .
< <http://example.org/cornell/xx/cd468cc8> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.loc.gov/mads/rdf/v1#Title> .
< <http://example.org/cornell/xx/cd468cc8> <http://www.w3.org/2000/01/rdf-schema#label> "Clinical cardiopulmonary physiology." .
< <http://example.org/cornell/xx/d2eef25f> <http://bibframe.org/vocab/unit> <http://example.org/cornell/xx/6ef0d391> .
< <http://example.org/cornell/xx/d2eef25f> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Extent> .
< <http://example.org/cornell/xx/d2eef25f> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "759" .
< <http://example.org/cornell/xx/f6109249> <http://bibframe.org/vocab/classificationPortion> "616.2" .
< <http://example.org/cornell/xx/f6109249> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationDdc> .
< <http://example.org/cornell/xx/fd6f3927> <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n85179829> .
< <http://example.org/cornell/xx/fd6f3927> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/LocalIlsIdentifier> .
< <http://example.org/cornell/xx/fd6f3927> <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "102063" .
---
> <http://example.org/bib/102063> <http://bib.ld4l.org/ontology/hasActivity> _:genid7 .
> <http://example.org/bib/102063> <http://bib.ld4l.org/ontology/hasActivity> _:genid8 .
> <http://example.org/bib/102063> <http://bib.ld4l.org/ontology/hasPreferredTitle> _:genid10 .
> <http://example.org/bib/102063> <http://bib.ld4l.org/ontology/illustrativeContent> <http://bib.ld4l.org/ontology/IllustrationsContent> .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/classification> _:genid1 .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/classification> _:genid2 .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/hasInstance> <http://example.org/bib/102063instance1> .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/identifiedBy> _:genid3 .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/identifiedBy> _:genid4 .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/identifiedBy> _:genid5 .
> <http://example.org/bib/102063> <http://bibframe.org/vocab/identifiedBy> _:genid6 .
> <http://example.org/bib/102063> <http://purl.org/dc/terms/language> <http://lexvo.org/id/iso639-3/eng> .
> <http://example.org/bib/102063> <http://purl.org/dc/terms/subject> <http://id.loc.gov/authorities/subjects/sh85023137> .
> <http://example.org/bib/102063> <http://purl.org/dc/terms/subject> <http://id.worldcat.org/fast/853831> .
> <http://example.org/bib/102063> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Text> .
> <http://example.org/bib/102063> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Work> .
> <http://example.org/bib/102063> <http://www.w3.org/2002/07/owl#sameAs> <http://lccn.loc.gov/56010158/L> .
> <http://example.org/bib/102063instance1> <http://bib.ld4l.org/ontology/hasActivity> _:genid15 .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/classification> _:genid11 .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/dimensions> "27 cm" .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/extent> _:genid13 .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/instanceOf> <http://example.org/bib/102063> .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
> <http://example.org/bib/102063instance1> <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
> <http://example.org/bib/102063instance1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
> _:genid1 <http://bibframe.org/vocab/classificationPortion> "RC941" .
> _:genid1 <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78089035> .
> _:genid1 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationLcc> .
> _:genid10 <http://purl.org/dc/terms/hasPart> _:genid9 .
> _:genid10 <http://purl.org/dc/terms/language> <http://lexvo.org/id/iso639-3/eng> .
> _:genid10 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.loc.gov/mads/rdf/v1#Title> .
> _:genid10 <http://www.w3.org/2000/01/rdf-schema#label> "Clinical cardiopulmonary physiology." .
> _:genid11 <http://bibframe.org/vocab/classificationPortion> "RC941" .
> _:genid11 <http://bibframe.org/vocab/itemPortion> ".C6" .
> _:genid11 <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78089035> .
> _:genid11 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationLcc> .
> _:genid12 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Unit> .
> _:genid12 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "page" .
> _:genid13 <http://bibframe.org/vocab/unit> _:genid12 .
> _:genid13 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Extent> .
> _:genid13 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "759" .
> _:genid14 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/ns/prov#Location> .
> _:genid14 <http://www.w3.org/2000/01/rdf-schema#label> "New York" .
> _:genid14 <http://www.w3.org/2002/07/owl#sameAs> <http://sws.geonames.org/5128581/> .
> _:genid15 <http://bib.ld4l.org/ontology/hasActivityStatement> "New York, Grune & Stratton, 1957." .
> _:genid15 <http://bibframe.org/vocab/agent> <http://id.loc.gov/rwo/agents/n83008217> .
> _:genid15 <http://bibframe.org/vocab/place> _:genid14 .
> _:genid15 <http://purl.org/dc/terms/date> "1957"^^<http://id.loc.gov/datatypes/edtf/EDTF> .
> _:genid15 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/PublicationActivity> .
> _:genid2 <http://bibframe.org/vocab/classificationPortion> "616.2" .
> _:genid2 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/ClassificationDdc> .
> _:genid3 <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n78015294> .
> _:genid3 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
> _:genid3 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "1345399" .
> _:genid4 <http://bibframe.org/vocab/source> "CStRLIN"^^<http://bib.ld4l.org/ontology/MARCOrgCode> .
> _:genid4 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bib.ld4l.org/ontology/Identifier> .
> _:genid4 <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> "NYCX86B63464" .
> _:genid5 <http://bibframe.org/vocab/source> <http://id.loc.gov/rwo/agents/n85179829> .
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

Without lots of eyestrain we don't learn very much. The `rdiffb.py` program is designed to do two things: First, it can treat URIs matching certain patterns like bnodes. In the examples here, we want to treat any URI starting `http://example.org/` as a bnode. Second, it uses a deterministic relabeling of bnodes to match-up bnodes from isomorphic graphs. Thus if the two graphs are the same up to bnodes and the specified URI patterms, we will see no diff:

``` sh
(py3)simeon@RottenApple rdiffb>python rdiffb.py -s -b http://example.org/ examples/102063.rdf examples/102063_simple.ttl
Graphs examples/102063.rdf and examples/102063_simple.ttl are isomorphic after bnode substitutions
```

(`-s` flag says report same, rather then being silent like default `diff` behavior, `-b http://example.org/` says theat URIs matching like bnodes.)

What if the converter were not perfect, but instead contained an error? The example <examples/102063_bad.rdf> is missing the dimensions of the book (one triple) and the output is then:

``` sh
(py3)simeon@RottenApple rdiffb>python rdiffb.py -s -b http://example.org/ examples/102063_bad.rdf examples/102063_simple.ttl
< _:cb0 <http://bibframe.org/vocab/hasInstance> _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bib.ld4l.org/ontology/hasActivity> _:cbd6ef0a0424b2585f9b4b39a3134b5afc59e91b9c0903f8462772d058a21931b2 .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/classification> _:cb96b9b72919db4d5927eea343ddef8f235eea8961f90762633ded92600a137754 .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/extent> _:cb1fb57421e323d69c9b8c5e56e678bc46a14e698011e6c62fc0e71a1d3d9b5830 .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/instanceOf> _:cb0 .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
< _:cb8986c6f134a9c58441bf205a8e94f583e5b50c5863f7231bac6bf7b6938ac225 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
> _:cb0 <http://bibframe.org/vocab/hasInstance> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bib.ld4l.org/ontology/hasActivity> _:cbd6ef0a0424b2585f9b4b39a3134b5afc59e91b9c0903f8462772d058a21931b2 .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/classification> _:cb96b9b72919db4d5927eea343ddef8f235eea8961f90762633ded92600a137754 .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/dimensions> "27 cm" .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/extent> _:cb1fb57421e323d69c9b8c5e56e678bc46a14e698011e6c62fc0e71a1d3d9b5830 .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/instanceOf> _:cb0 .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/issuance> <http://bib.ld4l.org/ontology/Monograph> .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/responsibilityStatement> "Sponsored by the American College of Chest Physicians. Editorial board: Burgess L. Gordon, chairman, editor-in-chief, Albert H. Andrews [and others]" .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/BibliographyContent> .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/supplementaryContent> <http://bib.ld4l.org/ontology/SupplementaryBibliography> .
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://bibframe.org/vocab/Instance> .
```

Sadly, the output is rather more than one triple. This is because the deterministic assignment of canonical bnode labels depends upon the environment of the bnode, and this is changed. Ideally, a helpful tool would have output just:

```
> _:cb67186689a3c33546ff69a5ceab24355ef3b77544e483432cfc845d3493fb87e3 <http://bibframe.org/vocab/dimensions> "27 cm" .
```

But at least one can tell a match from a mismatch, and output in the mismatching case is somewhat helpful.

FIXME -- Still to do: make `rdiffb` output show the original input URIs and not the bnode labels. 

