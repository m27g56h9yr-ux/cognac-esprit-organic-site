# Instructions projet — Cognac Esprit Organic

## Objectif

Reconstruire le site Cognac Esprit Organic pour :
- améliorer le référencement Google ;
- être facilement compris par ChatGPT et les agents IA ;
- mieux convertir les importateurs, cavistes, CHR, bars, hôtels et réseaux bio ;
- présenter clairement la gamme de Cognac biologique.

## Domaine officiel

Domaine officiel :
https://cognac-esprit-organic.com

Ne jamais utiliser croizet.fr.
Ne pas confondre Esprit Organic avec une autre maison ou marque.

## Regle permanente d'audit

- Auditer par defaut uniquement le nouveau site public : `https://cognac-esprit-organic.com/`.
- Ne pas inclure `https://ancien.cognac-esprit-organic.com/` dans les audits du nouveau site.
- `ancien.cognac-esprit-organic.com` est l'ancien site WordPress conserve pour memoire.
- Ne verifier `ancien.cognac-esprit-organic.com` que si l'utilisateur le demande explicitement, ou pour confirmer ponctuellement qu'il reste non indexable.
- Quand un audit mentionne "le site" ou "Cognac Esprit Organic", comprendre : le nouveau site sur `cognac-esprit-organic.com`, pas l'ancien WordPress.

## Regle OVH permanente

- Le nouveau site refait dans ce depot GitHub doit etre le site public principal.
- Il doit etre consultable a l'adresse : https://cognac-esprit-organic.com/
- L'ancien site WordPress doit rester accessible a l'adresse : https://ancien.cognac-esprit-organic.com/
- L'ancien site WordPress ne doit pas etre indexe par Google ni par les autres moteurs.
- Ne pas rediriger durablement `ancien.cognac-esprit-organic.com` vers le domaine principal.
- Toute correction SEO sur `ancien.cognac-esprit-organic.com` doit preserver son accessibilite tout en ajoutant une protection `noindex` fiable.

## Identité

Esprit Organic est une marque de Cognac biologique liée à Maison des Pierres.
La marque est portée par Léopold et Fanny Croizet.
Positionnement : Cognac bio, familial, naturel, premium, indépendant.

## Ton éditorial

- clair ;
- premium ;
- sobre ;
- professionnel ;
- factuel ;
- export-compatible ;
- compréhensible par un acheteur professionnel international.

## Priorités

1. Site rapide et sécurisé.
2. Pages produits propres.
3. Page importateurs.
4. Page “Organic Cognac Producer in France”.
5. Données structurées Schema.org.
6. Sitemap propre.
7. Robots.txt propre.
8. Fichier llms.txt.
9. Accessibilité agents IA.
10. Version anglaise professionnelle.

## Workflow GitHub

- Avant tout envoi vers GitHub (`git push`), demander l'autorisation réseau si elle n'est pas déjà active.
- Si GitHub répond `Could not resolve host: github.com`, refaire l'essai après autorisation réseau.

## Interdictions

- ne pas inventer d’informations ;
- ne pas inventer de récompenses ;
- ne pas inventer de volumes ;
- ne pas inventer de distributeurs ;
- ne pas ajouter de liens vers croizet.fr ;
- ne pas inclure de mots de passe, clés API ou identifiants.
