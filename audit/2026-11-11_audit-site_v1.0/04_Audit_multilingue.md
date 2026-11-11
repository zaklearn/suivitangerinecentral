# Livrable 4 — Audit multilingue FR / AR / EN

**Relevés du 11 novembre 2026.** Aucune page n'a été modifiée. Les corrections de langue sont des propositions, présentées à part en fin de document.

## Synthèse

- Les **7 pages institutionnelles existent dans les 3 langues** et sont associées entre elles de façon réciproque. Le sélecteur de langue conserve la page équivalente.
- Le **rendu arabe de droite à gauche est correct** sur ordinateur, tablette et téléphone.
- En revanche, **les liens internes des pages arabes et anglaises ne suivent pas la langue** : 78 pointent vers des pages françaises, en plus des liens en erreur 404.
- Le **pied de page est en français** dans les trois langues.
- Les **5 fiches projet et leur archive n'existent qu'en français**.
- Le **vocabulaire varie d'une page à l'autre** en anglais comme en arabe.

## Matrice des pages

« Association Polylang » est établie à partir des balises `hreflang` de chaque page : « réciproque » signifie que les trois pages se désignent mutuellement.

| Page FR | Page AR | Page EN | Association Polylang | Cohérence des contenus | Liens | Problèmes |
|---|---|---|---|---|---|---|
| `/` Accueil | `/ar/accueil-العربية/` | `/en/accueil-english/` | Réciproque | Même structure. Le bloc de bas de page interne est réduit en français mais complet en arabe et en anglais (8 liens). | FR : 1 lien en 404 (actualités). AR et EN : 12 liens en 404 chacun et 5 vers des pages françaises. | Titre d'onglet en français sur les pages AR et EN. Adresses « accueil-العربية » et « accueil-english ». 2 images de substitution par langue. |
| `/lassociation/` | `/ar/الجمعية/` | `/en/organization/` | Réciproque | Structure identique : 5 objectifs, 6 valeurs, 3 instances, 3 pôles. | 4 liens en 404 par langue (3 pôles et « nos pôles »). Bouton Contact AR et EN vers la page française. | Le menu anglais nomme cette page « Organization ». Phrase de consigne visible dans la bannière. 2 images de substitution. |
| `/pole-administration-et-gestion/` | `/ar/قطب-الإدارة-والتسيير/` | `/en/administration-and-management/` | Réciproque | Structure identique. | 2 liens « Découvrir le pôle » en 404 par langue. Contact AR et EN vers le français. | Statuts : « القانون الأساسي » en arabe, « bylaws » en anglais. 1 image de substitution. |
| `/pole-formation-et-integration/` | `/ar/قطب-التكوين-والإدماج/` | `/en/training-and-integration-department/` | Réciproque | Structure identique. Le texte arabe s'écarte du français sur plusieurs paragraphes (répétitions, une phrase non traduite), comme signalé à la livraison. | 2 liens en 404 par langue. Contact AR et EN vers le français. | Adresse anglaise avec « department », absent des deux autres pôles. Statuts : « النظام الأساسي » en arabe. 1 image de substitution. |
| `/pole-animation-culturelle-et-sociale/` | `/ar/قطب-التنشيط-الثقافي-والاجتماعي/` | `/en/cultural-and-social-engagement/` | Réciproque | Structure identique. | 2 liens en 404 par langue. Contact AR et EN vers le français. | Seule page anglaise à employer « Department » (13 fois) et « statutes ». Bouton arabe « اكتشف القطب » différent des autres pages. 1 image de substitution. |
| `/projets-et-programmes/` | `/ar/المشاريع-والبرامج/` | `/en/projects-and-programs/` | Réciproque | Structure identique. La page française n'a pas de titre principal (H1) ; les pages arabe et anglaise en ont un. | Le bouton vers les projets mène à l'archive française dans les 3 langues. Contact AR et EN vers le français. | Aucun contenu de projet en arabe ni en anglais. |
| `/contact/` | `/ar/اتصال/` | `/en/contact-2/` | Réciproque | Structure identique. La page française n'a pas de H1. | Menu français « Contact » → page anglaise. Menu anglais « Contact » → page française. Menu arabe correct. | Section « Coordonnées » vide et visible dans les 3 langues. En arabe et en anglais, un titre français « Coordonnées et localisation » s'affiche en haut de page. Adresse « contact-2 ». 1 image de substitution. |
| 5 fiches projet | — | — | Aucune | Français uniquement. | Le sélecteur de langue renvoie à l'accueil de la langue choisie. | Contenu d'expérience inaccessible en arabe et en anglais. |
| `/category/projets-programmes/` | — | — | Aucune | Français uniquement. | — | Titre « Projets & Programmes » différent du menu. |
| `/author/manager_web/` | `/ar/author/manager_web/` | `/en/author/manager_web/` | Aucune | Pages techniques sans intérêt pour le public. | — | Présentes dans le plan du site. |

## Éléments communs à toutes les pages

| Élément | Français | Arabe | Anglais |
|---|---|---|---|
| Menu principal | 7 entrées, correctes sauf « Contact » → page anglaise | 7 entrées, toutes correctes | 7 entrées, correctes sauf « Contact » → page française |
| Sélecteur de langue | Fonctionne | Fonctionne | Fonctionne |
| Barre d'informations (ordinateur) | Adresse et téléphone en français | Adresse en français | Adresse en français |
| Pied de page global | En français | **En français**, liens vers les pages françaises | **En français**, liens vers les pages françaises |
| Lien « Formation et Intégration » du pied de page | Mène au Pôle Administration | Idem | Idem |
| Code de langue déclaré | `fr-FR` | `ary` (arabe dialectal marocain) au lieu de `ar` | `en-US` |
| Page d'erreur 404 | En français | En arabe | En anglais |
| Méta-description | Absente | Absente | Absente |

## Rendu arabe (droite à gauche)

Contrôlé par rendu Chromium sur 7 pages et 3 largeurs d'écran (21 captures).

| Point vérifié | Résultat |
|---|---|
| Direction du document | `dir="rtl"` sur toutes les pages arabes |
| Alignement des titres et des textes | À droite pour les éléments non centrés ; centrage conservé ailleurs |
| Ordre des colonnes | Inversé : texte à droite, image à gauche |
| Ordre des cartes | De droite à gauche |
| Menu et sélecteur de langue | Inversés ; menu mobile fonctionnel |
| Boutons | Alignés à droite, libellés lisibles |
| Débordement horizontal | Aucun sur ordinateur, tablette et téléphone |
| Éléments restés en français | Pied de page global, adresse de l'en-tête, titre parasite de la page Contact |

Limite : le rendu a été contrôlé dans un seul navigateur (Chromium), sans test sur appareil réel ni avec un lecteur d'écran.

## Vocabulaire

### Anglais

| Notion | Variantes relevées | Pages |
|---|---|---|
| Pôle | « area(s) of work » ; « Department » | 6 pages ; 1 page (13 occurrences) |
| Pôle Animation Culturelle et Sociale | « Cultural and Social Engagement » ; « Cultural and Social Activities » ; « Cultural and Social Engagement Department » | Menu ; accueil et L'association ; titre de la page |
| Statuts | « bylaws » ; « statutes » | 3 pages (19 occurrences) ; 2 pages (6 occurrences) |
| Orientations statutaires | « statutory objectives » ; « statutory orientations » | 3 pages ; 2 pages |
| Domaines d'intervention | « fields of work » ; « areas of intervention » | 2 pages ; 1 page |
| Bouton « Découvrir le pôle » | « Explore This Area » ; « Discover the Department » | 3 pages ; 1 page |
| Fonctionnement collégial | « Shared Governance » ; « Collegial Functioning » | 1 page chacun |

### Arabe

| Notion | Variantes relevées | Pages |
|---|---|---|
| Statuts | « القانون الأساسي » ; « النظام الأساسي » ; « القوانين الأساسية » | 2 pages (12) ; 2 pages (12) ; 1 page (1) |
| Bouton « Découvrir le pôle » | « اكتشف هذا القطب » ; « اكتشف القطب » | 3 pages ; 1 page |
| Contribution | « إسهام » ; « مساهمة » | 2 pages ; 3 pages |
| Éducation non formelle | « التعليم غير النظامي » (la variante « التربية غير النظامية » a été écartée) | 1 page |
| Contact | « اتصال » (menu) ; « اتصلوا بنا » (titre) ; « تواصلوا معنا » (boutons) | Toutes |

Le terme arabe désignant les statuts doit être celui du document officiel de l'association ; il n'a pas été vérifié.

## Propositions de correction linguistique (non appliquées)

Ces propositions sont séparées des constats. Elles supposent qu'un glossaire soit d'abord arrêté par le superviseur.

| Langue | Élément | Texte actuel | Proposition | Motif |
|---|---|---|---|---|
| EN | Menu | Organization | About the Association | « Organization » désigne ici la page de présentation ; le terme est ambigu. |
| EN | Nom du 3ᵉ pôle | Trois variantes | Une seule forme dans le menu, les titres et les cartes | Éviter de faire croire à trois entités. |
| EN | Statuts | bylaws / statutes | Un seul terme | Cohérence ; « bylaws » est majoritaire. |
| EN | Page Projets | Projects Implemented by the Association | À revoir avec le titre français | « Implemented » affirme une exécution non démontrée (A1-08). |
| EN | Page L'association | An introduction to the association's identity and purpose. | À retirer ou remplacer | Phrase de consigne (A1-09). |
| AR | Statuts | Trois variantes | Le terme du document officiel | Exactitude institutionnelle. |
| AR | Menu Contact | اتصال | اتصل بنا ou اتصلوا بنا, comme le titre | Cohérence menu / page. |
| AR | Pôle Formation | Paragraphes répétés entre sections ; une phrase du français non traduite | Relecture face au texte français | Écarts déjà signalés à la livraison. |
| AR et EN | Titre d'onglet de l'accueil | Texte français | Titre dans la langue de la page | A6-03. |
| AR et EN | Pied de page | Français | Traduction | A6-05. |
