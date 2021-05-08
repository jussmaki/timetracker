# timetracker

Sovelluksen avulla voi pitää kirjaa ajankäytöstään. Sovelluksella on kirjautumattomia ja kirjautuneita käyttäjiä. Kirjautumattomat käyttäjät voivat kirjautua sisään, luoda uuden käyttäjän ja kirjautua sovellukseen.

## Sovellus Herokussa

[![Heroku](https://pyheroku-badge.herokuapp.com/?app=warm-crag-55403)](https://warm-crag-55403.herokuapp.com/)

https://warm-crag-55403.herokuapp.com/

## Keskeiset toiminnot

### Kirjautumaton käyttäjä voi:

#### reitti `/register`

* [x] Luoda uuden käyttäjätunnuksen

##### reitti `/login`

* [x] Kirjautua olemassa olevalla käyttäjätunnuksella

### Kirjautuneen käyttäjän toiminnot

* [x] Kirjautua ulos

#### reitti `/calendars`

> Kalenterilla on omistaja, nimi ja kuvaus. Kalenteri voi olla yksityinen tai julkinen.

Kirjautunut käyttäjä voi:

* [x] Luoda uuden julkisen tai yksityisen kalenterin ja asettaa sille nimen ja kuvauksen.
* [x] Valita kalenterin 
* [x] Tarkastella olemassa olevia omia kalentereita
* [x] Valita kalenterin

#### reitti `/calendar/<id>/settings`
    
Kalenterin omistaja voi:

* [x] Katsoa kalenterin nimen ja kuvauksen
* [x] Muokata kalenterin nimeä ja kuvausta
* [x] Vaihtaa kalenterin yksityisestä julkiseksi, ja julkisesta yksityiseksi
* [x] Lisätä kalenteriin kategorian
* [x] Poistaa kalenterista kategorian
* [x] Muokata kategoridoiden tietoja
* [x] Lisätä kategorialle työn (job)
* [x] Muokata työn tietoja (nimi)
* [x] Poistaa työn
* [x] Poistaa kalenterin


#### reitti `/calendar/<id>`

> Tehtävällä on nimi, selitys ja arvioitu kesto

Kalenterin omistaja voi:
* [ ] katsoa kalenteria tehtäviä viikkonäkymässä
* [ ] katsoa kalenteria tehtäviä viikkonäkymässä
* [ ] katsoa kalenteria toteumia viikkonäkymässä
* [ ] katsoa viikon tehtävälistaa
* [ ] Lisätä eri päiville tehtäviä
* [ ] Muokata tehtävää
* [ ] Poistaa tehtävän
* [ ] Lisätä tehtäville toteuman (event)
* [ ] Muokata toteumaa
* [ ] Poistaa toteuman

Kirjautunut käyttäjä:
* [ ] katsoa kalenteria tehtäviä viikkonäkymässä
* [ ] katsoa kalenteria tehtäviä viikkonäkymässä
* [ ] katsoa kalenteria toteumia viikkonäkymässä
* [ ] katsoa viikon tehtävälistaa

#### reitti `/calendar/<id>/raport`

Kalenterin omistaja voi:
* [ ] Katsoa raporttia kuluvan viikon ajankäytöstä
* [ ] Katsoa raporttia muiden viikkojen ajankäytöstä
