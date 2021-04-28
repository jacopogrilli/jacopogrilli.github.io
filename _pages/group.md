---
title: "Jacopo Grilli - Group"
layout: gridlay
excerpt: "Jacopo Grilli: Group"
sitemap: false
permalink: /group/
---

# Group

<!-- **We are  looking for new PhD students, Postdocs, and Master students to join the team** [(see openings)]({{ site.url }}{{ site.baseurl }}/vacancies) **!**-->


<!--Jump to [staff](#staff), [master and bachelor students](#master-and-bachelor-students), [alumni](#alumni), [administrative support](#administrative-support), [lab visitors](#lab-visitors).-->

<!--## Staff-->
{% assign number_printed = 0 %}
{% for member in site.data.team_members %}

<!--{% assign even_odd = number_printed | modulo: 2 %}-->

<!--{% if even_odd == 0 %}-->
<div class="row">
<!--{% endif %}-->

<div class="col-sm-12 clearfix">
  <img src="{{ site.url }}{{ site.baseurl }}/images/teampic/{{ member.photo }}" class="img-responsive" width="25%" style="float: left" />
  <h4>{{ member.name }}</h4>
  <i>{{ member.info }}<br>email: <{{ member.email }}></i>
  <ul style="overflow: hidden">
  
  {% if member.number_educ == 1 %}
  <li> {{ member.education1 }} </li>
  {% endif %}
  
  {% if member.number_educ == 2 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  {% endif %}
  
  {% if member.number_educ == 3 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  {% endif %}
  
  {% if member.number_educ == 4 %}
  <li> {{ member.education1 }} </li>
  <li> {{ member.education2 }} </li>
  <li> {{ member.education3 }} </li>
  <li> {{ member.education4 }} </li>
  {% endif %}
  
  </ul>

  <p style="text-align: justify">
  {{ member.description }}
  </p>

<!-- CUSTOMIZE --->


<p>
{% if member.cv %} <a target="_blank" href="{{ site.url }}{{ site.baseurl }}/images/teamcv/{{ member.cv }}.pdf">
<i class="fa fa-file-pdf-o"></i>  Download cv</a> - {% endif %} {% if member.scholarusername %} <a target="_blank" href="http://scholar.google.com/citations?user={{ member.scholarusername }}" class="waves-effect waves-teal btn-flat my-google-scholar-link" ><i class="ai ai-google-scholar"></i></a> - {% endif %} {% if member.resgateusername %} <a target="_blank" href="http://www.researchgate.net/profile/{{ member.resgateusername }}" class="waves-effect waves-teal btn-flat my-researchgate-link" ><i class="ai ai-researchgate"></i> </a> - {% endif %} {% if member.mendeleyusername %}<a target="_blank" href="https://www.mendeley.com/profiles/{{ member.mendeleyusername }}" class="waves-effect waves-teal btn-flat my-mendeley-link" ><i class="ai ai-mendeley"></i></a> -  {% endif %} {% if  member.orcidusername %}<a target="_blank" href="http://orcid.org/{{ member.orcidusername }}" class="waves-effect waves-teal btn-flat my-orcid-link" ><i class="ai ai-orcid"></i></a> - {% endif %} {% if member.publonsusername %}<a target="_blank" href="https://publons.com/a/{{ member.publonsusername }}" class="waves-effect waves-teal btn-flat my-publons-link" ><i class="ai ai-publons"></i></a> - {% endif %} {% if member.twitterusername %}<a target="_blank" href="https://twitter.com/{{ member.twitterusername }}" class="waves-effect waves-teal btn-flat my-twitter-link"><i class="fa fa-twitter"></i></a> - {% endif %} {% if member.linkedinusername %}<a target="_blank" href="http://www.linkedin.com/pub/{{ member.linkedinusername }}" class="waves-effect waves-teal btn-flat my-linkedin-link"><i class="fa fa-linkedin"></i></a> -  {% endif %} {% if member.stravausername  %}<a target="_blank" href="https://www.strava.com/athletes/{{ member.stravausername }}" class="waves-effect waves-teal btn-flat my-mail-link"><i class="fab fa-strava"></i></a> {% endif %}
</p>

</div>

<!--{% assign number_printed = number_printed | plus: 1 %}-->

<!--{% if even_odd == 1 %}-->
</div>
<!--{% endif %}-->


{% endfor %}

<!--{% assign even_odd = number_printed | modulo: 2 %}-->
<!--{% if even_odd == 1 %}-->
<!--</div>-->
<!--{% endif %}-->


<!--- OLD FROM TEMPLATE --->

<!--## Master and Bachelor Students -->
<!--{% assign number_printed = 0 %}-->
<!--{% for member in site.data.students %}-->

<!--{% assign even_odd = number_printed | modulo: 2 %}-->

<!--{% if even_odd == 0 %}-->
<!--<div class="row">-->
<!--{% endif %}-->

<!--<div class="col-sm-6 clearfix">-->
<!--  <h4>{{ member.name }}</h4>-->
<!--  <i>{{ member.info }}<br>email: <{{ member.email }}></i>-->
<!--  <ul style="overflow: hidden">-->
<!--  -->
<!--  {% if member.number_educ == 1 %}-->
<!--  <li> {{ member.education1 }} </li>-->
<!--  {% endif %}-->
<!--  -->
<!--  {% if member.number_educ == 2 %}-->
<!--  <li> {{ member.education1 }} </li>-->
<!--  <li> {{ member.education2 }} </li>-->
<!--  {% endif %}-->
<!--  -->
<!--  {% if member.number_educ == 3 %}-->
<!--  <li> {{ member.education1 }} </li>-->
<!--  <li> {{ member.education2 }} </li>-->
<!--  <li> {{ member.education3 }} </li>-->
<!--  {% endif %}-->
<!--  -->
<!--  {% if member.number_educ == 4 %}-->
<!--  <li> {{ member.education1 }} </li>-->
<!--  <li> {{ member.education2 }} </li>-->
<!--  <li> {{ member.education3 }} </li>-->
<!--  <li> {{ member.education4 }} </li>-->
<!--  {% endif %}-->
<!--  -->
<!--  </ul>-->
<!--</div>-->

<!--{% assign number_printed = number_printed | plus: 1 %}-->

<!--{% if even_odd == 1 %}-->
<!--</div>-->
<!--{% endif %}-->

<!--{% endfor %}-->

<!--{% assign even_odd = number_printed | modulo: 2 %}-->
<!--{% if even_odd == 1 %}-->
<!--</div>-->
<!--{% endif %}-->


<!--## Alumni-->
<!--<table align="center" style="width:100%">-->
<!--<tr><th>Visitors</th>-->
<!--    <th>Master Students</th> -->
<!--    <th>Bachelor Students</th>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td>Nikolaos Iliopoulos, Spring 2016</td>-->
<!--    <td>Oliver Ostojic, Spring 2016</td>-->
<!--    <td>Joey Braspenning, Spring 2017</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td>Vitaly Feedosev, all of 2016</td>-->
<!--    <td>Farshaad Hoeseni, Fall 2015</td>-->
<!--    <td>Margot Leemker, Spring 2017</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td></td>-->
<!--    <td></td>-->
<!--    <td>Sietske Lensen, Spring 2017</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td></td>-->
<!--    <td></td>-->
<!--    <td>Alexander Vanstone, Spring 2016</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td></td>-->
<!--    <td></td>-->
<!--    <td>Tjerk Benschop, Spring 2016</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td></td>-->
<!--    <td></td>-->
<!--    <td>Arjo Andringa, Spring 2016</td>-->
<!--  </tr>-->
<!--  <tr>-->
<!--    <td></td>-->
<!--    <td></td>-->
<!--    <td>Daniëlle van Klink, Spring 2016</td>-->
<!--  </tr>-->
<!--</table>-->

<!--## Administrative Support-->
<!--<a href="mailto:Rijsewijk@Physics.LeidenUniv.nl">Ellie van Rijsewijk</a> is helping us (and other groups) with administration.-->

<!--## Lab Guests-->

<!--[Amir Safavi-Naeini](http://stanford.edu/~safavi/) (Stanford), summer 2015-->

<!--[Mark H Fischer](https://people.phys.ethz.ch/~mfischer/) (Weizmann Institute of Science), fall 2015-->

<!--[Alexander Ako Khajetoorians](http://www.ru.nl/spm) (Radboud University), fall 2015-->

<!--[Mohammad Hamidian](http://www.mhamidian.com) (Harvard->UC Davis), spring 2016-->

<!--[Ivan Bozovic](https://www.bnl.gov/cmpmsd/mbe/default.asp) (BNL / Yale), spring 2016-->

<!--[Freek Massee](http://www.fmassee.nl) (Paris), spring 2016-->

<!--[Felix Baumberger](http://dqmp.unige.ch/baumberger/) (Geneva), spring 2016-->

<!--[Jasper van Wezel](http://www.jvanwezel.com/) (UvA), summer 2016-->
