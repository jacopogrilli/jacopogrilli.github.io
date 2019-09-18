---
title: "Jacopo Grilli - Talks"
layout: textlay
excerpt: "Jacopo Grilli -- Talks"
sitemap: false
permalink: /talks/
---

# Talks

<head>
<style>
    .redText
    {
        color:#ff1616;
    }
    .greenText
    {
        color:#1E90FF;
    }
    .futurepText
    {
        color:#0e9e00;
    }
    .pastpText
    {
        color:#595959;
    }
</style>
</head>

<!--count the number of upcoming talks-->
{% assign number_upc = 0 %}
{% for publi in site.data.talks %}
{% if publi.upcoming == 1 %}
  {% assign number_upc = number_upc | plus: 1 %}
{% endif %}
{% endfor %}


<div class="map" markdown="0">
<div id="talkMaps" class="templatemo-map"></div>
</div>


<em>click on the marker for more info </em>&nbsp;
[{% if number_upc > 0 %}<span class="pastpText"><em><i class="fa fa-map-marker" aria-hidden="true"></i></em></span>  past&nbsp;-&nbsp; <span class="futurepText"><em><i class="fa fa-map-marker" aria-hidden="true"></i></em></span> upcoming&nbsp;-&nbsp;{% endif %}<span class="redText"><em><i class="fa fa-calendar" aria-hidden="true"></i></em></span> talk&nbsp;-&nbsp; <span class="greenText"><em><i class="fa fa-calendar" aria-hidden="true"></i></em></span> organized workshop
]


{% assign number_upc = 0 %}

{% for publi in site.data.talks %}

{% if publi.upcoming == 1 %}

  {% if number_upc == 0 %}<h2 id="upcoming">Upcoming</h2>{% endif %}

  {% assign number_upc = 1 %}

  {% for loc in site.data.talks_location %}
  {% if loc.location == publi.location %}
  {% if publi.what == 0 %}
  <em><i class="fa fa-calendar" aria-hidden="true"  style="color:#ff1616" ></i> {{ publi.date }}</em><br>
  <a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>
  {{ publi.type }} @ {{publi.place}}, {{ loc.city }}, {{ loc.country }}
  {% endif %}
  {% if publi.what == 1 %}
  <em><i class="fa fa-calendar" aria-hidden="true"   style="color:#1E90FF"></i> {{ publi.date }}</em><br>
  <a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>
  {{ publi.type }} @ {{publi.place}}, {{ loc.city }}, {{ loc.country }}
  {% endif %}
  {% endif %}
  {% endfor %}
  

{% endif %}

{% endfor %}


## Past

{% assign number_printed = 0 %}

{% for publi in site.data.talks %}

{% if number_printed < 10000 %}

{% if publi.upcoming == 0 %}
  {% assign number_printed = number_printed | plus: 1 %}

  {% for loc in site.data.talks_location %}
  {% if loc.location == publi.location %}
  {% if publi.what == 0 %}
  <em><i class="fa fa-calendar" aria-hidden="true"  style="color:#ff1616" ></i> {{ publi.date }}</em><br>
  <a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>
  {{ publi.type }} @ {{publi.place}}, {{ loc.city }}, {{ loc.country }}{% if publi.video %}<br><a style="display:inline;"  target="_blank" href="{{ publi.video }}" ><i class="fa fa-play" aria-hidden="true"  ></i> video</a><br>{% endif %}
  {% endif %}
  {% if publi.what == 1 %}
  <em><i class="fa fa-calendar" aria-hidden="true"   style="color:#1E90FF"></i> {{ publi.date }}</em><br>
  <a style="display:inline;"  target="_blank" href="{{ publi.url }}" >{{ publi.title }}</a><br>
  {{ publi.type }} @ {{publi.place}}, {{ loc.city }}, {{ loc.country }},
  {% endif %}
  {% endif %}
  {% endfor %}

{% endif %}
{% endif %}


{% endfor %}



