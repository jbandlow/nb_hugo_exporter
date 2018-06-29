{% extends 'markdown.tpl' %}

{% block header %}---
{%- for key, value in resources.metadata.hugo.items() %}
{{ key }}:
{%- if value is string and key != 'date' -%}
  {{ ' "' ~ value }}"
{%- else -%}
  {{ ' ' ~ value }}
{%- endif -%}
{%- endfor %}
---
{% endblock header %}

{%- block any_cell scoped -%}
{{ '{{% jupyter_cell_start' }} {{ cell.cell_type }} {{ '%}}' }}
{{ super() }}
{{ '{{% jupyter_cell_end %}}' }}
{%- endblock any_cell -%}

{% block input %}
{{ '{{% jupyter_input_start %}}' }}
{{ super() }}
{{ '{{% jupyter_input_end %}}' }}
{% endblock input %}
