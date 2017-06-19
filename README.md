# Scrap DDL

Pour visualiser les dernières sorties de vos sites DDL préférés !

Films et séries :

- http://www.zone-telechargement.ws/
- https://www.extreme-down.in/home.html
- http://www.ddl-island.su/

Mangas :

- https://goldenkai.me/
- http://www.univers-animezi.com/

Ces données sont triées dans l'ordre chronologique et les doublons sont évités au possible.

Les notes IMDB sont également récupérées si possible (sauf pour la catégorie mangas)


## Aperçu du site

![capture d'écran](images/homev2.png)


## Lancer le site

Il faut au préalable installer les dépendances :

```
make install
```

Puis lancer le serveur en locale :

```
make serve
```

Se rendre sur son navigateur et taper l'url suivante :
http://127.0.0.1:5000/

ENJOY!


## Extra options

Un fichier settings permet d'activer ou non certaines options.

Activer ou non les sections, Films, Series ou Mangas selon vos envies avec les settings suivant :
(Toutes les sections sont activés par défaut)

```
MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = False  # Unactive mangas section
```

Activer ou non les notes imdb (default True)

```
IMDB_RATING_ACTIVE = True
```
