# Cognac Esprit Organic - nouveau site statique

Première version complète du nouveau site statique Cognac Esprit Organic.

## Tester localement

Depuis ce dossier, lancer un petit serveur local :

```bash
python3 -m http.server 8080
```

Puis ouvrir :

```text
http://localhost:8080
```

Il est aussi possible d'ouvrir `index.html` directement, mais le serveur local reproduit mieux un hébergement OVH.

## Mode préproduction

Le site contient volontairement :

- `<meta name="robots" content="noindex,nofollow">` sur chaque page ;
- `robots.txt` avec `Disallow: /`.

Avant la mise en ligne définitive, remplacer ces réglages par `index,follow` et autoriser l'exploration dans `robots.txt`.

## Fichiers principaux

- Pages HTML statiques à la racine ;
- Pages produits dans `produits/` ;
- Styles dans `assets/css/styles.css` ;
- JavaScript léger dans `assets/js/main.js` ;
- Images dans `assets/img/` ;
- SEO/agents IA : `sitemap.xml`, `robots.txt`, `llms.txt`.

## Mise en ligne OVH

Copier à la racine de l'hébergement OVH :

- tous les fichiers `.html` ;
- le dossier `produits/` ;
- le dossier `assets/` ;
- `robots.txt` ;
- `sitemap.xml` ;
- `llms.txt`.

Ne pas envoyer les dossiers de travail, les archives WordPress ou les fichiers de l'ancien site.
