# Réassemblage des archives Esprit Organic dans Codex

Les gros fichiers ont été découpés pour permettre un dépôt via l'interface web GitHub.

Depuis la racine du dépôt, exécuter :

```bash
mkdir -p ancien-site/reconstitue
cat ancien-site/site-ec-core-safe.zip.part-* > ancien-site/reconstitue/site-ec-core-safe.zip
cat ancien-site/site-ec-videos-safe.zip.part-* > ancien-site/reconstitue/site-ec-videos-safe.zip
unzip -q ancien-site/reconstitue/site-ec-core-safe.zip -d ancien-site/reconstitue/core
unzip -q ancien-site/reconstitue/site-ec-videos-safe.zip -d ancien-site/reconstitue/videos
```

Objectif : analyser le thème `site-ec/wp-content/themes/esprit-organic`, les médias dans `site-ec/wp-content/uploads`, les vidéos, puis reconstruire le nouveau site statique ou moderne.

Important : le pack exclut `wp-config.php`, `debug.log`, `wp-admin`, `wp-includes`, les caches, les miniatures générées et les métadonnées Mac.
