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

- `<meta name="robots" content="index,follow">` sur les pages publiques finalisées ;
- mentions légales finalisées, traduites et accessibles depuis le pied de page ;
- `robots.txt` autorise l'exploration et référence le sitemap officiel.

## Fichiers principaux

- Pages HTML statiques à la racine ;
- Pages produits dans `produits/` ;
- Styles dans `assets/css/styles.css` ;
- JavaScript léger dans `assets/js/main.js` ;
- Images dans `assets/img/` ;
- SEO/agents IA : `sitemap.xml`, `robots.txt`, `llms.txt`.
- Newsletter : `newsletter.php` enregistre les inscriptions dans `newsletter-data/subscriptions.csv` sur un hébergement PHP classique comme OVH.
- Marchés d'achat : `market.php` expose en JSON le marché détecté côté serveur/CDN pour le JavaScript principal.
- Suivi vendeurs : `suivi-vendeurs.html` appelle `suivi-vendeurs-data.php` à chaque chargement pour relire les données structurées des pages distributeurs externes.

## Géociblage des boutons Acheter

Les liens d'achat produits sont présents dans les pages, mais masqués par défaut. Ils ne s'affichent que si le marché visiteur est reconnu :

- `qc` : SAQ ;
- `dk` : Vinoble ;
- `no` : Vinmonopolet.

Le fonctionnement est complémentaire :

1. Le visiteur peut forcer son choix dans le menu langue / pays : `QC Québec` => `qc`, `DA Danemark` => `dk`, `NO Norvège` => `no`. Ce choix est enregistré en `localStorage` et dans le cookie `ceo-market`.
2. `assets/js/main.js` applique ensuite un éventuel signal déjà configuré (`window.CEO_SERVER_MARKET`, cookie `ceo-market`, balise meta, etc.).
3. Il interroge ensuite `market.php?format=json`, qui cherche un signal serveur/CDN : `X-CEO-Market`, `X-Market`, `CF-IPCountry`, variables GeoIP serveur courantes, puis pays/région si disponibles.
4. Si aucun marché serveur n'est disponible, le navigateur sert de fallback : `fr-CA` => `qc`, `da-DK` => `dk`, `no-NO` / `nb-NO` / `nn-NO` => `no`.

Pour Cloudflare ou un autre CDN, le plus propre est d'injecter `X-CEO-Market: qc`, `dk` ou `no` vers l'origine. Sans signal régional, `CF-IPCountry: CA` ne suffit pas à identifier le Québec ; dans ce cas le fallback navigateur `fr-CA` reste utile.

En local, on peut tester l'affichage avec :

```text
http://localhost:8080/produits/conviction-vsop.html?market=qc
http://localhost:8080/produits/conviction-vsop.html?market=dk
http://localhost:8080/produits/conviction-vsop.html?market=no
```

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
- `market.php` ;
- `suivi-vendeurs-data.php` ;
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
