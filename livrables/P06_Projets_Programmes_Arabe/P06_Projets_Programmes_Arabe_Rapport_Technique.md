# P-06 Projets et programmes — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Site institutionnel**

## 1. Fichiers utilisés

| Rôle | Fichier | Remarque |
|---|---|---|
| Source (seule source de contenu P-06) | `P06_Projets_Programmes_Elementor.json` | SHA-256 `95ca36d6…e4816e1d`, **non modifié** : empreinte identique avant et après génération |
| Livrable | `P06_Projets_Programmes_Arabe_Elementor.json` | Modèle arabe, prêt pour un import manuel |
| Contrôle anti-collision des ID | JSON français P-01 à P-05 et JSON arabes P-01 à P-05 | Lecture seule |

Le texte arabe a été **intégré tel que fourni** dans le task-prompt (§ 4.2), sans retraduction ni reformulation.

## 2. Structure des quatre sections (ordre conservé)

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | H1 centré |
| S2 | S2 — Présentation | `#FFFFFF` | H2 + texte de 2 paragraphes, centrés (820 px → 100 % mobile) |
| S3 | S3 — Portefeuille de projets | `#F4F6F6` | H2 + texte (780 px → 100 %) + bouton vers l’archive de catégorie |
| S4 | S4 — Appel à l’action | `#152A33` | H2 + texte de 2 paragraphes (760 px → 100 %) + bouton Contact |

## 3. Éléments

| Type | Source | Arabe |
|---|---|---|
| `container` (4 sections + 2 conteneurs de bouton) | 6 | 6 |
| `heading` (1 H1, 3 H2) | 4 | 4 |
| `text-editor` | 3 | 3 |
| `button` | 2 | 2 |
| **Total** | **15** | **15** |

Hiérarchie parent-enfant, types d’éléments et propriétés `isInner` : identiques, vérifié nœud à nœud. Aucun élément ajouté, supprimé, déplacé ou transformé.

## 4. Identifiants

- **Règle (exigence 5.2)** : nouveaux identifiants générés pour la version arabe. Ils sont hexadécimaux, sur 7 caractères, avec le préfixe `f6a`, de `f6a0001` à `f6a000f`. Ils sont attribués dans l’ordre de parcours de l’arbre, ce qui préserve les relations parent-enfant.
- Unicité dans le fichier : **15/15**.
- Collision avec le JSON français P-06 (`e5c…`) : **0**.
- Collision avec les JSON français P-01 à P-05 et les JSON arabes P-01 à P-05 : **0**.
- La correspondance ID FR ↔ ID AR figure dans la section 9.

## 5. Adaptations RTL

- **Aucune propriété ajoutée ni modifiée** : les 7 titres et textes de la source sont déjà **centrés** (`align: center`). Les deux boutons sont dans des conteneurs `flex_justify_content: center`. Le centrage est le comportement correct en arabe comme en français ; aucune inversion mécanique n’a été appliquée.
- Les largeurs, paddings et espacements sont symétriques et inchangés. Il n’y a ni colonnes à inverser, ni positionnement absolu.
- Le sens de lecture RTL du texte, la ponctuation (« ، » « ؟ ») et l’ordre des mots reposent sur le document en `dir="rtl"`. WordPress l’émet quand la page est assignée à la langue Arabe, en sens RTL, dans Polylang. **Aucune propriété Elementor inconnue n’a été créée.**

## 6. Responsive

Toutes les valeurs sont conservées :
- **Typographies :** H1 44/38/30 ; H2 34/30/26 ; textes 17/17/16 et 18/17/16 ; boutons 16.
- **Paddings :** sections 96–100 (88 pour S4) / 72 / 56 ; boutons 16×32, puis 14×24 sur mobile.
- **Largeurs :** largeurs personnalisées des textes, ramenées à 100 % sur mobile.
- **Flex :** `flex_gap` et `flex_wrap: wrap` des conteneurs de bouton.

## 7. Liens conservés

| Bouton | Libellé arabe | Destination conservée | Point à vérifier |
|---|---|---|---|
| `f6a000a` (S3) | اكتشفوا جميع مشاريعنا | `/category/projets-programmes/` | ⚠️ Associer, dans Polylang, la catégorie à sa traduction arabe. L’URL arabe de l’archive est **inconnue** et n’a pas été inventée. |
| `f6a000f` (S4) | تواصلوا معنا | `/contact/` | ⚠️ Associer à la page Contact arabe. URL **inconnue**. |

Aucun préfixe `/ar/`, aucun slug arabe et aucune destination Polylang n’ont été créés. Tant que ces liens ne sont pas remplacés, ils mènent vers l’archive et la page Contact **françaises**.

## 8. Contrôles

### 8.1 Contrôles effectivement réalisés (statiques, sur le JSON)

| Contrôle | Résultat |
|---|---|
| Validité syntaxique JSON (`json.load`) | ✅ Valide |
| 4 sections dans le même ordre | ✅ |
| Hiérarchie, types, `isInner`, nombre d’enfants | ✅ Identiques (15/15) |
| Réglages inchangés hors texte | ✅ Seules les clés `title` (×4), `editor` (×3) et `text` (×2) diffèrent |
| Alignements centrés conservés | ✅ 7/7 |
| 9 textes arabes fournis intégrés | ✅ 9/9 |
| Aucun texte français visible restant | ✅ 0 caractère latin dans les textes visibles |
| Unicité et absence de collision des ID | ✅ (section 4) |
| Liens identiques à la source | ✅ 2/2 |
| `template: elementor_header_footer`, `hide_title: yes` | ✅ Conservés |
| Widgets gratuits uniquement ; aucune section, aucun formulaire ni catalogue ajouté | ✅ |

### 8.2 Vérifications restant à effectuer (nécessitent un import réel)

**Aucun import ni test visuel n’a été réalisé.** Les points suivants restent à confirmer dans WordPress et Elementor :
1. **Import** : que le modèle s’importe sans erreur (Elementor → Modèles → Importer).
2. **Rendu RTL** : direction du texte, ponctuation arabe, police globale avec glyphes arabes.
3. **Responsive** : lisibilité, retours à la ligne des titres arabes et largeur des boutons sur tablette et mobile, sans débordement.
4. **Liens** : fonctionnement des deux boutons et remplacement par les destinations arabes.
5. **Polylang** : assigner la page à l’Arabe, la lier à la page française P-06 et associer la catégorie `projets-programmes` à sa traduction.
6. **En-tête et pied de page Astra** en RTL : ils ne font pas partie du modèle.

### 8.3 Remarques éditoriales (texte fourni intégré tel quel — pour information)

| # | ID | Constat |
|---|---|---|
| R1 | `e5c0007` | Le français « les programmes **portés** par l’association » est rendu ici par « التي **تحملها** الجمعية ». En P-01, le même texte français a été validé sous la forme « التي **تشارك الجمعية في تنفيذها** ». |
| R2 | `e5c000c` | Le texte français est identique à P-01 S6. L’arabe fourni diffère légèrement de la version P-01 validée : « إمكانية التعاون » au lieu de « فرص التعاون » ; « تبادل الآراء » au lieu de « تبادل الأفكار ». |
| R3 | `e5c0004` | Identique à la version P-01 validée (S4, § 1 et 2). |
| R4 | `e5c0006` | « المشاريع التي أنجزتها الجمعية » reprend fidèlement « Les projets réalisés ». Aucun projet n’est nommé ni présenté comme actif. |

À arbitrer par le superviseur si une harmonisation avec P-01 est souhaitée. Aucune correction n’a été faite.

## 9. Traductions intégrées — correspondance

| # | ID FR | ID AR | Section | Type | `_title` | Texte français | Texte arabe intégré | État |
|---|---|---|---|---|---|---|---|---|
| 1 | `e5c0002` | `f6a0001` | S1 | container | S1 — Bannière | — | — | Sans texte visible |
| 2 | `e5c0001` | `f6a0002` | S1 | heading | S1 · H1 | Projets et programmes | المشاريع والبرامج | Intégré tel que fourni |
| 3 | `e5c0005` | `f6a0003` | S2 | container | S2 — Présentation | — | — | Sans texte visible |
| 4 | `e5c0003` | `f6a0004` | S2 | heading | S2 · H2 | Des projets au cœur de l&#x27;engagement associatif | مشاريع في صميم الالتزام الجمعوي | Intégré tel que fourni |
| 5 | `e5c0004` | `f6a0005` | S2 | text-editor | S2 · Texte de présentation | &lt;p&gt;À travers ses projets et programmes, Amal Chabab Takaddoum met en œuvre des initiatives dans ses domaines d’intervention.&lt;/p&gt;<br>&lt;p&gt;Éducation, formation, accompagnement et animation : chaque initiative s’inscrit dans la volonté de répondre à des besoins identifiés et de favoriser la participation des personnes et des communautés.&lt;/p&gt; | &lt;p&gt;من خلال مشاريعها وبرامجها، تعمل جمعية أمل شباب التقدم على تنفيذ مبادرات في مجالات تدخلها.&lt;/p&gt;<br>&lt;p&gt;التعليم والتكوين والمواكبة والتنشيط: تندرج كل مبادرة ضمن إرادة الاستجابة للاحتياجات المحددة وتعزيز مشاركة الأفراد والمجتمعات.&lt;/p&gt; | Intégré tel que fourni |
| 6 | `e5c000a` | `f6a0006` | S3 | container | S3 — Portefeuille de projets (renvoi vers l&#x27;archive de catégorie) | — | — | Sans texte visible |
| 7 | `e5c0006` | `f6a0007` | S3 | heading | S3 · H2 | Les projets réalisés par l&#x27;association | المشاريع التي أنجزتها الجمعية | Intégré tel que fourni |
| 8 | `e5c0007` | `f6a0008` | S3 | text-editor | S3 · Texte | &lt;p&gt;Découvrez les projets documentés et les programmes portés par l’association.&lt;/p&gt; | &lt;p&gt;اكتشفوا المشاريع الموثقة والبرامج التي تحملها الجمعية.&lt;/p&gt; | Intégré tel que fourni |
| 9 | `e5c0009` | `f6a0009` | S3 | container | S3 · Bouton → archive de la catégorie projets-programmes | — | — | Sans texte visible |
| 10 | `e5c0008` | `f6a000a` | S3 | button | S3 · Bouton → /category/projets-programmes/ | Découvrir tous nos projets | اكتشفوا جميع مشاريعنا | Intégré tel que fourni |
| 11 | `e5c000f` | `f6a000b` | S4 | container | S4 — Appel à l’action | — | — | Sans texte visible |
| 12 | `e5c000b` | `f6a000c` | S4 | heading | S4 · H2 | Construisons ensemble de nouvelles initiatives | لنبنِ معًا مبادرات جديدة | Intégré tel que fourni |
| 13 | `e5c000c` | `f6a000d` | S4 | text-editor | S4 · Texte | &lt;p&gt;Vous souhaitez découvrir nos activités, échanger avec notre équipe ou envisager une collaboration avec l’Association Amal Chabab Takaddoum ?&lt;/p&gt;<br>&lt;p&gt;Nous serons heureux d&#x27;échanger avec vous.&lt;/p&gt; | &lt;p&gt;هل ترغبون في التعرف على أنشطتنا، أو التواصل مع فريقنا، أو بحث إمكانية التعاون مع جمعية أمل شباب التقدم؟&lt;/p&gt;<br>&lt;p&gt;يسعدنا التواصل معكم وتبادل الآراء.&lt;/p&gt; | Intégré tel que fourni |
| 14 | `e5c000e` | `f6a000e` | S4 | container | S4 · Bouton | — | — | Sans texte visible |
| 15 | `e5c000d` | `f6a000f` | S4 | button | S4 · Bouton → Contact | Nous contacter | تواصلوا معنا | Intégré tel que fourni |
