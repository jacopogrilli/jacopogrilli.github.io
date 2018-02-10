---
title: "Jacopo Grilli - Research"
layout: textlay
excerpt: "Jacopo Grilli -- Research"
sitemap: false
permalink: /research/
---

# Research

<em>"Simplicity is the greatest form of sophistication"</em> 



<div style="text-align: justify">

{% for reas in site.data.research %}
<br>
  <b>{{ reas.title }}</b> <br>
  <em>Mainly with:  {{ reas.with }} </em><br />
    {{ reas.description }}
    
{% endfor %}

<br><br>

</div>


