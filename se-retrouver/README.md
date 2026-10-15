# Se retrouver · Cognac Esprit Organic

## État de livraison

Préparé le 15 octobre 2026. Le propriétaire a explicitement autorisé la création du jeton administrateur, sa conservation privée sur son Mac et dans le secret GitHub `EO_SALON_ADMIN_TOKEN`, puis la publication. Le jeton est créé (fichier local 0600) et le secret GitHub provisionné. Publication et initialisation du stockage OVH en cours.

- Page permanente prévue : `https://cognac-esprit-organic.com/se-retrouver/`.
- Retrait : `https://cognac-esprit-organic.com/se-retrouver/desinscription/`.
- Les anciens chemins `/salon/` et `/salon/desinscription/`, avec ou sans `index.html`, redirigent en 301; les fragments privés sont conservés. Des pages HTML de repli accompagnent les règles Apache.
- Le public sert encore la version précédente, non connectée, tant que cette livraison n’est pas publiée.

## Fonctionnement préparé

Instagram reste l’action principale. L’inscription ne part qu’au clic sur « Recevoir vos nouvelles ». Le téléphone, l’e-mail ou les deux sont facultatifs individuellement. Les valeurs actuelles sont relues au clic pour prendre en compte l’autoremplissage mobile, sans accès au carnet d’adresses ni stockage navigateur.

`api/salon-contact.php` accepte du JSON de même origine HTTPS. Validation serveur des formats et des canaux consentis, version et texte du consentement, date UTC, marque et source `se-retrouver`. Déduplication séparée des canaux, opérations transactionnelles SQLite. Les confirmations ne s’affichent qu’après réponse positive du serveur.

Après inscription, un lien privé permet de retirer les SMS et/ou les e-mails sans ressaisir ses coordonnées. Le jeton signé se trouve dans le fragment `#`, hors URL envoyée au serveur lors de la navigation. Sans lien, le formulaire public permet l’opposition par coordonnée avec une réponse identique, qu’elle ait été inscrite ou non. Une visite seule ne déclenche jamais de désinscription. Le retrait retire immédiatement la coordonnée active des prochains exports.

Le service concerne les inscriptions de cette page Esprit Organic. Il ne modifie pas le fichier de l’ancienne newsletter, ne copie pas les contacts de Léopold Croizet et n’envoie aucun e-mail ni SMS. Les coordonnées sont déclarées, non vérifiées par code ou double opt-in. Pour une future campagne, utiliser un export à jour et les liens de retrait par canal.

## Stockage et accès privé

- Adaptation du moteur isolé Léopold Croizet, révision `50f67c76`, sans sa connexion ultérieure à la newsletter ni son envoi de CSV par e-mail.
- PHP avec PDO SQLite et OpenSSL. Coordonnées et preuves chiffrées AES-256-GCM; identifiants HMAC, clés distinctes selon l’usage.
- Répertoire `private-eo-se-retrouver` hors de `www` sur OVH, dossier 0700, base et clé 0600. `EO_SALON_PRIVATE_DIR` permet une configuration serveur explicite; les emplacements dans les racines publiques sont refusés.
- Clé aléatoire générée sur le serveur, jamais publiée ni déployée depuis Git. Conserver ensemble clé et base pour une sauvegarde privée/restauration.
- Protection des fichiers de configuration et bibliothèques par Apache, refus des liens symboliques et permissions non privées.
- Taille de requête limitée, origine contrôlée, challenge signé à usage unique, piège à robots, quotas via empreinte IP temporaire.
- Pas de journal applicatif contenant les coordonnées, IP brute, jetons privés ou clés.
- Conservation active : trois ans après le dernier consentement explicite. Preuves et empreinte d’opposition : trois ans. Purge aux accès et quotidiennement par le workflow `salon-retention.yml`.

### Accès administrateur autorisé

Un jeton aléatoire de 64 caractères hexadécimaux permet de consulter les compteurs et d’exporter les contacts Esprit Organic. Il est conservé dans `~/.config/cognac-esprit-organic/salon-admin.token` (0600), et dans le secret `EO_SALON_ADMIN_TOKEN` du dépôt GitHub `m27g56h9yr-ux/cognac-esprit-organic-site`.

Le déploiement ne place que son empreinte SHA-256 dans `api/salon-config.php` (0600). Ce fichier est hors Git et interdit par HTTP. Sans configuration valide, le service refuse de collecter. Le jeton est transmis uniquement en en-tête Authorization sur HTTPS, jamais dans l’URL. La configuration de déploiement appelle l’état du stockage puis l’accès privé avant de déclarer l’activation terminée.

Consultation/export après activation :

```sh
python3 scripts/salon-admin.py
python3 scripts/salon-admin.py --export /chemin/prive/contacts-esprit-organic.csv
```

Les exports sont créés en 0600 hors du dépôt; les destinations existantes sont refusées et les formules de tableur neutralisées. Ils incluent uniquement les contacts actifs, les dates, textes/version de consentement et liens individuels de désinscription. Refaire l’export avant chaque campagne pour intégrer les retraits.

## Préparation et limites constatées

Syntaxe PHP des trois fichiers et JavaScript contrôlée. Relecture du code et observation de la présentation locale. Aucune suite de tests ni inscription/désinscription synthétique exécutée; aucune donnée personnelle soumise. La disponibilité des extensions, du stockage privé et de l’accès administrateur OVH reste à confirmer pendant l’activation.

Les modifications préexistantes du site, de la newsletter et du workflow restent en dehors de cette livraison : seul le patch de provisionnement propre à ce service est ajouté au workflow publié.

Référence pour la présentation du consentement : https://design.cnil.fr/concepts/consentement/ (consultée le 15 octobre 2026). Responsable et contact repris des mentions légales Esprit Organic. La durée de trois ans est la politique appliquée par ce service, non une affirmation d’une durée légale unique.
