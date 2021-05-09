# timetracker

Sovelluksen avulla voi pitää kirjaa tehdyistä ja tekemättömistä tehtävistä. Sovelluksella on kirjautumattomia ja kirjautuneita käyttäjiä. Kirjautumattomat käyttäjät voivat kirjautua sisään, luoda uuden käyttäjän ja kirjautua sovellukseen.

## Sovellus Herokussa

[![Heroku](https://pyheroku-badge.herokuapp.com/?app=warm-crag-55403)](https://warm-crag-55403.herokuapp.com/)

https://warm-crag-55403.herokuapp.com/

## Keskeiset toiminnot

### Kirjautumaton käyttäjä voi:

#### reitti `/register`

* Luoda uuden käyttäjätunnuksen

##### reitti `/login`

* Kirjautua olemassa olevalla käyttäjätunnuksella

### Kirjautuneen käyttäjän toiminnot

* Kirjautua ulos

#### reitti `/calendars`


Kirjautunut käyttäjä voi:

*  Luoda uuden kalenterin ja asettaa sille nimen ja kuvauksen.
*  Valita kalenterin 
*  Tarkastella olemassa olevia omia kalentereitaan
*  Valita kalenterin

#### reitti `/calendar/<id>/settings`

Kalenterin omistaja voi:

* Katsoa kalenterin nimen ja kuvauksen
* Muokata kalenterin nimeä ja kuvausta
* Lisätä kalenteriin kategorian
* Poistaa kalenterista kategorian
* Muokata kategoridoiden tietoja
* Lisätä kategorialle työn
* Muokata työn tietoja (nimi ja kuvaus)
* Poistaa työn
* Poistaa kalenterin


#### reitti `/calendar/<id>`

> Tehtävällä on nimi, selitys, arvioitu kesto ja toteutunut kesto

Kalenterin omistaja voi:

* katsoa kalenteria tehtäviä
* Muokata tehtävää
* Poistaa tehtävän
