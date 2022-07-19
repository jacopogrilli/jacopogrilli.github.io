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
<!--{% if not reas.past %}-->
<br>
  <b>{{ reas.title }}</b> 
   {% if reas.with %}<br><em>Mainly with:  {{ reas.with }} </em> {% endif %}<br>
    {{ reas.description }}
<!--{% endif %}  -->
{% endfor %}

<br><br>

### Still in the back of my mind

<!--{% for reas in site.data.research %}-->
<!--{% if reas.past %}-->
<!--<br>-->
<!--  <b>{{ reas.title }}</b> -->
<!--   {% if reas.with %}<br><em>Mainly with:  {{ reas.with }} </em> {% endif %}<br>-->
<!--    {{ reas.description }}-->
<!--{% endif %}  -->
<!--{% endfor %}-->



</div>


