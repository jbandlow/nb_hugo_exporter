{% extends 'markdown.tpl' %}

{%- block any_cell scoped -%}
{{ '{{% jupyter_cell_start' }} {{ cell.cell_type }} {{ '%}}' }}
{{ super() }}
{{ '{{% jupyter_div_end %}}' }}
{%- endblock any_cell -%}

{% block input %}
{{ '{{% jupyter_input_start %}}' }}
{{ super() }}
{{ '{{% jupyter_div_end %}}' }}
{% endblock input %}
