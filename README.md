# Export Notebooks To Hugo Compatible Markdown

## Basic Installation and Use
```
pip install nb_hugo_exporter
nbconvert path/to/nb_file.ipynb --to hugo --output content/posts/insert-title-here
```
This will create a `content/posts/insert-title-here` directory with an
`index.md` file derived from `nb.ipynb`. The metadata will include
```
---
title: Nb File
date: <last file modification time for nb_file.ipynb>
draft: True
...
---
```
along with any other metadata you've specified in the notebook under the key
`hugo`. Note that `title` is the filename with snake\_case replaced by
Initial Caps. All auto-generated values (`title`, `date`, and `draft`) can
be overridden in the notebook metadata.

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
`markdown`, `code`, etc.  You must provide templates for these shortcodes in
your `layouts/shortcodes/` directory. To get started, you can use the
shortcodes from this repo:
```
TODO: One-liner for downloading just these files
```
You may also want to configure your CSS. In particular, the exporter currently
adds some unnecessary blank lines. These can be cleaned up with
```
.jupyter-cell p:empty { display: none; }
```

Finally, you will also want to [include the MathJax script](
https://gohugo.io/content-management/formats/#enable-mathjax) on your pages.
Note that `nbconvert --to hugo` solves the [underscore problem](
https://gohugo.io/content-management/formats/#issues-with-markdown) with the
"tedious" solution of simply quoting all underscores in math mode. So there
is no need for the MathJax configuration script that "fixes \<code\> tags" in
your Javascript, or the custom CSS described in that post.

That's it! Happy blogging with Jupyter notebooks and Hugo.

## Acknowledgements
Shout-out to the amazing [Hugo](https://gohugo.io), and
[Jupyter](https://jupyter.org) teams for building incredible tools.

Also thanks to [Stephan Fitzpatrick](https://github.com/knowsuchagency), whose
[hugo-jupyter](http://journalpanic.com/hugo_jupyter/) project inspired this
one. You should check it out -- it is a more automated solution than this one,
and may be a better fit for your use case.
