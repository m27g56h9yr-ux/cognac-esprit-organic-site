# Ancien site WordPress Cognac Esprit Organic

Ce dossier regroupe les elements sources issus de l'ancien site WordPress.

Il sert uniquement d'archive de travail pour comprendre et reconstruire le nouveau site statique. Il ne doit pas etre mis en ligne dans le meme dossier OVH que le nouveau site public.

En production, l'ancien site WordPress doit rester accessible a cette adresse :

```text
https://ancien.cognac-esprit-organic.com/
```

Cette version ancienne doit imperativement rester non indexable par Google et les autres moteurs (`noindex` fiable, idealement via en-tete HTTP et/ou configuration WordPress). Elle ne doit pas remplacer le nouveau site public sur `https://cognac-esprit-organic.com/`.

## Contenu

- `archives/` : fichiers d'archives decoupes `site-ec-*.zip.part-*`.
- `README-CODEX-site-ec.md` : description du pack securise cree pour l'analyse.
- `README-REASSEMBLAGE-GITHUB-site-ec.md` : commandes pour reconstituer les archives si besoin.

## A ne pas confondre

Les images de l'ancien site reprises dans le nouveau site restent dans `assets/img/old-site/`, parce qu'elles sont utilisees par les pages HTML publiees.

Les fichiers sensibles ou inutiles a la reconstruction ne doivent pas etre ajoutes ici : `wp-config.php`, logs, caches, mots de passe, cles API ou identifiants.
