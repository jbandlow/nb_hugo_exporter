# Export Notebooks To Hugo Compatible Markdown

## Basic Installation and Use
```
pip install nbhugoexporter
```
will install the exporter. You will also need to add some shortcode definitions
to Hugo. You can customize these as you wish, but an easy way to get started is
to run the following from the root of your Hugo project:
```
mkdir -p layouts/shortcodes
for x in cell input; do for y in start end;
  do curl -L https://github.com/jbandlow/nb_hugo_exporter/raw/master/resources/jupyter_$x\_$y.html > layouts/shortcodes/jupyter_$x\_$y.html;
done; done;
```

You can then run the exporter with
```
nbconvert path/to/nb_file.ipynb --to hugo --output-dir content/path/insert-title-here
```
This will create a `content/path/insert-title-here` directory with an
`index.md` file derived from `nb_file.ipynb`. The generated metadata will include
```
---
title: Nb File
date: <last file modification time for nb_file.ipynb>
draft: True
...
---
```
along with any other metadata you've specified. To set metadata, go to Edit ->
Edit Notebook Metadata from within your notebook, and add
```
"hugo": {
  "key1": value1,
  ...
}
```
with whatever keys and values you wish.  The `title` value will default to the
notebook filename with snake\_case replaced by Initial Caps. All auto-generated
values (`title`, `date`, and `draft`) can be overridden in the notebook
metadata.

The resulting markdown will contain the following hugo shortcodes:
```
{{% jupyter_cell_start <cell_type> }}
{{% jupyter_input_start }}
...
{{% jupyter_input_end }}
...
{{% jupyter_cell_end }}
```
in the places you'd expect.  `<cell_type>` is the Jupyter cell type, e.g.,
`markdown`, `code`, etc.

You may also want to configure your CSS. In particular, the exporter currently
adds some unnecessary blank lines. These can be cleaned up with
```
.jupyter-cell p:empty { display: none; }
```

Finally, for LaTeX to render properly, you should [include the MathJax script](
https://gohugo.io/content-management/formats/#enable-mathjax) on your pages.
Note that `nbconvert --to hugo` solves the [underscore problem](
https://gohugo.io/content-management/formats/#issues-with-markdown) with the
"tedious" solution of simply quoting all underscores in math mode. So there is
no need for the MathJax configuration script that "fixes \<code\> tags" in your
Javascript, or the custom CSS described in that post.

That's it! Happy blogging with Jupyter notebooks and Hugo.

## Acknowledgements
Shout-out to the amazing [Hugo](https://gohugo.io), and
[Jupyter](https://jupyter.org) teams for building incredible tools.

For another approach to this issue, see
[hugo-jupyter](http://journalpanic.com/hugo_jupyter/), from  [Stephan
Fitzpatrick](https://github.com/knowsuchagency). This didn't fully fit my needs,
but it might fit yours.
