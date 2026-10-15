# Se retrouver · Cognac Esprit Organic

## État de livraison

Préparé le 15 octobre 2026. Le propriétaire a explicitement autorisé la création du jeton administrateur, sa conservation privée sur son Mac et dans le secret GitHub `EO_SALON_ADMIN_TOKEN`, puis la publication. Le jeton est créé (fichier local 0600) et le secret GitHub provisionné. Publication et initialisation du stockage OVH terminées avec succès.

- Page permanente : `https://cognac-esprit-organic.com/se-retrouver/`.
- Retrait : `https://cognac-esprit-organic.com/se-retrouver/desinscription/`.
- Les anciens chemins `/salon/` et `/salon/desinscription/`, avec ou sans `index.html`, redirigent en 301; les fragments privés sont conservés. Des pages HTML de repli accompagnent les règles Apache.
- Livraison publique : révision `9284013778f518075a290e2d76bd0aaa3b0de315`, workflow OVH réussi en 5 min : https://github.com/m27g56h9yr-ux/cognac-esprit-organic-site/actions/runs/38767912780 .

## Fonctionnement publié

Instagram reste l’action principale. L’inscription ne part qu’au clic sur « Recevoir vos nouvelles ». Le téléphone, l’e-mail ou les deux sont facultatifs individuellement. Les valeurs actuelles sont relues au clic pour prendre en compte l’autoremplissage mobile, sans accès au carnet d’adresses ni stockage navigateur.

`api/salon-contact.php` accepte du JSON de même origine HTTPS. Validation serveur des formats et des canaux consentis, version et texte du consentement, date UTC, marque et source `se-retrouver`. Déduplication séparée des canaux, opérations transactionnelles SQLite. Les confirmations ne s’affichent qu’après réponse positive du serveur.

Après inscription, un lien privé permet de retirer les SMS et/ou les e-mails sans ressaisir ses coordonnées. Le jeton signé se trouve dans le fragment `#`, hors URL envoyée au serveur lors de la navigation. Sans lien, le formulaire public permet l’opposition par coordonnée avec une réponse identique, qu’elle ait été inscrite ou non. Une visite seule ne déclenche jamais de désinscription. Le retrait retire immédiatement la coordonnée active des prochains exports.

Le service réunit les inscriptions de cette page et celles du formulaire de nouvelles du site dans le fichier existant `newsletter-data/subscriptions.csv`. La désinscription retire le canal choisi dans les deux cas, y compris pour une adresse historique. Aucun contact de Léopold Croizet n’est copié. Chaque nouvelle inscription, depuis « Se retrouver » ou le formulaire du site, programme l’envoi de la liste complète à `cognac@mdpierre.com`. Le premier envoi est immédiat si aucun envoi ni tentative n’a eu lieu dans l’heure; les nouvelles inscriptions de la même heure sont regroupées. Les doublons et retraits seuls ne programment pas de nouvelle notification. La migration et les accès administrateur n’envoient pas de message. Les coordonnées sont déclarées, non vérifiées par code ou double opt-in. Pour une future campagne, utiliser un export à jour et les liens de retrait par canal.

## Stockage et accès privé

- Moteur Esprit Organic : preuves et opérations en attente chiffrées dans SQLite; annuaire commun dans le CSV historique protégé contre les accès HTTP. Clé, identifiants et anciens liens privés conservés.
- PHP avec PDO SQLite et OpenSSL. Preuves et coordonnées du registre de consentement chiffrées AES-256-GCM; identifiants HMAC, clés distinctes selon l’usage. Le CSV commun n’est pas chiffré : fichier 0600, dossier 0700, accès HTTP refusé par Apache, exclusion du déploiement.
- Répertoire `private-eo-se-retrouver` hors de `www` sur OVH, dossier 0700, base et clé 0600. `EO_SALON_PRIVATE_DIR` permet une configuration serveur explicite; les emplacements dans les racines publiques sont refusés.
- Clé aléatoire générée sur le serveur, jamais publiée ni déployée depuis Git. Conserver ensemble clé et base pour une sauvegarde privée/restauration.
- Protection des fichiers de configuration et bibliothèques par Apache, refus des liens symboliques et permissions non privées.
- Taille de requête limitée, origine contrôlée, challenge signé à usage unique, piège à robots, quotas via empreinte IP temporaire.
- Pas de journal applicatif contenant les coordonnées, IP brute, jetons privés ou clés.
- Conservation des nouveaux accords : trois ans après le dernier consentement explicite. Preuves et empreinte d’opposition : trois ans. Purge aux accès et quotidiennement par le workflow `salon-retention.yml`. Les lignes historiques sans version de consentement restent conservées avec leurs dates et pages originales, sans inventer de nouvelle preuve ni de consentement SMS.

### Accès administrateur autorisé

Un jeton aléatoire de 64 caractères hexadécimaux permet de consulter les compteurs et d’exporter les contacts Esprit Organic. Il est conservé dans `~/.config/cognac-esprit-organic/salon-admin.token` (0600), et dans le secret `EO_SALON_ADMIN_TOKEN` du dépôt GitHub `m27g56h9yr-ux/cognac-esprit-organic-site`.

Le déploiement ne place que son empreinte SHA-256 dans `api/salon-config.php` (0600). Ce fichier est hors Git et interdit par HTTP. Sans configuration valide, le service refuse de collecter. Le jeton est transmis uniquement en en-tête Authorization sur HTTPS, jamais dans l’URL. La configuration de déploiement appelle l’état du stockage puis l’accès privé avant de déclarer l’activation terminée.

Consultation/export après activation :

```sh
python3 scripts/salon-admin.py
python3 scripts/salon-admin.py --export /chemin/prive/contacts-esprit-organic.csv
```

Les exports sont créés en 0600 hors du dépôt; les destinations existantes sont refusées et les formules de tableur neutralisées. L’export par défaut inclut la base commune : contacts historiques et nouveaux, téléphone, pages d’inscription, accords par canal et liens individuels de retrait. `--export /chemin/prive/preuves.csv --proofs` permet l’export séparé des preuves actives du registre chiffré; les anciens contacts sans preuve nouvelle n’y figurent pas. Refaire l’export avant chaque campagne pour intégrer les retraits.

## Préparation et limites constatées

Syntaxe PHP des trois fichiers et JavaScript contrôlée. Relecture du code et observation de la présentation locale. Aucune suite de tests ni inscription/désinscription synthétique exécutée; aucune donnée personnelle soumise. Le 15 octobre 2026, le service public indique `ok: true`, `status: ready`, version `eo-se-retrouver-2026-10-15-v1`; l’accès administrateur authentifié confirme `AES-256-GCM` et `outside_public_root`. Les compteurs initiaux sont à zéro. Le parcours de saisie/soumission/retrait avec un contact synthétique n’a pas été exécuté.

Les modifications préexistantes des pages du site et du workflow de tests restent hors de cette livraison. Le point d’entrée `newsletter.php` est remplacé par le raccordement commun; sa version locale précédente et son diff sont conservés hors dépôt dans `/var/folders/l6/j383mp9n06l5lbnqzff37p2w0000gn/T/eo-shared-newsletter-hvrv0cra`. La notification utilise le destinataire déjà publié, sans publier le changement local de destinataire.

Référence pour la présentation du consentement : https://design.cnil.fr/concepts/consentement/ (consultée le 15 octobre 2026). Responsable et contact repris des mentions légales Esprit Organic. La durée de trois ans est la politique appliquée par ce service, non une affirmation d’une durée légale unique.

## Preuves de publication

- L’ancien lien `/salon/` a ouvert `/se-retrouver/` dans le navigateur public. Le lien « Désinscription » affiche le formulaire automatique à `/se-retrouver/desinscription/`.
- Capture publique mobile (390 × 844) : `/Users/leopold/.codex/visualizations/2026/10/14/01a13c74-98de-7891-9483-a9a757bfcad9/se-retrouver-public.png`.
- Le jeton du Mac est bien en 0600. Sa valeur n’a jamais été affichée ni versionnée; le secret GitHub a été installé sur autorisation explicite.
- La modification concurrente `8e75cc3` (déploiement incrémental) a été intégrée. La configuration privée passe hors du manifeste public. Une erreur OVH 550 sur les dossiers existants a été corrigée : seule leur préparation tolère ce retour; les transferts et la publication du manifeste restent stricts.
- Les modifications locales préexistantes du workflow newsletter ont été sauvegardées puis restituées; elles restent non publiées. Une sauvegarde récupérable du workflow est conservée dans `/var/folders/l6/j383mp9n06l5lbnqzff37p2w0000gn/T/eo-workflow-merge-9sl_sfxo`.


## Raccordement à la base commune — 15 octobre 2026

- Les cinq colonnes historiques `registered_at`, `email`, `language`, `market`, `page` sont conservées. Ajouts : `phone`, accords par canal, `email_page`, `phone_page`, `last_page`, dates/textes/versions d’accord, `source` et `last_source`.
- `page` conserve la première page connue; `email_page` et `phone_page` indiquent la page du dernier accord pour chaque canal; `last_page` la dernière inscription. Les nouveaux chemins excluent les paramètres et fragments d’URL. Les inscriptions du pied de page fournissent déjà l’URL courante via le JavaScript publié.
- Un téléphone seul est accepté sur Se retrouver. Une adresse connue est enrichie sans nouvelle ligne; les deux coordonnées saisies ensemble sont réunies si cela n’écrase pas une autre coordonnée. Les doublons déjà présents sont préservés; un retrait les concerne tous.
- Migration idempotente, sauvegarde chiffrée du CSV original dans SQLite pour sept jours, verrou stable entre les deux formulaires et remplacements atomiques du CSV. Les opérations sont mises en file chiffrée avant écriture du fichier, puis supprimées seulement après sauvegarde réussie. Une reprise rejoue sans dupliquer.
- Le drapeau serveur `newsletter_schema=2` est publié après les fichiers pour activer le raccordement. Si la lecture du CSV existant échoue, le service retourne une indisponibilité et ne remplace pas le fichier.
- L’accès administrateur retourne la structure, le nombre de lignes historiques, les compteurs communs, les pages et le nombre d’opérations en attente, sans coordonnées. Le statut `storage=outside_public_root` concerne le registre chiffré; `newsletter.storage=protected_newsletter_csv` décrit l’annuaire partagé.
- Syntaxe PHP relue par `php -l`; aucun test de soumission ni envoi de message effectué pendant ce raccordement. Raccordement publié avec succès : révision `5a785efdfcc7fcb37d3879f60b57a08dc931bfd4`, [workflow OVH](https://github.com/m27g56h9yr-ux/cognac-esprit-organic-site/actions/runs/38773244415) réussi en 46 secondes. La relecture administrateur confirme une ligne historique conservée, un e-mail actif, zéro téléphone et zéro opération en attente. Les 21 colonnes sont relues dans l’en-tête réel du fichier, dont `phone`, `page`, `email_page`, `phone_page` et `last_page`. La sauvegarde chiffrée expire le 22 octobre 2026 à 16:57:52 UTC.


### Observation publique du raccordement

La notice publique indique bien que les deux formulaires alimentent le même fichier et que le retrait s’applique à toute la base. Capture : `/Users/leopold/.codex/visualizations/2026/10/14/01a13c74-98de-7891-9483-a9a757bfcad9/esprit-organic-base-commune.png`. Aucune coordonnée n’a été soumise et aucun message n’a été envoyé par l’agent. Les contrôles ont porté sur la syntaxe, le déploiement, les colonnes réellement persistées et les réponses HTTP; le parcours complet d’inscription/retrait n’a pas été exécuté.


Révision finale en ligne : `169852f4088d63b323399f9fc6b4b49a0f095e80`, [déploiement réussi](https://github.com/m27g56h9yr-ux/cognac-esprit-organic-site/actions/runs/38773539408). Accès public au CSV et aux deux bibliothèques : HTTP 403; administrateur sans jeton : HTTP 401. La règle `FilesMatch` de `api/.htaccess` complète celle de la racine car les règles de réécriture locales du sous-dossier remplacent celles du parent. Après cette livraison, la base commune conserve toujours sa ligne historique et aucune opération n’est en attente.


## Notifications regroupées et essais — 15 octobre 2026

- Destinataire conservé : `cognac@mdpierre.com`. Expéditeur : `Cognac Esprit Organic <no-reply@cognac-esprit-organic.com>`. Objet : « Inscriptions Esprit Organic — liste actualisée ». Pièce jointe CSV datée : liste commune complète, téléphone et pages inclus.
- Au moins 3 600 secondes entre deux envois, avec verrou de processus et réservation persistante. Les inscriptions arrivées pendant l’attente ou l’envoi restent en attente du lot suivant. Un échec de transport conserve le lot et la réservation d’une heure avant nouvelle tentative.
- Le workflow `salon-retention.yml` passe aux minutes 7, 22, 37 et 52 de chaque heure. Il reprend les lots éligibles même sans nouvelle visite; l’heure exacte dépend aussi du déclenchement GitHub Actions. Un passage sans nouveauté n’envoie rien. Le CSV joint reflète l’état au moment de l’envoi et exclut les coordonnées retirées avant cet instant.
- Une intention d’envoi est enregistrée avant le remplacement du CSV; les opérations ne sont acquittées qu’après remplacement. Un arrêt entre les deux étapes ne perd ni inscription ni notification.
- L’état administrateur expose le destinataire, l’intervalle, l’attente, le nombre d’envois, la date et le Message-ID du dernier essai. `sent` confirme l’acceptation par le transport PHP; la réception doit être constatée dans la boîte du destinataire.
- `php scripts/test-shared-newsletter.php` utilise uniquement un hébergement et une base temporaires, des coordonnées fictives et des transports simulés. Tests : migration, inscription e-mail/téléphone, origine, doublon, retrait privé et public, adresse historique, délai de 3 599/3 600 secondes, reprise après redémarrage, panne d’envoi, inscription pendant l’envoi et quatre processus simultanés. Aucun e-mail réel dans ces tests.
- Les numéros des essais sont issus de la plage fictive [Ofcom](https://www.ofcom.org.uk/phones-and-broadband/phone-numbers/numbers-for-drama); les adresses de test utilisent `example.invalid`.
- Publication des notifications : `efd67c0bbe1513d9fc44f9092a976d621c71495a`, [déploiement réussi](https://github.com/m27g56h9yr-ux/cognac-esprit-organic-site/actions/runs/38780071103), y compris les tests isolés dans GitHub Actions.
- Essai public le 15 octobre 2026 : inscription depuis le navigateur avec une adresse `example.invalid` et un numéro fictif, relecture authentifiée de la ligne e-mail+téléphone et de la source `/se-retrouver/`. Retrait de l’e-mail par lien privé : le téléphone reste actif; retrait du téléphone : la ligne disparaît de l’annuaire commun.
- Second essai via le point d’entrée réel `newsletter.php`, avec la source `/contact.html` : ligne présente et notification `pending`, `mail_sent=false`, compteur d’envois inchangé à 1. Retrait par coordonnée via le service commun : ligne retirée.
- Réception réellement constatée dans l’INBOX `cognac@mdpierre.com` par direct_mail à 19:47:41, heure de Paris. Sujet « Inscriptions Esprit Organic — liste actualisée », expéditeur `no-reply@cognac-esprit-organic.com`, pièce jointe `contacts-esprit-organic-20261015-174739-UTC.csv` (1 494 octets). Message-ID correspondant à celui conservé par le serveur : `<eo-list-03b2a59ca62bc08d665e81b885a8a8d0@cognac-esprit-organic.com>`. Message consulté sans marquage lu.
- État final relu : zéro coordonnée d’essai dans la liste active; l’unique ligne historique est strictement identique (comparaison d’empreinte SHA-256 avant/après). Trois empreintes d’opposition restent dans le registre, conformément à la conservation des preuves. Synchronisation CSV : zéro opération en attente.
- Le second essai laisse une notification groupée en attente, éligible à partir de 20:47:39 heure de Paris. Elle utilisera la liste courante sans les contacts de test. Un seul mail reçu pendant les deux inscriptions; borne de 3 600 secondes vérifiée localement, reprise périodique conservée.
- Capture de la confirmation publique : `/Users/leopold/.codex/visualizations/2026/10/14/01a13c74-98de-7891-9483-a9a757bfcad9/esprit-organic-desinscription-test.png`.
