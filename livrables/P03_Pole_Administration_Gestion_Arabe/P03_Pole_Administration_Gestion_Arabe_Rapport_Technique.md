# P-03 Pôle Administration et Gestion — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**
Livrable associé : `P03_Pole_Administration_Gestion_Arabe_Elementor.json`
Source : `P03_Pole_Administration_Gestion_Elementor.json` (SHA-256 `9f135af7…a9f29e8d`, **non modifiée** : empreinte identique avant et après génération).
Références : P-01 arabe (terminologie validée), P-02 arabe (méthode et terminologie retenue).

> ⚠️ **Entrée manquante** : `P03_Pole_Administration_Gestion_Documentation_Technique.md` **n’a pas été transmis**. La classification « 5 imposés / 17 validés / 24 propositions » qu’il définit n’a donc **pas pu être reproduite telle quelle**. Une classification équivalente a été établie élément par élément à partir des textes réellement repris de P-01 / P-02 (section 6). Le décompte diffère (38 textes visibles dans le JSON, contre 46 blocs annoncés) : **à rapprocher par le superviseur** avec la documentation.

---

## 0. Contrôles — statiques exécutés vs tests réels

| Contrôle | Méthode | Statut |
|---|---|---|
| Validité syntaxique JSON | `json.load` Python | ✅ Exécuté |
| 7 sections, même ordre | Comparaison arborescente source ↔ arabe | ✅ Exécuté |
| 68 éléments, hiérarchie, types, `isInner`, nombre d’enfants | Comparaison récursive nœud à nœud | ✅ Exécuté (29 conteneurs, 16 headings, 17 text-editors, 5 boutons, 1 image) |
| Réglages inchangés hors texte et alignement RTL | Diff clé par clé de tous les `settings` | ✅ Exécuté (modifiés : `title` ×16, `editor` ×17, `text` ×5 ; `align` ajouté ×21) |
| IDs identiques à la source et uniques | Comparaison ordonnée + comptage | ✅ Exécuté (68/68 identiques, 68/68 uniques) |
| Aucun texte français visible restant | Recherche de caractères latins dans `title`, `editor`, `text` | ✅ Exécuté (0) |
| Ancres `#missions` et `#contribution` | Boutons S1 ↔ `_element_id` S3/S4 | ✅ Exécuté (2/2) |
| Liens internes conservés | Lecture des URL | ✅ Exécuté (3 liens, cibles FR inchangées) |
| Image de substitution | URL et `alt` | ✅ Exécuté (URL inchangée, `alt` vide comme la source) |
| Paramètres de page | `page_settings` | ✅ Exécuté |
| Widgets gratuits uniquement | Liste des `widgetType` | ✅ Exécuté |
| **Import Elementor** | — | ⛔ **Non testé** |
| **Affichage RTL réel (bureau / tablette / mobile)** | — | ⛔ **Non testé** |
| **Défilement vers les ancres** | — | ⛔ **Non testé** |
| **Liens Polylang vers les pages arabes** | — | ⛔ **Non configurés / non testés** |
| **Validation éditoriale des propositions** | — | ⛔ **En attente du superviseur** |

## 1. Structure des sept sections

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | Ligne 2 colonnes (58 % / 38 %) : H1 + sous-titre + texte + 2 boutons d’ancre ‖ image de substitution |
| S2 | S2 — Présentation | `#FFFFFF` | H2 + texte 3 paragraphes, centrés (largeur 820 px) |
| S3 | S3 — Trois domaines d’intervention (ancre `#missions`) | `#F4F6F6` | En-tête centré + grille de 3 cartes (33 % → 48 % → 100 %) |
| S4 | S4 — Contribution transversale (ancre `#contribution`) | `#FFFFFF` | H2 + texte 3 paragraphes, centrés |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | En-tête centré + grille de 4 cartes (48 % → 48 % → 100 %) |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | En-tête centré + 2 cartes pôles avec bouton |
| S7 | S7 — Appel à l’action | `#152A33` | H2 + texte + bouton Contact, centrés |

## 2. Éléments

| Type | Source | Arabe |
|---|---|---|
| `container` | 29 | 29 |
| `heading` | 16 | 16 |
| `text-editor` | 17 | 17 |
| `button` | 5 | 5 |
| `image` | 1 | 1 |
| **Total** | **68** | **68** |

## 3. Identifiants — règle appliquée

**Règle : les 68 IDs source sont conservés à l’identique. Aucun ID n’a été régénéré.**

Raisons :
1. Les ID Elementor n’ont besoin d’être uniques qu’**à l’intérieur d’une page** ; les styles générés sont préfixés par l’identifiant de la page WordPress (`.elementor-<post_id> .elementor-element-<id>`). Deux pages distinctes peuvent partager des ID sans conflit. Aucune contrainte technique n’impose donc une régénération.
2. La conservation garantit une correspondance FR ↔ AR **1 pour 1, sans table de conversion** (ID source = ID arabe dans le tableau de la section 9), et lève l’ambiguïté signalée pour P-02.

Contrôles :
- Unicité dans le fichier : **68/68**.
- Partage avec P-03 français : **68/68** (voulu).
- Partage avec P-01 arabe : **0**.
- Partage avec P-02 arabe : **68/68** ⚠️ — **constat** : le JSON P-03 français utilise la même plage `4c3…` que celle générée pour P-02 arabe (`4c30001`–`4c3005e`). Pour la raison 1, ce partage **n’a pas d’effet** sur des pages distinctes. Il n’aurait d’impact que si des éléments des deux pages étaient copiés dans **une même page**, ou sur un outil externe qui exigerait des ID uniques sur tout le site. Si le superviseur souhaite une séparation stricte, régénérer la plage dans un fichier dédié (règle et table de correspondance à documenter) — **non fait ici** pour respecter la règle « ne jamais régénérer silencieusement ».

Ce modèle ne comporte aucun identifiant interne de répéteur (`_id`).

## 4. Paramètres de page

| Clé | Source | Arabe |
|---|---|---|
| `version` / `type` | `0.4` / `page` | `0.4` / `page` |
| `page_settings.template` | `elementor_header_footer` | identique ✅ |
| `page_settings.hide_title` | `yes` | identique ✅ |
| `title` (nom du modèle en bibliothèque) | `P-03 Pôle Administration et Gestion — Amal Chabab Takaddoum` | `P-03 Pôle Administration et Gestion (AR) — Amal Chabab Takaddoum` |

## 5. RTL et responsive

### 5.1 `align: "right"` ajouté sur 21 widgets

Uniquement sur les titres et paragraphes **sans alignement** dans la source. Les **12 éléments centrés** restent centrés (H2 + textes de S2, S3, S4, S5, S6, S7). Aucune marge, largeur, police ou propriété inconnue n’a été ajoutée.

| ID | Widget | Libellé |
|---|---|---|
| `4c30001` | heading | S1 · H1 |
| `4c30002` | text-editor | S1 · Sous-titre |
| `4c30003` | text-editor | S1 · Texte |
| `4c30012` | heading | S3 · H3 domaine 1 |
| `4c30013` | text-editor | S3 · Texte domaine 1 |
| `4c30015` | heading | S3 · H3 domaine 2 |
| `4c30016` | text-editor | S3 · Texte domaine 2 |
| `4c30018` | heading | S3 · H3 domaine 3 |
| `4c30019` | text-editor | S3 · Texte domaine 3 |
| `4c30023` | heading | S5 · H3 principe 1 |
| `4c30024` | text-editor | S5 · Texte principe 1 |
| `4c30026` | heading | S5 · H3 principe 2 |
| `4c30027` | text-editor | S5 · Texte principe 2 |
| `4c30029` | heading | S5 · H3 principe 3 |
| `4c3002a` | text-editor | S5 · Texte principe 3 |
| `4c3002c` | heading | S5 · H3 principe 4 |
| `4c3002d` | text-editor | S5 · Texte principe 4 |
| `4c30034` | heading | S6 · H3 carte 1 |
| `4c30035` | text-editor | S6 · Texte carte 1 |
| `4c30039` | heading | S6 · H3 carte 2 |
| `4c3003a` | text-editor | S6 · Texte carte 2 |

### 5.2 Comportements attendus en document RTL (non testés)

Si la page est assignée à l’Arabe (sens RTL) dans Polylang : colonne texte à droite et image à gauche en S1 ; cartes de S3, S5, S6 remplies de droite à gauche ; boutons de S1 alignés à droite. Sur mobile, l’ordre du contenu reste celui de la source.

### 5.3 Responsive

**Toutes les valeurs sont conservées** : typographies bureau/tablette/mobile (H1 44/38/30 ; H2 34/30/26 ; H3 20/20/19 et 18/18/17 ; textes 20/19/17, 18/17/16, 17/17/16, 16/16/15), largeurs (58/38 ; 33/48/100 ; 48/48/100 ; 820, 760 px → 100 % mobile), paddings, `flex_gap`, `flex_wrap`, `flex_direction_mobile`.

## 6. Classification rédactionnelle (38 textes visibles)

| Statut | Nombre | Définition |
|---|---|---|
| Imposé | 1 | Terminologie imposée par le brief §4 (H1 قطب الإدارة والتسيير). |
| Validé — identique P-01 | 5 | Repris mot pour mot de P-01 arabe validé (noms des 2 autres pôles, « اكتشف هذا القطب » ×2, « تواصلوا معنا »). |
| Validé — adapté de P-01 | 4 | Extraits du texte validé de la carte 1 de P-01 S3, avec la ponctuation adaptée. |
| Repris de P-02 arabe | 9 | Identiques à P-02 arabe (valeurs Responsabilité / Solidarité / Initiative, descriptions des deux autres pôles, introduction S6). ⚠️ P-02 a été livré comme « proposition non validée » ; le brief les présente comme validés : **à confirmer**. |
| Mixte | 1 | `4c30003` : §1 adapté de P-01, §2 proposition. |
| **Proposition non validée** | **18** (+ 1 paragraphe mixte) | Rédaction nouvelle, à valider. |

Dans les propositions, les **termes imposés** du brief sont utilisés systématiquement : قطب، الإدارة والتسيير، المكتب التنفيذي، الجمع العام، اللجان، التوجهات المنصوص عليها في القانون الأساسي.

## 7. Ancres et liens

| Élément | Libellé arabe | Destination | Contrôle |
|---|---|---|---|
| `4c30004` bouton S1 | مجالات تدخله | `#missions` → S3 `4c3001c` | ✅ Ancre présente |
| `4c30005` bouton S1 | إسهامه | `#contribution` → S4 `4c3001f` | ✅ Ancre présente |
| `4c30036` bouton S6 | اكتشف هذا القطب | `/nos-poles/formation-et-integration/` | ⚠️ Cible FR conservée — page AR P-04 à associer |
| `4c3003b` bouton S6 | اكتشف هذا القطب | `/nos-poles/animation-culturelle-et-sociale/` | ⚠️ Cible FR conservée — page AR P-05 à associer |
| `4c30042` bouton S7 | تواصلوا معنا | `/contact/` | ⚠️ Cible FR conservée — page AR Contact à associer |

Aucune URL arabe, aucun slug ni aucun préfixe de langue n’a été inventé. Tant qu’elles ne sont pas remplacées, les trois cibles mènent aux pages **françaises**.

## 8. Points à décider par le superviseur (Livrable 4)

| # | ID | Point | Choix proposé | Alternative |
|---|---|---|---|---|
| 1 | — | Documentation technique P-03 absente ; décompte 5/17/24 = 46 non rapprochable des 38 textes du JSON. | Classification de la section 6. | Fournir la documentation pour rapprochement. |
| 2 | 9 textes | Statut des reprises P-02 (livré comme proposition non validée). | Marqués « repris de P-02 ». | Confirmer qu’ils sont validés. |
| 3 | `4c30004` | « Ses domaines d’intervention » : possessif renvoyant au pôle. | مجالات تدخله | مجالات تدخل القطب (plus explicite) |
| 4 | `4c30005` | « Sa contribution ». | إسهامه | مساهمته — le terme إسهام est utilisé de façon cohérente en S4. |
| 5 | `4c3001d` | « transversale ». | أفقي | عرضاني / مشترك بين الأقطاب |
| 6 | `4c3002c` | « Fonctionnement collégial ». | التسيير الجماعي | العمل التشاركي / الاشتغال الجماعي — « collégial » n’a pas d’équivalent institutionnel unique. |
| 7 | `4c30019` | « locaux ». | المقرات | الفضاءات |
| 8 | `4c30019` | « ressources » : pourrait être lu comme financier alors que la source exclut le financier. | الموارد (sens matériel, précisé par la phrase suivante) | الموارد المادية — plus explicite, mais ajoute une précision absente de la source. |
| 9 | `4c30019` | Exclusion comptable et financière. | Traduite fidèlement (المهام المحاسبية والمالية التي تخضع لإطار خاص بها) ; seule mention de ces termes dans la page. | — |
| 10 | `4c30013` | « concourt à l’articulation entre… ». | الربط بين | التنسيق بين — non retenu pour éviter de répéter تنسيق, déjà employé dans la phrase. |
| 11 | `4c30016` | « tenue et conservation des documents ». | مسك الوثائق الجمعوية وحفظها | — |
| 12 | `4c3002d` | Phrase elliptique (« leur supervision du Bureau exécutif »). | Explicitée : ويتولى المكتب التنفيذي الإشراف عليها | — |
| 13 | `4c3000d` | « élu par l’Assemblée générale ». | المنتخب من طرف الجمع العام | الذي ينتخبه الجمع العام (forme employée en P-02) |
| 14 | S5 | Textes des principes en majuscule en P-03 FR, en minuscule en P-02 FR ; texte identique. | Arabe identique à P-02. | — |

## 9. Limites non testées (Livrable 5)

- **Import Elementor** : non réalisé ; compatibilité vérifiée uniquement par analyse statique (format 0.4, widgets gratuits, aucune clé nouvelle sauf `align`).
- **Affichage RTL réel** : non testé ; dépend du sens RTL de la langue Arabe dans Polylang et de l’interprétation de `align: right` par la version d’Elementor installée (« Droite » ou « Fin »).
- **Mobile** : non testé ; longueurs des textes arabes à contrôler dans les cartes S3/S5 et les boutons S1.
- **Ancres** : présentes dans la structure ; défilement non testé.
- **Liens Polylang** : 3 cibles françaises provisoires (section 7) ; associations à faire manuellement.
- **Police** : aucune imposée ; vérifier que la police globale couvre l’arabe.
- **Image** : à remplacer ; texte alternatif arabe à fournir (rien inventé).

Aucune modification de WordPress, Polylang, Astra, Elementor ou des réglages globaux. Rien n’est importé ni publié.

## 10. Métadonnées SEO proposées (non injectées — propositions non validées)

| Champ | Proposition |
|---|---|
| Titre SEO | قطب الإدارة والتسيير \| جمعية أمل شباب التقدم |
| Méta-description | قطب الإدارة والتسيير بجمعية أمل شباب التقدم: تنظيم الحياة الجمعوية وتنسيقها، والتتبع الإداري، وتدبير الوسائل الضرورية لسير عمل الجمعية. |
| Slug (**non validé**) | `قطب-الإدارة-والتسيير` (alternative latine : `administration-et-gestion-ar`) |

## 11. Tableau de correspondance exhaustif (68 éléments)

IDs arabes = IDs source (section 3). 38 textes visibles couverts, **0 oublié**. HTML échappé.

| # | ID source | ID arabe | Section | Type | `_title` (FR conservé) | Texte français | Texte arabe | Statut rédactionnel | Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `4c3000b` | `4c3000b` | S1 | container | S1 — Bannière | — | — | Sans texte visible |  |
| 2 | `4c3000a` | `4c3000a` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible |  |
| 3 | `4c30007` | `4c30007` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible |  |
| 4 | `4c30001` | `4c30001` | S1 | heading | S1 · H1 | Pôle Administration et Gestion | قطب الإدارة والتسيير | Imposé (brief §4) | Dénomination imposée (brief §4 : قطب + الإدارة والتسيير) — identique P-01 |
| 5 | `4c30002` | `4c30002` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un pôle dédié à l&#x27;organisation et à la coordination de la vie associative.&lt;/p&gt; | &lt;p&gt;قطب يُعنى بتنظيم الحياة الجمعوية وتنسيقها.&lt;/p&gt; | Validé — adapté de P-01 | 1ʳᵉ proposition de la carte 1 P-01 S3 (validée), ponctuation finale adaptée |
| 6 | `4c30003` | `4c30003` | S1 | text-editor | S1 · Texte | &lt;p&gt;Il contribue au suivi administratif et à la gestion des moyens nécessaires au fonctionnement de l&#x27;association.&lt;/p&gt;<br>&lt;p&gt;Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يساهم في التتبع الإداري وتدبير الوسائل الضرورية لسير عمل الجمعية.&lt;/p&gt;<br>&lt;p&gt;وتندرج مجالات تدخله ضمن التوجهات المنصوص عليها في القانون الأساسي للجمعية.&lt;/p&gt; | Mixte : §1 adapté P-01 / §2 **proposition non validée** | §1 adapté de P-01 S3 carte 1 (validé) ; §2 proposition (terme imposé : التوجهات المنصوص عليها في القانون الأساسي) |
| 7 | `4c30006` | `4c30006` | S1 | container | S1 · Boutons | — | — | Sans texte visible |  |
| 8 | `4c30004` | `4c30004` | S1 | button | S1 · Bouton 1 → ancre #missions | Ses domaines d&#x27;intervention | مجالات تدخله | **Proposition non validée** |  |
| 9 | `4c30005` | `4c30005` | S1 | button | S1 · Bouton 2 → ancre #contribution | Sa contribution | إسهامه | **Proposition non validée** |  |
| 10 | `4c30009` | `4c30009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |  |
| 11 | `4c30008` | `4c30008` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée |  |
| 12 | `4c3000e` | `4c3000e` | S2 | container | S2 — Présentation | — | — | Sans texte visible |  |
| 13 | `4c3000c` | `4c3000c` | S2 | heading | S2 · H2 | Un pôle au service de l&#x27;organisation associative | قطب في خدمة التنظيم الجمعوي | **Proposition non validée** |  |
| 14 | `4c3000d` | `4c3000d` | S2 | text-editor | S2 · Texte (3 paragraphes) | &lt;p&gt;Le Pôle Administration et Gestion est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt;<br>&lt;p&gt;Son rôle se situe en appui des activités portées par l&#x27;association : il contribue à l&#x27;organisation de la vie associative, au suivi administratif et à la disponibilité des moyens nécessaires à la conduite des activités.&lt;/p&gt;<br>&lt;p&gt;Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale.&lt;/p&gt; | &lt;p&gt;يُعدّ قطب الإدارة والتسيير أحد الأقطاب الثلاثة المنصوص عليها في القانون الأساسي لجمعية أمل شباب التقدم. ويساهم في تنظيم الهيكل الجمعوي وسير عمله.&lt;/p&gt;<br>&lt;p&gt;ويتمثل دوره في دعم الأنشطة التي تضطلع بها الجمعية، إذ يساهم في تنظيم الحياة الجمعوية، والتتبع الإداري، وتوفير الوسائل الضرورية لتنفيذ الأنشطة.&lt;/p&gt;<br>&lt;p&gt;ووفقًا للقانون الأساسي، يندرج تنظيم أقطاب العمل وتتبع تنفيذ البرامج ضمن إشراف المكتب التنفيذي المنتخب من طرف الجمع العام.&lt;/p&gt; | **Proposition non validée** | 2ᵉ phrase du §1 reprise de P-02 (3b2004e) ; termes imposés المكتب التنفيذي / الجمع العام |
| 15 | `4c3001c` | `4c3001c` | S3 | container | S3 — Trois domaines d&#x27;intervention (ancre #missions) | — | — | Ancre `#missions` conservée |  |
| 16 | `4c30011` | `4c30011` | S3 | container | S3 · En-tête | — | — | Sans texte visible |  |
| 17 | `4c3000f` | `4c3000f` | S3 | heading | S3 · H2 | Trois domaines d&#x27;intervention | ثلاثة مجالات للتدخل | **Proposition non validée** |  |
| 18 | `4c30010` | `4c30010` | S3 | text-editor | S3 · Introduction | &lt;p&gt;Les activités du pôle s&#x27;organisent autour de trois domaines complémentaires.&lt;/p&gt; | &lt;p&gt;تنتظم أنشطة القطب حول ثلاثة مجالات متكاملة.&lt;/p&gt; | **Proposition non validée** |  |
| 19 | `4c3001b` | `4c3001b` | S3 | container | S3 · Grille des 3 domaines | — | — | Sans texte visible |  |
| 20 | `4c30014` | `4c30014` | S3 | container | S3 · Domaine 1 — Organisation de la vie associative | — | — | Sans texte visible |  |
| 21 | `4c30012` | `4c30012` | S3 | heading | S3 · H3 domaine 1 | Organisation de la vie associative | تنظيم الحياة الجمعوية | Validé — adapté de P-01 | Expression de P-01 S3 carte 1 (validée) |
| 22 | `4c30013` | `4c30013` | S3 | text-editor | S3 · Texte domaine 1 | &lt;p&gt;Le pôle contribue à l&#x27;organisation et à la coordination de la vie associative. Il concourt à l&#x27;articulation entre les instances, les commissions et les pôles de travail prévus par les statuts, ainsi qu&#x27;à la continuité du fonctionnement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يساهم القطب في تنظيم الحياة الجمعوية وتنسيقها. كما يساهم في الربط بين الهيئات واللجان وأقطاب العمل المنصوص عليها في القانون الأساسي، وفي ضمان استمرارية سير عمل الجمعية.&lt;/p&gt; | **Proposition non validée** |  |
| 23 | `4c30017` | `4c30017` | S3 | container | S3 · Domaine 2 — Suivi administratif | — | — | Sans texte visible |  |
| 24 | `4c30015` | `4c30015` | S3 | heading | S3 · H3 domaine 2 | Suivi administratif | التتبع الإداري | Validé — adapté de P-01 | Expression de P-01 S3 carte 1 (validée) |
| 25 | `4c30016` | `4c30016` | S3 | text-editor | S3 · Texte domaine 2 | &lt;p&gt;Le pôle contribue au suivi administratif de l&#x27;association. Ce domaine couvre la tenue et la conservation des documents associatifs, ainsi que le suivi des obligations administratives qui s&#x27;attachent à la vie de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يساهم القطب في التتبع الإداري للجمعية. ويشمل هذا المجال مسك الوثائق الجمعوية وحفظها، وتتبع الالتزامات الإدارية المرتبطة بحياة الجمعية.&lt;/p&gt; | **Proposition non validée** |  |
| 26 | `4c3001a` | `4c3001a` | S3 | container | S3 · Domaine 3 — Gestion des moyens nécessaires | — | — | Sans texte visible |  |
| 27 | `4c30018` | `4c30018` | S3 | heading | S3 · H3 domaine 3 | Gestion des moyens nécessaires | تدبير الوسائل الضرورية | Validé — adapté de P-01 | Expression de P-01 S3 carte 1 (validée) |
| 28 | `4c30019` | `4c30019` | S3 | text-editor | S3 · Texte domaine 3 | &lt;p&gt;Le pôle contribue à la gestion des moyens nécessaires au fonctionnement de l&#x27;association : locaux, équipements et ressources mobilisés pour la conduite des activités. Cette gestion s&#x27;entend comme un appui matériel et organisationnel, distinct des fonctions comptables et financières, qui relèvent d&#x27;un cadre propre.&lt;/p&gt; | &lt;p&gt;يساهم القطب في تدبير الوسائل الضرورية لسير عمل الجمعية: المقرات والتجهيزات والموارد المعبأة لتنفيذ الأنشطة. ويُقصد بهذا التدبير الدعم المادي والتنظيمي، وهو متميز عن المهام المحاسبية والمالية التي تخضع لإطار خاص بها.&lt;/p&gt; | **Proposition non validée** | Exclusion comptable/financière conservée telle que dans la source |
| 29 | `4c3001f` | `4c3001f` | S4 | container | S4 — Contribution transversale (ancre #contribution) | — | — | Ancre `#contribution` conservée |  |
| 30 | `4c3001d` | `4c3001d` | S4 | heading | S4 · H2 | Une contribution transversale aux autres pôles | إسهام أفقي لفائدة الأقطاب الأخرى | **Proposition non validée** |  |
| 31 | `4c3001e` | `4c3001e` | S4 | text-editor | S4 · Texte (3 paragraphes) | &lt;p&gt;La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités.&lt;/p&gt;<br>&lt;p&gt;En soutenant l&#x27;organisation, le suivi administratif et la disponibilité des moyens, le pôle participe à un cadre de fonctionnement commun au Pôle Formation et Intégration et au Pôle Animation Culturelle et Sociale.&lt;/p&gt;<br>&lt;p&gt;Cette fonction d&#x27;appui s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;لا يقتصر إسهام القطب على نطاقه الخاص، بل يساهم أيضًا في تهيئة الظروف التي يزاول فيها القطبان الآخران المنصوص عليهما في القانون الأساسي أنشطتهما.&lt;/p&gt;<br>&lt;p&gt;ومن خلال دعم التنظيم والتتبع الإداري وتوفير الوسائل، يساهم القطب في إرساء إطار عمل مشترك بين قطب التكوين والإدماج وقطب التنشيط الثقافي والاجتماعي.&lt;/p&gt;<br>&lt;p&gt;وتُمارَس وظيفة الدعم هذه في الإطار الذي يحدده القانون الأساسي، حيث يتولى المكتب التنفيذي الإشراف على تنظيم اللجان وأقطاب العمل، وتتبع تنفيذ البرامج المسطرة.&lt;/p&gt; | **Proposition non validée** | Noms des pôles = P-01 validés ; fin du §3 reprise de P-02 (3b20043) |
| 32 | `4c30030` | `4c30030` | S5 | container | S5 — Principes de fonctionnement | — | — | Sans texte visible |  |
| 33 | `4c30022` | `4c30022` | S5 | container | S5 · En-tête | — | — | Sans texte visible |  |
| 34 | `4c30020` | `4c30020` | S5 | heading | S5 · H2 | Les principes qui guident son fonctionnement | المبادئ التي توجّه سير عمله | **Proposition non validée** |  |
| 35 | `4c30021` | `4c30021` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يندرج سير عمل القطب ضمن المبادئ التي توجّه التزام الجمعية.&lt;/p&gt; | **Proposition non validée** |  |
| 36 | `4c3002f` | `4c3002f` | S5 | container | S5 · Grille des 4 principes | — | — | Sans texte visible |  |
| 37 | `4c30025` | `4c30025` | S5 | container | S5 · Principe 1 — Responsabilité | — | — | Sans texte visible |  |
| 38 | `4c30023` | `4c30023` | S5 | heading | S5 · H3 principe 1 | Responsabilité | المسؤولية | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20034) |
| 39 | `4c30024` | `4c30024` | S5 | text-editor | S5 · Texte principe 1 | &lt;p&gt;Inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;إدراج الالتزام ضمن مقاربة جادة وبنّاءة.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20035) |
| 40 | `4c30028` | `4c30028` | S5 | container | S5 · Principe 2 — Solidarité | — | — | Sans texte visible |  |
| 41 | `4c30026` | `4c30026` | S5 | heading | S5 · H3 principe 2 | Solidarité | التضامن | Repris de P-02 AR (à confirmer) | Identique P-02 (3b2002e) |
| 42 | `4c30027` | `4c30027` | S5 | text-editor | S5 · Texte principe 2 | &lt;p&gt;Développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;تنمية التآزر والعمل التطوعي والتعاون.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | Identique P-02 (3b2002f) |
| 43 | `4c3002b` | `4c3002b` | S5 | container | S5 · Principe 3 — Initiative | — | — | Sans texte visible |  |
| 44 | `4c30029` | `4c30029` | S5 | heading | S5 · H3 principe 3 | Initiative | المبادرة | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20037) |
| 45 | `4c3002a` | `4c3002a` | S5 | text-editor | S5 · Texte principe 3 | &lt;p&gt;Valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;تثمين المواهب والأفكار والقدرات على الفعل.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20038) |
| 46 | `4c3002e` | `4c3002e` | S5 | container | S5 · Principe 4 — Fonctionnement collégial | — | — | Sans texte visible |  |
| 47 | `4c3002c` | `4c3002c` | S5 | heading | S5 · H3 principe 4 | Fonctionnement collégial | التسيير الجماعي | **Proposition non validée** |  |
| 48 | `4c3002d` | `4c3002d` | S5 | text-editor | S5 · Texte principe 4 | &lt;p&gt;Les orientations générales relèvent de l&#x27;Assemblée générale, leur supervision du Bureau exécutif, et les commissions contribuent à l&#x27;étude des programmes et au suivi des activités relevant de leurs domaines de travail.&lt;/p&gt; | &lt;p&gt;تعود التوجهات العامة إلى الجمع العام، ويتولى المكتب التنفيذي الإشراف عليها، فيما تساهم اللجان في دراسة البرامج وتتبع الأنشطة المندرجة ضمن مجالات عملها.&lt;/p&gt; | **Proposition non validée** | Fin de phrase reprise de P-02 (3b20046) ; termes imposés |
| 49 | `4c3003f` | `4c3003f` | S6 | container | S6 — Les deux autres pôles | — | — | Sans texte visible |  |
| 50 | `4c30033` | `4c30033` | S6 | container | S6 · En-tête | — | — | Sans texte visible |  |
| 51 | `4c30031` | `4c30031` | S6 | heading | S6 · H2 | Les deux autres pôles | القطبان الآخران | **Proposition non validée** |  |
| 52 | `4c30032` | `4c30032` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires.&lt;/p&gt; | &lt;p&gt;يرتكز تنظيم الجمعية على ثلاثة أقطاب متكاملة منصوص عليها في القانون الأساسي.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | P-02 (3b2004b), deux-points remplacés par un point comme dans la source FR |
| 53 | `4c3003e` | `4c3003e` | S6 | container | S6 · Grille des 2 pôles | — | — | Sans texte visible |  |
| 54 | `4c30038` | `4c30038` | S6 | container | S6 · Carte 1 — Pôle Formation et Intégration → P-04 | — | — | Sans texte visible |  |
| 55 | `4c30034` | `4c30034` | S6 | heading | S6 · H3 carte 1 | Pôle Formation et Intégration | قطب التكوين والإدماج | Validé — identique P-01 | Identique P-01 (validé) |
| 56 | `4c30035` | `4c30035` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt; | &lt;p&gt;يندرج ضمن التوجهات المتعلقة بالتعلم وتنمية الكفاءات والإدماج.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20051) |
| 57 | `4c30037` | `4c30037` | S6 | container | S6 · Bouton carte 1 | — | — | Sans texte visible |  |
| 58 | `4c30036` | `4c30036` | S6 | button | S6 · Bouton carte 1 → P-04 | Découvrir le pôle | اكتشف هذا القطب | Validé — identique P-01 | Identique P-01 (validé) |
| 59 | `4c3003d` | `4c3003d` | S6 | container | S6 · Carte 2 — Pôle Animation Culturelle et Sociale → P-05 | — | — | Sans texte visible |  |
| 60 | `4c30039` | `4c30039` | S6 | heading | S6 · H3 carte 2 | Pôle Animation Culturelle et Sociale | قطب التنشيط الثقافي والاجتماعي | Validé — identique P-01 | Identique P-01 (validé) |
| 61 | `4c3003a` | `4c3003a` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;يُعنى بالتوجهات المتعلقة بالثقافة والتنشيط والمشاركة الاجتماعية.&lt;/p&gt; | Repris de P-02 AR (à confirmer) | Identique P-02 (3b20054) |
| 62 | `4c3003c` | `4c3003c` | S6 | container | S6 · Bouton carte 2 | — | — | Sans texte visible |  |
| 63 | `4c3003b` | `4c3003b` | S6 | button | S6 · Bouton carte 2 → P-05 | Découvrir le pôle | اكتشف هذا القطب | Validé — identique P-01 | Identique P-01 (validé) |
| 64 | `4c30044` | `4c30044` | S7 | container | S7 — Appel à l’action | — | — | Sans texte visible |  |
| 65 | `4c30040` | `4c30040` | S7 | heading | S7 · H2 | Une question sur le fonctionnement de l&#x27;association ? | هل لديكم سؤال حول سير عمل الجمعية؟ | **Proposition non validée** |  |
| 66 | `4c30041` | `4c30041` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez en savoir plus sur l&#x27;organisation de l&#x27;Association Amal Chabab Takaddoum, obtenir une information d&#x27;ordre administratif ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;هل ترغبون في معرفة المزيد عن تنظيم جمعية أمل شباب التقدم، أو الحصول على معلومة ذات طابع إداري، أو بحث إمكانيات التعاون؟&lt;/p&gt;<br>&lt;p&gt;لنتواصل من أجل تحديد إمكانيات التبادل.&lt;/p&gt; | **Proposition non validée** | Formulations calquées sur P-02 S7 (3b2005b) |
| 67 | `4c30043` | `4c30043` | S7 | container | S7 · Bouton | — | — | Sans texte visible |  |
| 68 | `4c30042` | `4c30042` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | تواصلوا معنا | Validé — identique P-01 | Identique P-01 (validé) |
