---
title: "Jacopo Grilli - Publications"
layout: gridlay
excerpt: "Jacopo Grilli -- Publications."
sitemap: false
permalink: /publications/
---


# Publications

For a full list see [below](#full-list) or go to
[<i class="ai ai-google-scholar"></i>  Google Scholar](https://scholar.google.ch/citations?user={{ site.scholar_username }}),
[<i class="ai ai-researchgate"></i>  Research Gate](http://www.researchgate.net/profile/{{ site.resgate_username }}),
[<i class="ai ai-orcid"></i> Orcid](http://orcid.org/{{ site.orcid_username }}) <br>
Pre-prints are [here](#preprints) or on
[<i class="ai ai-arxiv"></i>  Arxiv](https://arxiv.org/a/{{ site.arxiv_username }}) and
[<i class="ai ai-biorxiv"></i>  Biorxiv](http://www.biorxiv.org/search/author1%3A{{ site.biorxiv_username }})


## Highlights


{% assign number_printed = 0 %}
{% for publi in site.data.publist %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if publi.highlight == 1 %}

{% if even_odd == 0 %}
<div class="row">
{% endif %}

<div class="col-sm-6 clearfix">
 <div class="well">
  <pubtit>{{ publi.title }}</pubtit>
  <img src="{{ site.url }}{{ site.baseurl }}/images/pubpic/{{ publi.image }}" class="img-responsive" width="33%" style="float: left" />
  <p align = "justify"><em>{{ publi.description }}</em></p>
  <p>{{ publi.authors }}<br /><strong><a target="_blank" href="http://doi.org/{{ publi.doi }}">{{ publi.journalshort }}. {{publi.reference}}. {{publi.year}}</a> </strong></p>
  {% if publi.news %}<p><strong><em>News:</em></strong> {{ publi.news }}</p>{% endif %}
<div data-badge-popover="right" data-badge-type="bar" data-doi="{{ publi.doi }}" data-hide-no-mentions="true" class="altmetric-embed"></div>
 </div>
</div>

{% assign number_printed = number_printed | plus: 1 %}

{% if even_odd == 1 %}
</div>
{% endif %}

{% endif %}
{% endfor %}

{% assign even_odd = number_printed | modulo: 2 %}
{% if even_odd == 1 %}
</div>
{% endif %}




{% assign total_pub = 0 %}

{% for publi in site.data.publist %}

{% if publi.preprint == 0 %}

{% assign total_pub = total_pub | plus: 1 %}

{% endif %}

{% endfor %}





## Preprints

{% for publi in site.data.publist %}

{% if publi.preprint == 1 %}

<!--  [{{ number_pub }}]-->
  {{ publi.authors }}<br />
  <em><a target="_blank" href="http://doi.org/{{ publi.doi }}">{{ publi.title }}</a></em><br />
  {{publi.year}} - 
  {% if publi.arxiv %}<a target="_blank" href="https://arxiv.org/abs/{{ publi.arxiv }}" ><i class="ai ai-arxiv"></i> arXiv</a>{% endif %}{% if publi.biorxiv %}<a target="_blank" href="https://www.biorxiv.org/content/early/{{ publi.biorxiv }}" ><i class="ai ai-biorxiv"></i> biorXiv</a>{% endif %}

<!--{% assign number_pub = number_pub | minus: 1 %}-->

{% endif %}

{% endfor %}


## Full List

{% assign number_pub = total_pub %}


{% for publi in site.data.publist %}

{% if publi.preprint == 0 %}

  [{{ number_pub }}] {{ publi.authors }}<br />
  <em><a target="_blank" href="http://doi.org/{{ publi.doi }}">{{ publi.title }}</a></em><br />
  {{ publi.journal }}, {{publi.reference}}. {{publi.year}}<br>
  {% if publi.arxiv %}<a style="display:inline;"  target="_blank" href="https://arxiv.org/abs/{{ publi.arxiv }}" ><i class="ai ai-arxiv"></i> arXiv</a> - {% endif %}{% if publi.biorxiv %}<a style="display:inline;"  target="_blank" href="https://www.biorxiv.org/content/early/{{ publi.biorxiv }}" ><i class="ai ai-biorxiv"></i> biorXiv</a> - {% endif %}<a style="display:inline;"  target="_blank" href="https://www.researchgate.net/search.Search.html?type=doi&query={{ publi.doi }}" ><i class="ai ai-researchgate"></i></a>{% if publi.mendeley %} - <a style="display:inline;"  target="_blank" href="https://www.mendeley.com/{{ publi.mendeley }}" ><i class="ai ai-mendeley"></i></a>{% endif %}{% if publi.pmid %} - <a style="display:inline;"  target="_blank" href="https://www.ncbi.nlm.nih.gov/pubmed/{{ publi.pmid }}" ><i class="ai ai-pubmed"></i></a> {% endif %} -
<span style="display:inline;" class="__dimensions_badge_embed__" data-doi="{{ publi.doi }}" data-style="small_rectangle"></span><script async src="https://badge.dimensions.ai/badge.js" charset="utf-8"></script>


{% assign number_pub = number_pub | minus: 1 %}

{% endif %}

{% endfor %}



<br><br>

