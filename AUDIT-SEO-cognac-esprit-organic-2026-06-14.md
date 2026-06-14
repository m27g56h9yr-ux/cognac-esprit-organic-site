# Audit SEO technique + contenu/entity

Site audite : https://cognac-esprit-organic.com  
Depot GitHub connecte : https://github.com/m27g56h9yr-ux/cognac-esprit-organic-site  
Date : 14 juin 2026  
Mode : audit uniquement, aucune modification de production.

## Erratum apres verification utilisateur

Verification complementaire apres mise en ligne recente :

- Le constat initial "`www.cognac-esprit-organic.com` redirige vers `ancien.cognac-esprit-organic.com`" doit etre considere comme non confirme / obsolète.
- Depuis une verification web externe ulterieure, `https://www.cognac-esprit-organic.com/` redirige vers `https://cognac-esprit-organic.com/`, ce qui est le comportement attendu.
- Le point critique a suivre n'est donc plus "`www` vers `ancien`", mais "coherence de propagation et version servie selon point d'observation". Certains tests externes voient encore une page au contenu proche de l'ancien site sur l'apex, tandis que le depot audite contient le nouveau site statique.
- Action recommandee : valider dans Google Search Console avec l'inspection d'URL live que Googlebot voit bien la version nouvellement mise en ligne, puis re-crawler apres propagation DNS/cache.

Mise a jour Search Console du 14 juin 2026 :

- Propriete de domaine `cognac-esprit-organic.com` validee dans Google Search Console par enregistrement DNS TXT OVH.
- Test live de `https://cognac-esprit-organic.com/` lance a 21:26 : "Google a acces a cette URL" et "La page peut etre indexee".
- HTML teste par Google : titre `Cognac Esprit Organic | Cognac bio familial en France`, meta description du nouveau site statique, canonical `https://cognac-esprit-organic.com/`, stylesheet `assets/css/styles.css?v=20260611-pineau-rouge03`.
- Conclusion : Googlebot voit bien la version statique issue du depot audite pour l'URL d'accueil.

Correctifs appliques apres audit le 14 juin 2026 :

- Les 8 pages produits ont maintenant un H1 unique correspondant au nom du produit.
- Les pages du sitemap ont maintenant des variantes linguistiques statiques pour `en`, `da`, `no` et `sv`.
- Chaque page expose un bloc `hreflang` reciproque : `fr`, `en`, `da`, `no`, `sv` et `x-default`.
- Le sitemap liste maintenant 105 URLs, soit les 21 pages principales dans 5 variantes linguistiques.
- Le selecteur de langue en JavaScript navigue vers l'URL de langue correspondante au lieu de seulement changer le texte sur la meme URL.
- Les variantes `en`, `da`, `no` et `sv` ont maintenant leurs propres titres, meta descriptions, `og:title`, `og:description` et JSON-LD localises.
- Le JSON-LD localise couvre les fils d'Ariane, les descriptions/categories produits, la FAQ et les recettes `Recipe`; les fils d'Ariane pointent vers la home de chaque langue.

## Sources et perimetre

- Crawl live de `https://cognac-esprit-organic.com`, `robots.txt`, `sitemap.xml`, variantes `http`, `www`, `index.html`, anciennes URLs et sous-domaine `ancien`.
- Inspection du depot local clone depuis GitHub : HTML statique, `robots.txt`, `sitemap.xml`, `llms.txt`, `assets/js/main.js`, pages produits et pages institutionnelles.
- References Google Search Central :
  - Canonicalisation : https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
  - Sitemaps : https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
  - Donnees structurees : https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
  - Hreflang / versions localisees : https://developers.google.com/search/docs/specialty/international/localized-versions
  - Robots.txt : https://developers.google.com/search/docs/crawling-indexing/robots/intro

## Executive diagnosis

Le nouveau site statique est deja bien pose : sitemap live, robots ouvert, canonicals propres sur les 21 URLs du sitemap, titres/meta uniques, pages produits et premiers JSON-LD.

Le plus gros risque SEO a verifier n'est pas dans les pages du nouveau site, mais dans l'infrastructure d'hotes et la propagation recente : il faut confirmer que tous les points d'observation servent bien la nouvelle version statique sur l'apex et que l'ancien WordPress reste isole sur `ancien.cognac-esprit-organic.com`.

Deuxieme risque fort : `http://cognac-esprit-organic.com/` sert la page en 200 au lieu de rediriger en 301 vers HTTPS. Le canonical HTTPS aide, mais la redirection serveur est le signal attendu.

Les 8 pages produits n'ont pas de H1 : le nom produit visible est en H2. Pour une gamme courte, c'est une correction simple et prioritaire.

Le multilingue actuel repose sur JS et une seule URL par page, sans URLs localisees ni hreflang. C'est acceptable pour UX de base, mais insuffisant pour une strategie export Google/Bing.

L'entite de marque est claire, mais le schema manque d'`@id` stables, de `sameAs`, de liaison Organization -> Product, et de preuves visibles pour les claims bio/certification.

## Priority fixes

| Priorite | Issue | Severite | URLs/templates | Fix | Validation | Delai attendu |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Coherence de version servie apres mise en ligne recente | Critical a revalider | `https://cognac-esprit-organic.com/`, `https://www.cognac-esprit-organic.com/`, `https://ancien.cognac-esprit-organic.com/` | Confirmer que l'apex et `www` servent/redirigent vers la nouvelle version statique, et que l'ancien WordPress reste uniquement sur `ancien`. Si l'ancien reste public, le mettre en `noindex` ou le rediriger page-a-page selon strategie. | Inspection live Google Search Console + tests depuis plusieurs reseaux/user-agents. | Heures a jours selon propagation |
| 2 | HTTP apex sert une copie 200 | High | `http://cognac-esprit-organic.com/` | Redirection 301 HTTP -> HTTPS au niveau Apache/OVH. | `curl -I http://...` doit retourner 301 vers HTTPS. | Jours a semaines |
| 3 | Pages produits sans H1 | High | 8 URLs `/produits/*.html` | Remplacer le H2 principal du nom produit par H1, puis descendre les sections internes si besoin. | Crawl : exactement 1 H1 par page produit. | Prochain crawl |
| 4 | Multilingue sans URLs localisees ni hreflang | High | Toutes les pages avec `data-en`, `data-da`, `data-no`, `data-sv` | Creer une vraie architecture `/en/`, `/da/`, `/no/`, `/sv/` pour les pages prioritaires, avec self-canonical et hreflang reciproque. A defaut, garder la page indexable en FR et traiter les langues comme aide UX seulement. | Inspecter le head : alternates complets, pages 200, canonicals self. | Semaines |
| 5 | JSON-LD sans `@id` stables et Product minimal | Medium | Sitewide + produits | Construire un graph JSON-LD : Organization/Brand/WebSite/Breadcrumb/Product avec `@id` stables et liens `brand`, `manufacturer`, `isPartOf`. | Rich Results / Schema validator + crawl JSON-LD. | Prochain crawl |
| 6 | Claims bio/premium insuffisamment prouves | Medium/High contenu | Accueil, `/production/`, produits, `/organic-cognac-producer-france.html` | Creer une page preuve/certification : organisme, certificat, portee, produits couverts, mentions legales. Lier tous les claims "biologique" vers cette page. | La page contient les preuves visibles, le schema ne depasse pas le contenu. | Semaines |
| 7 | Anciennes URLs en meta refresh 200 | Medium | `/production.html`, `/demarche-bio.html`, `/leopold-et-fanny.html` | Remplacer par 301 serveur vers `/demarche/`, `/production/`, `/leopold-et-fanny/`. | `curl -I` retourne 301, pas 200. | Prochain crawl |
| 8 | `index.html` accessible en 200 | Medium | `/index.html` | 301 vers `/`. | `curl -I /index.html` retourne 301 vers `/`. | Prochain crawl |
| 9 | Pages provisoires indexables | Medium | `/mentions-legales.html`, `/valeurs-nutritionnelles.html` | Completer avant publication durable, ou `noindex` temporaire. | Contenu final valide, ou meta noindex temporaire. | Rapide |
| 10 | Galerie lourde et peu strategique | Low/Opportunity | `/galerie.html` | Noindex si reserve media interne, ou transformer en vraie page presse/media kit. | Page sortie sitemap ou enrichie. | Selon strategie |

## Technical evidence

### Crawl sitemap

- `https://cognac-esprit-organic.com/sitemap.xml` contient 21 URLs.
- Les 21 URLs du sitemap repondent en 200.
- Les 21 URLs ont `meta robots="index,follow"`.
- Les canonicals des 21 URLs correspondent aux URLs du sitemap.
- Les titres et descriptions sont presents sur les pages crawlées.
- Aucun `hreflang` n'est present, alors que la plupart des pages contiennent des blocs `data-en`.

### Host and canonical tests

- `https://cognac-esprit-organic.com/` -> 200, nouveau site statique, canonical `https://cognac-esprit-organic.com/`.
- `http://cognac-esprit-organic.com/` -> 200, meme HTML, canonical HTTPS mais pas de 301.
- Constat initial non confirme apres verification utilisateur : `https://www.cognac-esprit-organic.com/` ne doit pas etre retenu comme redirection permanente vers `ancien` sans nouveau test HTTP hors cache.
- `https://ancien.cognac-esprit-organic.com/robots.txt` -> autorise le crawl hors `/wp-admin/` et declare `https://ancien.cognac-esprit-organic.com/wp-sitemap.xml`.
- `https://ancien.cognac-esprit-organic.com/` -> canonical self vers `https://ancien.cognac-esprit-organic.com/`, meta robots `max-image-preview:large`, donc pas de `noindex`.
- `https://cognac-esprit-organique.com/` ne resout pas en DNS depuis l'environnement de test. L'ecart `organic` / `organique` est a traiter comme risque de coherence d'entite si le nom apparait ailleurs.

### Page-level evidence

- Pages produits avec H1 manquant : `fondation-vs`, `conviction-vsop`, `cohesion-napoleon`, `transmission-xo`, `xxo`, `single-cask`, `pineau`, `pineau-rouge`.
- Les pages produits utilisent un H2 pour le nom produit principal.
- `production.html`, `demarche-bio.html`, `leopold-et-fanny.html` sont des pages 200 avec `meta http-equiv="refresh"`, pas des 301 serveur.
- `assets/js/main.js` change `document.documentElement.lang` et le contenu selon `navigator.languages` / localStorage ; la version HTML initiale reste `lang="fr"`.
- `assets/css/styles.css` masque certains blocs selon `body[data-lang]`. Les versions linguistiques ne sont pas des URLs indexables distinctes.

### Structured data evidence

- Sitewide : `Organization` + `BreadcrumbList` presents.
- FAQ : `FAQPage` present sur `/faq.html` et les questions sont visibles.
- Produits : `Product` present sur les 8 pages produits.
- Tous les objets JSON-LD crawles manquent d'`@id` stable.
- Les Product schema sont utiles mais minimaux : pas d'`alcoholByVolume`, pas de `countryOfOrigin`, pas de `manufacturer`, pas de liaison stable avec l'organisation, pas d'identifiants produit. Pas d'`Offer`, ce qui est prudent tant que prix/stock/seller ne sont pas maintenus sur la page.

## Implementation notes

### Redirections Apache/OVH indicatives

Adapter selon le vhost OVH, car le probleme `www -> ancien` peut etre dans la configuration d'hebergement ou WordPress, pas seulement dans le `.htaccess` du nouveau site.

```apache
RewriteEngine On

# HTTP -> HTTPS et www -> apex
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} ^www\.cognac-esprit-organic\.com$ [NC]
RewriteRule ^ https://cognac-esprit-organic.com%{REQUEST_URI} [R=301,L]

# index.html -> racine
RewriteCond %{THE_REQUEST} \s/+index\.html[\s?] [NC]
RewriteRule ^index\.html$ https://cognac-esprit-organic.com/ [R=301,L]

# anciennes URLs statiques
RewriteRule ^production\.html$ https://cognac-esprit-organic.com/demarche/ [R=301,L]
RewriteRule ^demarche-bio\.html$ https://cognac-esprit-organic.com/production/ [R=301,L]
RewriteRule ^leopold-et-fanny\.html$ https://cognac-esprit-organic.com/leopold-et-fanny/ [R=301,L]
```

### H1 produits

Sur chaque page produit, remplacer le titre principal :

```html
<h2>Transmission XO</h2>
```

par :

```html
<h1>Transmission XO</h1>
```

Puis garder les sections "Degustation", "Notes sensorielles", etc. en H2.

### JSON-LD cible

Pattern sitewide :

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://cognac-esprit-organic.com/#organization",
      "name": "Cognac Esprit Organic",
      "url": "https://cognac-esprit-organic.com/",
      "logo": "https://cognac-esprit-organic.com/assets/img/logo-esprit-organic-brown.svg",
      "email": "Cognac@mdpierre.com",
      "telephone": "+33 5 45 35 88 10",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "30 Rue d'Angouleme",
        "postalCode": "16200",
        "addressLocality": "Triac-Lautrait",
        "addressCountry": "FR"
      },
      "sameAs": [
        "https://www.instagram.com/cognac_esprit_organic/"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://cognac-esprit-organic.com/#website",
      "url": "https://cognac-esprit-organic.com/",
      "name": "Cognac Esprit Organic",
      "publisher": {
        "@id": "https://cognac-esprit-organic.com/#organization"
      }
    }
  ]
}
```

Pattern produit :

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "@id": "https://cognac-esprit-organic.com/produits/transmission-xo.html#product",
  "name": "Transmission XO",
  "brand": {
    "@id": "https://cognac-esprit-organic.com/#organization"
  },
  "manufacturer": {
    "@id": "https://cognac-esprit-organic.com/#organization"
  },
  "category": "Cognac XO",
  "countryOfOrigin": "France",
  "image": [
    "https://cognac-esprit-organic.com/assets/img/products/transmission-xo.jpg"
  ],
  "description": "Description visible et verifiee sur la page."
}
```

Ajouter `alcoholByVolume`, `size`, `award`, `certification`, `offers` uniquement si ces informations sont visibles, verifiees et maintenues.

## Entity diagnosis

### Clair

- Nom de marque : Cognac Esprit Organic.
- Domaine officiel dans `llms.txt` : `https://cognac-esprit-organic.com`.
- Contact : `Cognac@mdpierre.com`, `+33 5 45 35 88 10`, `30 Rue d'Angouleme, 16200 Triac-Lautrait, France`.
- Personnes associees : Leopold et Fanny Croizet.
- Positionnement : cognac biologique familial, producteur, Fins Bois, export Europe/USA/Canada.
- Gamme : Fondation VS, Conviction VSOP, Cohesion Napoleon, Transmission XO, XXO, Single Cask, Pineau blanc, Pineau rouge.

### Ambigu ou a confirmer

- Statut legal exact de l'organisation / producteur / exploitant : Needs confirmation.
- Lien exact avec "Maison des Pierres" vu dans les URLs distributeurs externes : Needs confirmation.
- Portee exacte de la certification biologique : marque, domaine, produits, millesimes/lots : Needs confirmation.
- Organisme certificateur et preuve documentaire : Needs confirmation.
- "Premier XXO en agriculture biologique" : claim fort a prouver avant amplification : Needs confirmation.
- "Edition limitee" Single Cask : quantite, lot, millesime, disponibilite : Needs confirmation.
- Domaine `cognac-esprit-organique.com` absent : a reserver/rediriger si utilise oralement ou dans des supports.

## Content architecture

| Page | Intent cible | Diagnostic | Action |
| --- | --- | --- | --- |
| `/` | Marque + gamme bio | Bonne porte d'entree, message clair | Ajouter liens vers preuve bio, importateurs, produits forts |
| `/production/` | Demarche bio / durabilite | Bon contenu narratif | Devenir page preuve bio avec certification, methode, portee |
| `/demarche/` | Production / savoir-faire / Fins Bois | Bon contenu de production | Ajouter schema Article ou AboutPage si enrichi, liens vers produits |
| `/leopold-et-fanny/` | Personnes / histoire / confiance | Utile pour E-E-A-T | Ajouter role, experience, photos, liens vers production |
| `/produits/*.html` | Requetes produit | Pages substantielles mais H1/schema/facts incomplets | Ajouter H1, table de faits, ABV/bottle size/proof |
| `/organic-cognac-producer-france.html` | English organic cognac buyer intent | Page utile mais fine | Transformer en vraie landing EN ou migrer vers `/en/` |
| `/importers.html` | B2B importateurs | Bonne intention commerciale | Ajouter fiches telechargeables ou demandes de docs, sans inventer volumes |
| `/visiter.html` | Visite domaine | Bon contenu local | Ajouter informations pratiques et eventuellement LocalBusiness si valide |
| `/faq.html` | Questions marque/gamme/export | FAQ visible et schema coherent | Ajouter questions d'achat reelles, certification, livraison si valide |
| `/valeurs-nutritionnelles.html` | Reglementaire/nutrition | Incomplet mais indexable | Completer ou noindex temporaire |
| `/galerie.html` | Reserve media | Peu strategique SEO | Noindex ou transformer en media kit |

## Priority briefs

### 1. Page preuve bio / certification

- URL cible : `/production/` enrichie ou nouvelle `/certification-biologique.html`.
- Requete primaire : `cognac biologique`.
- Requetes secondaires : `organic cognac France`, `cognac bio Fins Bois`, `Cognac Esprit Organic certification`.
- Promesse : expliquer ce qui est certifie, par qui, depuis quand, sur quels produits, avec quelles limites.
- Preuves requises : certificat, organisme, numero, portee, date de validite, produits couverts.
- Liens internes : accueil, chaque produit, FAQ, importers.
- Schema : `Organization`, `Brand`, `Article` ou `AboutPage`, `ImageObject`; pas de certification schema non standard si non visible.

### 2. Template page produit

- URL cible : les 8 pages produits.
- Requete primaire : nom exact du produit.
- Structure : H1, short answer, table de faits, notes de degustation, production/provenance, preuves, disponibilite, liens internes.
- Table minimale : Brand, Product, Category, Origin, Age/blend, ABV, Bottle size, Tasting notes, Certifications, Awards, Availability.
- Schema : `Product` lie a `Organization`; `Offer` seulement si prix/seller/stock visibles et maintenables.

### 3. Landing export anglaise

- URL cible : idealement `/en/organic-cognac-producer-france/`.
- Requete primaire : `organic cognac producer France`.
- Audience : importateurs, cavistes, distributeurs, bars/hotels, reseaux bio.
- Promesse : gamme bio francaise, production Fins Bois, contact export.
- Preuves : certification bio, fiches produits, pays deja distribues seulement si confirmes.
- CTA : contact export / request product sheets.

### 4. FAQ commerciale et preuve

- URL cible : `/faq.html`.
- Ajouter seulement des questions visibles et utiles :
  - Which products are certified organic?
  - Where is Cognac Esprit Organic produced?
  - What documents are available for importers?
  - Is pricing available on the website?
  - How can professional buyers contact the producer?

## Copy upgrades

### Accueil, bloc de preuve

Actuel : le site repete le positionnement "cognac biologique" mais la preuve est diffuse.

Proposition :

> Cognac Esprit Organic est une gamme de cognacs et Pineaux des Charentes issus d'une demarche biologique conduite par Leopold et Fanny Croizet a Triac-Lautrait, dans le cru des Fins Bois. La page certification detaille les produits concernes, l'organisme de controle et les informations utiles aux acheteurs professionnels.

### Page produit, short answer

Actuel :

> Cognac biologique structure et genereux, marque par la cerise noire, les fleurs sechees et le rancio.

Proposition :

> Transmission XO est le XO de la gamme Cognac Esprit Organic. Il associe une structure genereuse a des notes de cerise noire, de fleurs sechees et de rancio, avec une production rattachee a la maison de Leopold et Fanny Croizet dans les Fins Bois.

### Importers

Actuel : page tres factuelle et volontairement prudente.

Proposition :

> For importers, Cognac Esprit Organic presents a concise organic Cognac range from France, with VS, VSOP, Napoleon, XO, XXO, Single Cask and Pineau des Charentes. Professional buyers can request product sheets, certification details, bottle photography and regulatory information before discussing availability by market.

## Schema plan

- Homepage : `Organization`, `Brand`, `WebSite`, optional `ImageObject`.
- All pages deeper than home : `BreadcrumbList`.
- Product pages : `Product` with stable `@id`, `brand`, `manufacturer`, `countryOfOrigin`, `category`, `image`, `description`, and verified fields only.
- FAQ : `FAQPage` only for questions visible on `/faq.html`.
- Cocktails : `Recipe` can remain, but ensure alcohol responsibility wording and visible ingredients/instructions match JSON-LD.
- Visit/contact : consider `Organization` only unless full LocalBusiness opening-hour data and business category are confirmed.
- Avoid `Review`, `aggregateRating`, fake `Offer`, unsupported awards, unsupported certification, or stock/price fields.

## Proof gaps

- Certification bio document, organism, number, validity dates, products/lots covered.
- Legal entity name, SIRET/company details, publication director, host details for legal notices.
- Product ABV and bottle size for every product.
- Product availability by market and whether external retailers are official partners.
- Awards/medals shown in images: source, year, competition, product, permission to claim.
- "Premier XXO en agriculture biologique" proof.
- Single Cask batch/lot, number of bottles if "limited edition" is emphasized.
- Relationship with Maison des Pierres.
- Official social profiles for `sameAs`.

## Monitoring

### Google Search Console

- Verify domain property for `cognac-esprit-organic.com`.
- Inspect these URLs after fixes: `/`, `/produits/transmission-xo.html`, `/production/`, `/demarche/`, `/organic-cognac-producer-france.html`.
- Check "Pages" for old indexed hosts: `ancien.cognac-esprit-organic.com`, `www.cognac-esprit-organic.com`, HTTP URLs and `/index.html`.
- Submit only the canonical sitemap `https://cognac-esprit-organic.com/sitemap.xml`.

### Bing / IndexNow

- Add Bing Webmaster Tools.
- After redirects and sitemap cleanup, submit sitemap and consider IndexNow for changed URLs.

### Yandex / Baidu, if international expansion continues

- Add only after canonical host and language architecture are stable.
- Submit locale-specific sitemaps only when real localized pages exist.

## 30/60/90-day roadmap

### 30 jours

- Corriger `www`, HTTP, `index.html`, anciennes URLs meta refresh.
- Ajouter H1 sur les 8 pages produits.
- Completer ou noindex temporairement mentions legales / valeurs nutritionnelles.
- Verifier que l'ancien WordPress ne s'indexe plus ou redirige proprement.

### 60 jours

- Refaire le graph JSON-LD avec `@id` stables.
- Ajouter tables de faits produits.
- Creer la page preuve bio/certification.
- Enrichir FAQ avec questions commerciales et preuve.

### 90 jours

- Decider l'architecture internationale : rester FR + page EN unique, ou deployer `/en/`, `/da/`, `/no/`, `/sv/`.
- Si architecture locale retenue, ajouter hreflang reciproque et sitemaps par langue.
- Transformer `/organic-cognac-producer-france.html` en vraie landing export ou migrer proprement vers `/en/`.
- Mettre en place monitoring GSC/Bing et suivi des anciennes URLs.
