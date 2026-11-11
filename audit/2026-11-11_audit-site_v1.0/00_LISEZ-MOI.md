# Audit du site de l'Association Amal Chabab Takaddoum — dossier v1.0

**Site audité :** https://amalchababtakadoum.org/
**Date des relevés :** 11 novembre 2026
**Version du dossier :** 1.0
**Nature du travail :** diagnostic uniquement. Le site n'a pas été modifié, rien n'a été publié, aucun formulaire n'a été envoyé et personne n'a été contacté.

## Contenu du dossier

| Fichier | Contenu |
|---|---|
| `01_Rapport_executif.md` | Livrable 1 — synthèse pour le superviseur |
| `02_Rapport_audit_detaille.md` | Livrable 2 — 74 constats sur les axes 1 à 3 et 5 à 8, et grille des références européennes (axe 9) |
| `03_Matrice_comparative_FCC_Amal.md` | Livrable 3 — comparaison des catégories de contenu avec FCC Morocco (axe 4) |
| `04_Audit_multilingue.md` | Livrable 4 — matrice des pages FR / AR / EN, rendu arabe, vocabulaire, propositions de langue |
| `05_Plan_amelioration_priorise.md` | Livrable 5 — 29 actions classées de P0 à P3 |
| `06_Registre_informations_et_decisions.md` | Livrable 6 — 10 informations à obtenir et 14 décisions à soumettre |
| `07_Registre_des_sources.md` | Adresses consultées, avec leur statut |
| `donnees/` | Tableaux CSV : constats, inventaire des pages, liens à corriger, mesures de rendu, plan d'actions, matrices |
| `captures/` | 35 captures d'écran (ordinateur, tablette, téléphone ; français, arabe, anglais) |

Les fichiers CSV s'ouvrent dans un tableur (encodage UTF-8, séparateur virgule).

## Méthode

1. **Recensement :** lecture du plan du site, puis suivi de tous les liens internes. 40 adresses explorées, dont 30 pages et 9 adresses en erreur 404.
2. **Lecture des contenus :** extraction des titres, textes, menus, liens, images et balises de chaque page, dans les trois langues.
3. **Contrôle des liens :** chaque lien interne a été confronté au statut de sa destination.
4. **Rendu réel :** 25 pages affichées dans un navigateur Chromium à trois largeurs (1366, 820 et 390 px), soit 75 rendus, avec mesure du débordement, des contrastes, des titres visibles, des images, du focus clavier et des requêtes réseau.
5. **Comparaison :** lecture de 45 pages de FCC Morocco, pour les catégories de contenu seulement.
6. **Références :** consultation directe des pages officielles de la Commission européenne, du programme Erasmus+ et du W3C.

Toutes les requêtes étaient des lectures simples, espacées d'environ une seconde. Aucun test d'intrusion, aucun scan, aucun accès à un espace privé.

## Statuts de preuve

| Statut | Sens |
|---|---|
| **VÉRIFIÉ** | Observé directement ou établi par une source identifiable |
| **À RE-VÉRIFIER** | Observé, mais exactitude ou actualité à confirmer |
| **DÉCLARÉ** | Affirmé par le site, sans preuve indépendante |
| **HYPOTHÈSE** | Interprétation plausible, non démontrée |
| **INCONNU** | Information indisponible |
| **CONTRADICTOIRE** | Informations incompatibles entre elles |

## Limites

- **Documents internes absents.** Le dossier de passation v2.1, son addendum, les statuts, les documentations techniques des pages et les relevés rédactionnels n'étaient pas disponibles dans l'environnement de travail. Les règles de gouvernance rappelées dans la demande ont été appliquées, mais les contenus du site n'ont pas pu être rapprochés de ces documents.
- **Accès public seulement.** Les réglages de WordPress, Polylang, Astra et Elementor n'ont pas été consultés ; ils sont déduits de ce que les pages affichent.
- **Mesures techniques.** Un seul navigateur, sans appareil réel ni lecteur d'écran. Aucun score Lighthouse ou PageSpeed n'a été produit. Les temps de chargement ont été mesurés à travers un proxy et sont indicatifs.
- **Artefact de l'environnement.** Dans les captures, une petite icône d'image cassée apparaît à gauche de l'adresse, dans la barre supérieure. Elle vient du blocage de `s.w.org` dans l'environnement d'audit, pas du site : un visiteur normal voit l'emoji. Ce point n'est pas compté comme un défaut. De même, la redirection de `http://` vers `https://` n'a pas pu être testée.
- **Registre des participants et plateforme des résultats Erasmus+.** Le statut du PIC et une éventuelle participation à des projets n'ont pas été recherchés.
- **FCC Morocco.** 45 pages lues sur 94 repérées ; certaines pages sont protégées contre la lecture automatique.
- **Droit.** Aucune conclusion de conformité juridique n'est tirée.

## Origine probable de certains défauts

Plusieurs défauts constatés viennent des modèles de pages importés, et non d'une erreur de saisie sur le site :

- **Liens vers des adresses inexistantes** (`/nos-poles/…`, `/l-association/`, `/actualites/`, etc.) : ces adresses provisoires figuraient dans les modèles français et ont été conservées dans les modèles arabes et anglais, avec la consigne de les remplacer après l'import.
- **Blocs « masqués » visibles :** les modèles utilisent la valeur `hidden` pour le masquage, ce qui produit la classe `elementor-hidden`. Elementor n'applique le masquage qu'avec `elementor-hidden-desktop`, `-tablet` et `-mobile`. Les contrôles faits sur les fichiers avant import avaient vérifié la présence du réglage, pas son effet à l'écran.
- **Images de substitution et double pied de page de l'accueil :** prévus comme provisoires dans les modèles.
- **Vocabulaire variable :** les textes arabes et anglais ont été fournis ou rédigés page par page, sans glossaire commun.

Ces points étaient signalés comme « à faire après l'import » dans les rapports techniques des modèles. L'audit constate qu'ils n'ont pas encore été traités.

## Point d'arrêt

La mission s'arrête à la remise de ce dossier. Toute correction relève d'une décision distincte du superviseur.
