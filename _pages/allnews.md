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
<em>{% if article.fullnews %}{{ article.fullnews }}<br>{% endif %}</em>
{% if article.image %}
<img src="../images/news/{{ article.image }}" class="img" height = "250px" width="auto"  style="float: left" alt = "sometext" />
<br><br><br><br><br><br><br><br><br><br><br><br><br>
{% endif %}
</p>
{% endfor %}
