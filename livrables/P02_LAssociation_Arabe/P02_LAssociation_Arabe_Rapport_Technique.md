# P-02 L’association — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**
Livrable associé : `P02_LAssociation_Amal_Chabab_Takaddoum_Arabe_Elementor.json`
Source de référence : `P02_LAssociation_Amal_Chabab_Takaddoum_Elementor.json` (SHA-256 `5c023191…ff64a001`, **non modifié**, empreinte identique avant et après génération).
Référence complémentaire : `P01_Accueil_Amal_Chabab_Takaddoum_Arabe_Elementor.json` (méthode RTL, libellés validés réutilisés).

> ⚠️ **TRADUCTION : PROPOSITION NON VALIDÉE.**
> Aucun contenu arabe n’ayant été transmis pour P-02, le superviseur a demandé un **brouillon de traduction** réalisé à partir du JSON français.
> **Les 52 textes arabes de ce modèle sont des propositions non validées.** Ils doivent faire l’objet d’une validation éditoriale avant toute intégration. Les points de traduction ambigus sont listés en section 8.

---

## 0. Statut des contrôles

| Contrôle | Méthode | Statut |
|---|---|---|
| Validité syntaxique JSON | `json.load` Python | ✅ Exécuté |
| 7 sections, même ordre | Comparaison arborescente source ↔ arabe | ✅ Exécuté |
| 94 éléments, hiérarchie, types, `isInner`, nombre d’enfants | Comparaison récursive nœud à nœud | ✅ Exécuté (94/94 : 40 conteneurs, 24 headings, 24 text-editors, 4 boutons, 2 images) |
| Aucun réglage modifié hors texte et alignement RTL | Diff clé par clé de tous les `settings` | ✅ Exécuté (seules clés modifiées : `title` ×24, `editor` ×24, `text` ×4, `align` ajouté ×39) |
| Unicité des identifiants | Comptage | ✅ Exécuté (94/94 uniques) |
| Absence de collision avec P-02 FR et P-01 AR | Intersection des ensembles d’ID | ✅ Exécuté (0 et 0) |
| Aucun texte français visible restant | Recherche de caractères latins dans `title`, `editor`, `text` | ✅ Exécuté — seule exception volontaire : le nom anglais officiel « Amal for Progress » (voir 8.2) |
| Ancres `#missions` et `#organisation` | Correspondance boutons S1 ↔ `_element_id` des sections S3/S5 | ✅ Exécuté (2/2) |
| Images de substitution | Lecture des URL | ✅ Exécuté (2/2, URL identiques à la source) |
| Paramètres de page | Lecture `page_settings` | ✅ Exécuté |
| Absence de widget Pro | Liste des `widgetType` | ✅ Exécuté (heading, text-editor, button, image : tous gratuits) |
| **Import dans Elementor** | — | ⛔ **Non réalisé** — à faire par le superviseur |
| **Rendu visuel RTL (bureau / tablette / mobile)** | — | ⛔ **Non réalisé** — aucun test dans WordPress/Elementor |
| **Défilement vers les ancres, absence de débordement mobile** | — | ⛔ **Non vérifiable hors import réel** |
| **Qualité éditoriale de la traduction** | — | ⛔ **Non validée** — relecture par un rédacteur arabophone requise |

---

## 1. Structure des sept sections

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | Ligne 2 colonnes (58 % / 38 %) : H1 + sous-titre + texte + 2 boutons d’ancre ‖ image de substitution |
| S2 | S2 — Identité | `#FFFFFF` | Ligne 2 colonnes (57 % / 39 %) : H2 + texte (4 paragraphes) ‖ image de substitution |
| S3 | S3 — Mission et objectifs (ancre `#missions`) | `#F4F6F6` | H2 centré + grille de 5 cartes objectifs (4 × 48 % + 1 × 100 %) |
| S4 | S4 — Valeurs | `#FFFFFF` | En-tête centré (H2 + intro) + grille de 6 cartes valeurs (32 % → 48 % → 100 %) |
| S5 | S5 — Organisation (ancre `#organisation`) | `#F4F6F6` | En-tête centré + grille de 3 instances (33 % → 48 % → 100 %) |
| S6 | S6 — Trois pôles | `#FFFFFF` | En-tête centré + grille de 3 cartes pôles (titres liés) + bouton général |
| S7 | S7 — Appel à l’action | `#152A33` | H2 + texte + bouton Contact, centrés |

## 2. Nombre et types d’éléments

| Type | Source FR | Arabe |
|---|---|---|
| `container` | 40 | 40 |
| `heading` | 24 | 24 |
| `text-editor` | 24 | 24 |
| `button` | 4 | 4 |
| `image` | 2 | 2 |
| **Total** | **94** | **94** |

Aucun élément ajouté, supprimé, fusionné ou déplacé.

## 3. Identifiants

- 94 identifiants d’éléments, **tous uniques**. Aucun widget de ce modèle ne contient d’identifiant interne de répéteur (`_id`).
- **Nouveaux identifiants** au format hexadécimal à 7 caractères, préfixe `4c3` (`4c30001` à `4c3005e`), distincts du P-02 français (`3b2…`) et du P-01 arabe (`3a2…`) : **0 collision** avec chacun.
- Note : la consigne « conserver leurs identifiants » et l’exigence 5.5 « absence de collision avec le modèle français » sont contradictoires pour les identifiants Elementor internes. L’exigence 5.5 du task-prompt a été appliquée. Les **identifiants techniques visibles** — les ancres `missions` et `organisation` — sont, eux, **conservés à l’identique**. La correspondance FR ↔ AR de chaque ID figure dans le tableau de la section 11.
- Hiérarchie parent-enfant inchangée (renumérotation sur place pendant le parcours de l’arbre).

## 4. Paramètres de page

| Clé | Source | Arabe |
|---|---|---|
| `version` | `0.4` | `0.4` |
| `type` | `page` | `page` |
| `page_settings.template` | `elementor_header_footer` | `elementor_header_footer` ✅ |
| `page_settings.hide_title` | `yes` | `yes` ✅ |
| `title` (nom du modèle, bibliothèque admin uniquement) | `P-02 L’association — Association Amal Chabab Takaddoum` | `P-02 L’association (AR) — Association Amal Chabab Takaddoum` |

## 5. Paramètres RTL appliqués

### 5.1 Propriété ajoutée : `align: "right"` (39 widgets)

Ajoutée uniquement aux titres et paragraphes **sans alignement défini** dans la source. Les **9 éléments centrés** de la version française restent centrés : H2 de S3 ; H2 + intro de S4, S5 et S6 ; H2 + texte de S7. Aucune autre propriété n’a été ajoutée ; aucune police, marge, padding ou largeur n’a été modifié.

| ID FR → ID AR | Widget | Libellé |
|---|---|---|
| `3b20001` → `4c30004` | heading | S1 · H1 |
| `3b20002` → `4c30005` | text-editor | S1 · Sous-titre |
| `3b20003` → `4c30006` | text-editor | S1 · Texte |
| `3b2000c` → `4c3000f` | heading | S2 · H2 |
| `3b2000d` → `4c30010` | text-editor | S2 · Texte (4 paragraphes) |
| `3b20014` → `4c30017` | heading | S3 · H3 objectif 1 |
| `3b20015` → `4c30018` | text-editor | S3 · Texte objectif 1 |
| `3b20017` → `4c3001a` | heading | S3 · H3 objectif 2 |
| `3b20018` → `4c3001b` | text-editor | S3 · Texte objectif 2 |
| `3b2001a` → `4c3001d` | heading | S3 · H3 objectif 3 |
| `3b2001b` → `4c3001e` | text-editor | S3 · Texte objectif 3 |
| `3b2001d` → `4c30020` | heading | S3 · H3 objectif 4 |
| `3b2001e` → `4c30021` | text-editor | S3 · Texte objectif 4 |
| `3b20020` → `4c30023` | heading | S3 · H3 objectif 5 |
| `3b20021` → `4c30024` | text-editor | S3 · Texte objectif 5 |
| `3b20028` → `4c3002b` | heading | S4 · H3 valeur 1 |
| `3b20029` → `4c3002c` | text-editor | S4 · Texte valeur 1 |
| `3b2002b` → `4c3002e` | heading | S4 · H3 valeur 2 |
| `3b2002c` → `4c3002f` | text-editor | S4 · Texte valeur 2 |
| `3b2002e` → `4c30031` | heading | S4 · H3 valeur 3 |
| `3b2002f` → `4c30032` | text-editor | S4 · Texte valeur 3 |
| `3b20031` → `4c30034` | heading | S4 · H3 valeur 4 |
| `3b20032` → `4c30035` | text-editor | S4 · Texte valeur 4 |
| `3b20034` → `4c30037` | heading | S4 · H3 valeur 5 |
| `3b20035` → `4c30038` | text-editor | S4 · Texte valeur 5 |
| `3b20037` → `4c3003a` | heading | S4 · H3 valeur 6 |
| `3b20038` → `4c3003b` | text-editor | S4 · Texte valeur 6 |
| `3b2003f` → `4c30042` | heading | S5 · H3 instance 1 |
| `3b20040` → `4c30043` | text-editor | S5 · Texte instance 1 |
| `3b20042` → `4c30045` | heading | S5 · H3 instance 2 |
| `3b20043` → `4c30046` | text-editor | S5 · Texte instance 2 |
| `3b20045` → `4c30048` | heading | S5 · H3 instance 3 |
| `3b20046` → `4c30049` | text-editor | S5 · Texte instance 3 |
| `3b2004d` → `4c30050` | heading | S6 · H3 carte 1 (lien P-03) |
| `3b2004e` → `4c30051` | text-editor | S6 · Texte carte 1 |
| `3b20050` → `4c30053` | heading | S6 · H3 carte 2 (lien P-04) |
| `3b20051` → `4c30054` | text-editor | S6 · Texte carte 2 |
| `3b20053` → `4c30056` | heading | S6 · H3 carte 3 (lien P-05) |
| `3b20054` → `4c30057` | text-editor | S6 · Texte carte 3 |

### 5.2 Comportements RTL dépendant du document en `dir="rtl"` (aucune propriété ajoutée)

Comme pour P-01, aucune propriété « direction » n’existe par widget dans Elementor gratuit ; aucune propriété inconnue n’a été créée. Lorsque la page est assignée à la langue Arabe (RTL) dans Polylang :
- **S1, S2** : la colonne texte s’affiche à droite et l’image à gauche ; sur mobile l’ordre reste texte puis image.
- **Grilles S3, S4, S5, S6** (`flex_direction: row` + `wrap`) : les cartes se remplissent de droite à gauche (carte 1 en haut à droite). La 5ᵉ carte objectif (100 %) reste pleine largeur.
- **Boutons S1** (conteneur `flex-start`) : alignés à droite, bouton « مهامنا » à droite. Boutons S6 et S7 : conservent leur justification source.

### 5.3 Réglages manuels RTL requis

1. Polylang → Langues → Arabe : vérifier « Sens du texte » = **RTL** (vérification seulement).
2. Après import, vérifier sur les 39 widgets listés en 5.1 que l’alignement affiché est bien à droite (le contrôle peut apparaître en « Gauche/Droite » ou « Début/Fin » selon la version d’Elementor).
3. Vérifier que la police globale dispose de glyphes arabes (aucune police imposée).
4. Vérifier l’affichage du nom latin « Amal for Progress » au sein du paragraphe arabe S2 (mélange bidirectionnel : les guillemets « » et la virgule arabe doivent rester à leur place).

## 6. Paramètres responsive conservés

**Aucune valeur modifiée** : typographies bureau/tablette/mobile (H1 44/38/30 ; H2 34/30/26 ; H3 20/20/19 et 18/18/17 ; sous-titre 20/19/17 ; textes 18/17/16, 17/17/16, 16/16/15), largeurs de colonnes et de cartes (58/38, 57/39, 48/100, 32/48/100, 33/48/100), paddings de sections (96–100 / 72 / 56) et de cartes, `flex_gap` et déclinaisons, `flex_wrap`, `flex_direction_mobile: column`, largeurs personnalisées des textes centrés.
Point d’attention : les textes arabes ont une longueur différente du français ; contrôler visuellement les hauteurs de cartes (S3, S4, S5) et les boutons de S1 sur mobile.

## 7. Ancres et liens internes

### 7.1 Ancres (fonctionnelles dans la structure)

| Bouton S1 | Libellé arabe | Lien | Section cible | `_element_id` | Statut |
|---|---|---|---|---|---|
| `4c30008` | مهامنا | `#missions` | S3 (`4c30013`) | `missions` | ✅ Correspondance vérifiée |
| `4c30009` | تنظيمنا | `#organisation` | S5 (`4c3003c`) | `organisation` | ✅ Correspondance vérifiée |

Les identifiants d’ancre sont conservés en caractères latins (non traduits) : ils ne sont pas visibles et restent fonctionnels.

### 7.2 Liens internes à associer manuellement dans Polylang

Aucun permalien arabe n’étant confirmé, **les cibles françaises sont conservées comme références provisoires** ; aucun slug, préfixe de langue ou URL Polylang n’a été inventé.

| # | Section | Élément (ID AR) | Libellé arabe | Cible conservée (FR) | Page arabe à associer | Statut |
|---|---|---|---|---|---|---|
| 1 | S6 | Titre carte 1 (`4c30050`) | قطب الإدارة والتسيير | `/nos-poles/administration-et-gestion/` | P-03 (AR) | ⚠️ Inconnue |
| 2 | S6 | Titre carte 2 (`4c30053`) | قطب التكوين والإدماج | `/nos-poles/formation-et-integration/` | P-04 (AR) | ⚠️ Inconnue |
| 3 | S6 | Titre carte 3 (`4c30056`) | قطب التنشيط الثقافي والاجتماعي | `/nos-poles/animation-culturelle-et-sociale/` | P-05 (AR) | ⚠️ Inconnue |
| 4 | S6 | Bouton général (`4c30059`) | اكتشف أقطابنا الثلاثة | `/nos-poles/` | Nos pôles (AR) | ⚠️ Inconnue |
| 5 | S7 | Bouton (`4c3005e`) | تواصلوا معنا | `/contact/` | Contact (AR) | ⚠️ Inconnue |

La correspondance fonctionnelle pôle ↔ lien est préservée (chaque titre arabe pointe vers la cible de son équivalent français). Tant que ces liens ne sont pas remplacés, ils mènent aux pages **françaises**.

## 8. Points de traduction à valider (ambiguïtés signalées, non résolues par invention)

| # | ID FR | Point | Choix proposé | Alternative / question |
|---|---|---|---|---|
| 1 | `3b20003` | « Présentation de l’identité et de la vocation de l’association. » ressemble à une **note éditoriale** plutôt qu’à un texte public. | Traduit littéralement : تقديم هوية الجمعية ورسالتها. | Confirmer si ce texte doit rester visible (FR et AR). |
| 2 | `3b2000d` | Nom anglais « Amal for Progress ». | Conservé en caractères latins entre « ». | Seul texte latin de la page, volontaire. |
| 3 | `3b2003f`, `3b20043` | « Assemblée générale ». | **الجمع العام** (usage associatif marocain). | الجمعية العامة. ⚠️ Si retenu, accorder au féminin le texte `3b20040` (تشكل… وتساهم…). |
| 4 | `3b20042` | « Bureau exécutif ». | المكتب التنفيذي | Vérifier la dénomination exacte dans les statuts arabes (ex. المكتب المسير). |
| 5 | `3b20018` | « lutte contre l’illettrisme ». | محاربة الأمية | L’arabe ne distingue pas usuellement illettrisme / analphabétisme ; vérifier le terme des statuts. |
| 6 | `3b20018` | « éducation non formelle ». | التربية غير النظامية (terme institutionnel marocain). | — |
| 7 | plusieurs | « statuts », « orientations statutaires », « pôles statutaires ». | القانون الأساسي / التوجهات المنصوص عليها في القانون الأساسي. | Vérifier l’intitulé arabe officiel des statuts. |
| 8 | `3b2000d` (§4) | « tout en prévoyant une ouverture à la coopération » — « prévoyant » peut signifier une disposition statutaire ou une intention. | مع التنصيص على الانفتاح… (lecture statutaire). | مع الانفتاح على التعاون… si le sens est une simple intention. |
| 9 | `3b20040` | Sujet implicite « Elle » (= l’Assemblée générale, donné par le titre). | Phrase sans sujet répété : يشكل الهيئة… (accord masculin avec الجمع العام). | Voir point 3. |
| 10 | S4 | Textes des valeurs commençant en minuscule (suite du titre). | Rendus par des groupes nominaux (masdar) terminés par un point. | — |
| 11 | `3b20037` | « Initiative ». | المبادرة | روح المبادرة |
| 12 | `3b20004`, `3b20013` | Pluriel « Nos missions » (bouton) / singulier « Notre mission » (H2) dans la source. | مهامنا / مهمتنا — différence conservée. | Harmoniser si souhaité (FR et AR). |
| 13 | `3b20005` | « Notre organisation ». | تنظيمنا | هيكلتنا التنظيمية |
| 14 | `3b2003c` | « Une organisation structurée ». | تنظيم مُهيكل | — |
| 15 | `3b20017` | « éducation » dans le titre. | التعليم (cohérence avec P-01 validé). | التربية ; le texte associé emploie التربية pour « éducation non formelle » et « accompagnement éducatif ». |
| 16 | `3b2005b` | « vos attentes ». | انتظاراتكم (usage marocain). | تطلعاتكم |
| 17 | réutilisés | Nom de l’association, noms des trois pôles, « Nous contacter » → تواصلوا معنا. | Repris **à l’identique** du P-01 arabe validé. | — |

## 9. Points de configuration manuelle et limites

1. **Validation éditoriale** des 52 textes (sections 8 et 11) avant import.
2. **Import** : Elementor → Modèles → Importer, puis insertion dans une nouvelle page.
3. **Polylang** : assigner la page à l’Arabe et la lier comme traduction de la page française « L’association ».
4. **Liens** : remplacer les 5 cibles de la section 7.2 dès que les pages arabes existent.
5. **Ancres** : après import, cliquer sur les deux boutons de S1 et vérifier le défilement vers S3 et S5 (non testé).
6. **Images** : remplacer les 2 images de substitution et renseigner un texte alternatif arabe (vide dans la source ; rien inventé).
7. **Limites** : contrôles exclusivement statiques sur le JSON. L’interprétation de `align: right` et le rendu RTL dépendent de la version d’Elementor et de la configuration Polylang ; **non testés** dans WordPress.

**Réglages globaux** : aucune modification d’Astra, des réglages globaux Elementor (couleurs, polices), de Polylang, des menus, des en-têtes/pieds de page ou du SEO global. Aucune intervention sur le site, aucune publication.

## 10. Métadonnées SEO proposées (non injectées dans le JSON — propositions non validées)

| Champ | Proposition | Longueur |
|---|---|---|
| Titre SEO | الجمعية \| جمعية أمل شباب التقدم بالرباط | ≈ 40 caractères |
| Méta-description | تعرّفوا على جمعية أمل شباب التقدم بالرباط: هويتها، ومهمتها وأهدافها، وقيمها، وهيئاتها التنظيمية، وأقطابها الثلاثة في خدمة الشباب والتنمية الاجتماعية. | ≈ 150 caractères |
| Slug (**proposition non validée**) | `الجمعية` (alternative latine : `l-association-ar`) | — |

Formulations tirées exclusivement du contenu de la page ; « الجمعية » reprend le libellé de menu validé dans P-01 (S7).

## 11. Tableau de correspondance (Livrable 4)

94 lignes, une par élément. Tous les textes visibles (24 titres, 24 éditeurs de texte, 4 boutons = **52 textes**) sont couverts : **52/52 traduits — statut « proposition non validée »**, 0 oublié. Les conteneurs et images sont listés pour contrôle de complétude. HTML affiché échappé.

| # | ID FR | ID AR | Section | Type | Libellé interne (`_title`) | Contenu français | Contenu arabe (proposition) | Statut |
|---|---|---|---|---|---|---|---|---|
| 1 | `3b2000b` | `4c30001` | S1 | container | S1 — Bannière | — | — | Sans texte visible |
| 2 | `3b2000a` | `4c30002` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible |
| 3 | `3b20007` | `4c30003` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible |
| 4 | `3b20001` | `4c30004` | S1 | heading | S1 · H1 | L’association Amal Chabab Takaddoum | جمعية أمل شباب التقدم | Traduit — proposition non validée |
| 5 | `3b20002` | `4c30005` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Une ambition collective au service de la jeunesse et du développement social.&lt;/p&gt; | &lt;p&gt;طموح جماعي في خدمة الشباب والتنمية الاجتماعية.&lt;/p&gt; | Traduit — proposition non validée |
| 6 | `3b20003` | `4c30006` | S1 | text-editor | S1 · Texte | &lt;p&gt;Présentation de l&#x27;identité et de la vocation de l&#x27;association.&lt;/p&gt; | &lt;p&gt;تقديم هوية الجمعية ورسالتها.&lt;/p&gt; | Traduit — proposition non validée |
| 7 | `3b20006` | `4c30007` | S1 | container | S1 · Boutons | — | — | Sans texte visible |
| 8 | `3b20004` | `4c30008` | S1 | button | S1 · Bouton 1 → ancre #missions | Nos missions | مهامنا | Traduit — proposition non validée |
| 9 | `3b20005` | `4c30009` | S1 | button | S1 · Bouton 2 → ancre #organisation | Notre organisation | تنظيمنا | Traduit — proposition non validée |
| 10 | `3b20009` | `4c3000a` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |
| 11 | `3b20008` | `4c3000b` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée (URL inchangée) |
| 12 | `3b20012` | `4c3000c` | S2 | container | S2 — Identité | — | — | Sans texte visible |
| 13 | `3b20011` | `4c3000d` | S2 | container | S2 · Ligne 2 colonnes | — | — | Sans texte visible |
| 14 | `3b2000e` | `4c3000e` | S2 | container | S2 · Colonne texte | — | — | Sans texte visible |
| 15 | `3b2000c` | `4c3000f` | S2 | heading | S2 · H2 | Une association ancrée dans son territoire | جمعية متجذرة في محيطها الترابي | Traduit — proposition non validée |
| 16 | `3b2000d` | `4c30010` | S2 | text-editor | S2 · Texte (4 paragraphes) | &lt;p&gt;L’Association Amal Chabab Takaddoum est une organisation associative marocaine dont le siège social est établi à Rabat. Connue en anglais sous le nom « Amal for Progress », elle inscrit son engagement dans la promotion du développement, de la culture, de l&#x27;action sociale et du sport au profit de la jeunesse.&lt;/p&gt;<br>&lt;p&gt;Son projet associatif repose sur une conviction : l&#x27;engagement des jeunes, la solidarité et la participation citoyenne constituent des leviers importants pour accompagner les dynamiques de progrès au sein de la société.&lt;/p&gt;<br>&lt;p&gt;À travers ses orientations statutaires, l&#x27;association entend contribuer à la valorisation des talents, à l&#x27;amélioration des opportunités éducatives et formatives, au renforcement des solidarités et à la participation des jeunes à la vie collective.&lt;/p&gt;<br>&lt;p&gt;Son ancrage à Rabat constitue le cadre territorial de son engagement, tout en prévoyant une ouverture à la coopération avec des associations et des organismes partageant des objectifs similaires, au niveau national et international.&lt;/p&gt; | &lt;p&gt;جمعية أمل شباب التقدم منظمة جمعوية مغربية يوجد مقرها الاجتماعي بمدينة الرباط. وتُعرف باللغة الإنجليزية باسم «Amal for Progress»، وتندرج التزاماتها ضمن النهوض بالتنمية والثقافة والعمل الاجتماعي والرياضة لفائدة الشباب.&lt;/p&gt;<br>&lt;p&gt;ويقوم مشروعها الجمعوي على قناعة مفادها أن انخراط الشباب والتضامن والمشاركة المواطنة تشكل روافع مهمة لمواكبة ديناميات التقدم داخل المجتمع.&lt;/p&gt;<br>&lt;p&gt;ومن خلال توجهاتها المنصوص عليها في قانونها الأساسي، تسعى الجمعية إلى الإسهام في تثمين المواهب، وتحسين فرص التعليم والتكوين، وتعزيز التضامن، ومشاركة الشباب في الحياة الجماعية.&lt;/p&gt;<br>&lt;p&gt;ويشكل حضورها بمدينة الرباط الإطار الترابي لالتزامها، مع التنصيص على الانفتاح على التعاون مع الجمعيات والهيئات التي تتقاسم معها أهدافًا مماثلة، على المستويين الوطني والدولي.&lt;/p&gt; | Traduit — proposition non validée |
| 17 | `3b20010` | `4c30011` | S2 | container | S2 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |
| 18 | `3b2000f` | `4c30012` | S2 | image | S2 · IMAGE À REMPLACER — ancrage territorial à Rabat | — | — | Image de substitution conservée (URL inchangée) |
| 19 | `3b20024` | `4c30013` | S3 | container | S3 — Mission et objectifs (ancre #missions) | — | — | Ancre `#missions` conservée |
| 20 | `3b20013` | `4c30014` | S3 | heading | S3 · H2 | Notre mission et nos objectifs | مهمتنا وأهدافنا | Traduit — proposition non validée |
| 21 | `3b20023` | `4c30015` | S3 | container | S3 · Grille des 5 objectifs | — | — | Sans texte visible |
| 22 | `3b20016` | `4c30016` | S3 | container | S3 · Objectif 1 — Encourager l&#x27;engagement et la part | — | — | Sans texte visible |
| 23 | `3b20014` | `4c30017` | S3 | heading | S3 · H3 objectif 1 | Encourager l&#x27;engagement et la participation citoyenne | تشجيع الانخراط والمشاركة المواطنة | Traduit — proposition non validée |
| 24 | `3b20015` | `4c30018` | S3 | text-editor | S3 · Texte objectif 1 | &lt;p&gt;L&#x27;association entend favoriser l&#x27;implication des jeunes dans la vie civique, encourager leurs initiatives et contribuer à la valorisation de leurs compétences, de leurs talents et de leur capacité à agir dans leur environnement.&lt;/p&gt; | &lt;p&gt;تسعى الجمعية إلى تعزيز انخراط الشباب في الحياة المدنية، وتشجيع مبادراتهم، والإسهام في تثمين كفاءاتهم ومواهبهم وقدرتهم على الفعل في محيطهم.&lt;/p&gt; | Traduit — proposition non validée |
| 25 | `3b20019` | `4c30019` | S3 | container | S3 · Objectif 2 — Promouvoir l&#x27;éducation et la forma | — | — | Sans texte visible |
| 26 | `3b20017` | `4c3001a` | S3 | heading | S3 · H3 objectif 2 | Promouvoir l&#x27;éducation et la formation | النهوض بالتعليم والتكوين | Traduit — proposition non validée |
| 27 | `3b20018` | `4c3001b` | S3 | text-editor | S3 · Texte objectif 2 | &lt;p&gt;Les orientations statutaires accordent une place importante à l&#x27;éducation non formelle, à la lutte contre l&#x27;illettrisme, à la formation professionnelle et à l&#x27;accompagnement éducatif des enfants et des jeunes.&lt;/p&gt; | &lt;p&gt;تولي التوجهات المنصوص عليها في القانون الأساسي مكانة مهمة للتربية غير النظامية، ومحاربة الأمية، والتكوين المهني، والمواكبة التربوية للأطفال والشباب.&lt;/p&gt; | Traduit — proposition non validée |
| 28 | `3b2001c` | `4c3001c` | S3 | container | S3 · Objectif 3 — Renforcer la solidarité et l&#x27;inclu | — | — | Sans texte visible |
| 29 | `3b2001a` | `4c3001d` | S3 | heading | S3 · H3 objectif 3 | Renforcer la solidarité et l&#x27;inclusion sociale | تعزيز التضامن والإدماج الاجتماعي | Traduit — proposition non validée |
| 30 | `3b2001b` | `4c3001e` | S3 | text-editor | S3 · Texte objectif 3 | &lt;p&gt;L&#x27;association inscrit la solidarité et le bénévolat parmi les leviers de son action. Ses statuts prévoient également une attention aux personnes en situation de vulnérabilité et aux catégories nécessitant un accompagnement adapté, dans la limite des ressources et des conditions disponibles.&lt;/p&gt; | &lt;p&gt;تُدرج الجمعية التضامن والعمل التطوعي ضمن روافع عملها. كما ينص قانونها الأساسي على إيلاء العناية للأشخاص في وضعية هشاشة وللفئات التي تحتاج إلى مواكبة ملائمة، وذلك في حدود الموارد والظروف المتاحة.&lt;/p&gt; | Traduit — proposition non validée |
| 31 | `3b2001f` | `4c3001f` | S3 | container | S3 · Objectif 4 — Valoriser la culture, les arts et  | — | — | Sans texte visible |
| 32 | `3b2001d` | `4c30020` | S3 | heading | S3 · H3 objectif 4 | Valoriser la culture, les arts et le sport | تثمين الثقافة والفنون والرياضة | Traduit — proposition non validée |
| 33 | `3b2001e` | `4c30021` | S3 | text-editor | S3 · Texte objectif 4 | &lt;p&gt;La promotion des activités culturelles, artistiques, cinématographiques et sportives fait partie des domaines d&#x27;intervention prévus par les statuts. Ces activités sont envisagées comme des espaces d&#x27;expression, d&#x27;apprentissage, de rencontre et de participation.&lt;/p&gt; | &lt;p&gt;يندرج النهوض بالأنشطة الثقافية والفنية والسينمائية والرياضية ضمن مجالات التدخل المنصوص عليها في القانون الأساسي. ويُنظر إلى هذه الأنشطة باعتبارها فضاءات للتعبير والتعلم واللقاء والمشاركة.&lt;/p&gt; | Traduit — proposition non validée |
| 34 | `3b20022` | `4c30022` | S3 | container | S3 · Objectif 5 — Sensibiliser à l&#x27;environnement et  | — | — | Sans texte visible |
| 35 | `3b20020` | `4c30023` | S3 | heading | S3 · H3 objectif 5 | Sensibiliser à l&#x27;environnement et au développement durable | التحسيس بقضايا البيئة والتنمية المستدامة | Traduit — proposition non validée |
| 36 | `3b20021` | `4c30024` | S3 | text-editor | S3 · Texte objectif 5 | &lt;p&gt;L&#x27;association inscrit également dans ses objectifs la sensibilisation aux enjeux environnementaux et aux exigences du développement durable, à travers des initiatives et des actions adaptées.&lt;/p&gt; | &lt;p&gt;كما تُدرج الجمعية ضمن أهدافها التحسيس بالقضايا البيئية وبمتطلبات التنمية المستدامة، من خلال مبادرات وأنشطة ملائمة.&lt;/p&gt; | Traduit — proposition non validée |
| 37 | `3b2003b` | `4c30025` | S4 | container | S4 — Valeurs | — | — | Sans texte visible |
| 38 | `3b20027` | `4c30026` | S4 | container | S4 · En-tête | — | — | Sans texte visible |
| 39 | `3b20025` | `4c30027` | S4 | heading | S4 · H2 | Les valeurs qui guident notre engagement | القيم التي توجّه التزامنا | Traduit — proposition non validée |
| 40 | `3b20026` | `4c30028` | S4 | text-editor | S4 · Introduction | &lt;p&gt;L&#x27;action associative d&#x27;Amal Chabab Takaddoum s&#x27;appuie sur des principes qui orientent ses objectifs et son fonctionnement :&lt;/p&gt; | &lt;p&gt;يستند العمل الجمعوي لجمعية أمل شباب التقدم إلى مبادئ توجّه أهدافها وطريقة اشتغالها:&lt;/p&gt; | Traduit — proposition non validée |
| 41 | `3b2003a` | `4c30029` | S4 | container | S4 · Grille des 6 valeurs | — | — | Sans texte visible |
| 42 | `3b2002a` | `4c3002a` | S4 | container | S4 · Valeur 1 — Citoyenneté | — | — | Sans texte visible |
| 43 | `3b20028` | `4c3002b` | S4 | heading | S4 · H3 valeur 1 | Citoyenneté | المواطنة | Traduit — proposition non validée |
| 44 | `3b20029` | `4c3002c` | S4 | text-editor | S4 · Texte valeur 1 | &lt;p&gt;encourager la participation responsable à la vie collective.&lt;/p&gt; | &lt;p&gt;تشجيع المشاركة المسؤولة في الحياة الجماعية.&lt;/p&gt; | Traduit — proposition non validée |
| 45 | `3b2002d` | `4c3002d` | S4 | container | S4 · Valeur 2 — Égalité et justice sociale | — | — | Sans texte visible |
| 46 | `3b2002b` | `4c3002e` | S4 | heading | S4 · H3 valeur 2 | Égalité et justice sociale | المساواة والعدالة الاجتماعية | Traduit — proposition non validée |
| 47 | `3b2002c` | `4c3002f` | S4 | text-editor | S4 · Texte valeur 2 | &lt;p&gt;promouvoir des relations fondées sur le respect des droits et de la dignité.&lt;/p&gt; | &lt;p&gt;النهوض بعلاقات قائمة على احترام الحقوق والكرامة.&lt;/p&gt; | Traduit — proposition non validée |
| 48 | `3b20030` | `4c30030` | S4 | container | S4 · Valeur 3 — Solidarité | — | — | Sans texte visible |
| 49 | `3b2002e` | `4c30031` | S4 | heading | S4 · H3 valeur 3 | Solidarité | التضامن | Traduit — proposition non validée |
| 50 | `3b2002f` | `4c30032` | S4 | text-editor | S4 · Texte valeur 3 | &lt;p&gt;développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;تنمية التآزر والعمل التطوعي والتعاون.&lt;/p&gt; | Traduit — proposition non validée |
| 51 | `3b20033` | `4c30033` | S4 | container | S4 · Valeur 4 — Tolérance | — | — | Sans texte visible |
| 52 | `3b20031` | `4c30034` | S4 | heading | S4 · H3 valeur 4 | Tolérance | التسامح | Traduit — proposition non validée |
| 53 | `3b20032` | `4c30035` | S4 | text-editor | S4 · Texte valeur 4 | &lt;p&gt;favoriser le dialogue, la compréhension et le respect mutuel.&lt;/p&gt; | &lt;p&gt;تعزيز الحوار والتفاهم والاحترام المتبادل.&lt;/p&gt; | Traduit — proposition non validée |
| 54 | `3b20036` | `4c30036` | S4 | container | S4 · Valeur 5 — Responsabilité | — | — | Sans texte visible |
| 55 | `3b20034` | `4c30037` | S4 | heading | S4 · H3 valeur 5 | Responsabilité | المسؤولية | Traduit — proposition non validée |
| 56 | `3b20035` | `4c30038` | S4 | text-editor | S4 · Texte valeur 5 | &lt;p&gt;inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;إدراج الالتزام ضمن مقاربة جادة وبنّاءة.&lt;/p&gt; | Traduit — proposition non validée |
| 57 | `3b20039` | `4c30039` | S4 | container | S4 · Valeur 6 — Initiative | — | — | Sans texte visible |
| 58 | `3b20037` | `4c3003a` | S4 | heading | S4 · H3 valeur 6 | Initiative | المبادرة | Traduit — proposition non validée |
| 59 | `3b20038` | `4c3003b` | S4 | text-editor | S4 · Texte valeur 6 | &lt;p&gt;valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;تثمين المواهب والأفكار والقدرات على الفعل.&lt;/p&gt; | Traduit — proposition non validée |
| 60 | `3b20049` | `4c3003c` | S5 | container | S5 — Organisation (ancre #organisation) | — | — | Ancre `#organisation` conservée |
| 61 | `3b2003e` | `4c3003d` | S5 | container | S5 · En-tête | — | — | Sans texte visible |
| 62 | `3b2003c` | `4c3003e` | S5 | heading | S5 · H2 | Une organisation structurée | تنظيم مُهيكل | Traduit — proposition non validée |
| 63 | `3b2003d` | `4c3003f` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Les statuts de l&#x27;association prévoient plusieurs instances qui contribuent à son organisation et à son fonctionnement.&lt;/p&gt; | &lt;p&gt;ينص القانون الأساسي للجمعية على عدة هيئات تساهم في تنظيمها وسير عملها.&lt;/p&gt; | Traduit — proposition non validée |
| 64 | `3b20048` | `4c30040` | S5 | container | S5 · Grille des 3 instances | — | — | Sans texte visible |
| 65 | `3b20041` | `4c30041` | S5 | container | S5 · Instance 1 — L&#x27;Assemblée générale | — | — | Sans texte visible |
| 66 | `3b2003f` | `4c30042` | S5 | heading | S5 · H3 instance 1 | L&#x27;Assemblée générale | الجمع العام | Traduit — proposition non validée |
| 67 | `3b20040` | `4c30043` | S5 | text-editor | S5 · Texte instance 1 | &lt;p&gt;Elle constitue l&#x27;instance associative réunissant les catégories de membres prévues par les statuts. Elle intervient dans la définition des orientations générales et l&#x27;examen des rapports de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يشكل الهيئة الجمعوية التي تضم فئات الأعضاء المنصوص عليها في القانون الأساسي. ويساهم في تحديد التوجهات العامة ودراسة تقارير الجمعية.&lt;/p&gt; | Traduit — proposition non validée |
| 68 | `3b20044` | `4c30044` | S5 | container | S5 · Instance 2 — Le Bureau exécutif | — | — | Sans texte visible |
| 69 | `3b20042` | `4c30045` | S5 | heading | S5 · H3 instance 2 | Le Bureau exécutif | المكتب التنفيذي | Traduit — proposition non validée |
| 70 | `3b20043` | `4c30046` | S5 | text-editor | S5 · Texte instance 2 | &lt;p&gt;Les statuts prévoient un Bureau exécutif composé de cinq membres élus par l&#x27;Assemblée générale. Il assure notamment la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;ينص القانون الأساسي على مكتب تنفيذي يتكون من خمسة أعضاء ينتخبهم الجمع العام. ويتولى على الخصوص الإشراف على تنظيم اللجان وأقطاب العمل، وتتبع تنفيذ البرامج المسطرة.&lt;/p&gt; | Traduit — proposition non validée |
| 71 | `3b20047` | `4c30047` | S5 | container | S5 · Instance 3 — Les commissions | — | — | Sans texte visible |
| 72 | `3b20045` | `4c30048` | S5 | heading | S5 · H3 instance 3 | Les commissions | اللجان | Traduit — proposition non validée |
| 73 | `3b20046` | `4c30049` | S5 | text-editor | S5 · Texte instance 3 | &lt;p&gt;Les commissions sont constituées selon les besoins de l&#x27;association. Elles contribuent à l&#x27;étude des programmes et au suivi des activités relevant de leurs domaines de travail.&lt;/p&gt; | &lt;p&gt;تُحدث اللجان حسب حاجيات الجمعية. وتساهم في دراسة البرامج وتتبع الأنشطة المندرجة ضمن مجالات عملها.&lt;/p&gt; | Traduit — proposition non validée |
| 74 | `3b20059` | `4c3004a` | S6 | container | S6 — Trois pôles | — | — | Sans texte visible |
| 75 | `3b2004c` | `4c3004b` | S6 | container | S6 · En-tête | — | — | Sans texte visible |
| 76 | `3b2004a` | `4c3004c` | S6 | heading | S6 · H2 | Trois pôles au service du projet associatif | ثلاثة أقطاب في خدمة المشروع الجمعوي | Traduit — proposition non validée |
| 77 | `3b2004b` | `4c3004d` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires :&lt;/p&gt; | &lt;p&gt;يرتكز تنظيم الجمعية على ثلاثة أقطاب متكاملة منصوص عليها في القانون الأساسي:&lt;/p&gt; | Traduit — proposition non validée |
| 78 | `3b20056` | `4c3004e` | S6 | container | S6 · Grille des 3 pôles | — | — | Sans texte visible |
| 79 | `3b2004f` | `4c3004f` | S6 | container | S6 · Carte 1 — Pôle Administration et Gestion → P-03 | — | — | Sans texte visible |
| 80 | `3b2004d` | `4c30050` | S6 | heading | S6 · H3 carte 1 (lien P-03) | Pôle Administration et Gestion | قطب الإدارة والتسيير | Traduit — proposition non validée |
| 81 | `3b2004e` | `4c30051` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt; | &lt;p&gt;يساهم في تنظيم الهيكل الجمعوي وسير عمله.&lt;/p&gt; | Traduit — proposition non validée |
| 82 | `3b20052` | `4c30052` | S6 | container | S6 · Carte 2 — Pôle Formation et Intégration → P-04 | — | — | Sans texte visible |
| 83 | `3b20050` | `4c30053` | S6 | heading | S6 · H3 carte 2 (lien P-04) | Pôle Formation et Intégration | قطب التكوين والإدماج | Traduit — proposition non validée |
| 84 | `3b20051` | `4c30054` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt; | &lt;p&gt;يندرج ضمن التوجهات المتعلقة بالتعلم وتنمية الكفاءات والإدماج.&lt;/p&gt; | Traduit — proposition non validée |
| 85 | `3b20055` | `4c30055` | S6 | container | S6 · Carte 3 — Pôle Animation Culturelle et Sociale → P-05 | — | — | Sans texte visible |
| 86 | `3b20053` | `4c30056` | S6 | heading | S6 · H3 carte 3 (lien P-05) | Pôle Animation Culturelle et Sociale | قطب التنشيط الثقافي والاجتماعي | Traduit — proposition non validée |
| 87 | `3b20054` | `4c30057` | S6 | text-editor | S6 · Texte carte 3 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;يُعنى بالتوجهات المتعلقة بالثقافة والتنشيط والمشاركة الاجتماعية.&lt;/p&gt; | Traduit — proposition non validée |
| 88 | `3b20058` | `4c30058` | S6 | container | S6 · Bouton général | — | — | Sans texte visible |
| 89 | `3b20057` | `4c30059` | S6 | button | S6 · Bouton → page Nos pôles | Découvrir nos trois pôles | اكتشف أقطابنا الثلاثة | Traduit — proposition non validée |
| 90 | `3b2005e` | `4c3005a` | S7 | container | S7 — Appel à l’action | — | — | Sans texte visible |
| 91 | `3b2005a` | `4c3005b` | S7 | heading | S7 · H2 | Vous souhaitez mieux connaître notre association ? | هل ترغبون في التعرف أكثر على جمعيتنا؟ | Traduit — proposition non validée |
| 92 | `3b2005b` | `4c3005c` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez découvrir les missions de l&#x27;Association Amal Chabab Takaddoum, échanger avec ses représentants ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour mieux connaître vos attentes et identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;هل ترغبون في التعرف على مهام جمعية أمل شباب التقدم، أو التواصل مع ممثليها، أو بحث إمكانيات التعاون؟&lt;/p&gt;<br>&lt;p&gt;لنتواصل من أجل التعرف بشكل أفضل على انتظاراتكم وتحديد إمكانيات التبادل.&lt;/p&gt; | Traduit — proposition non validée |
| 93 | `3b2005d` | `4c3005d` | S7 | container | S7 · Bouton | — | — | Sans texte visible |
| 94 | `3b2005c` | `4c3005e` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | تواصلوا معنا | Traduit — proposition non validée |
