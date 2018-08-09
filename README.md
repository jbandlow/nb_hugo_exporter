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
python3 -m nbconvert path/to/nb_file.ipynb --to hugo --output-dir content/path/insert-title-here
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
{{% jupyter_cell_start [cell_type] }}
{{% jupyter_input_start }}
...
{{% jupyter_input_end }}
...
{{% jupyter_cell_end }}
```
in the places you'd expect.  `[cell_type]` is the Jupyter cell type, e.g.,
`markdown`, `code`, etc. Code itself will have GitHub style code fences:

````
```python
import this
```
````

Set `pygmentsCodeFences` to `true` in your Hugo configuration file to use a
syntax highlighter. See the [hugo
documentation](https://gohugo.io/content-management/syntax-highlighting/) for
much more on this.

You may also want to enable the `noEmptyLineBeforeBlock` [BlackFriday
extension](https://gohugo.io/content-management/formats/#blackfriday-extensions).
Markdown in Jupyter is processed as though this setting were enabled.


## CSS configuration

You may also want to configure your CSS. The main design goal for this project
was to generate markdown that could be styled to my particular tastes.  The
shortcodes are simply used to generate `div`s, and the corresponding classes are
then easy to style. With the shortcodes in this repo, the resulting HTML
looks like:

```
<div class="jupyter-cell [cell_type]">
  <div class="jupyter-input"> ... </div>
  ...
</div>
```

In concert with styling the syntax highlighter, this can be
made to look more or less like Jupyter's own theme, or like anything else you
wish.  Note that the exporter currently adds some unnecessary blank lines. These
can be cleaned up with

```
.jupyter-cell p:empty { display: none; }
```

## Latex

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
