---
title: "Jacopo Grilli - Talks"
layout: textlay
excerpt: "Jacopo Grilli -- Talks"
sitemap: false
permalink: /talks/
---

{% include map_talks.html %}

# Talks

<head>
<style>
    .redText
    {
        color:#ffb778;
    }
    .greenText
    {
        color:#c78aff;
    }
    .futurepText
    {
        color:#ff0808;
    }
    .pastpText
    {
        color:#228B22;
    }
</style>
</head>

<!--count the number of upcoming talks-->
{% assign number_upc = 0 %}
{% for publi in site.data.talks %}
  {% if publi.what == 0 %}
{% if publi.upcoming == 1 %}
  {% assign number_upc = number_upc | plus: 1 %}
{% endif %}
{% endif %}
{% endfor %}


<div class="map" markdown="0">
<div id="talkMaps" class="templatemo-map"></div>
</div>


<em>click on the marker for more info </em>&nbsp;
{% if number_upc > 0 %}[<span class="pastpText"><em><i class="fa fa-map-marker" aria-hidden="true"></i></em></span>  past&nbsp;-&nbsp; <span class="futurepText"><em><i class="fa fa-map-marker" aria-hidden="true"></i></em></span> upcoming
]
{% endif %}

  {% if number_upc > 0 %}<h2 id="upcoming">Upcoming</h2>{% endif %}


{% for publi in site.data.talks %}

{% if publi.upcoming == 1 %}




  {% for loc in site.data.talks_location %}
  {% if loc.location == publi.location %}
  {% if publi.what == 0 %}
  <em>~ {{ publi.date }} ~</em><br>{% if publi.title %}<a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>{% endif %}{{ publi.type }} @ {{publi.place}}, {{ loc.city }}{% if loc.state %}, {{ loc.state }}{% endif %}{% if loc.country %}, {{ loc.country }}{% endif %}
  {% endif %}
  {% endif %}
  {% endfor %}
  

{% endif %}

{% endfor %}


  {% if number_upc > 0 %}<h2 id="past">Past</h2>{% endif %}



{% assign number_printed = 0 %}

{% for publi in site.data.talks %}

{% if number_printed < 10000 %}

{% if publi.upcoming == 0 %}
  {% assign number_printed = number_printed | plus: 1 %}

  {% for loc in site.data.talks_location %}
  {% if loc.location == publi.location %}
  {% if publi.what == 0 %}
  <em>~ {{ publi.date }} ~</em><br>{% if publi.title %}<a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>{% endif %}{{ publi.type }} @ {{publi.place}}, {{ loc.city }}{% if loc.state %}, {{ loc.state }}{% endif %}{% if loc.country %}, {{ loc.country }}{% endif %}{% if publi.video %}<br><a style="display:inline;"  target="_blank" href="{{ publi.video }}" ><i class="fa fa-play" aria-hidden="true"  ></i> video</a><br>{% endif %}
  {% if publi.youtube %}<br><a style="display:inline;"  target="_blank" href="{{ publi.youtube }}" ><i class="fa fa-youtube" aria-hidden="true"  ></i> video</a><br>{% endif %}
  {% endif %}
  {% endif %}
  {% endfor %}

{% endif %}
{% endif %}


{% endfor %}



