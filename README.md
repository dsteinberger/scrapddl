# Scrap DDL

Pour visualiser les dernières sorties de vos sites DDL préférés !

Attention : il est possible que votre FAI bloque les sites ci-dessous, vous pouvez utiliser un VPN (ex: ProtonVPN).

## Providers supportés

- https://www.zone-telechargement.promo/
- https://www.extreme-down.promo/
- https://www.wawacity.promo/
- https://www.tirexo.promo/
- https://www.annuaire-telechargement.promo/

Ces données sont triées dans l'ordre chronologique et les doublons sont évités au possible.

Les notes IMDB sont également récupérées si possible.

Un lien vers https://www.opensubtitles.org/fr/ est présent pour chaque film/série/manga
et permet de télécharger les sous-titres français correspondants.


## Aperçu du site

![screenshot](images/homev3.png)


## Installation

Installer [uv](https://docs.astral.sh/uv/getting-started/installation/)

```bash
make install
```

Lancer le serveur en local :

```bash
make serve
```

Se rendre sur http://127.0.0.1:5000/


## Options

Le fichier `scrapddl/settings.py` permet de configurer l'application.

Activer ou non les sections Films, Séries ou Mangas :

```python
MOVIES_SECTION_ACTIVE = True
TVSHOWS_SECTION_ACTIVE = True
MANGAS_SECTION_ACTIVE = False  # Désactiver la section mangas
```

Activer ou non les notes IMDB :

```python
IMDB_RATING_ACTIVE = True
```

Définir la note minimale pour considérer un contenu en tant que "top" :

```python
IMDB_RATING_MINIMAL_TOP = 8
```

Voir le fichier settings pour toutes les options disponibles.


## Mise à jour des URLs

Les sites DDL changent régulièrement de domaine. Un script permet de détecter et mettre à jour automatiquement les URLs :

```bash
uv run check_urls.py              # Vérifier les URLs
uv run check_urls.py --update     # Mettre à jour settings.py et README.md
uv run check_urls.py --commit     # Mettre à jour et créer un commit
```

Une GitHub Action exécute ce script quotidiennement.
