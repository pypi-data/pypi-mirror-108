# delphin-latex

LaTeX exporters for DELPH-IN data.

Currently only one exporter is available:

* `delphin.codecs.dmrstikz` -- export DMRS for rendering with
  [`tikz-dependency`][]

Contributions of other exporters are welcome!


# Example

Here is an image of the PDF produced for the DMRS for "The chef whose
soup spilled quit":

![DMRS rendering for "The chef whose soup spilled quit."](https://raw.githubusercontent.com/delph-in/delphin-latex/master/images/dmrs-tikz-pdf.png)


# Installation and Requirements

This package is a plugin for [PyDelphin][]. Install it with `pip`:

``` console
$ pip install delphin-latex
```

It depends on the `delphin.dmrs` and `delphin.predicate` modules in
PyDelphin version `1.0.0`. For rendering, [LaTeX][] and the
[`tikz-dependency`] package are required.

# Usage

The `delphin.codecs.dmrstikz` module implements the output functions
of PyDelphin's [Codec API][]:

* [`dump()`][] - serialize list and write to a file
* [`dumps()`][] - serialize list and return a string
* [`encode()`][] - serialize a single instance and return a string

The [`dump()`][] and [`dumps()`][] functions insert the LaTeX preamble
and postamble so the result is a full document, while [`encode()`][]
only serializes the individual `dependency` environment.

# Related

For visually presenting MRSs, DMRSs, and derivation trees, you may
also be interested in [delphin-viz][] which can save visualizations as
PNG or SVG files.

[delphin-viz]: https://github.com/delph-in/delphin-viz
[Codec API]: https://pydelphin.readthedocs.io/en/latest/api/delphin.codecs.html
[`dump()`]: https://pydelphin.readthedocs.io/en/latest/api/delphin.codecs.html#dump
[`dumps()`]: https://pydelphin.readthedocs.io/en/latest/api/delphin.codecs.html#dumps
[`encode()`]: https://pydelphin.readthedocs.io/en/latest/api/delphin.codecs.html#encode
[LaTeX]: https://www.latex-project.org/
[PyDelphin]: https://github.com/delph-in/pydelphin/
[`tikz-dependency`]: https://ctan.org/pkg/tikz-dependency
