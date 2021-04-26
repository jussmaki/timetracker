# timetracker

Sovelluksen avulla voi pitää kirjaa ajankäytöstään. Sovelluksella kirjautumattomia ja kirjautuneita käyttäjiä. Kirjautumattomat käyttäjät voivat kirjautua sisään, luoda uuden käyttäjän ja kirjautua sovellukseen. Jos aikaa jää, toteutan kalenteriin mahdollisuuden kirjautuneilla käyttäjille antaa kalentereihin erilaisia oikeuksia toisille käyttäjille. Tähän liittyvät kohdat on merkitty vaatimusmäärittelyssä tähdellä.

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
* [ ] Tarkastella olemassa olevia kalentereita, joihin hänelle on annettu katseluoikeus*
* [x] Valita kalenterin

#### reitti `/calendar/<id>/settings`
    
Kalenterin omistaja ja käyttäjä, jolla on samat oikeudet kuin omistajalla tai kalenterin muokkausoikeudet voi:

* [x] Katsoa kalenterin nimen ja kuvauksen
* [x] Muokata kalenterin nimeä ja kuvausta
* [x] Vaihtaa kalenterin yksityisestä julkiseksi, ja julkisesta yksityiseksi
* [x] Lisätä kalenteriin kategorian
* [x] Poistaa kalenterista kategorian
* [x] Muokata kategoridoiden tietoja
* [x] Lisätä kategorialle työn (job)
* [ ] Siirtää työn eri kategoriaan
* [x] Muokata työn tietoja (nimi)
* [x] Poistaa työn

Kalenterin omistaja ja käyttäjä, jolla on samat oikeudet kuin omistajalla voi:

* [x] Poistaa kalenterin
* [ ] Lisätä kalenteriin käyttäjille oikeuksia (view_calendar, modify_calendar, same_as_owner)*
* [ ] Muokata käyttäjien oikeuksia*
* [ ] Poistaa käyttäjältä kaikki oikeudet*

#### reitti `/calendar/<id>`

> Tehtävällä on nimi, selitys ja arvioitu kesto

Julkisessa kalenterissa kirjautunut käyttäjä ja yksityisessä kalenterissa kalenterin omistaja ja käyttäjä, jolla on samat oikeudet kuin omistajalla tai kalenterin katseluoikus voi:
* [ ] katsoa kalenteria tehtäviä viikkonäkymässä
* [ ] katsoa kalenteria tehtäviä kuukausinäkymässä
* [ ] katsoa kalenteria toteumia viikkonäkymässä
* [ ] katsoa kalenteria toteumia kuukausinäkymässä
* [ ] katsoa tehtävälistaa

Kalenterin omistaja ja käyttäjä, jolla on samat oikeudet kuin omistajalla tai kalenterin muokkausoikeus voi:

* [ ] Lisätä eri päiville tehtäviä
* [ ] Muokata tehtävää
* [ ] Poistaa tehtävän
* [ ] Lisätä tehtäville toteuman (event)
* [ ] Muokata toteumaa
* [ ] Poistaa toteuman

#### reitti `/calendar/<id>/raport`
  
Julkisessa kalenterissa kirjautunut käyttäjä ja yksityisessä kalenterissa kalenterin omistaja ja käyttäjä, jolla on samat oikeudet kuin omistajalla tai kalenterin katseluoikeus voi:
* [ ] Katsoa raporttia viikon ajankäytöstä
* [ ] Katsoa raporttia kuukauden ajankäytöstä
* [ ] Katsoa raporttia vapaavalintaiselta aikaväliltä ajankäytösta
