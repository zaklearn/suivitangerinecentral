# P-05 Pôle Animation Culturelle et Sociale — Version arabe (RTL) — Rapport technique

**Association Amal Chabab Takaddoum — Rabat**
Livrable associé : `P05_Pole_Animation_Culturelle_Sociale_Arabe_Elementor.json`
Source : `P05_Pole_Animation_Culturelle_Sociale_Elementor.json` (SHA-256 `7dcd0146…32c7c5c0`, **non modifiée** : empreinte identique avant et après génération).
Référence structurelle : `P03_Pole_Administration_Gestion_Elementor.json` (français, non modifié).
Contenu arabe : **intégré tel que fourni dans le task-prompt**, sans retraduction ni réécriture.

> ⚠️ **Entrées non transmises** : `P05_Pole_Animation_Culturelle_Sociale_Documentation_Technique.md` et `P05_Releve_Redactionnel.md` n’ont pas été reçus (seul le JSON P-05 a été joint).
> Conséquence : la classification **13 imposés / 15 validés repris / 17 propositions** (45 blocs) n’a pas pu être affectée bloc par bloc. Dans le tableau de correspondance, seuls les statuts **explicitement indiqués dans le brief** sont renseignés : Principe 4 = proposition à valider ; texte Culture = validé repris de P-02. Tous les autres textes sont marqués « non déterminée ». **Aucun texte n’a été reclassé** : en particulier, aucune proposition n’est présentée comme validée. Le report de la classification est à faire par le superviseur à partir du relevé.

---

## 0. Contrôles — exécutés vs non effectués

| Contrôle | Méthode | Statut |
|---|---|---|
| Validité syntaxique JSON | `json.load` Python | ✅ Exécuté |
| 7 sections, même ordre | Comparaison arborescente source ↔ arabe | ✅ Exécuté |
| 68 éléments, hiérarchie, types, `isInner`, nombre d’enfants | Comparaison récursive nœud à nœud | ✅ Exécuté (29 conteneurs, 16 headings : 1 H1, 6 H2, 9 H3 ; 17 text-editors, 5 boutons, 1 image) |
| Conformité structurelle avec P-03 FR | Comparaison de la forme de l’arbre et de tous les réglages, hors textes et liens | ✅ Exécuté : identique sur les 7 sections |
| Réglages inchangés hors texte et alignement RTL | Diff clé par clé | ✅ Exécuté (modifiés : `title` ×16, `editor` ×17, `text` ×5 ; `align` ajouté ×21) |
| Identifiants uniques | Comptage | ✅ Exécuté (68/68) |
| Absence de collision avec P-01 à P-04 arabes | Intersection des ensembles d’ID | ✅ Exécuté (0 / 0 / 0 / 0) |
| Aucun texte français visible restant | Recherche de caractères latins | ✅ Exécuté (0) |
| 38 textes arabes fournis intégrés | Contrôle à la génération | ✅ Exécuté (38/38) |
| Ordre des domaines : Culture, Animation, Participation sociale | Lecture des H3 | ✅ Exécuté |
| Ordre des principes : Responsabilité, Solidarité, Initiative, Fonctionnement collégial | Lecture des H3 | ✅ Exécuté |
| Deux cartes « autres pôles » présentes | Lecture des H3 | ✅ Exécuté |
| Ancres `#missions` et `#contribution` | Boutons S1 ↔ `_element_id` S3/S4 | ✅ Exécuté (2/2) |
| Liens internes conservés | Lecture des URL | ✅ Exécuté (3, cibles FR inchangées) |
| Image de substitution | URL et `alt` | ✅ Exécuté (inchangés) |
| Paramètres de page | `page_settings` | ✅ Exécuté |
| Widgets gratuits ; pas de header, menu, footer ou formulaire | Liste des `widgetType` | ✅ Exécuté |
| Contenus interdits absents | Recherche de termes : inscription, candidature, académie, football, atelier, festival, environnement, catégories marginalisées, « ouvert » | ✅ Exécuté (0) — seule mention sportive : « الرياضية » dans la carte Culture, conservée conformément au brief |
| **Import Elementor** | — | ⛔ **Non effectué** |
| **Rendu RTL (bureau / tablette / mobile), débordement** | — | ⛔ **Non effectué** |
| **Inversion des colonnes S1, ponctuation arabe, en-tête et pied de page Astra en RTL** | — | ⛔ **Non effectué** (déjà signalé comme non testé par la documentation P-05) |
| **Défilement vers les ancres ; liens Polylang** | — | ⛔ **Non effectué** |

## 1. Structure des sept sections

| # | Section (`_title` conservé) | Fond | Contenu |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | Ligne 2 colonnes (58 % / 38 %) : H1 + sous-titre + texte (2 §) + 2 boutons d’ancre ‖ image de substitution |
| S2 | S2 — Présentation | `#FFFFFF` | H2 + texte de 3 §, centrés (820 px) |
| S3 | S3 — Trois domaines d’intervention (ancre `#missions`) | `#F4F6F6` | En-tête centré + 3 cartes : Culture, Animation, Participation sociale (33 % → 48 % → 100 %) |
| S4 | S4 — Contribution transversale (ancre `#contribution`) | `#FFFFFF` | H2 + texte de 3 §, centrés (820 px) |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | En-tête centré + 4 cartes : Responsabilité, Solidarité, Initiative, Fonctionnement collégial (48 % → 48 % → 100 %) |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | En-tête centré + 2 cartes pôles (Administration et Gestion ; Formation et Intégration) avec bouton |
| S7 | S7 — Appel à l’action | `#152A33` | H2 + texte + bouton Contact, centrés |

## 2. Widgets

| Type | Source | Arabe |
|---|---|---|
| `container` | 29 | 29 |
| `heading` (1 H1, 6 H2, 9 H3) | 16 | 16 |
| `text-editor` | 17 | 17 |
| `button` | 5 | 5 |
| `image` | 1 | 1 |
| **Total** | **68** | **68** |

## 3. Identifiants

**Règle (identique à P-03 et P-04) : les 68 identifiants source sont conservés tels quels. Aucune régénération.** Elle n’est pas nécessaire : les identifiants Elementor n’ont à être uniques qu’à l’intérieur d’une page.
Contrôles :
- Unicité : **68/68**.
- Partage avec P-05 FR : **68/68**, voulu pour garder une correspondance 1 pour 1.
- Partage avec P-01, P-02, P-03 et P-04 arabes : **0**.
- Aucun identifiant interne de répéteur.

## 4. Paramètres de page

| Clé | Source | Arabe |
|---|---|---|
| `version` / `type` | `0.4` / `page` | identiques |
| `page_settings.template` | `elementor_header_footer` | identique ✅ |
| `page_settings.hide_title` | `yes` | identique ✅ |
| `title` (nom du modèle en bibliothèque) | `P-05 Pôle Animation Culturelle et Sociale — Amal Chabab Takaddoum` | `P-05 Pôle Animation Culturelle et Sociale (AR) — Amal Chabab Takaddoum` |

## 5. RTL et responsive

### 5.1 `align: "right"` ajouté sur 21 widgets

Il est ajouté uniquement sur les titres et paragraphes **sans alignement** dans la source. Les **12 éléments centrés** (H2 et textes de S2 à S7) restent centrés. Aucune marge, largeur, police ou propriété inconnue n’est ajoutée. Les espacements horizontaux sont symétriques et il n’y a aucun positionnement absolu, ce qui est cohérent avec la documentation P-05.

| ID | Widget | Libellé |
|---|---|---|
| `6e50001` | heading | S1 · H1 |
| `6e50002` | text-editor | S1 · Sous-titre |
| `6e50003` | text-editor | S1 · Texte |
| `6e50012` | heading | S3 · H3 domaine 1 |
| `6e50013` | text-editor | S3 · Texte domaine 1 |
| `6e50015` | heading | S3 · H3 domaine 2 |
| `6e50016` | text-editor | S3 · Texte domaine 2 |
| `6e50018` | heading | S3 · H3 domaine 3 |
| `6e50019` | text-editor | S3 · Texte domaine 3 |
| `6e50023` | heading | S5 · H3 principe 1 |
| `6e50024` | text-editor | S5 · Texte principe 1 |
| `6e50026` | heading | S5 · H3 principe 2 |
| `6e50027` | text-editor | S5 · Texte principe 2 |
| `6e50029` | heading | S5 · H3 principe 3 |
| `6e5002a` | text-editor | S5 · Texte principe 3 |
| `6e5002c` | heading | S5 · H3 principe 4 |
| `6e5002d` | text-editor | S5 · Texte principe 4 |
| `6e50034` | heading | S6 · H3 carte 1 |
| `6e50035` | text-editor | S6 · Texte carte 1 |
| `6e50039` | heading | S6 · H3 carte 2 |
| `6e5003a` | text-editor | S6 · Texte carte 2 |

### 5.2 Comportements dépendant du document RTL (non testés)

Une fois la page assignée à l’Arabe (sens RTL) dans Polylang :
- En S1, la colonne texte doit s’afficher à droite et l’image à gauche, par la direction flex du document. **Non testé.**
- Les cartes de S3, S5 et S6 se remplissent de droite à gauche.
- Les boutons de S1 s’alignent à droite.
- Sur mobile, l’ordre du contenu reste celui de la source.

### 5.3 Réglages manuels RTL

1. Polylang → Langues → Arabe : vérifier que le sens du texte est RTL.
2. Vérifier l’alignement à droite des 21 widgets de 5.1. Selon la version d’Elementor, le réglage s’affiche « Droite » ou « Fin ».
3. Vérifier le rendu de la ponctuation arabe (« ، »، « ؟ »، « ؛ ») et la police globale.
4. Vérifier l’en-tête et le pied de page Astra en RTL. Ils ne font pas partie du modèle et n’ont pas été modifiés.

### 5.4 Responsive

Toutes les valeurs sont conservées, sans adaptation :
- **Typographies :** H1 44/38/30 ; H2 34/30/26 ; H3 20/20/19 et 18/18/17 ; textes 20/19/17, 18/17/16, 17/17/16, 16/16/15.
- **Largeurs :** 58/38 ; 33/48/100 ; 48/48/100 ; 820 et 760 px, ramenés à 100 % sur mobile.
- **Espacements et flex :** paddings, `flex_gap`, `flex_wrap` et `flex_direction_mobile`.

## 6. Liens et ancres

| Élément | Libellé arabe | Destination conservée | État |
|---|---|---|---|
| `6e50004` S1 bouton 1 | مجالات تدخله | `#missions` → S3 `6e5001c` | ✅ Ancre présente |
| `6e50005` S1 bouton 2 | مساهمته | `#contribution` → S4 `6e5001f` | ✅ Ancre présente |
| `6e50036` S6 carte 1 | اكتشف القطب | `/nos-poles/administration-et-gestion/` (P-03) | ⚠️ **Destination arabe inconnue** — à associer à P-03 AR |
| `6e5003b` S6 carte 2 | اكتشف القطب | `/nos-poles/formation-et-integration/` (P-04) | ⚠️ **Destination arabe inconnue** — à associer à P-04 AR |
| `6e50042` S7 bouton | تواصلوا معنا | `/contact/` (P-11) | ⚠️ **Destination arabe inconnue** — à associer à P-11 AR |

La page arabe doit être liée dans Polylang comme traduction de la page française `/nos-poles/animation-culturelle-et-sociale/`. Aucune URL, aucun slug ni aucun préfixe arabe n’a été inventé. Tant que les liens ne sont pas remplacés, ils mènent aux pages **françaises**.

## 7. Points de vigilance éditoriale (conservés, non corrigés)

| # | ID | Point | Traitement |
|---|---|---|---|
| V1 | `6e5002c`, `6e5002d` | Principe 4 « Fonctionnement collégial » | **Proposition à valider** ; statut inchangé par la traduction. |
| V2 | `6e50013` | « الرياضية » dans la carte Culture | Conservé : formulation validée de P-02, qui décrit les domaines de l’association et non une activité du pôle. Aucun domaine sportif distinct n’a été ajouté. |
| V3 | `6e5000d` §3, `6e5001e` §3 | Formulations relatives au Bureau exécutif, reprises de P-02/P-03 | Écart statutaire signalé dans le relevé ; **non corrigé** par l’intégrateur. |
| V4 | — | Propositions traduites | Elles **restent des propositions** ; aucun reclassement. |

### Écarts de cohérence observés dans le texte fourni (intégrés tels quels, pour information)

| # | ID | Constat |
|---|---|---|
| E1 | `6e50036`, `6e5003b` | Le bouton « اكتشف القطب » diffère de « اكتشف هذا القطب » utilisé en P-01, P-03 et P-04. |
| E2 | `6e50027` | La formulation de Solidarité « تنمية روح المساعدة المتبادلة والعمل التطوعي والتعاون » est une 3ᵉ variante. En P-02/P-03 : « تنمية التآزر… » ; en P-04 : « تنمية روح التعاون… والتكافل ». |
| E3 | `6e5001d` | « مساهمة أفقية » combine le أفقي de P-03 et le مساهمة de P-04. |
| E4 | toute la page | Le terme النظام الأساسي est cohérent avec P-04, mais P-02 et P-03 emploient القانون الأساسي. |
| E5 | `6e50003` | « يتولى » traduit « Il porte » ; P-02, P-03 et P-04 emploient « يُعنى » pour la même phrase française. |
| E6 | `6e50041` | « تبادل الخبرات » est plus précis que le français (« possibilités d’échange »), comme en P-04. |
| E7 | 13 widgets | Les textes ont été fournis sans `<p>`. Ils ont été enveloppés dans `<p>…</p>` comme la source, sans modifier leur contenu. Les deux paragraphes du texte S1 sont placés dans les deux `<p>` du widget source. |

## 8. Réglages manuels et limites

1. **Import :** Elementor → Modèles → Importer, puis insertion dans une nouvelle page.
2. **Polylang :** assigner la page à l’Arabe et la lier à la page française P-05.
3. **Liens :** remplacer les 3 cibles de la section 6.
4. **Image :** remplacer l’image de substitution et renseigner un texte alternatif arabe. Il est vide dans la source et aucun texte n’a été inventé.
5. **Classification :** reporter les 45 blocs du relevé P-05 sur le tableau de la section 10.
6. **Limites :** tous les contrôles sont statiques. L’interprétation de `align: right`, le rendu RTL, le comportement mobile et les thèmes Astra **n’ont pas été testés**.

Aucune modification d’Astra, d’Elementor (couleurs et polices globales), des en-têtes et pieds de page, des menus, de Polylang ou du SEO global. Rien n’a été importé ni publié. P-03 et P-04 n’ont pas été modifiés.

## 9. Métadonnées SEO proposées (non injectées — propositions non validées)

| Champ | Proposition |
|---|---|
| Titre SEO | قطب التنشيط الثقافي والاجتماعي \| جمعية أمل شباب التقدم |
| Méta-description | قطب التنشيط الثقافي والاجتماعي بجمعية أمل شباب التقدم: توجهات في مجالات الثقافة والتنشيط والمشاركة الاجتماعية باعتبارها فضاءات للقاء والمشاركة وتعزيز الروابط المجتمعية. |
| Slug (**proposition non validée**) | `قطب-التنشيط-الثقافي-والاجتماعي` (alternative latine : `animation-culturelle-et-sociale-ar`) |

Ces propositions reprennent uniquement des formulations fournies. Elles n’annoncent aucune activité, offre ni inscription.

## 10. Tableau de correspondance (68 éléments)

L’ID arabe est identique à l’ID source. **38 textes visibles** (16 titres, 17 éditeurs de texte, 5 boutons) : **38/38 intégrés, 0 oublié**. Le HTML est affiché échappé.

| # | ID source (= ID arabe) | Section | Type | `_title` | Contenu français d’origine | Contenu arabe intégré | État de traduction | Catégorie éditoriale | Note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `6e5000b` | S1 | container | S1 — Bannière | — | — | Sans texte visible | — |  |
| 2 | `6e5000a` | S1 | container | S1 · Ligne 2 colonnes | — | — | Sans texte visible | — |  |
| 3 | `6e50007` | S1 | container | S1 · Colonne texte | — | — | Sans texte visible | — |  |
| 4 | `6e50001` | S1 | heading | S1 · H1 | Pôle Animation Culturelle et Sociale | قطب التنشيط الثقافي والاجتماعي | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 5 | `6e50002` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un pôle qui valorise la culture, les activités sociales et les initiatives collectives comme espaces de rencontre, de participation et de lien communautaire.&lt;/p&gt; | &lt;p&gt;قطب يثمن الثقافة والأنشطة الاجتماعية والمبادرات الجماعية باعتبارها فضاءات للقاء والمشاركة وتعزيز الروابط المجتمعية.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 6 | `6e50003` | S1 | text-editor | S1 · Texte | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt;<br>&lt;p&gt;Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يتولى هذا القطب التوجهات المرتبطة بالثقافة والتنشيط والمشاركة الاجتماعية.&lt;/p&gt;<br>&lt;p&gt;تندرج مجالات تدخله ضمن التوجهات النظامية للجمعية.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis | §1 et §2 fournis séparément sans balise ; placés dans deux &lt;p&gt; comme la source |
| 7 | `6e50006` | S1 | container | S1 · Boutons | — | — | Sans texte visible | — |  |
| 8 | `6e50004` | S1 | button | S1 · Bouton 1 → ancre #missions | Ses domaines d&#x27;intervention | مجالات تدخله | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 9 | `6e50005` | S1 | button | S1 · Bouton 2 → ancre #contribution | Sa contribution | مساهمته | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 10 | `6e50009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | Sans texte visible | — |  |
| 11 | `6e50008` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image de substitution conservée | — |  |
| 12 | `6e5000e` | S2 | container | S2 — Présentation | — | — | Sans texte visible | — |  |
| 13 | `6e5000c` | S2 | heading | S2 · H2 | Un pôle au service de la culture et de la participation sociale | قطب في خدمة الثقافة والمشاركة الاجتماعية | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 14 | `6e5000d` | S2 | text-editor | S2 · Texte (3 paragraphes) | &lt;p&gt;Le Pôle Animation Culturelle et Sociale est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt;<br>&lt;p&gt;Son action se rattache à la vocation de l&#x27;association, qui a pour but de promouvoir des activités de développement, culturelles, sociales et sportives qui profitent à la jeunesse de Rabat.&lt;/p&gt;<br>&lt;p&gt;Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale.&lt;/p&gt; | &lt;p&gt;يُعد قطب التنشيط الثقافي والاجتماعي أحد الأقطاب الثلاثة المنصوص عليها في النظام الأساسي لجمعية أمل شباب التقدم. ويتولى التوجهات المرتبطة بالثقافة والتنشيط والمشاركة الاجتماعية.&lt;/p&gt;<br>&lt;p&gt;ويرتبط عمله برسالة الجمعية الرامية إلى النهوض بالأنشطة التنموية والثقافية والاجتماعية والرياضية التي تعود بالنفع على شباب الرباط.&lt;/p&gt;<br>&lt;p&gt;وطبقًا للنظام الأساسي، يخضع تنظيم أقطاب العمل وتتبع تنفيذ البرامج لإشراف المكتب التنفيذي، المنتخب من طرف الجمع العام.&lt;/p&gt; | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis | §3 : formulation Bureau exécutif reprise de P-02/P-03 — écart statutaire signalé par le relevé, non corrigé |
| 15 | `6e5001c` | S3 | container | S3 — Trois domaines d&#x27;intervention (ancre #missions) | — | — | Ancre `#missions` conservée | — |  |
| 16 | `6e50011` | S3 | container | S3 · En-tête | — | — | Sans texte visible | — |  |
| 17 | `6e5000f` | S3 | heading | S3 · H2 | Trois domaines d&#x27;intervention | ثلاثة مجالات للتدخل | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 18 | `6e50010` | S3 | text-editor | S3 · Introduction | &lt;p&gt;Les activités du pôle s&#x27;organisent autour de trois domaines complémentaires.&lt;/p&gt; | &lt;p&gt;تنتظم أنشطة القطب حول ثلاثة مجالات متكاملة.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 19 | `6e5001b` | S3 | container | S3 · Grille des 3 domaines | — | — | Sans texte visible | — |  |
| 20 | `6e50014` | S3 | container | S3 · Domaine 1 — Culture | — | — | Sans texte visible | — |  |
| 21 | `6e50012` | S3 | heading | S3 · H3 domaine 1 | Culture | الثقافة | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 22 | `6e50013` | S3 | text-editor | S3 · Texte domaine 1 | &lt;p&gt;La promotion des activités culturelles, artistiques, cinématographiques et sportives fait partie des domaines d&#x27;intervention prévus par les statuts. Ces activités sont envisagées comme des espaces d&#x27;expression, d&#x27;apprentissage, de rencontre et de participation.&lt;/p&gt; | &lt;p&gt;يُعد النهوض بالأنشطة الثقافية والفنية والسينمائية والرياضية من مجالات تدخل الجمعية المنصوص عليها في نظامها الأساسي. وتُعتبر هذه الأنشطة فضاءات للتعبير والتعلم واللقاء والمشاركة.&lt;/p&gt; | Intégré tel que fourni | **Validé — repris (P-02)** — indiqué par le brief | « الرياضية » conservé : domaines de l’association, pas activité propre du pôle |
| 23 | `6e50017` | S3 | container | S3 · Domaine 2 — Animation | — | — | Sans texte visible | — |  |
| 24 | `6e50015` | S3 | heading | S3 · H3 domaine 2 | Animation | التنشيط | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 25 | `6e50016` | S3 | text-editor | S3 · Texte domaine 2 | &lt;p&gt;L&#x27;animation désigne les initiatives collectives que l&#x27;association envisage comme des espaces de rencontre, de participation et de lien communautaire.&lt;/p&gt; | &lt;p&gt;يشير التنشيط إلى المبادرات الجماعية التي تتوخاها الجمعية باعتبارها فضاءات للقاء والمشاركة وتعزيز الروابط المجتمعية.&lt;/p&gt; | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 26 | `6e5001a` | S3 | container | S3 · Domaine 3 — Participation sociale | — | — | Sans texte visible | — |  |
| 27 | `6e50018` | S3 | heading | S3 · H3 domaine 3 | Participation sociale | المشاركة الاجتماعية | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 28 | `6e50019` | S3 | text-editor | S3 · Texte domaine 3 | &lt;p&gt;La participation sociale renvoie à l&#x27;implication des personnes dans la vie collective. Les statuts prévoient de créer un esprit de coopération et de solidarité au sein de la société civile.&lt;/p&gt; | &lt;p&gt;تشير المشاركة الاجتماعية إلى انخراط الأفراد في الحياة الجماعية. وينص النظام الأساسي على ترسيخ روح التعاون والتضامن داخل المجتمع المدني.&lt;/p&gt; | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 29 | `6e5001f` | S4 | container | S4 — Contribution transversale (ancre #contribution) | — | — | Ancre `#contribution` conservée | — |  |
| 30 | `6e5001d` | S4 | heading | S4 · H2 | Une contribution transversale aux autres pôles | مساهمة أفقية مع القطبين الآخرين | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 31 | `6e5001e` | S4 | text-editor | S4 · Texte (3 paragraphes) | &lt;p&gt;La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités.&lt;/p&gt;<br>&lt;p&gt;Les espaces de rencontre et les initiatives collectives rejoignent les orientations d&#x27;apprentissage et d&#x27;intégration portées par le Pôle Formation et Intégration, tandis que le Pôle Administration et Gestion contribue à l&#x27;organisation et aux moyens nécessaires à leur conduite.&lt;/p&gt;<br>&lt;p&gt;Cette articulation s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;لا تقتصر مساهمة القطب على مجال تدخله الخاص، بل تسهم أيضًا في تهيئة الظروف التي يضطلع فيها القطبان النظاميان الآخران بأنشطتهما.&lt;/p&gt;<br>&lt;p&gt;تلتقي فضاءات اللقاء والمبادرات الجماعية مع التوجهات المتعلقة بالتعلم والإدماج التي يتولاها قطب التكوين والإدماج، في حين يساهم قطب الإدارة والتسيير في التنظيم وتوفير الوسائل اللازمة لتنفيذها.&lt;/p&gt;<br>&lt;p&gt;ويتم هذا التنسيق في الإطار الذي يحدده النظام الأساسي، حيث يتولى المكتب التنفيذي الإشراف على تنظيم اللجان وأقطاب العمل، فضلًا عن تتبع تنفيذ البرامج المعتمدة.&lt;/p&gt; | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis | §3 : formulation Bureau exécutif reprise de P-02/P-03 — écart statutaire signalé par le relevé, non corrigé |
| 32 | `6e50030` | S5 | container | S5 — Principes de fonctionnement | — | — | Sans texte visible | — |  |
| 33 | `6e50022` | S5 | container | S5 · En-tête | — | — | Sans texte visible | — |  |
| 34 | `6e50020` | S5 | heading | S5 · H2 | Les principes qui guident son fonctionnement | المبادئ التي توجه سير عمل القطب | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 35 | `6e50021` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;يندرج عمل القطب ضمن المبادئ التي توجه التزام الجمعية.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 36 | `6e5002f` | S5 | container | S5 · Grille des 4 principes | — | — | Sans texte visible | — |  |
| 37 | `6e50025` | S5 | container | S5 · Principe 1 — Responsabilité | — | — | Sans texte visible | — |  |
| 38 | `6e50023` | S5 | heading | S5 · H3 principe 1 | Responsabilité | المسؤولية | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 39 | `6e50024` | S5 | text-editor | S5 · Texte principe 1 | &lt;p&gt;Inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;ترسيخ الالتزام ضمن نهج جاد وبنّاء.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 40 | `6e50028` | S5 | container | S5 · Principe 2 — Solidarité | — | — | Sans texte visible | — |  |
| 41 | `6e50026` | S5 | heading | S5 · H3 principe 2 | Solidarité | التضامن | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 42 | `6e50027` | S5 | text-editor | S5 · Texte principe 2 | &lt;p&gt;Développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;تنمية روح المساعدة المتبادلة والعمل التطوعي والتعاون.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 43 | `6e5002b` | S5 | container | S5 · Principe 3 — Initiative | — | — | Sans texte visible | — |  |
| 44 | `6e50029` | S5 | heading | S5 · H3 principe 3 | Initiative | المبادرة | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 45 | `6e5002a` | S5 | text-editor | S5 · Texte principe 3 | &lt;p&gt;Valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;تثمين المواهب والأفكار والقدرات على العمل والمبادرة.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 46 | `6e5002e` | S5 | container | S5 · Principe 4 — Fonctionnement collégial | — | — | Sans texte visible | — |  |
| 47 | `6e5002c` | S5 | heading | S5 · H3 principe 4 | Fonctionnement collégial | التسيير الجماعي | Intégré tel que fourni | **Proposition à valider** — indiqué par le brief | Principe 4 |
| 48 | `6e5002d` | S5 | text-editor | S5 · Texte principe 4 | &lt;p&gt;Les orientations générales relèvent de l&#x27;Assemblée générale, leur supervision du Bureau exécutif, et les commissions contribuent à l&#x27;étude des programmes et au suivi des activités relevant de leurs domaines de travail.&lt;/p&gt; | &lt;p&gt;تعود التوجهات العامة إلى الجمع العام، ويضطلع المكتب التنفيذي بالإشراف عليها، فيما تساهم اللجان في دراسة البرامج وتتبع الأنشطة المرتبطة بمجالات عملها.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | **Proposition à valider** — indiqué par le brief | Principe 4 |
| 49 | `6e5003f` | S6 | container | S6 — Les deux autres pôles | — | — | Sans texte visible | — |  |
| 50 | `6e50033` | S6 | container | S6 · En-tête | — | — | Sans texte visible | — |  |
| 51 | `6e50031` | S6 | heading | S6 · H2 | Les deux autres pôles | القطبان الآخران | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 52 | `6e50032` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires.&lt;/p&gt; | &lt;p&gt;يقوم تنظيم الجمعية على ثلاثة أقطاب نظامية متكاملة.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 53 | `6e5003e` | S6 | container | S6 · Grille des 2 pôles | — | — | Sans texte visible | — |  |
| 54 | `6e50038` | S6 | container | S6 · Carte 1 — Pôle Administration et Gestion → P-03 | — | — | Sans texte visible | — |  |
| 55 | `6e50034` | S6 | heading | S6 · H3 carte 1 | Pôle Administration et Gestion | قطب الإدارة والتسيير | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 56 | `6e50035` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt; | &lt;p&gt;يساهم في تنظيم البنية الجمعوية وضمان سير عملها.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 57 | `6e50037` | S6 | container | S6 · Bouton carte 1 | — | — | Sans texte visible | — |  |
| 58 | `6e50036` | S6 | button | S6 · Bouton carte 1 → P-03 | Découvrir le pôle | اكتشف القطب | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 59 | `6e5003d` | S6 | container | S6 · Carte 2 — Pôle Formation et Intégration → P-04 | — | — | Sans texte visible | — |  |
| 60 | `6e50039` | S6 | heading | S6 · H3 carte 2 | Pôle Formation et Intégration | قطب التكوين والإدماج | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 61 | `6e5003a` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt; | &lt;p&gt;يندرج ضمن التوجهات المتعلقة بالتعلم وتنمية الكفاءات والإدماج.&lt;/p&gt; | Intégré tel que fourni (`<p>` ajouté) | Non déterminée — relevé P-05 non transmis |  |
| 62 | `6e5003c` | S6 | container | S6 · Bouton carte 2 | — | — | Sans texte visible | — |  |
| 63 | `6e5003b` | S6 | button | S6 · Bouton carte 2 → P-04 | Découvrir le pôle | اكتشف القطب | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 64 | `6e50044` | S7 | container | S7 — Appel à l’action | — | — | Sans texte visible | — |  |
| 65 | `6e50040` | S7 | heading | S7 · H2 | Une question sur les orientations de ce pôle ? | هل لديكم استفسار حول توجهات هذا القطب؟ | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 66 | `6e50041` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez en savoir plus sur les orientations du Pôle Animation Culturelle et Sociale, échanger avec l&#x27;Association Amal Chabab Takaddoum ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;هل ترغبون في معرفة المزيد عن توجهات قطب التنشيط الثقافي والاجتماعي، أو التواصل مع جمعية أمل شباب التقدم، أو بحث إمكانية التعاون؟&lt;/p&gt;<br>&lt;p&gt;لنتواصل معًا لتحديد إمكانيات تبادل الخبرات.&lt;/p&gt; | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
| 67 | `6e50043` | S7 | container | S7 · Bouton | — | — | Sans texte visible | — |  |
| 68 | `6e50042` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | تواصلوا معنا | Intégré tel que fourni | Non déterminée — relevé P-05 non transmis |  |
