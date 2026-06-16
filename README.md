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

## Mode production

Le site est prêt pour la mise en ligne :

- `<meta name="robots" content="index,follow">` sur chaque page ;
- `robots.txt` autorise l'exploration et référence le sitemap officiel.

## Fichiers principaux

- Pages HTML statiques à la racine ;
- Pages produits dans `produits/` ;
- Styles dans `assets/css/styles.css` ;
- JavaScript léger dans `assets/js/main.js` ;
- Images dans `assets/img/` ;
- SEO/agents IA : `sitemap.xml`, `robots.txt`, `llms.txt`.
- Newsletter : `newsletter.php` enregistre les inscriptions dans `newsletter-data/subscriptions.csv` sur un hébergement PHP classique comme OVH.

## Ancien site WordPress

Les archives de l'ancien site WordPress sont rangées dans `ancien-site-wordpress/`.

- `ancien-site-wordpress/archives/` contient les fichiers `.zip.part-*` à réassembler si nécessaire ;
- `ancien-site-wordpress/README-CODEX-site-ec.md` explique le contenu du pack sécurisé ;
- `ancien-site-wordpress/README-REASSEMBLAGE-GITHUB-site-ec.md` explique comment reconstituer les archives.

Les images récupérées de l'ancien site et utilisées par le nouveau site restent dans `assets/img/old-site/`, car elles servent directement aux pages publiées.

En production OVH, l'ancien site WordPress doit rester accessible sur :

```text
https://ancien.cognac-esprit-organic.com/
```

Ce sous-domaine doit rester separe du nouveau site GitHub et doit etre protege contre l'indexation Google avec `noindex`. Il ne doit pas devenir la version principale du site, et le domaine principal doit rester :

```text
https://cognac-esprit-organic.com/
```

## Mise en ligne OVH

Copier à la racine de l'hébergement OVH :

- tous les fichiers `.html` ;
- le dossier `produits/` ;
- le dossier `assets/` ;
- `robots.txt` ;
- `sitemap.xml` ;
- `llms.txt` ;
- `.htaccess` ;
- `newsletter.php` ;
- le dossier `newsletter-data/`.

Ne pas envoyer `ancien-site-wordpress/`, les dossiers de travail ou les archives WordPress.

## Inscriptions newsletter

Sur OVH, le formulaire du pied de page enregistre automatiquement chaque adresse e-mail dans :

```text
newsletter-data/subscriptions.csv
```

Chaque ligne contient la date d'inscription, l'adresse e-mail, la langue, le marché détecté et la page d'inscription.

Après chaque inscription, `newsletter.php` envoie aussi le fichier CSV complet en pièce jointe à `cognac@mdpierre.com`.

Le dossier `newsletter-data/` contient un fichier `.htaccess` pour empêcher la lecture publique du fichier CSV. GitHub Pages ne peut pas enregistrer les inscriptions, car il héberge uniquement des fichiers statiques et n'exécute pas PHP.
