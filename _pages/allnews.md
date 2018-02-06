---
title: "Home"
layout: textlay
excerpt: "Jacopo Grilli @ the Santa Fe Institute."
sitemap: false
permalink: /allnews.html
---

# News

{% for article in site.data.news %}
<p>
<strong>
{{ article.date }}</strong>  --- {{ article.headline }} <br>
<em>{% if article.fullnews %}{{ article.fullnews }}{% endif %}</em>
{% if article.image %}
<br><img src="../images/news/{{ article.image }}" class="img-responsive" width="275px" style="float: left" alt = "sometext" />
<br><br><br><br><br><br><br><br><br>
{% endif %}
</p>
{% endfor %}
