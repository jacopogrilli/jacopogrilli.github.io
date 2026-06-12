---
title: "Jacopo Grilli - Group"
layout: gridlay
excerpt: "Jacopo Grilli: Group"
sitemap: false
permalink: /group/
---



# Group

<!-- **We are looking for new PhD students, Postdocs, and Master students to join the team** [(see openings)]({{ site.url }}{{ site.baseurl }}/vacancies) **!**-->

<!--
  CURRENT members: a single flat list (Jacopo first, then everyone with past == 0,
  in data order). No role sub-headings here — role headings are used only for the
  PAST members below. Member markup lives in _includes/member_card.html.
-->
{% for member in site.data.team_members %}{% if member.past == 0 %}{% include member_card.html member=member %}{% endif %}{% endfor %}


<br/>

&nbsp;

## Past Members

<!--
  PAST members: first the continuously-scrolling photo flow (just under the
  title), then the role-grouped text lists, then the map at the very bottom.
  Roles (set in _data/team_members.yml): postdoc, phd, master/undergrad/diploma,
  visiting. The social-icon row is shared with the cards via member_links.html.
-->

{%- comment %} Continuous photo flow of alumni with a headshot (_includes/past_carousel.html) {% endcomment %}
{% include past_carousel.html %}

{%- comment %} ---- Past postdocs ---- {% endcomment %}
{% assign past_postdocs = site.data.team_members | where: "past", 1 | where: "role", "postdoc" %}
{% if past_postdocs.size > 0 %}
### Postdocs
<div class="past-list">
{% for member in past_postdocs %}<p>{{ member.name }}{% if member.website %} <a target="_blank" href="{{ member.website }}"><i class="fa fa-external-link"></i></a>{% endif %}, {{ member.info }}. {% include member_links.html member=member %}<span class="flag-icon flag-icon-{{ member.country }}"></span></p>
{% endfor %}
</div>
{% endif %}

{%- comment %} ---- Past PhD students ---- {% endcomment %}
{% assign past_phds = site.data.team_members | where: "past", 1 | where: "role", "phd" %}
{% if past_phds.size > 0 %}
### PhD Students
<div class="past-list">
{% for member in past_phds %}<p>{{ member.name }}{% if member.website %} <a target="_blank" href="{{ member.website }}"><i class="fa fa-external-link"></i></a>{% endif %}, {{ member.info }}. {% include member_links.html member=member %}<span class="flag-icon flag-icon-{{ member.country }}"></span></p>
{% endfor %}
</div>
{% endif %}

{%- comment %} ---- Past master / undergraduate / diploma students ---- {% endcomment %}
{% assign past_students = site.data.team_members | where: "past", 1 | where_exp: "m", "m.role == 'master' or m.role == 'undergrad' or m.role == 'diploma'" %}
{% if past_students.size > 0 %}
### Master &amp; Undergraduate Students
<div class="past-list">
{% for member in past_students %}<p>{{ member.name }}{% if member.website %} <a target="_blank" href="{{ member.website }}"><i class="fa fa-external-link"></i></a>{% endif %}, {{ member.info }}. {% include member_links.html member=member %}<span class="flag-icon flag-icon-{{ member.country }}"></span></p>
{% endfor %}
</div>
{% endif %}

{%- comment %} ---- Past visiting students ---- {% endcomment %}
{% assign past_visitors = site.data.team_members | where: "past", 1 | where: "role", "visiting" %}
{% if past_visitors.size > 0 %}
### Visiting Students
<div class="past-list">
{% for member in past_visitors %}<p>{{ member.name }}{% if member.website %} <a target="_blank" href="{{ member.website }}"><i class="fa fa-external-link"></i></a>{% endif %}, {{ member.info }}. {% include member_links.html member=member %}<span class="flag-icon flag-icon-{{ member.country }}"></span></p>
{% endfor %}
</div>
{% endif %}

<div class="map" markdown="0" box-shadow="none">
<div id="groupMaps" class="templatemo-map" box-shadow="none"></div>
</div>
--- where we are from (<span style="color:#E4431B">**present**</span>
and
<span style="color:#419794">**past**</span>) ---

<!--TO CREATE MAP https://developers.google.com/chart/interactive/docs/gallery/geochart?csw=1#Example-->
