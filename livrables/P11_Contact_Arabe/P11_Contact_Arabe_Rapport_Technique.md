# P-11 Contact — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**

## 1. Fichiers utilisés

| Rôle | Fichier | Remarque |
|---|---|---|
| Source | `P11_Contact_Amal_Chabab_Takaddoum_Elementor.json` | SHA-256 `0f5a9675…f756c2557d`, **non modifié** (empreinte identique avant et après génération) |
| Documentation technique | `P11_Contact_Documentation_Technique.md` | ⚠️ **Non transmise** avec la demande. Les décisions qu’elle établit (coordonnées non vérifiées, formulaire non implémenté, bouton S6 absent) ont été appliquées telles que résumées dans le task-prompt et telles qu’elles apparaissent dans le JSON (sections et blocs masqués et vides). |
| Livrable | `P11_Contact_Amal_Chabab_Takaddoum_Arabe_Elementor.json` | Modèle arabe prêt pour un import manuel |
| Contrôle anti-collision des ID | JSON français P-01 à P-06 et JSON arabes P-01 à P-06 | Lecture seule |

Les textes arabes ont été **intégrés tels que fournis** au § 4.2 du task-prompt, sans retraduction ni reformulation.

## 2. Structure des six sections (ordre conservé)

| # | Section (`_title` conservé) | Fond | Visibilité | Contenu |
|---|---|---|---|---|
| S1 | S1 — Bannière principale | `#F4F6F6` | Visible | 2 colonnes (58 % / 38 %) : H1 + sous-titre + texte + bouton d’ancre ‖ image de substitution |
| S2 | S2 — Prendre contact avec l’association | `#FFFFFF` | Visible | H2 + texte 2 paragraphes, centrés (820 px) |
| S3 | S3 — Coordonnées et localisation | `#F4F6F6` | **Masquée D/T/M** | H2 (traduit) + grille de 4 blocs réservés **vides et masqués** |
| S4 | S4 — Motifs de prise de contact (ancre `#motifs`) | `#F4F6F6` | Visible | En-tête centré + 3 cartes (33 % → 48 % → 100 %) |
| S5 | S5 — Zone réservée : formulaire | `#FFFFFF` | **Masquée D/T/M** | **Vide** (0 enfant) |
| S6 | S6 — Appel à l’action | `#152A33` | Visible | H2 + texte centrés + bloc bouton réservé **vide et masqué** |

## 3. Éléments

| Type | Source | Arabe |
|---|---|---|
| `container` | 21 | 21 |
| `heading` (1 H1, 5 H2, 3 H3) | 8 | 8 |
| `text-editor` | 8 | 8 |
| `button` | 1 | 1 |
| `image` | 1 | 1 |
| **Total** | **39** | **39** |

Hiérarchie, types et `isInner` sont identiques (vérifiés nœud à nœud). Aucun élément n’a été ajouté, supprimé, déplacé ou transformé.

## 4. Identifiants

- **Règle (5.2)** : nouveaux identifiants générés, **aucun ID du fichier français n’est réutilisé**. Format hexadécimal à 7 caractères, préfixe `a7b` (`a7b0001` → `a7b0027`), attribués dans l’ordre de parcours de l’arbre ; les relations parent-enfant sont préservées.
- Unicité : **39/39**.
- Collision avec le P-11 français (`7f6…`) : **0**.
- Collision avec les 6 autres JSON français et les 6 JSON arabes déjà produits : **0** (13 fichiers contrôlés au total).
- La correspondance FR ↔ AR figure en section 10.

## 5. Adaptations RTL

### 5.1 Propriété ajoutée : `align: "right"` (9 widgets)

Ajoutée uniquement sur les titres et paragraphes **sans alignement** dans la source :
- **S1** : H1 `a7b0004`, sous-titre `a7b0005`, texte `a7b0006` ;
- **S4** : H3 et textes des 3 cartes (`a7b001b`, `a7b001c`, `a7b001e`, `a7b001f`, `a7b0021`, `a7b0022`).

Les **8 éléments centrés** de la source restent centrés : H2 et textes de S2, S4 en-tête, S6, ainsi que le H2 de S3, masqué. Aucune marge, largeur, police ni propriété inconnue n’a été ajoutée, et aucune inversion mécanique n’a été appliquée.

### 5.2 Comportement attendu en document RTL (non testé)

Une fois la page assignée à l’Arabe (sens RTL) dans Polylang :
- **S1** : la ligne flex suit la direction du document. La colonne texte devrait s’afficher **à droite** et l’image à gauche, sans modification de l’ordre dans le JSON. Sur mobile, l’ordre reste texte puis image.
- **Bouton d’ancre S1** : son conteneur est aligné au début de ligne, donc à droite en RTL.
- **Cartes S4** : remplies de droite à gauche.

## 6. Ancre, liens et permalien

| Élément | Libellé arabe | Destination | Contrôle |
|---|---|---|---|
| `a7b0008` bouton S1 | أسباب التواصل | `#motifs` | ✅ L’ancre `motifs` est portée par la section S4 (`a7b0015`) |

- Le fichier ne contient **aucun autre lien** : ni `tel:`, ni `mailto:`, ni lien externe.
- Le permalien source `/contact/` est inchangé. La page arabe devra être liée à la page française dans Polylang.
- Aucun préfixe `/ar/`, aucun slug ni aucune destination arabe n’a été inventé.

## 7. Sections masquées, coordonnées et formulaire

| Élément | Source | Arabe |
|---|---|---|
| S3 (`a7b000e`) | Masquée D/T/M | **Masquée D/T/M** ✅ — seul son H2 est traduit (بيانات الاتصال والموقع) |
| 4 blocs réservés S3 : adresse, téléphone, courriel, localisation | Vides, masqués | **Vides (0 enfant), masqués D/T/M** ✅ |
| S5 formulaire (`a7b0023`) | Vide, masquée | **Vide (0 enfant), masquée D/T/M** ✅ |
| Bloc bouton S6 (`a7b0027`) | Vide, masqué | **Vide (0 enfant), masqué D/T/M** ✅ |

Les contrôles le confirment : aucune adresse, aucun téléphone, aucun courriel, aucune carte, aucun formulaire, aucun horaire, aucun délai de réponse et aucun réseau social. Aucune visibilité n’a été modifiée.

## 8. Contrôles

### 8.1 Contrôles effectivement réalisés (statiques, sur le JSON)

| Contrôle | Résultat |
|---|---|
| Validité syntaxique JSON | ✅ |
| 6 sections dans le même ordre ; hiérarchie, types et `isInner` | ✅ 39/39 |
| Réglages inchangés hors texte et alignement RTL | ✅ Clés modifiées : `title` ×8, `editor` ×8, `text` ×1 ; `align` ajouté ×9 |
| 17 textes arabes fournis intégrés (dont le H2 de S3) | ✅ 17/17 |
| Aucun texte français visible restant | ✅ 0 caractère latin dans les textes |
| Visibilité de S3, S5 et des blocs réservés | ✅ Inchangée (masqués sur bureau, tablette et mobile) |
| Ancre `#motifs` ↔ `_element_id` de S4 | ✅ |
| Absence de `tel:`, `mailto:`, lien externe, widget formulaire ou carte | ✅ |
| Unicité et absence de collision des ID | ✅ |
| `template: elementor_header_footer`, `hide_title: yes` | ✅ |
| Widgets gratuits uniquement | ✅ |

### 8.2 Points à vérifier manuellement (import réel nécessaire)

**Aucun import ni test visuel n’a été réalisé.**
1. **Import** sans erreur (Elementor → Modèles → Importer).
2. **Rendu RTL** : direction du texte, alignement à droite effectif des 9 widgets de 5.1 (selon la version d’Elementor, le contrôle peut afficher « Droite » ou « Fin »).
3. **Inversion des colonnes de S1** : le texte doit être à droite et l’image à gauche sur bureau.
4. **Ponctuation arabe** (« ، » « ؟ ») et police globale couvrant l’arabe.
5. **Responsive** : bureau, tablette et mobile — pas de débordement, retour à la ligne correct du bouton et des titres.
6. **Ancre `#motifs`** : défilement vers S4, et éventuel masquage du titre par un en-tête fixe Astra.
7. **En-tête et pied de page Astra** en RTL (hors modèle).
8. **Polylang** : assigner la page à l’Arabe et la lier à `/contact/`. Les autres pages arabes qui pointent vers `/contact/` devront aussi être raccordées à cette page arabe.
9. **Image** : remplacer le visuel de substitution et renseigner un texte alternatif arabe (vide dans la source, rien n’a été inventé).

## 9. Remarques éditoriales (textes intégrés tels quels — pour information)

| # | ID | Constat |
|---|---|---|
| R1 | `7f60001` | H1 « اتصلوا بنا » ; P-01 S7 utilise « اتصل بنا » comme libellé du lien vers Contact. |
| R2 | `7f60003` | « فتح باب للتواصل **وتبادل الآراء** » est un peu plus développé que le français « envisager un échange ». |
| R3 | `7f6001c` | « **القوانين الأساسية** » (pluriel) ; les autres pages emploient « النظام الأساسي » (P-04, P-05) ou « القانون الأساسي » (P-02, P-03). |
| R4 | `7f60019` | « توجهاتها **النظامية** » : cohérent avec P-04 et P-05. |
| R5 | `7f6001f` | « التي **تحملها** الجمعية » : cohérent avec P-06. |

Aucune correction n’a été faite. Une harmonisation de la terminologie des statuts sur l’ensemble des pages arabes reste recommandée.

## 10. Traductions intégrées — correspondance (39 éléments)

| # | ID FR | ID AR | Section | Type | `_title` (FR conservé) | Texte français | Texte arabe intégré | État |
|---|---|---|---|---|---|---|---|---|
| 1 | `7f6000a` | `a7b0001` | S1 | container | S1 — Bannière principale | — | — | Sans texte visible |
| 2 | `7f60009` | `a7b0002` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible |
| 3 | `7f60006` | `a7b0003` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible |
| 4 | `7f60001` | `a7b0004` | S1 | heading | S1 · H1 | Contact | اتصلوا بنا | Intégré tel que fourni |
| 5 | `7f60002` | `a7b0005` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un point d&#x27;entrée pour échanger avec l&#x27;Association Amal Chabab Takaddoum.&lt;/p&gt; | &lt;p&gt;بوابتكم للتواصل مع جمعية أمل شباب التقدم.&lt;/p&gt; | Intégré tel que fourni |
| 6 | `7f60003` | `a7b0006` | S1 | text-editor | S1 · Texte | &lt;p&gt;Cette page réunit les moyens d&#x27;entrer en relation avec l&#x27;association, à Rabat.&lt;/p&gt;<br>&lt;p&gt;Elle s&#x27;adresse aux personnes, aux associations et aux institutions souhaitant obtenir une information ou envisager un échange.&lt;/p&gt; | &lt;p&gt;تجمع هذه الصفحة الوسائل المتاحة للتواصل مع الجمعية بالرباط.&lt;/p&gt;<br>&lt;p&gt;وهي موجهة إلى الأشخاص والجمعيات والمؤسسات الراغبة في الحصول على معلومات أو فتح باب للتواصل وتبادل الآراء.&lt;/p&gt; | Intégré tel que fourni |
| 7 | `7f60005` | `a7b0007` | S1 | container | S1 · Bouton | — | — | Sans texte visible |
| 8 | `7f60004` | `a7b0008` | S1 | button | S1 · Bouton → ancre #motifs | Motifs de prise de contact | أسباب التواصل | Intégré tel que fourni |
| 9 | `7f60008` | `a7b0009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |
| 10 | `7f60007` | `a7b000a` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée (URL inchangée) |
| 11 | `7f6000d` | `a7b000b` | S2 | container | S2 — Prendre contact avec l&#x27;association | — | — | Sans texte visible |
| 12 | `7f6000b` | `a7b000c` | S2 | heading | S2 · H2 | Prendre contact avec l&#x27;association | التواصل مع الجمعية | Intégré tel que fourni |
| 13 | `7f6000c` | `a7b000d` | S2 | text-editor | S2 · Texte (2 paragraphes) | &lt;p&gt;L&#x27;Association Amal Chabab Takaddoum est une association marocaine basée à Rabat. Cette page indique comment la joindre et dans quels cas la solliciter.&lt;/p&gt;<br>&lt;p&gt;Toute demande d&#x27;information ou proposition d&#x27;échange peut être adressée à l&#x27;association.&lt;/p&gt; | &lt;p&gt;جمعية أمل شباب التقدم جمعية مغربية مقرها بالرباط. توضح هذه الصفحة كيفية التواصل معها والحالات التي يمكن فيها التوجه إليها.&lt;/p&gt;<br>&lt;p&gt;يمكن توجيه أي طلب للحصول على معلومات أو أي مقترح للتبادل والتواصل إلى الجمعية.&lt;/p&gt; | Intégré tel que fourni |
| 14 | `7f60014` | `a7b000e` | S3 | container | S3 — Coordonnées et localisation (SECTION MASQUÉE — aucune coordonnée vérifiée) | — | — | Sans texte visible |
| 15 | `7f6000e` | `a7b000f` | S3 | heading | S3 · H2 | Coordonnées et localisation | بيانات الاتصال والموقع | Intégré tel que fourni (section masquée) |
| 16 | `7f60013` | `a7b0010` | S3 | container | S3 · Grille des blocs de coordonnées | — | — | Sans texte visible |
| 17 | `7f6000f` | `a7b0011` | S3 | container | S3 · BLOC RÉSERVÉ — Adresse physique (à confirmer, voir documentation) | — | — | Sans texte visible |
| 18 | `7f60010` | `a7b0012` | S3 | container | S3 · BLOC RÉSERVÉ — Téléphone (non établi) | — | — | Sans texte visible |
| 19 | `7f60011` | `a7b0013` | S3 | container | S3 · BLOC RÉSERVÉ — Courriel (non établi) | — | — | Sans texte visible |
| 20 | `7f60012` | `a7b0014` | S3 | container | S3 · BLOC RÉSERVÉ — Localisation géographique (subordonnée à l&#x27;adresse) | — | — | Sans texte visible |
| 21 | `7f60022` | `a7b0015` | S4 | container | S4 — Motifs de prise de contact (ancre #motifs) | — | — | Ancre `#motifs` conservée |
| 22 | `7f60017` | `a7b0016` | S4 | container | S4 · En-tête | — | — | Sans texte visible |
| 23 | `7f60015` | `a7b0017` | S4 | heading | S4 · H2 | Motifs de prise de contact | أسباب التواصل مع الجمعية | Intégré tel que fourni |
| 24 | `7f60016` | `a7b0018` | S4 | text-editor | S4 · Introduction | &lt;p&gt;Les demandes adressées à l&#x27;association peuvent relever notamment des motifs suivants.&lt;/p&gt; | &lt;p&gt;قد تتعلق الطلبات الموجهة إلى الجمعية، على وجه الخصوص، بالأسباب التالية.&lt;/p&gt; | Intégré tel que fourni |
| 25 | `7f60021` | `a7b0019` | S4 | container | S4 · Grille des 3 motifs | — | — | Sans texte visible |
| 26 | `7f6001a` | `a7b001a` | S4 | container | S4 · Motif 1 — Informations générales sur l&#x27;associati | — | — | Sans texte visible |
| 27 | `7f60018` | `a7b001b` | S4 | heading | S4 · H3 motif 1 | Informations générales sur l&#x27;association | معلومات عامة حول الجمعية | Intégré tel que fourni |
| 28 | `7f60019` | `a7b001c` | S4 | text-editor | S4 · Texte motif 1 | &lt;p&gt;Demander une information sur l&#x27;identité de l&#x27;association, ses orientations statutaires ou son organisation.&lt;/p&gt; | &lt;p&gt;طلب معلومات حول هوية الجمعية أو توجهاتها النظامية أو تنظيمها.&lt;/p&gt; | Intégré tel que fourni |
| 29 | `7f6001d` | `a7b001d` | S4 | container | S4 · Motif 2 — Échanges institutionnels et partenaria | — | — | Sans texte visible |
| 30 | `7f6001b` | `a7b001e` | S4 | heading | S4 · H3 motif 2 | Échanges institutionnels et partenariats | التواصل المؤسساتي والشراكات | Intégré tel que fourni |
| 31 | `7f6001c` | `a7b001f` | S4 | text-editor | S4 · Texte motif 2 | &lt;p&gt;Proposer un échange entre organisations. Les statuts prévoient de collaborer avec les associations partageant les mêmes objectifs, tant au niveau national qu&#x27;international.&lt;/p&gt; | &lt;p&gt;اقتراح تبادل أو تواصل بين المنظمات. وتنص القوانين الأساسية على التعاون مع الجمعيات التي تتقاسم الأهداف نفسها، على المستويين الوطني والدولي.&lt;/p&gt; | Intégré tel que fourni |
| 32 | `7f60020` | `a7b0020` | S4 | container | S4 · Motif 3 — Questions relatives aux projets et aux | — | — | Sans texte visible |
| 33 | `7f6001e` | `a7b0021` | S4 | heading | S4 · H3 motif 3 | Questions relatives aux projets et aux initiatives associatives | استفسارات حول المشاريع والمبادرات الجمعوية | Intégré tel que fourni |
| 34 | `7f6001f` | `a7b0022` | S4 | text-editor | S4 · Texte motif 3 | &lt;p&gt;Adresser une question portant sur les projets et les initiatives portés par l&#x27;association.&lt;/p&gt; | &lt;p&gt;توجيه استفسار يتعلق بالمشاريع والمبادرات التي تحملها الجمعية.&lt;/p&gt; | Intégré tel que fourni |
| 35 | `7f60023` | `a7b0023` | S5 | container | S5 — ZONE RÉSERVÉE : formulaire de contact (NON IMPLÉMENTÉ — périmètre contractuel non établi) | — | — | Sans texte visible |
| 36 | `7f60027` | `a7b0024` | S6 | container | S6 — Appel à l’action (sans bouton : aucune destination de contact vérifiée) | — | — | Sans texte visible |
| 37 | `7f60024` | `a7b0025` | S6 | heading | S6 · H2 | Échanger avec l&#x27;association | التواصل وتبادل الآراء مع الجمعية | Intégré tel que fourni |
| 38 | `7f60025` | `a7b0026` | S6 | text-editor | S6 · Texte | &lt;p&gt;L&#x27;Association Amal Chabab Takaddoum est ouverte aux échanges avec les personnes, les associations et les institutions intéressées par son action.&lt;/p&gt;<br>&lt;p&gt;Nous serons heureux d&#x27;échanger avec vous.&lt;/p&gt; | &lt;p&gt;جمعية أمل شباب التقدم منفتحة على التواصل وتبادل الآراء مع الأشخاص والجمعيات والمؤسسات المهتمة بعملها.&lt;/p&gt;<br>&lt;p&gt;يسعدنا التواصل معكم وتبادل الآراء.&lt;/p&gt; | Intégré tel que fourni |
| 39 | `7f60026` | `a7b0027` | S6 | container | S6 · BLOC RÉSERVÉ — bouton de contact (à activer dès qu&#x27;une destination vérifiée existe) | — | — | Sans texte visible |
