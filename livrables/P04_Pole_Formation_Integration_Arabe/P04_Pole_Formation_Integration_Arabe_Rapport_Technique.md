# P-04 Pôle Formation et Intégration — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**
Livrable associé : `P04_Pole_Formation_Integration_Arabe_Elementor.json`
Source : `P04_Pole_Formation_Integration_Elementor.json` (SHA-256 `7dd41dec…e3e6b3de`, **non modifiée** : empreinte identique avant et après génération).
Contenu arabe : **intégré tel que fourni dans le task-prompt**, sans retraduction ni réécriture. Les écarts constatés entre ce texte fourni et le français source sont **signalés** (section 8) et **non corrigés**.

---

## 0. Contrôles — exécutés vs nécessitant un import réel

| Contrôle | Méthode | Statut |
|---|---|---|
| Validité syntaxique JSON | `json.load` Python | ✅ Exécuté |
| 7 sections, même ordre | Comparaison arborescente source ↔ arabe | ✅ Exécuté |
| 71 éléments, hiérarchie, types, `isInner`, nombre d’enfants | Comparaison récursive nœud à nœud | ✅ Exécuté (30 conteneurs, 17 headings, 18 text-editors, 5 boutons, 1 image) |
| Hiérarchie des titres | Comptage `header_size` | ✅ Exécuté (1 H1, 6 H2, 10 H3 — conforme à la documentation) |
| Réglages inchangés hors texte et alignement RTL | Diff clé par clé de tous les `settings` | ✅ Exécuté (modifiés : `title` ×17, `editor` ×18, `text` ×5 ; `align` ajouté ×23) |
| Identifiants uniques | Comptage | ✅ Exécuté (71/71) |
| Absence de collision avec P-01, P-02 et P-03 arabes | Intersection des ensembles d’ID | ✅ Exécuté (0 / 0 / 0) |
| Aucun texte français visible restant | Recherche de caractères latins dans `title`, `editor`, `text` | ✅ Exécuté (0) |
| 40 textes arabes fournis intégrés | Contrôle à la génération (tous les ID ciblés consommés) | ✅ Exécuté (40/40) |
| Ancres `#missions` et `#contribution` | Boutons S1 ↔ `_element_id` des sections S3 et S4 | ✅ Exécuté (2/2) |
| Liens conservés | Lecture des URL | ✅ Exécuté (3 liens internes, cibles FR inchangées) |
| Image de substitution | URL et `alt` | ✅ Exécuté (inchangés) |
| Paramètres de page | `page_settings` | ✅ Exécuté |
| Widgets gratuits uniquement ; aucun header, menu, footer ou formulaire ajouté | Liste des `widgetType` | ✅ Exécuté |
| Contenus interdits absents | Recherche de termes : inscription, candidature, restauration, cuisine, préscolaire, langue arabe | ✅ Exécuté (0) — seule occurrence de « مفتوحة » : la mention S3 précisant que la page **n’est pas** un catalogue des activités ouvertes |
| **Import Elementor** | — | ⛔ **Non réalisé** |
| **Rendu RTL (bureau / tablette / mobile), absence de débordement** | — | ⛔ **Non testé** |
| **Défilement vers les ancres** | — | ⛔ **Non testé** |
| **Liens Polylang vers les pages arabes** | — | ⛔ **Non configurés** |

## 1. Structure des sept sections

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | Ligne 2 colonnes (58 % / 38 %) : H1 + sous-titre + texte + 2 boutons d’ancre ‖ image de substitution |
| S2 | S2 — Présentation | `#FFFFFF` | H2 + texte 3 paragraphes, centrés (820 px) |
| S3 | S3 — Domaines d’intervention (ancre `#missions`) | `#F4F6F6` | En-tête centré (H2 + intro 2 paragraphes, 780 px) + grille de 4 cartes (48 % → 48 % → 100 %) |
| S4 | S4 — Contribution transversale (ancre `#contribution`) | `#FFFFFF` | H2 + texte 3 paragraphes, centrés (820 px) |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | En-tête centré + grille de 4 cartes (48 % → 48 % → 100 %) |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | En-tête centré + 2 cartes pôles avec bouton |
| S7 | S7 — Appel à l’action | `#152A33` | H2 + texte + bouton Contact, centrés |

## 2. Widgets

| Type | Source | Arabe |
|---|---|---|
| `container` | 30 | 30 |
| `heading` (1 H1, 6 H2, 10 H3) | 17 | 17 |
| `text-editor` | 18 | 18 |
| `button` | 5 | 5 |
| `image` | 1 | 1 |
| **Total** | **71** | **71** |

## 3. Identifiants

**Règle : les 71 identifiants source sont conservés à l’identique. Aucune régénération.**
Raison : l’exigence 5.3 ne prévoit de nouveaux ID que si la duplication l’exige. Ce n’est pas le cas ici, car les ID Elementor n’ont besoin d’être uniques qu’à l’intérieur d’une page. C’est aussi la méthode appliquée à P-03.
Contrôles : unicité **71/71** ; partage avec P-04 FR **71/71** (voulu, correspondance 1 pour 1) ; partage avec P-01 / P-02 / P-03 arabes : **0 / 0 / 0**. Aucun identifiant interne de répéteur.

## 4. Paramètres de page

| Clé | Source | Arabe |
|---|---|---|
| `version` / `type` | `0.4` / `page` | identiques |
| `page_settings.template` | `elementor_header_footer` | identique ✅ |
| `page_settings.hide_title` | `yes` | identique ✅ |
| `title` (nom du modèle, bibliothèque admin) | `P-04 Pôle Formation et Intégration — Amal Chabab Takaddoum` | `P-04 Pôle Formation et Intégration (AR) — Amal Chabab Takaddoum` |

## 5. RTL et responsive

### 5.1 `align: "right"` ajouté sur 23 widgets

Uniquement sur les titres et paragraphes **sans alignement** dans la source. Les **12 éléments centrés** (H2 et textes de S2 à S7) restent centrés. Aucune marge, largeur, police ou propriété inconnue n’a été ajoutée.

| ID | Widget | Libellé |
|---|---|---|
| `5d40001` | heading | S1 · H1 |
| `5d40002` | text-editor | S1 · Sous-titre |
| `5d40003` | text-editor | S1 · Texte |
| `5d40012` | heading | S3 · H3 domaine 1 |
| `5d40013` | text-editor | S3 · Texte domaine 1 |
| `5d40015` | heading | S3 · H3 domaine 2 |
| `5d40016` | text-editor | S3 · Texte domaine 2 |
| `5d40018` | heading | S3 · H3 domaine 3 |
| `5d40019` | text-editor | S3 · Texte domaine 3 |
| `5d4001b` | heading | S3 · H3 domaine 4 |
| `5d4001c` | text-editor | S3 · Texte domaine 4 |
| `5d40026` | heading | S5 · H3 principe 1 |
| `5d40027` | text-editor | S5 · Texte principe 1 |
| `5d40029` | heading | S5 · H3 principe 2 |
| `5d4002a` | text-editor | S5 · Texte principe 2 |
| `5d4002c` | heading | S5 · H3 principe 3 |
| `5d4002d` | text-editor | S5 · Texte principe 3 |
| `5d4002f` | heading | S5 · H3 principe 4 |
| `5d40030` | text-editor | S5 · Texte principe 4 |
| `5d40037` | heading | S6 · H3 carte 1 |
| `5d40038` | text-editor | S6 · Texte carte 1 |
| `5d4003c` | heading | S6 · H3 carte 2 |
| `5d4003d` | text-editor | S6 · Texte carte 2 |

### 5.2 Comportements dépendant du document RTL (non testés)

Une fois la page assignée à l’Arabe (sens RTL) dans Polylang : en S1, la colonne texte s’affiche à droite et l’image à gauche ; les cartes de S3, S5 et S6 se remplissent de droite à gauche ; les boutons de S1 s’alignent à droite. Sur mobile, l’ordre du contenu reste celui de la source.

### 5.3 Réglages manuels RTL

1. Polylang → Langues → Arabe : vérifier « Sens du texte » = RTL.
2. Après import, vérifier que les 23 widgets de 5.1 sont bien alignés à droite. Selon la version d’Elementor, le contrôle peut afficher « Droite » ou « Fin ».
3. Vérifier que la police globale couvre l’arabe (aucune police imposée).

### 5.4 Responsive

Toutes les valeurs sont conservées, sans adaptation :
- **Typographies :** H1 44/38/30 ; H2 34/30/26 ; H3 20/20/19 et 18/18/17 ; textes 20/19/17, 18/17/16, 17/17/16, 16/16/15.
- **Largeurs :** 58/38, puis 48/48/100 pour les grilles ; 820 et 780 px, ramenés à 100 % sur mobile.
- **Espacements et flex :** paddings, `flex_gap`, `flex_wrap` et `flex_direction_mobile`.

Point d’attention : le texte S1 arabe compte un paragraphe plus long que le français (voir R1). À contrôler sur mobile.

## 6. Liens et ancres

| Élément | Libellé arabe | Destination | État |
|---|---|---|---|
| `5d40004` bouton S1 | مجالات تدخله | `#missions` → S3 `5d4001f` | ✅ Ancre présente |
| `5d40005` bouton S1 | مساهمته | `#contribution` → S4 `5d40022` | ✅ Ancre présente |
| `5d40039` bouton S6 | اكتشف هذا القطب | `/nos-poles/administration-et-gestion/` | ⚠️ Cible FR conservée — **destination arabe inconnue** (P-03 AR à associer) |
| `5d4003e` bouton S6 | اكتشف هذا القطب | `/nos-poles/animation-culturelle-et-sociale/` | ⚠️ Cible FR conservée — **destination arabe inconnue** (P-05 AR à associer) |
| `5d40045` bouton S7 | تواصلوا معنا | `/contact/` | ⚠️ Cible FR conservée — **destination arabe inconnue** (Contact AR à associer) |

Le permalien de la page française P-04 est `/nos-poles/formation-et-integration/`. La page arabe doit lui être liée comme traduction dans Polylang. Aucune URL ni aucun slug arabe n’a été inventé.

## 7. Réglages manuels et limites de compatibilité

1. **Import** : Elementor → Modèles → Importer, puis insertion dans une nouvelle page.
2. **Polylang** : assigner la page à l’Arabe et la lier à la page française P-04.
3. **Liens** : remplacer les 3 cibles de la section 6 une fois les pages arabes créées. Tant qu’elles ne sont pas remplacées, elles mènent aux pages **françaises**.
4. **Image** : remplacer l’image de substitution et renseigner un texte alternatif arabe (vide dans la source ; rien n’a été inventé).
5. **Décisions éditoriales** : trancher les points de la section 8 avant publication.
6. **Limites** : les contrôles sont purement statiques. L’interprétation de `align: right`, le rendu RTL et l’affichage mobile dépendent de la version d’Elementor et de la configuration Polylang. **Rien n’a été testé** dans WordPress.

Aucune modification d’Astra, des couleurs ou polices globales Elementor, des en-têtes et pieds de page, des menus, de Polylang ou du SEO global. Rien n’est importé ni publié.

## 8. Écarts relevés entre le texte arabe fourni et la source (intégrés tels quels, à arbitrer)

| # | ID | Constat | Impact |
|---|---|---|---|
| R1 | `5d40003` | Le 1ᵉʳ paragraphe arabe de S1 reprend **mot pour mot** le 1ᵉʳ paragraphe de S2 (`5d4000d`) ; le français S1 ne contient que « Il s’inscrit dans les orientations… ». | Répétition visible entre S1 et S2. |
| R2 | toute la page | Terme **النظام الأساسي**, alors que P-02 et P-03 utilisent **القانون الأساسي** (terme imposé dans le brief P-03 : « التوجهات المنصوص عليها في القانون الأساسي »). Aussi « التوجهات النظامية » (`5d4001c`) et « أقطاب نظامية » (`5d40035`). | Incohérence terminologique entre les pages. |
| R3 | `5d4000d`, `5d40015`, `5d40016` | **التعليم غير النظامي**, contre **التربية غير النظامية** en P-02. | Incohérence avec P-02. |
| R4 | `5d40013` | « النظام الأساسي **للقطب** » : le pôle n’a pas de statuts propres ; le français dit « orientations statutaires du pôle ». | Possible contresens. |
| R5 | `5d40016` | La 2ᵉ phrase française n’est **pas traduite** : « Ce domaine désigne les apprentissages conduits en dehors des cadres scolaires habituels. » | Contenu manquant par rapport au FR. |
| R6 | `5d4001c` | Le français fait de l’intégration « la finalité à laquelle les autres domaines concourent » ; l’arabe la présente comme une orientation parmi d’autres. | Nuance de sens perdue. |
| R7 | `5d40021` | S4 est **différent** du français : §1 (« ne se limite pas à son propre périmètre… ») et §2 (articulation précise avec chaque pôle) sont reformulés ; §3 reprend mot pour mot le §3 de S2 et omet la supervision des **commissions**. | Écart de contenu ; répétition S2/S4. |
| R8 | `5d40005`, `5d40020` | **مساهمته / مساهمة** ici, contre **إسهامه / إسهام** en P-03 pour les mêmes libellés français ; « transversale » rendu par **متكاملة** ici, par **أفقي** en P-03. | Incohérence entre P-03 et P-04. |
| R9 | S5 | Les principes diffèrent de P-02 et P-03 pour des textes français identiques (Solidarité : « تنمية روح التعاون والعمل التطوعي والتكافل » contre « تنمية التآزر والعمل التطوعي والتعاون » ; Responsabilité : « ترسيخ… نهج » contre « إدراج… مقاربة » ; Initiative : ajout de « والمبادرة »). | Incohérence entre les pages. |
| R10 | `5d40038`, `5d4003d` | Les descriptions des pôles diffèrent de P-02 et P-03 (« البنية الجمعوية وضمان سير عملها » contre « الهيكل الجمعوي وسير عمله » ; « يعنى » sans signes contre « يُعنى »). | Incohérence mineure. |
| R11 | `5d40044` | « تبادل **الخبرات** والتعاون » : le français dit seulement « possibilités d’échange ». | Léger ajout. |
| R12 | 9 widgets | Textes fournis **sans balise `<p>`** (sous-titre, intros S5 et S6, principes, cartes). Ils ont été enveloppés dans `<p>…</p>`, comme dans la source, sans modifier le texte. | Technique ; sans effet éditorial. |

**Recommandation** : harmoniser R2, R3, R8, R9 et R10 dans les quatre pages arabes avant publication, une fois la terminologie de référence choisie.

## 9. Métadonnées SEO proposées (non injectées — propositions non validées)

| Champ | Proposition |
|---|---|
| Titre SEO | قطب التكوين والإدماج \| جمعية أمل شباب التقدم |
| Méta-description | قطب التكوين والإدماج بجمعية أمل شباب التقدم: توجهات في مجالات التعليم والتعلم، والتعليم غير النظامي ومحو الأمية، والتكوين المهني والتأهيل، والإدماج الاجتماعي والمهني. |
| Slug (**proposition non validée**) | `قطب-التكوين-والإدماج` (alternative latine : `formation-et-integration-ar`) |

Les formulations reprennent uniquement les titres fournis. Elles ne présentent aucune activité comme ouverte et n’invitent à aucune inscription.

## 10. Tableau de correspondance (71 éléments)

ID arabe = ID source (section 3). **40 textes visibles** (17 titres, 18 éditeurs de texte, 5 boutons) : **40/40 intégrés, 0 oublié**. HTML échappé.

| # | ID source (= ID arabe) | Section | Type | `_title` | Contenu français d’origine | Contenu arabe intégré | État de traduction | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | `5d4000b` | S1 | container | S1 — Bannière | — | — | Sans texte visible |  |
| 2 | `5d4000a` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible |  |
| 3 | `5d40007` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible |  |
| 4 | `5d40001` | S1 | heading | S1 · H1 | Pôle Formation et Intégration | قطب التكوين والإدماج | Intégré tel que fourni |  |
| 5 | `5d40002` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un pôle orienté vers l&#x27;apprentissage, le développement des compétences et les initiatives favorisant l&#x27;intégration sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;قطب يركز على التعلم وتنمية الكفاءات والمبادرات التي تعزز الإدماج الاجتماعي والمهني.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Texte fourni sans balise ; enveloppé dans &lt;p&gt; comme la source |
| 6 | `5d40003` | S1 | text-editor | S1 · Texte | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt;<br>&lt;p&gt;Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يُعد قطب التكوين والإدماج أحد الأقطاب الثلاثة المنصوص عليها في النظام الأساسي لجمعية أمل شباب التقدم. ويندرج ضمن التوجهات المتعلقة بالتعلم وتنمية الكفاءات والإدماج.&lt;/p&gt;<br>&lt;p&gt;وتندرج مجالات تدخله ضمن التوجهات المنصوص عليها في النظام الأساسي للجمعية.&lt;/p&gt; | Intégré tel que fourni — **écart avec le FR signalé** | Voir point R1 |
| 7 | `5d40006` | S1 | container | S1 · Boutons | — | — | Sans texte visible |  |
| 8 | `5d40004` | S1 | button | S1 · Bouton 1 → ancre #missions | Ses domaines d&#x27;intervention | مجالات تدخله | Intégré tel que fourni |  |
| 9 | `5d40005` | S1 | button | S1 · Bouton 2 → ancre #contribution | Sa contribution | مساهمته | Intégré tel que fourni |  |
| 10 | `5d40009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |  |
| 11 | `5d40008` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée |  |
| 12 | `5d4000e` | S2 | container | S2 — Présentation | — | — | Sans texte visible |  |
| 13 | `5d4000c` | S2 | heading | S2 · H2 | Un pôle au service de l&#x27;apprentissage et de l&#x27;intégration | قطب في خدمة التعلم والإدماج | Intégré tel que fourni |  |
| 14 | `5d4000d` | S2 | text-editor | S2 · Texte (3 paragraphes) | &lt;p&gt;Le Pôle Formation et Intégration est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt;<br>&lt;p&gt;Les orientations statutaires accordent une place importante à l&#x27;éducation non formelle, à la lutte contre l&#x27;illettrisme, à la formation professionnelle et à l&#x27;accompagnement éducatif des enfants et des jeunes.&lt;/p&gt;<br>&lt;p&gt;Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale.&lt;/p&gt; | &lt;p&gt;يُعد قطب التكوين والإدماج أحد الأقطاب الثلاثة المنصوص عليها في النظام الأساسي لجمعية أمل شباب التقدم. ويندرج ضمن التوجهات المتعلقة بالتعلم وتنمية الكفاءات والإدماج.&lt;/p&gt;<br>&lt;p&gt;وتولي التوجهات المنصوص عليها في النظام الأساسي أهمية للتعليم غير النظامي، ومحاربة الأمية، والتكوين المهني، والمواكبة التربوية للأطفال والشباب.&lt;/p&gt;<br>&lt;p&gt;وطبقًا للنظام الأساسي، يخضع تنظيم أقطاب العمل وتتبع تنفيذ البرامج لإشراف المكتب التنفيذي، المنتخب من طرف الجمع العام.&lt;/p&gt; | Intégré tel que fourni |  |
| 15 | `5d4001f` | S3 | container | S3 — Domaines d&#x27;intervention (ancre #missions) | — | — | Ancre `#missions` conservée |  |
| 16 | `5d40011` | S3 | container | S3 · En-tête | — | — | Sans texte visible |  |
| 17 | `5d4000f` | S3 | heading | S3 · H2 | Les domaines d&#x27;intervention du pôle | مجالات تدخل القطب | Intégré tel que fourni |  |
| 18 | `5d40010` | S3 | text-editor | S3 · Introduction | &lt;p&gt;Les orientations statutaires de l&#x27;association définissent les domaines dans lesquels le pôle est appelé à intervenir.&lt;/p&gt;<br>&lt;p&gt;Cette page présente ces orientations. Elle ne constitue pas un catalogue : les activités effectivement ouvertes à un moment donné font l&#x27;objet d&#x27;une information distincte.&lt;/p&gt; | &lt;p&gt;تحدد التوجهات المنصوص عليها في النظام الأساسي للجمعية المجالات التي يُعنى القطب بالتدخل فيها.&lt;/p&gt;<br>&lt;p&gt;تعرض هذه الصفحة تلك التوجهات، ولا تشكل دليلاً للأنشطة المتاحة؛ إذ يتم تقديم معلومات مستقلة بشأن الأنشطة المفتوحة فعليًا في فترة معينة.&lt;/p&gt; | Intégré tel que fourni |  |
| 19 | `5d4001e` | S3 | container | S3 · Grille des 4 domaines | — | — | Sans texte visible |  |
| 20 | `5d40014` | S3 | container | S3 · Domaine 1 — Éducation et apprentissage | — | — | Sans texte visible |  |
| 21 | `5d40012` | S3 | heading | S3 · H3 domaine 1 | Éducation et apprentissage | التعليم والتعلم | Intégré tel que fourni |  |
| 22 | `5d40013` | S3 | text-editor | S3 · Texte domaine 1 | &lt;p&gt;L&#x27;éducation et l&#x27;apprentissage figurent parmi les orientations statutaires du pôle. Ce domaine englobe l&#x27;accompagnement éducatif des enfants et des jeunes prévu par les statuts de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يُعد التعليم والتعلم من بين التوجهات المنصوص عليها في النظام الأساسي للقطب. ويشمل هذا المجال المواكبة التربوية للأطفال والشباب التي ينص عليها النظام الأساسي للجمعية.&lt;/p&gt; | Intégré tel que fourni — **écart avec le FR signalé** | Voir point R4 |
| 23 | `5d40017` | S3 | container | S3 · Domaine 2 — Éducation non formelle et alphabétisation | — | — | Sans texte visible |  |
| 24 | `5d40015` | S3 | heading | S3 · H3 domaine 2 | Éducation non formelle et alphabétisation | التعليم غير النظامي ومحو الأمية | Intégré tel que fourni |  |
| 25 | `5d40016` | S3 | text-editor | S3 · Texte domaine 2 | &lt;p&gt;Les statuts accordent une place à l&#x27;éducation non formelle et à la lutte contre l&#x27;illettrisme. Ce domaine désigne les apprentissages conduits en dehors des cadres scolaires habituels.&lt;/p&gt; | &lt;p&gt;يشمل هذا المجال التوجهات المتعلقة بالتعليم غير النظامي ومحاربة الأمية، باعتبارهما من المجالات التي يوليها النظام الأساسي للجمعية أهمية خاصة.&lt;/p&gt; | Intégré tel que fourni — **écart avec le FR signalé** | Voir point R5 |
| 26 | `5d4001a` | S3 | container | S3 · Domaine 3 — Formation professionnelle et qualification | — | — | Sans texte visible |  |
| 27 | `5d40018` | S3 | heading | S3 · H3 domaine 3 | Formation professionnelle et qualification | التكوين المهني والتأهيل | Intégré tel que fourni |  |
| 28 | `5d40019` | S3 | text-editor | S3 · Texte domaine 3 | &lt;p&gt;La formation professionnelle et la qualification constituent un domaine d&#x27;intervention prévu par les orientations statutaires, envisagé comme un appui au développement des compétences.&lt;/p&gt; | &lt;p&gt;يندرج التكوين المهني والتأهيل ضمن التوجهات المرتبطة بتنمية الكفاءات، ويشكلان مجالًا من مجالات تدخل القطب وفقًا للتوجهات المنصوص عليها في النظام الأساسي.&lt;/p&gt; | Intégré tel que fourni |  |
| 29 | `5d4001d` | S3 | container | S3 · Domaine 4 — Intégration sociale et professionnelle | — | — | Sans texte visible |  |
| 30 | `5d4001b` | S3 | heading | S3 · H3 domaine 4 | Intégration sociale et professionnelle | الإدماج الاجتماعي والمهني | Intégré tel que fourni |  |
| 31 | `5d4001c` | S3 | text-editor | S3 · Texte domaine 4 | &lt;p&gt;L&#x27;intégration constitue la finalité à laquelle les autres domaines concourent : favoriser les initiatives qui soutiennent la participation sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;يمثل الإدماج الاجتماعي والمهني أحد التوجهات التي يندرج ضمنها عمل القطب، ويرتبط بالمجالات المحددة في التوجهات النظامية للجمعية.&lt;/p&gt; | Intégré tel que fourni — **écart avec le FR signalé** | Voir point R6 |
| 32 | `5d40022` | S4 | container | S4 — Contribution transversale (ancre #contribution) | — | — | Ancre `#contribution` conservée |  |
| 33 | `5d40020` | S4 | heading | S4 · H2 | Une contribution transversale aux autres pôles | مساهمة متكاملة مع الأقطاب الأخرى | Intégré tel que fourni |  |
| 34 | `5d40021` | S4 | text-editor | S4 · Texte (3 paragraphes) | &lt;p&gt;La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités.&lt;/p&gt;<br>&lt;p&gt;Les apprentissages, le développement des compétences et les initiatives d&#x27;intégration rejoignent les orientations portées par le Pôle Animation Culturelle et Sociale, tandis que le Pôle Administration et Gestion contribue à l&#x27;organisation et aux moyens nécessaires à leur conduite.&lt;/p&gt;<br>&lt;p&gt;Cette articulation s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;يساهم قطب التكوين والإدماج، ضمن حدود مجالات تدخله، في تحقيق التكامل بين أقطاب الجمعية الثلاثة.&lt;/p&gt;<br>&lt;p&gt;وتندرج علاقته بقطب الإدارة والتسيير وقطب التنشيط الثقافي والاجتماعي ضمن التنظيم العام للجمعية والتوجهات المحددة في نظامها الأساسي.&lt;/p&gt;<br>&lt;p&gt;وطبقًا للنظام الأساسي، يخضع تنظيم أقطاب العمل وتتبع تنفيذ البرامج لإشراف المكتب التنفيذي، المنتخب من طرف الجمع العام.&lt;/p&gt; | Intégré tel que fourni — **écart avec le FR signalé** | Voir point R7 |
| 35 | `5d40033` | S5 | container | S5 — Principes de fonctionnement | — | — | Sans texte visible |  |
| 36 | `5d40025` | S5 | container | S5 · En-tête | — | — | Sans texte visible |  |
| 37 | `5d40023` | S5 | heading | S5 · H2 | Les principes qui guident son fonctionnement | المبادئ المؤطرة لعمل القطب | Intégré tel que fourni |  |
| 38 | `5d40024` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;تستند طريقة عمل القطب إلى المبادئ والقيم المعتمدة في جمعية أمل شباب التقدم.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Texte fourni sans balise ; enveloppé dans &lt;p&gt; |
| 39 | `5d40032` | S5 | container | S5 · Grille des 4 principes | — | — | Sans texte visible |  |
| 40 | `5d40028` | S5 | container | S5 · Principe 1 — Égalité et justice sociale | — | — | Sans texte visible |  |
| 41 | `5d40026` | S5 | heading | S5 · H3 principe 1 | Égalité et justice sociale | المساواة والعدالة الاجتماعية | Intégré tel que fourni |  |
| 42 | `5d40027` | S5 | text-editor | S5 · Texte principe 1 | &lt;p&gt;Promouvoir des relations fondées sur le respect des droits et de la dignité.&lt;/p&gt; | &lt;p&gt;تعزيز العلاقات القائمة على احترام الحقوق والكرامة.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R9 |
| 43 | `5d4002b` | S5 | container | S5 · Principe 2 — Solidarité | — | — | Sans texte visible |  |
| 44 | `5d40029` | S5 | heading | S5 · H3 principe 2 | Solidarité | التضامن | Intégré tel que fourni |  |
| 45 | `5d4002a` | S5 | text-editor | S5 · Texte principe 2 | &lt;p&gt;Développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;تنمية روح التعاون والعمل التطوعي والتكافل.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R9 |
| 46 | `5d4002e` | S5 | container | S5 · Principe 3 — Initiative | — | — | Sans texte visible |  |
| 47 | `5d4002c` | S5 | heading | S5 · H3 principe 3 | Initiative | المبادرة | Intégré tel que fourni |  |
| 48 | `5d4002d` | S5 | text-editor | S5 · Texte principe 3 | &lt;p&gt;Valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;تثمين المواهب والأفكار والقدرات على العمل والمبادرة.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R9 |
| 49 | `5d40031` | S5 | container | S5 · Principe 4 — Responsabilité | — | — | Sans texte visible |  |
| 50 | `5d4002f` | S5 | heading | S5 · H3 principe 4 | Responsabilité | المسؤولية | Intégré tel que fourni |  |
| 51 | `5d40030` | S5 | text-editor | S5 · Texte principe 4 | &lt;p&gt;Inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;ترسيخ الالتزام ضمن نهج جاد وبنّاء.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R9 |
| 52 | `5d40042` | S6 | container | S6 — Les deux autres pôles | — | — | Sans texte visible |  |
| 53 | `5d40036` | S6 | container | S6 · En-tête | — | — | Sans texte visible |  |
| 54 | `5d40034` | S6 | heading | S6 · H2 | Les deux autres pôles | القطبان الآخران للجمعية | Intégré tel que fourni |  |
| 55 | `5d40035` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires.&lt;/p&gt; | &lt;p&gt;يقوم تنظيم الجمعية على ثلاثة أقطاب نظامية متكاملة.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; |
| 56 | `5d40041` | S6 | container | S6 · Grille des 2 pôles | — | — | Sans texte visible |  |
| 57 | `5d4003b` | S6 | container | S6 · Carte 1 — Pôle Administration et Gestion → P-03 | — | — | Sans texte visible |  |
| 58 | `5d40037` | S6 | heading | S6 · H3 carte 1 | Pôle Administration et Gestion | قطب الإدارة والتسيير | Intégré tel que fourni |  |
| 59 | `5d40038` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt; | &lt;p&gt;يساهم في تنظيم البنية الجمعوية وضمان سير عملها.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R10 |
| 60 | `5d4003a` | S6 | container | S6 · Bouton carte 1 | — | — | Sans texte visible |  |
| 61 | `5d40039` | S6 | button | S6 · Bouton carte 1 → P-03 | Découvrir le pôle | اكتشف هذا القطب | Intégré tel que fourni |  |
| 62 | `5d40040` | S6 | container | S6 · Carte 2 — Pôle Animation Culturelle et Sociale → P-05 | — | — | Sans texte visible |  |
| 63 | `5d4003c` | S6 | heading | S6 · H3 carte 2 | Pôle Animation Culturelle et Sociale | قطب التنشيط الثقافي والاجتماعي | Intégré tel que fourni |  |
| 64 | `5d4003d` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;يعنى بالتوجهات المرتبطة بالثقافة والتنشيط والمشاركة الاجتماعية.&lt;/p&gt; | Intégré tel que fourni (balise `<p>` ajoutée) | Enveloppé dans &lt;p&gt; ; voir point R10 |
| 65 | `5d4003f` | S6 | container | S6 · Bouton carte 2 | — | — | Sans texte visible |  |
| 66 | `5d4003e` | S6 | button | S6 · Bouton carte 2 → P-05 | Découvrir le pôle | اكتشف هذا القطب | Intégré tel que fourni |  |
| 67 | `5d40047` | S7 | container | S7 — Appel à l’action | — | — | Sans texte visible |  |
| 68 | `5d40043` | S7 | heading | S7 · H2 | Une question sur les orientations de ce pôle ? | هل لديكم استفسار حول توجهات هذا القطب؟ | Intégré tel que fourni |  |
| 69 | `5d40044` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez en savoir plus sur les orientations du Pôle Formation et Intégration, échanger avec l&#x27;Association Amal Chabab Takaddoum ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;هل ترغبون في معرفة المزيد عن توجهات قطب التكوين والإدماج، أو التواصل مع جمعية أمل شباب التقدم، أو بحث إمكانية التعاون؟&lt;/p&gt;<br>&lt;p&gt;لنتواصل معًا من أجل تحديد إمكانيات تبادل الخبرات والتعاون.&lt;/p&gt; | Intégré tel que fourni |  |
| 70 | `5d40046` | S7 | container | S7 · Bouton | — | — | Sans texte visible |  |
| 71 | `5d40045` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | تواصلوا معنا | Intégré tel que fourni |  |
