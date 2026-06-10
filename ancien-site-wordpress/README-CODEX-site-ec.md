# Ancien site Esprit Organic - pack sécurisé pour GitHub/Codex

Source d'origine : `site-ec.zip`.

Ce pack a été créé pour aider Codex à reconstruire le site sans déposer d'éléments sensibles dans GitHub.

## Fichiers créés

- `site-ec-core-safe.zip` : thème WordPress, médias utiles sans miniatures générées, fichiers wp-content utiles.
- `site-ec-videos-safe.zip` : vidéos originales du site, séparées pour rester sous les limites GitHub en ligne de commande.

## Exclusions de sécurité / allègement

- `wp-config.php` exclu : peut contenir identifiants base de données OVH.
- `wp-content/debug.log` exclu : fichier de log volumineux et potentiellement sensible.
- `wp-admin/` et `wp-includes/` exclus : coeur WordPress standard inutile pour reconstruire un site moderne.
- `__MACOSX/`, `.DS_Store`, fichiers `._*` exclus.
- miniatures WordPress du type `-300x200.jpg`, `-1024x768.png`, etc. exclues.
- caches, backups, archives imbriquées exclus.
- code des plugins exclu ; liste des plugins conservée ci-dessous.

## Thèmes détectés

- esprit-organic
- twentytwentyfive
- twentytwentyfour

## Plugins détectés

- acfml
- advanced-custom-fields
- akismet
- disable-comments
- elementor
- jetformbuilder
- navz-photo-gallery
- redirection
- regenerate-thumbnails
- safe-svg
- sitepress-multilingual-cms
- wpml-media-translation
- wpml-string-translation

## À savoir

Les contenus complets des pages WordPress peuvent être stockés dans la base de données MySQL, pas uniquement dans les fichiers FTP. Ce pack contient surtout : thème, images, vidéos, fichiers CSS/JS et structure utile.
