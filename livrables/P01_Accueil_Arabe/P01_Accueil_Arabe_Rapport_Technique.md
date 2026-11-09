# P-01 Accueil — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**
Livrable associé : `P01_Accueil_Amal_Chabab_Takaddoum_Arabe_Elementor.json`
Source de référence : `P01_Accueil_Amal_Chabab_Takaddoum_Elementor(1).json` (SHA-256 `4a575b06…a4ba32cf`, **non modifié**, vérifié par empreinte avant/après génération).

---

## 0. Statut des contrôles

| Contrôle | Méthode | Statut |
|---|---|---|
| Validité syntaxique JSON | `json.load` Python | ✅ Exécuté |
| 7 sections, même ordre | Comparaison arborescente source ↔ arabe | ✅ Exécuté |
| Structure parent-enfant, types d’éléments, `isInner`, nombre d’enfants | Comparaison récursive nœud à nœud | ✅ Exécuté |
| 68 éléments pris en compte | Comptage récursif | ✅ Exécuté (68/68) |
| Unicité des identifiants | Comptage (éléments + `_id` des éléments de liste) | ✅ Exécuté (76/76 uniques, 0 collision avec la source) |
| Aucun réglage modifié hors texte et alignement RTL | Diff clé par clé de tous les `settings` | ✅ Exécuté |
| Aucun texte français visible restant | Recherche de caractères latins dans `title`, `editor`, `text`, `icon_list[].text` | ✅ Exécuté (0 occurrence) |
| Images de substitution conservées | Lecture des URL | ✅ Exécuté (2/2, URL identiques) |
| Zones réservées masquées D/T/M | Lecture `hide_desktop/tablet/mobile` | ✅ Exécuté (2/2) |
| Paramètres de page | Lecture `page_settings` | ✅ Exécuté |
| Absence de widget Pro | Liste des `widgetType` | ✅ Exécuté |
| **Import dans Elementor** | — | ⛔ **Non réalisé** — à faire par le superviseur |
| **Rendu visuel RTL (bureau / tablette / mobile)** | — | ⛔ **Non réalisé** — aucun test dans WordPress/Elementor n’a été effectué |
| **Absence de débordement horizontal mobile** | — | ⛔ **Non vérifiable hors import réel** (aucune largeur n’a été modifiée ; les largeurs mobiles source à 100 % sont conservées) |

---

## 1. Structure des sept sections

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière principale | `#F4F6F6` | Ligne 2 colonnes (58 % / 38 %) : H1 + texte + 2 boutons ‖ image de substitution |
| S2 | S2 — Présentation | `#FFFFFF` | Ligne 2 colonnes (55 % / 41 %) : H2 + texte + bouton ‖ image de substitution |
| S3 | S3 — Nos pôles | `#F4F6F6` | En-tête centré (H2 + intro) + grille de 3 cartes (H3 + texte + bouton) |
| S4 | S4 — Projets et programmes | `#FFFFFF` | Bloc éditorial centré (H2 + texte + bouton) + **zone réservée masquée** |
| S5 | S5 — Actualités | `#F4F6F6` | Bloc éditorial centré (H2 + texte + bouton) + **zone réservée masquée** |
| S6 | S6 — Appel à l’action | `#152A33` | H2 + texte + bouton, centrés |
| S7 | S7 — Bloc pied de page (contenu de page) | `#152A33` | Nom + signature + 2 listes de 4 liens + séparateur + mention légale |

## 2. Nombre et types d’éléments

| Type | Nombre |
|---|---|
| `container` (Flexbox natif) | 33 (dont 7 conteneurs principaux) |
| `heading` | 10 |
| `text-editor` | 11 |
| `button` | 9 |
| `image` | 2 |
| `icon-list` | 2 (4 éléments de liste chacun) |
| `divider` | 1 |
| **Total éléments** | **68** (identique à la source) |

Tous les widgets sont des widgets Elementor gratuits. Aucun widget n’a été ajouté ou supprimé.

## 3. Identifiants

- 68 identifiants d’éléments + 8 `_id` d’éléments de liste (`icon-list`) = **76 identifiants**, tous **uniques**.
- Nouveaux identifiants générés (format hexadécimal à 7 caractères, préfixe `3a2`, de `3a20001` à `3a2004c`) afin qu’aucun identifiant ne soit partagé avec le modèle français (`2a1…`). **0 collision** avec la source.
- Les relations parent-enfant sont inchangées (la renumérotation est faite sur place pendant le parcours de l’arbre). La correspondance ancien ↔ nouvel ID figure dans le tableau de la section 9.
- Remarque : Elementor régénère généralement les identifiants à l’insertion d’un modèle ; les ID ci-dessus garantissent l’unicité au niveau du fichier.

## 4. Paramètres de page et métadonnées du modèle

| Clé | Source | Arabe |
|---|---|---|
| `version` | `0.4` | `0.4` |
| `type` | `page` | `page` |
| `page_settings.template` | `elementor_header_footer` | `elementor_header_footer` ✅ |
| `page_settings.hide_title` | `yes` | `yes` ✅ |
| `title` (nom du modèle, visible uniquement dans la bibliothèque admin) | `P-01 Accueil — Association Amal Chabab Takaddoum` | `P-01 Accueil (AR) — Association Amal Chabab Takaddoum` |

Le nom du modèle a seulement reçu le suffixe « (AR) » pour le distinguer du modèle français dans la bibliothèque Elementor ; il n’est pas affiché au public.

## 5. Paramètres RTL appliqués

### 5.1 Propriétés ajoutées dans le JSON

Seule propriété ajoutée : `align: "right"` sur les 10 titres et paragraphes **qui n’avaient aucun alignement** dans la source (alignement implicite à gauche en LTR). C’est une propriété native existante des widgets `heading` et `text-editor` (déjà utilisée dans le modèle source avec la valeur `center`).

| ID FR → ID AR | Widget | Libellé |
|---|---|---|
| `2a10001` → `3a20004` | heading | S1 · H1 |
| `2a10002` → `3a20005` | text-editor | S1 · Texte d’introduction |
| `2a1000b` → `3a2000e` | heading | S2 · H2 |
| `2a1000c` → `3a2000f` | text-editor | S2 · Texte |
| `2a10017` → `3a2001a` | heading | S3 · H3 carte 1 |
| `2a10018` → `3a2001b` | text-editor | S3 · Texte carte 1 |
| `2a1001c` → `3a2001f` | heading | S3 · H3 carte 2 |
| `2a1001d` → `3a20020` | text-editor | S3 · Texte carte 2 |
| `2a10021` → `3a20024` | heading | S3 · H3 carte 3 |
| `2a10022` → `3a20025` | text-editor | S3 · Texte carte 3 |

Les éléments **centrés** dans la version française (`align: center` : H2/intro S3, S4, S5, S6, tout S7, séparateur, images) **restent centrés**. Les justifications de conteneurs (`flex_justify_content: center`) sont inchangées.

### 5.2 Comportements RTL obtenus sans propriété ajoutée (dépendent du document en `dir="rtl"`)

Elementor ne propose pas, dans ses widgets gratuits, de propriété « direction » par widget, et les attributs HTML personnalisés / CSS personnalisé par élément relèvent d’Elementor Pro. **Aucune propriété inconnue n’a été créée.** La direction RTL repose donc sur la langue de la page :

- Lorsque la page est assignée à la langue **Arabe** dans Polylang (sens du texte RTL), WordPress émet `<html dir="rtl">` et charge les feuilles RTL d’Astra et d’Elementor.
- **Ordre visuel des colonnes (S1, S2, S3, S7)** : les conteneurs Flexbox en `flex_direction: row` suivent la direction du document ; en RTL la première colonne (texte) s’affiche **à droite** et l’image à gauche — c’est l’adaptation logique attendue, sans modifier l’ordre du contenu dans le JSON. Sur mobile (`flex_direction_mobile: column`), l’ordre reste texte puis image, comme en français.
- **Boutons** (conteneurs `flex-start` / `wrap`) : alignés à droite en RTL ; les deux boutons de S1 se lisent de droite à gauche (bouton principal à droite).
- **Cartes S3** : en RTL, la carte 1 (Administration et Gestion) s’affiche à droite ; titres et textes alignés à droite ; boutons alignés à droite (début de ligne).
- **Listes de liens S7** (`icon-list`, sans `icon_align` défini dans la source) : alignement par défaut « début », donc à droite en RTL. Non modifié pour ne pas forcer une valeur non vérifiée.

### 5.3 Réglages manuels RTL requis

1. **Polylang → Langues → Arabe** : vérifier que le « Sens du texte » est réglé sur **droite à gauche (RTL)** et que la locale est `ar`. *(Ne pas modifier la configuration globale si elle est déjà correcte ; simple vérification.)*
2. Après import, ouvrir chaque titre/paragraphe listé en 5.1 : selon la version d’Elementor, le contrôle d’alignement peut afficher « Gauche/Droite » ou « Début/Fin ». Vérifier que l’icône **droite** est active et que le texte est bien aligné à droite à l’écran. Corriger manuellement si la version installée interprète la valeur différemment.
3. Vérifier que la police utilisée par le thème/Elementor dispose de glyphes arabes ; sinon le navigateur utilisera une police de repli. **Aucune police n’a été modifiée** (réglage global hors périmètre).
4. Vérifier l’ordre et l’alignement des listes S7 et des boutons de S1 en mode RTL.

## 6. Paramètres responsive

**Tous conservés à l’identique** (aucune valeur modifiée) :

- Typographies bureau/tablette/mobile : H1 44/38/30 px ; H2 34/30/26 px ; H3 20/20/19 px ; textes 18/17/16, 17/17/16, 16/16/15 px ; boutons 16 ou 15 px ; graisses et interlignes identiques.
- Largeurs de colonnes : 58/38 %, 55/41 %, cartes 33 % → 48 % (tablette) → 100 % (mobile) ; colonnes de liens 30 % → 45 % → 100 %.
- Paddings de sections 96–100 / 72 / 56 px ; paddings internes des cartes et des boutons, y compris mobile.
- `flex_wrap` / `flex_wrap_tablet`, `flex_direction_mobile: column`, `flex_gap` et déclinaisons tablette/mobile.
- Largeurs personnalisées des textes centrés (720/780/760 px, 100 % sur mobile).

**Adapté** : aucun paramètre responsive. Point d’attention : les textes arabes peuvent avoir une longueur de ligne différente du français ; à contrôler visuellement (notamment le H1 à 30 px sur mobile et les boutons de S1).

## 7. Liens internes à associer manuellement (Polylang)

Aucune URL arabe n’a été fournie. **Toutes les cibles françaises ont été conservées telles quelles** ; aucun slug arabe n’a été inventé. **Les 17 liens ci-dessous ont une destination arabe inconnue** et doivent être remplacés après création des pages arabes correspondantes.

| # | Section | Élément (ID AR) | Libellé arabe | Cible conservée (FR) | Page arabe à associer | Statut |
|---|---|---|---|---|---|---|
| 1 | S1 | Bouton 1 (`3a20007`) | اكتشف الجمعية | `/l-association/` | Traduction AR de « L’association » | ⚠️ Inconnue |
| 2 | S1 | Bouton 2 (`3a20008`) | تعرّف على مبادراتنا | `/projets-et-programmes/` | Traduction AR de « Projets et programmes » | ⚠️ Inconnue |
| 3 | S2 | Bouton (`3a20011`) | اكتشف المزيد عن الجمعية | `/l-association/` | Traduction AR de « L’association » | ⚠️ Inconnue |
| 4 | S3 | Bouton carte 1 (`3a2001d`) | اكتشف هذا القطب | `/nos-poles/administration-et-gestion/` | Traduction AR du pôle Administration et Gestion | ⚠️ Inconnue |
| 5 | S3 | Bouton carte 2 (`3a20022`) | اكتشف هذا القطب | `/nos-poles/formation-et-integration/` | Traduction AR du pôle Formation et Intégration | ⚠️ Inconnue |
| 6 | S3 | Bouton carte 3 (`3a20027`) | اكتشف هذا القطب | `/nos-poles/animation-culturelle-et-sociale/` | Traduction AR du pôle Animation Culturelle et Sociale | ⚠️ Inconnue |
| 7 | S4 | Bouton (`3a2002d`) | اكتشف مشاريعنا وبرامجنا | `/projets-et-programmes/` | Traduction AR de « Projets et programmes » | ⚠️ Inconnue |
| 8 | S5 | Bouton (`3a20034`) | اطلعوا على جميع المستجدات | `/actualites/` | Traduction AR de « Actualités » | ⚠️ Inconnue |
| 9 | S6 | Bouton (`3a2003a`) | تواصلوا معنا | `/contact/` | Traduction AR de « Contact » | ⚠️ Inconnue |
| 10 | S7 | Liste 1 › 1 | الجمعية | `/l-association/` | L’association (AR) | ⚠️ Inconnue |
| 11 | S7 | Liste 1 › 2 | أقطابنا | `/nos-poles/` | Nos pôles (AR) | ⚠️ Inconnue |
| 12 | S7 | Liste 1 › 3 | المشاريع والبرامج | `/projets-et-programmes/` | Projets et programmes (AR) | ⚠️ Inconnue |
| 13 | S7 | Liste 1 › 4 | المستجدات | `/actualites/` | Actualités (AR) | ⚠️ Inconnue |
| 14 | S7 | Liste 2 › 1 | الشركاء | `/partenaires/` | Partenaires (AR) | ⚠️ Inconnue |
| 15 | S7 | Liste 2 › 2 | الإنجازات | `/realisations/` | Réalisations (AR) | ⚠️ Inconnue |
| 16 | S7 | Liste 2 › 3 | المنشورات والموارد | `/publications-et-ressources/` | Publications et ressources (AR) | ⚠️ Inconnue |
| 17 | S7 | Liste 2 › 4 | اتصل بنا | `/contact/` | Contact (AR) | ⚠️ Inconnue |

**Risque** : tant que ces liens ne sont pas remplacés, les visiteurs de la page arabe seront dirigés vers les pages **françaises**. Les liens étant relatifs, ils ne contiennent pas le préfixe de langue Polylang (ex. `/ar/`) éventuellement utilisé par le site.

## 8. Réglages manuels restant nécessaires et limites

1. **Import** : Elementor → Modèles → Importer le fichier JSON, puis l’insérer dans une nouvelle page.
2. **Polylang** : assigner la page à la langue Arabe et la lier comme traduction de la page d’accueil française ; si la page française est la page d’accueil statique, Polylang utilisera la traduction arabe comme page d’accueil de la langue arabe.
3. **Liens** : remplacer les 17 cibles de la section 7 dès que les pages arabes existent.
4. **Images** : remplacer les 2 images de substitution (S1 visuel institutionnel, S2 vie associative) et renseigner un texte alternatif arabe (actuellement vide, comme dans la source ; aucun texte alternatif n’a été inventé).
5. **Mise en gras S1** : dans la version française, le premier paragraphe de S1 est en `<strong>`. Le contenu arabe fourni ne contient pas cette balise ; il a été intégré **tel que fourni**. Si l’accroche doit rester en gras, l’ajouter manuellement : `<p><strong>جمعية فاعلة من أجل الشباب والتضامن والتنمية الاجتماعية بمدينة الرباط.</strong></p>`.
6. **Doublon S7 / pied de page Astra** : le bloc S7 est conservé (partie intégrante du JSON source). Avec le modèle `elementor_header_footer`, le pied de page du thème Astra reste affiché : **risque de double pied de page** à vérifier visuellement.
7. **Zones réservées S4 et S5** : conservées vides et masquées sur bureau, tablette et mobile ; ne pas les activer avant l’existence de contenus réels.
8. **Libellés internes** (`_title` dans le Navigateur Elementor) : volontairement conservés en français (autorisé par le critère 6).
9. **Limites de compatibilité** : le modèle a été produit et contrôlé par analyse statique du JSON uniquement. Le comportement du contrôle d’alignement (`right` vs `start/end`) et le rendu RTL dépendent de la version d’Elementor installée et de la configuration Polylang ; ils **n’ont pas été testés** dans WordPress.

**Réglages globaux** : aucun réglage Astra, couleur ou police globale Elementor, modèle d’en-tête/pied de page, menu, configuration Polylang ou réglage SEO n’a été modifié (le livrable est un fichier JSON autonome ; aucune intervention sur le site).

## 9. Métadonnées SEO proposées (à saisir manuellement — non injectées dans le JSON)

| Champ | Proposition | Longueur |
|---|---|---|
| Titre SEO | جمعية أمل شباب التقدم بالرباط \| معًا من أجل مجتمع متضامن | ≈ 55 caractères |
| Méta-description | جمعية أمل شباب التقدم بمدينة الرباط: مبادرات جمعوية في مجالات التعليم والتكوين والثقافة والمشاركة الاجتماعية، من أجل الشباب والتضامن وتنمية المجتمع. | ≈ 150 caractères |
| Slug (**proposition non validée**) | `الرئيسية` (alternative en caractères latins : `accueil-ar`) | — |

Notes : les propositions reprennent exclusivement des formulations du contenu validé. S’agissant de la page d’accueil, l’URL publique arabe sera généralement déterminée par Polylang (ex. racine de langue) plutôt que par le slug ; le slug doit être validé par le superviseur.

## 10. Tableau de correspondance (Livrable 4)

76 lignes : 68 éléments Elementor + 8 éléments de liste (`icon-list`). Les conteneurs et widgets sans texte visible (images, séparateur, zones réservées) sont listés pour contrôle de complétude. Le HTML est affiché échappé.

**Bilan** : 30 widgets textuels traduits (10 titres, 11 éditeurs de texte, 9 boutons) + 8 éléments de liste = **38 textes visibles traduits, 0 oublié**.

| # | ID source (FR) | Nouvel ID (AR) | Section | Type | Libellé interne (`_title`, conservé FR) | Contenu français d’origine | Contenu arabe intégré | État |
|---|---|---|---|---|---|---|---|---|
| 1 | `2a1000a` | `3a20001` | S1 | container | S1 — Bannière principale | — | — | Sans texte visible |
| 2 | `2a10009` | `3a20002` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible |
| 3 | `2a10006` | `3a20003` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible |
| 4 | `2a10001` | `3a20004` | S1 | heading | S1 · H1 | Amal Chabab Takaddoum : agir ensemble pour une société solidaire | جمعية أمل شباب التقدم: معًا من أجل مجتمع متضامن | Traduit |
| 5 | `2a10002` | `3a20005` | S1 | text-editor | S1 · Texte d’introduction | &lt;p&gt;&lt;strong&gt;Une association engagée pour la jeunesse, la solidarité et le développement social à Rabat.&lt;/strong&gt;&lt;/p&gt;<br>&lt;p&gt;Depuis Rabat, l’Association Amal Chabab Takaddoum développe une action associative autour de l’éducation, de la formation, de la culture et de la participation sociale.&lt;/p&gt;<br>&lt;p&gt;À travers ses pôles d’intervention, elle porte une ambition : encourager les initiatives, renforcer les solidarités et contribuer au développement de la communauté.&lt;/p&gt; | &lt;p&gt;جمعية فاعلة من أجل الشباب والتضامن والتنمية الاجتماعية بمدينة الرباط.&lt;/p&gt;<br>&lt;p&gt;تعمل جمعية أمل شباب التقدم، انطلاقًا من مدينة الرباط، على تطوير مبادرات جمعوية في مجالات التعليم والتكوين والثقافة والمشاركة الاجتماعية.&lt;/p&gt;<br>&lt;p&gt;ومن خلال أقطاب تدخلها، تسعى الجمعية إلى تشجيع المبادرات، وتعزيز قيم التضامن، والمساهمة في تنمية المجتمع.&lt;/p&gt; | Traduit |
| 6 | `2a10005` | `3a20006` | S1 | container | S1 · Boutons | — | — | Sans texte visible |
| 7 | `2a10003` | `3a20007` | S1 | button | S1 · Bouton 1 → L’association | Découvrir l’association | اكتشف الجمعية | Traduit |
| 8 | `2a10004` | `3a20008` | S1 | button | S1 · Bouton 2 → Projets &amp; Programmes | Explorer nos actions | تعرّف على مبادراتنا | Traduit |
| 9 | `2a10008` | `3a20009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |
| 10 | `2a10007` | `3a2000a` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée (URL inchangée) |
| 11 | `2a10013` | `3a2000b` | S2 | container | S2 — Présentation | — | — | Sans texte visible |
| 12 | `2a10012` | `3a2000c` | S2 | container | S2 · Ligne 2 colonnes | — | — | Sans texte visible |
| 13 | `2a1000f` | `3a2000d` | S2 | container | S2 · Colonne texte | — | — | Sans texte visible |
| 14 | `2a1000b` | `3a2000e` | S2 | heading | S2 · H2 | Une dynamique associative tournée vers l’action | دينامية جمعوية متجددة ومنفتحة على العمل | Traduit |
| 15 | `2a1000c` | `3a2000f` | S2 | text-editor | S2 · Texte | &lt;p&gt;L’Association Amal Chabab Takaddoum est une association marocaine basée à Rabat. Son action s’inscrit dans une démarche de développement éducatif, culturel, social et sportif, avec une attention particulière portée à la jeunesse.&lt;/p&gt;<br>&lt;p&gt;Convaincue de l’importance de l’engagement collectif, l’association développe ses initiatives autour de la solidarité, de la participation et de l’accompagnement. Elle entend favoriser les opportunités d’apprentissage, d’épanouissement et d’implication dans la vie sociale.&lt;/p&gt; | &lt;p&gt;جمعية أمل شباب التقدم جمعية مغربية مقرها بمدينة الرباط. ويندرج عملها ضمن مقاربة للتنمية التربوية والثقافية والاجتماعية والرياضية، مع إيلاء اهتمام خاص بقضايا الشباب.&lt;/p&gt;<br>&lt;p&gt;وانطلاقًا من إيمانها بأهمية العمل الجماعي، تطور الجمعية مبادراتها على أساس التضامن والمشاركة والمواكبة. كما تسعى إلى تعزيز فرص التعلم وتحقيق الذات والانخراط الفاعل في الحياة الاجتماعية.&lt;/p&gt; | Traduit |
| 16 | `2a1000e` | `3a20010` | S2 | container | S2 · Bouton | — | — | Sans texte visible |
| 17 | `2a1000d` | `3a20011` | S2 | button | S2 · Bouton → L’association | En savoir plus sur l’association | اكتشف المزيد عن الجمعية | Traduit |
| 18 | `2a10011` | `3a20012` | S2 | container | S2 · Colonne visuel (image à remplacer) | — | — | Sans texte visible |
| 19 | `2a10010` | `3a20013` | S2 | image | S2 · IMAGE À REMPLACER — vie associative | — | — | Image de substitution conservée (URL inchangée) |
| 20 | `2a10027` | `3a20014` | S3 | container | S3 — Nos pôles | — | — | Sans texte visible |
| 21 | `2a10016` | `3a20015` | S3 | container | S3 · En-tête | — | — | Sans texte visible |
| 22 | `2a10014` | `3a20016` | S3 | heading | S3 · H2 | Trois pôles complémentaires, une même ambition | ثلاثة أقطاب متكاملة من أجل هدف مشترك | Traduit |
| 23 | `2a10015` | `3a20017` | S3 | text-editor | S3 · Texte d’introduction | &lt;p&gt;Les activités de l’association s’organisent autour de trois pôles qui structurent son action et contribuent à la réalisation de ses objectifs.&lt;/p&gt; | &lt;p&gt;تنتظم أنشطة الجمعية ضمن ثلاثة أقطاب تشكل إطارًا منظمًا لعملها وتساهم في تحقيق أهدافها.&lt;/p&gt; | Traduit |
| 24 | `2a10026` | `3a20018` | S3 | container | S3 · Grille des 3 cartes | — | — | Sans texte visible |
| 25 | `2a1001b` | `3a20019` | S3 | container | S3 · Carte 1 — Pôle Administration et Gestion | — | — | Sans texte visible |
| 26 | `2a10017` | `3a2001a` | S3 | heading | S3 · H3 carte 1 | Pôle Administration et Gestion | قطب الإدارة والتسيير | Traduit |
| 27 | `2a10018` | `3a2001b` | S3 | text-editor | S3 · Texte carte 1 | &lt;p&gt;Un pôle dédié à l’organisation et à la coordination de la vie associative. Il contribue au suivi administratif et à la gestion des moyens nécessaires au fonctionnement de l’association.&lt;/p&gt; | &lt;p&gt;قطب يُعنى بتنظيم الحياة الجمعوية وتنسيقها، ويساهم في التتبع الإداري وتدبير الوسائل الضرورية لسير عمل الجمعية.&lt;/p&gt; | Traduit |
| 28 | `2a1001a` | `3a2001c` | S3 | container | S3 · Bouton carte 1 | — | — | Sans texte visible |
| 29 | `2a10019` | `3a2001d` | S3 | button | S3 · Bouton carte 1 | Découvrir le pôle | اكتشف هذا القطب | Traduit |
| 30 | `2a10020` | `3a2001e` | S3 | container | S3 · Carte 2 — Pôle Formation et Intégration | — | — | Sans texte visible |
| 31 | `2a1001c` | `3a2001f` | S3 | heading | S3 · H3 carte 2 | Pôle Formation et Intégration | قطب التكوين والإدماج | Traduit |
| 32 | `2a1001d` | `3a20020` | S3 | text-editor | S3 · Texte carte 2 | &lt;p&gt;Un pôle orienté vers l’apprentissage, le développement des compétences et les initiatives favorisant l’intégration sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;قطب يركز على التعلم وتنمية الكفاءات والمبادرات التي تعزز الإدماج الاجتماعي والمهني.&lt;/p&gt; | Traduit |
| 33 | `2a1001f` | `3a20021` | S3 | container | S3 · Bouton carte 2 | — | — | Sans texte visible |
| 34 | `2a1001e` | `3a20022` | S3 | button | S3 · Bouton carte 2 | Découvrir le pôle | اكتشف هذا القطب | Traduit |
| 35 | `2a10025` | `3a20023` | S3 | container | S3 · Carte 3 — Pôle Animation Culturelle et Sociale | — | — | Sans texte visible |
| 36 | `2a10021` | `3a20024` | S3 | heading | S3 · H3 carte 3 | Pôle Animation Culturelle et Sociale | قطب التنشيط الثقافي والاجتماعي | Traduit |
| 37 | `2a10022` | `3a20025` | S3 | text-editor | S3 · Texte carte 3 | &lt;p&gt;Un pôle qui valorise la culture, les activités sociales et les initiatives collectives comme espaces de rencontre, de participation et de lien communautaire.&lt;/p&gt; | &lt;p&gt;قطب يثمن الثقافة والأنشطة الاجتماعية والمبادرات الجماعية باعتبارها فضاءات للقاء والمشاركة وتعزيز الروابط المجتمعية.&lt;/p&gt; | Traduit |
| 38 | `2a10024` | `3a20026` | S3 | container | S3 · Bouton carte 3 | — | — | Sans texte visible |
| 39 | `2a10023` | `3a20027` | S3 | button | S3 · Bouton carte 3 | Découvrir le pôle | اكتشف هذا القطب | Traduit |
| 40 | `2a1002e` | `3a20028` | S4 | container | S4 — Projets et programmes | — | — | Sans texte visible |
| 41 | `2a1002c` | `3a20029` | S4 | container | S4 · Bloc éditorial | — | — | Sans texte visible |
| 42 | `2a10028` | `3a2002a` | S4 | heading | S4 · H2 | Des actions concrètes au plus près des besoins | مبادرات ملموسة تستجيب للاحتياجات | Traduit |
| 43 | `2a10029` | `3a2002b` | S4 | text-editor | S4 · Texte | &lt;p&gt;À travers ses projets et programmes, Amal Chabab Takaddoum met en œuvre des initiatives dans ses domaines d’intervention.&lt;/p&gt;<br>&lt;p&gt;Éducation, formation, accompagnement et animation : chaque initiative s’inscrit dans la volonté de répondre à des besoins identifiés et de favoriser la participation des personnes et des communautés.&lt;/p&gt;<br>&lt;p&gt;Découvrez les projets documentés et les programmes portés par l’association.&lt;/p&gt; | &lt;p&gt;من خلال مشاريعها وبرامجها، تعمل جمعية أمل شباب التقدم على تنفيذ مبادرات في مجالات تدخلها.&lt;/p&gt;<br>&lt;p&gt;التعليم والتكوين والمواكبة والتنشيط: تندرج كل مبادرة ضمن إرادة الاستجابة للاحتياجات المحددة وتعزيز مشاركة الأفراد والمجتمعات.&lt;/p&gt;<br>&lt;p&gt;اكتشفوا المشاريع الموثقة والبرامج التي تشارك الجمعية في تنفيذها.&lt;/p&gt; | Traduit |
| 44 | `2a1002b` | `3a2002c` | S4 | container | S4 · Bouton | — | — | Sans texte visible |
| 45 | `2a1002a` | `3a2002d` | S4 | button | S4 · Bouton → Projets &amp; Programmes | Voir nos projets et programmes | اكتشف مشاريعنا وبرامجنا | Traduit |
| 46 | `2a1002d` | `3a2002e` | S4 | container | S4 · ZONE RÉSERVÉE — cartes de projets (masquée, à activer quand des fiches réelles existent) | — | — | Zone réservée masquée (D/T/M) conservée |
| 47 | `2a10035` | `3a2002f` | S5 | container | S5 — Actualités | — | — | Sans texte visible |
| 48 | `2a10033` | `3a20030` | S5 | container | S5 · Bloc éditorial | — | — | Sans texte visible |
| 49 | `2a1002f` | `3a20031` | S5 | heading | S5 · H2 | Suivre la vie associative et nos initiatives | تابعوا الحياة الجمعوية ومبادراتنا | Traduit |
| 50 | `2a10030` | `3a20032` | S5 | text-editor | S5 · Texte | &lt;p&gt;Activités, événements, rencontres et nouvelles initiatives : retrouvez les actualités d’Amal Chabab Takaddoum et suivez les actions menées par l’association.&lt;/p&gt; | &lt;p&gt;الأنشطة والفعاليات واللقاءات والمبادرات الجديدة: اكتشفوا مستجدات جمعية أمل شباب التقدم وتابعوا الأعمال والمبادرات التي تقوم بها الجمعية.&lt;/p&gt; | Traduit |
| 51 | `2a10032` | `3a20033` | S5 | container | S5 · Bouton | — | — | Sans texte visible |
| 52 | `2a10031` | `3a20034` | S5 | button | S5 · Bouton → Actualités | Consulter toutes les actualités | اطلعوا على جميع المستجدات | Traduit |
| 53 | `2a10034` | `3a20035` | S5 | container | S5 · ZONE RÉSERVÉE — articles WordPress réels (masquée, aucun article fictif) | — | — | Zone réservée masquée (D/T/M) conservée |
| 54 | `2a1003a` | `3a20036` | S6 | container | S6 — Appel à l’action | — | — | Sans texte visible |
| 55 | `2a10036` | `3a20037` | S6 | heading | S6 · H2 | Construisons ensemble des initiatives porteuses de sens | لنبنِ معًا مبادرات هادفة وذات أثر | Traduit |
| 56 | `2a10037` | `3a20038` | S6 | text-editor | S6 · Texte | &lt;p&gt;Vous souhaitez découvrir nos activités, échanger avec notre équipe ou envisager une collaboration avec l’Association Amal Chabab Takaddoum ?&lt;/p&gt;<br>&lt;p&gt;Nous serons heureux d&#x27;échanger avec vous.&lt;/p&gt; | &lt;p&gt;هل ترغبون في التعرف على أنشطتنا، أو التواصل مع فريقنا، أو بحث فرص التعاون مع جمعية أمل شباب التقدم؟&lt;/p&gt;<br>&lt;p&gt;يسعدنا التواصل معكم وتبادل الأفكار.&lt;/p&gt; | Traduit |
| 57 | `2a10039` | `3a20039` | S6 | container | S6 · Bouton | — | — | Sans texte visible |
| 58 | `2a10038` | `3a2003a` | S6 | button | S6 · Bouton → Contact | Nous contacter | تواصلوا معنا | Traduit |
| 59 | `2a1004c` | `3a2003b` | S7 | container | S7 — Bloc pied de page (contenu de page, pas un footer global) | — | — | Sans texte visible |
| 60 | `2a1003b` | `3a2003c` | S7 | heading | S7 · Nom de l’association | Association Amal Chabab Takaddoum | جمعية أمل شباب التقدم | Traduit |
| 61 | `2a1003c` | `3a2003d` | S7 | text-editor | S7 · Signature | &lt;p&gt;Jeunesse · Éducation · Formation · Solidarité · Culture&lt;/p&gt; | &lt;p&gt;الشباب · التعليم · التكوين · التضامن · الثقافة&lt;/p&gt; | Traduit |
| 62 | `2a10049` | `3a2003e` | S7 | container | S7 · Liens (2 colonnes) | — | — | Sans texte visible |
| 63 | `2a10042` | `3a2003f` | S7 | container | S7 · Liens colonne 1 | — | — | Sans texte visible |
| 64 | `2a10041` | `3a20040` | S7 | icon-list | S7 · Liens 1-4 | — | — | Sans texte visible |
| 65 | `2a1003d` | `3a20041` | S7 | icon-list › élément | lien → /l-association/ | L’association | الجمعية | Traduit (lien source conservé) |
| 66 | `2a1003e` | `3a20042` | S7 | icon-list › élément | lien → /nos-poles/ | Nos pôles | أقطابنا | Traduit (lien source conservé) |
| 67 | `2a1003f` | `3a20043` | S7 | icon-list › élément | lien → /projets-et-programmes/ | Projets et programmes | المشاريع والبرامج | Traduit (lien source conservé) |
| 68 | `2a10040` | `3a20044` | S7 | icon-list › élément | lien → /actualites/ | Actualités | المستجدات | Traduit (lien source conservé) |
| 69 | `2a10048` | `3a20045` | S7 | container | S7 · Liens colonne 2 | — | — | Sans texte visible |
| 70 | `2a10047` | `3a20046` | S7 | icon-list | S7 · Liens 5-8 | — | — | Sans texte visible |
| 71 | `2a10043` | `3a20047` | S7 | icon-list › élément | lien → /partenaires/ | Partenaires | الشركاء | Traduit (lien source conservé) |
| 72 | `2a10044` | `3a20048` | S7 | icon-list › élément | lien → /realisations/ | Réalisations | الإنجازات | Traduit (lien source conservé) |
| 73 | `2a10045` | `3a20049` | S7 | icon-list › élément | lien → /publications-et-ressources/ | Publications et ressources | المنشورات والموارد | Traduit (lien source conservé) |
| 74 | `2a10046` | `3a2004a` | S7 | icon-list › élément | lien → /contact/ | Contact | اتصل بنا | Traduit (lien source conservé) |
| 75 | `2a1004a` | `3a2004b` | S7 | divider | S7 · Séparateur | — | — | Sans texte visible |
| 76 | `2a1004b` | `3a2004c` | S7 | text-editor | S7 · Mention légale | &lt;p&gt;© Association Amal Chabab Takaddoum — Tous droits réservés.&lt;/p&gt; | &lt;p&gt;© جمعية أمل شباب التقدم — جميع الحقوق محفوظة.&lt;/p&gt; | Traduit |

