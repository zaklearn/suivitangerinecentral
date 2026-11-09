# P-01 Home Page — American English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**
Deliverable: `P01_Accueil_Amal_Chabab_Takaddoum_English_Elementor.json`
Source: `P01_Accueil_Amal_Chabab_Takaddoum_Elementor(1).json`. SHA-256 `4a575b06…a4ba32cf`. The source was **not modified**; its hash is identical before and after generation.
English content: **integrated exactly as supplied** in the task prompt. It was not retranslated or rewritten.

---

## 0. Checks performed vs. checks requiring a real import

| Check | Method | Status |
|---|---|---|
| JSON syntax | Python `json.load` | ✅ Performed |
| 7 sections, same order | Tree comparison source ↔ English | ✅ Performed |
| 68 elements: hierarchy, types, `isInner`, child counts | Recursive node-by-node comparison | ✅ Performed (68/68) |
| Settings unchanged except public text | Key-by-key diff of every `settings` object | ✅ Performed. Only these differ: `title` ×9, `editor` ×11, `text` ×9, and the `text` of the 8 `icon_list` items. No other key changed, including links. |
| Identifier uniqueness | Count | ✅ Performed (76/76 unique) |
| No collision with the other project templates | Set intersection with the 6 other French templates and the 6 Arabic templates | ✅ Performed (0) |
| All supplied English content integrated | Every targeted ID consumed at build time | ✅ Performed (30 widget fields + 8 list items = 38/38) |
| No French public-facing text left | Search for French accented characters and common French words in all public text fields | ✅ Performed (0) |
| Image placeholders | URL check | ✅ Performed (2/2, URLs unchanged) |
| Reserved areas hidden | `hide_desktop/tablet/mobile` | ✅ Performed (2/2, still empty and hidden) |
| Page settings | `page_settings` | ✅ Performed |
| Free widgets only | List of `widgetType` | ✅ Performed |
| **Import into Elementor** | — | ⛔ **Not performed** |
| **Visual rendering (desktop / tablet / mobile), horizontal overflow** | — | ⛔ **Not performed** |
| **Polylang association, link behavior** | — | ⛔ **Not performed** |

## 1. Structure of the seven sections

| # | Section (`_title`, kept) | Background | Content |
|---|---|---|---|
| S1 | S1 — Bannière principale | `#F4F6F6` | 2-column row (58% / 38%): H1, intro text and 2 buttons on one side, image placeholder on the other |
| S2 | S2 — Présentation | `#FFFFFF` | 2-column row (55% / 41%): H2, text and button on one side, image placeholder on the other |
| S3 | S3 — Nos pôles | `#F4F6F6` | Centered header (H2 + intro) and a grid of 3 cards (H3 + text + button); 33% → 48% → 100% |
| S4 | S4 — Projets et programmes | `#FFFFFF` | Centered editorial block (H2 + text + button) and a **hidden reserved area** |
| S5 | S5 — Actualités | `#F4F6F6` | Centered editorial block (H2 + text + button) and a **hidden reserved area** |
| S6 | S6 — Appel à l’action | `#152A33` | Centered H2, text and button |
| S7 | S7 — Bloc pied de page | `#152A33` | Name, signature, 2 lists of 4 links, divider and legal notice |

## 2. Number and types of elements

| Type | Source | English |
|---|---|---|
| `container` | 33 | 33 |
| `heading` | 10 | 10 |
| `text-editor` | 11 | 11 |
| `button` | 9 | 9 |
| `image` | 2 | 2 |
| `icon-list` (4 items each) | 2 | 2 |
| `divider` | 1 | 1 |
| **Total** | **68** | **68** |

## 3. Identifiers

**Rule: the 76 source identifiers are kept unchanged. No IDs were regenerated.** This covers the 68 element IDs and the 8 `icon_list` item `_id`s.
Rationale: requirement 5.3 calls for new IDs only if duplication requires them. It does not: Elementor IDs only need to be unique within a page, because generated CSS is scoped by the WordPress post ID. Keeping the IDs gives a 1-to-1 FR ↔ EN correspondence with no mapping table. This is the same rule used for the Arabic P-03, P-04 and P-05 templates.

Results:
- Uniqueness within the file: **76/76**.
- Shared with the French P-01: **76/76** (intended).
- Shared with the Arabic P-01 (`3a2…`), the other French templates and the other Arabic templates: **0**.

## 4. Page settings

| Key | Source | English |
|---|---|---|
| `version` / `type` | `0.4` / `page` | identical |
| `page_settings.template` | `elementor_header_footer` | identical ✅ |
| `page_settings.hide_title` | `yes` | identical ✅ |
| `title` (template name, visible in the admin library only) | `P-01 Accueil — Association Amal Chabab Takaddoum` | `P-01 Accueil (EN) — Association Amal Chabab Takaddoum` |

## 5. LTR presentation

- **No direction or alignment property was added or changed.** The French source is already LTR, so its layout carries over unchanged:
  - The **11 centered** headings and texts stay centered (S3–S7).
  - The **10 headings and texts with no alignment set** inherit start alignment, which is left in an LTR document (S1, S2, S3 cards).
  - Column order is unchanged: text on the left, image on the right in S1 and S2. Cards are ordered left to right, and the S7 lists follow the source order.
- No `dir` attribute and no unknown Elementor property was introduced.
- **Manual check:** in Polylang → Languages, the English language must use **left-to-right** text direction. This is the default for `en_US`.

## 6. Responsive settings

All values are **preserved without adaptation**:
- **Typography** (desktop/tablet/mobile): H1 44/38/30; H2 34/30/26; H3 20/20/19; texts 18/17/16, 17/17/16, 16/16/15; buttons 16 and 15.
- **Widths:** column widths (58/38, 55/41, 33/48/100, S7 lists 30/45/100) and custom text widths (720/780/760 px, then 100% on mobile).
- **Spacing:** section paddings (96–100 / 72 / 56), card and button paddings, and `flex_gap`.
- **Wrapping:** `flex_wrap` and `flex_direction_mobile: column`.

Point to watch: the English H1 has 84 characters, longer than the French one (61). Check line breaks at 30 px on mobile and 38 px on tablet. Button labels such as “Explore Our Projects and Programs” and “Learn More About the Association” should also be checked on mobile, since wrapping is enabled in their containers.

## 7. Internal links requiring manual Polylang association

No approved English URLs were supplied. **All French source targets are kept unchanged**, and no English slugs or translation URLs were invented. Until they are replaced, these links lead to the **French** pages.

| # | Section | Element | English label | Kept target (FR) | English page to associate | Status |
|---|---|---|---|---|---|---|
| 1 | S1 | Button `2a10003` | Discover the Association | `/l-association/` | About (EN) | ⚠️ Unknown |
| 2 | S1 | Button `2a10004` | Explore Our Initiatives | `/projets-et-programmes/` | Projects and Programs (EN) | ⚠️ Unknown |
| 3 | S2 | Button `2a1000d` | Learn More About the Association | `/l-association/` | About (EN) | ⚠️ Unknown |
| 4 | S3 | Button `2a10019` | Explore This Area | `/nos-poles/administration-et-gestion/` | Administration and Management (EN) | ⚠️ Unknown |
| 5 | S3 | Button `2a1001e` | Explore This Area | `/nos-poles/formation-et-integration/` | Training and Integration (EN) | ⚠️ Unknown |
| 6 | S3 | Button `2a10023` | Explore This Area | `/nos-poles/animation-culturelle-et-sociale/` | Cultural and Social Activities (EN) | ⚠️ Unknown |
| 7 | S4 | Button `2a1002a` | Explore Our Projects and Programs | `/projets-et-programmes/` | Projects and Programs (EN) | ⚠️ Unknown |
| 8 | S5 | Button `2a10031` | View All Updates | `/actualites/` | News and Updates (EN) | ⚠️ Unknown |
| 9 | S6 | Button `2a10038` | Contact Us | `/contact/` | Contact (EN) | ⚠️ Unknown |
| 10 | S7 | List 1 › 1 `2a1003d` | About the Association | `/l-association/` | About (EN) | ⚠️ Unknown |
| 11 | S7 | List 1 › 2 `2a1003e` | Our Areas of Work | `/nos-poles/` | Areas of Work (EN) | ⚠️ Unknown |
| 12 | S7 | List 1 › 3 `2a1003f` | Projects and Programs | `/projets-et-programmes/` | Projects and Programs (EN) | ⚠️ Unknown |
| 13 | S7 | List 1 › 4 `2a10040` | News and Updates | `/actualites/` | News and Updates (EN) | ⚠️ Unknown |
| 14 | S7 | List 2 › 1 `2a10043` | Partners | `/partenaires/` | Partners (EN) | ⚠️ Unknown |
| 15 | S7 | List 2 › 2 `2a10044` | Achievements | `/realisations/` | Achievements (EN) | ⚠️ Unknown |
| 16 | S7 | List 2 › 3 `2a10045` | Publications and Resources | `/publications-et-ressources/` | Publications and Resources (EN) | ⚠️ Unknown |
| 17 | S7 | List 2 › 4 `2a10046` | Contact | `/contact/` | Contact (EN) | ⚠️ Unknown |

Relative URLs do not include any Polylang language prefix the site may use.

## 8. Remaining manual configuration and limitations

1. **Import:** Elementor → Templates → Import, then insert the template into a new page.
2. **Polylang:** assign the page to English and link it as the translation of the French home page. If the French page is the static front page, Polylang will serve the English translation as the English front page.
3. **Links:** replace the 17 targets in section 7 once the English pages exist.
4. **Images:** replace the 2 placeholders and add English alt text. Alt text is empty in the source, and none was invented.
5. **S1 bold lead-in:** in the French source, the first S1 paragraph is wrapped in `<strong>`. The supplied English text has no `<strong>`, and it was integrated as supplied. If the lead-in should stay bold, add it manually: `<p><strong>Working for young people, solidarity, and social development in Rabat.</strong></p>`.
6. **Duplicate footer risk:** S7 is kept because it is part of the source. With `elementor_header_footer`, the Astra footer is also displayed, so the page may show two footers. Check visually.
7. **Hidden reserved areas** (S4, S5): kept empty and hidden. Do not enable them until real content exists.
8. **Internal labels** (`_title` in the Elementor Navigator): intentionally kept in French, as allowed by criterion 6.
9. **Limitations:** all checks are static. Rendering, line wrapping and link behavior depend on the installed Elementor, Astra and Polylang setup and were **not tested** in WordPress.

**Global settings:** no changes to Astra, global Elementor colors or fonts, header or footer templates, menus, Polylang configuration or global SEO. Nothing was imported, published or deployed. The French version was not modified.

### Editorial notes (supplied text integrated as is — for information)

| # | ID | Note |
|---|---|---|
| N1 | `2a10001` | “for a **More Inclusive** and Supportive Community” goes slightly beyond the French “pour une société solidaire”, which has no “inclusive”. |
| N2 | `2a1000b` | “**Open to Collaboration**” differs from the French “tournée vers l’action” (action-oriented). |
| N3 | `2a1000c` | The supplied text adds “nonprofit” (FR: “association marocaine”). This is a natural U.S. usage that does not change the meaning. |
| N4 | `2a10017`, `2a1001c`, `2a10021` | The three “pôles” are rendered as “areas of work” and named without the word “Pôle”, for example “Administration and Management”. Future English pages (P-03 to P-05) should use the same names. |

No corrections were made; these are for the supervisor’s review.

## 9. Proposed SEO metadata (not injected — **proposals pending supervisor approval**)

| Field | Proposal |
|---|---|
| SEO title | Association Amal Chabab Takaddoum \| Youth, Solidarity & Community in Rabat |
| Meta description | Association Amal Chabab Takaddoum is a Moroccan nonprofit based in Rabat, developing community-based initiatives in education, training, culture, and social participation. |
| Slug (**unapproved proposal**) | `home` (if not set as the English front page); otherwise the URL is determined by Polylang’s language root |

These proposals use wording from the supplied content only.

## 10. Translation correspondence table (68 elements + 8 list items)

The English ID is the same as the source ID (section 3). Public-facing text covered: 10 headings, 11 text editors, 9 buttons and 8 list items, for **38/38 integrated, none missing**. The S7 association name heading (“Association Amal Chabab Takaddoum”) is identical in both languages, so only 9 heading values actually differ. HTML is shown escaped.

| # | Source ID (= EN ID) | Section | Widget type | Internal label (`_title`, kept in French) | Original French content | Integrated American English content | Translation status |
|---|---|---|---|---|---|---|---|
| 1 | `2a1000a` | S1 | container | S1 — Bannière principale | — | — | No public text |
| 2 | `2a10009` | S1 | container | S1 · Ligne 2 colonnes | — | — | No public text |
| 3 | `2a10006` | S1 | container | S1 · Colonne texte | — | — | No public text |
| 4 | `2a10001` | S1 | heading | S1 · H1 | Amal Chabab Takaddoum : agir ensemble pour une société solidaire | Association Amal Chabab Takaddoum: Together for a More Inclusive and Supportive Community | Integrated as supplied |
| 5 | `2a10002` | S1 | text-editor | S1 · Texte d’introduction | &lt;p&gt;&lt;strong&gt;Une association engagée pour la jeunesse, la solidarité et le développement social à Rabat.&lt;/strong&gt;&lt;/p&gt;<br>&lt;p&gt;Depuis Rabat, l’Association Amal Chabab Takaddoum développe une action associative autour de l’éducation, de la formation, de la culture et de la participation sociale.&lt;/p&gt;<br>&lt;p&gt;À travers ses pôles d’intervention, elle porte une ambition : encourager les initiatives, renforcer les solidarités et contribuer au développement de la communauté.&lt;/p&gt; | &lt;p&gt;Working for young people, solidarity, and social development in Rabat.&lt;/p&gt;<br>&lt;p&gt;Based in Rabat, Association Amal Chabab Takaddoum develops community-based initiatives in education, training, culture, and social participation.&lt;/p&gt;<br>&lt;p&gt;Through its areas of work, the association seeks to encourage initiatives, strengthen solidarity, and contribute to community development.&lt;/p&gt; | Integrated as supplied |
| 6 | `2a10005` | S1 | container | S1 · Boutons | — | — | No public text |
| 7 | `2a10003` | S1 | button | S1 · Bouton 1 → L’association | Découvrir l’association | Discover the Association | Integrated as supplied |
| 8 | `2a10004` | S1 | button | S1 · Bouton 2 → Projets &amp; Programmes | Explorer nos actions | Explore Our Initiatives | Integrated as supplied |
| 9 | `2a10008` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | No public text |
| 10 | `2a10007` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image placeholder preserved (URL unchanged) |
| 11 | `2a10013` | S2 | container | S2 — Présentation | — | — | No public text |
| 12 | `2a10012` | S2 | container | S2 · Ligne 2 colonnes | — | — | No public text |
| 13 | `2a1000f` | S2 | container | S2 · Colonne texte | — | — | No public text |
| 14 | `2a1000b` | S2 | heading | S2 · H2 | Une dynamique associative tournée vers l’action | A Dynamic Community Organization, Open to Collaboration | Integrated as supplied |
| 15 | `2a1000c` | S2 | text-editor | S2 · Texte | &lt;p&gt;L’Association Amal Chabab Takaddoum est une association marocaine basée à Rabat. Son action s’inscrit dans une démarche de développement éducatif, culturel, social et sportif, avec une attention particulière portée à la jeunesse.&lt;/p&gt;<br>&lt;p&gt;Convaincue de l’importance de l’engagement collectif, l’association développe ses initiatives autour de la solidarité, de la participation et de l’accompagnement. Elle entend favoriser les opportunités d’apprentissage, d’épanouissement et d’implication dans la vie sociale.&lt;/p&gt; | &lt;p&gt;Association Amal Chabab Takaddoum is a Moroccan nonprofit association based in Rabat. Its work is guided by an approach to educational, cultural, social, and sports development, with particular attention to issues affecting young people.&lt;/p&gt;<br>&lt;p&gt;Believing in the importance of collective action, the association develops its initiatives around solidarity, participation, and support. It also seeks to expand opportunities for learning, personal development, and active involvement in social life.&lt;/p&gt; | Integrated as supplied |
| 16 | `2a1000e` | S2 | container | S2 · Bouton | — | — | No public text |
| 17 | `2a1000d` | S2 | button | S2 · Bouton → L’association | En savoir plus sur l’association | Learn More About the Association | Integrated as supplied |
| 18 | `2a10011` | S2 | container | S2 · Colonne visuel (image à remplacer) | — | — | No public text |
| 19 | `2a10010` | S2 | image | S2 · IMAGE À REMPLACER — vie associative | — | — | Image placeholder preserved (URL unchanged) |
| 20 | `2a10027` | S3 | container | S3 — Nos pôles | — | — | No public text |
| 21 | `2a10016` | S3 | container | S3 · En-tête | — | — | No public text |
| 22 | `2a10014` | S3 | heading | S3 · H2 | Trois pôles complémentaires, une même ambition | Three Complementary Areas of Work, One Shared Purpose | Integrated as supplied |
| 23 | `2a10015` | S3 | text-editor | S3 · Texte d’introduction | &lt;p&gt;Les activités de l’association s’organisent autour de trois pôles qui structurent son action et contribuent à la réalisation de ses objectifs.&lt;/p&gt; | &lt;p&gt;The association&#x27;s work is organized around three complementary areas that provide a structured framework for its activities and contribute to achieving its objectives.&lt;/p&gt; | Integrated as supplied |
| 24 | `2a10026` | S3 | container | S3 · Grille des 3 cartes | — | — | No public text |
| 25 | `2a1001b` | S3 | container | S3 · Carte 1 — Pôle Administration et Gestion | — | — | No public text |
| 26 | `2a10017` | S3 | heading | S3 · H3 carte 1 | Pôle Administration et Gestion | Administration and Management | Integrated as supplied |
| 27 | `2a10018` | S3 | text-editor | S3 · Texte carte 1 | &lt;p&gt;Un pôle dédié à l’organisation et à la coordination de la vie associative. Il contribue au suivi administratif et à la gestion des moyens nécessaires au fonctionnement de l’association.&lt;/p&gt; | &lt;p&gt;This area focuses on organizing and coordinating the association&#x27;s operations. It contributes to administrative follow-up and the management of the resources needed to support the association&#x27;s work.&lt;/p&gt; | Integrated as supplied |
| 28 | `2a1001a` | S3 | container | S3 · Bouton carte 1 | — | — | No public text |
| 29 | `2a10019` | S3 | button | S3 · Bouton carte 1 | Découvrir le pôle | Explore This Area | Integrated as supplied |
| 30 | `2a10020` | S3 | container | S3 · Carte 2 — Pôle Formation et Intégration | — | — | No public text |
| 31 | `2a1001c` | S3 | heading | S3 · H3 carte 2 | Pôle Formation et Intégration | Training and Integration | Integrated as supplied |
| 32 | `2a1001d` | S3 | text-editor | S3 · Texte carte 2 | &lt;p&gt;Un pôle orienté vers l’apprentissage, le développement des compétences et les initiatives favorisant l’intégration sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;This area focuses on learning, skills development, and initiatives that support social and professional integration.&lt;/p&gt; | Integrated as supplied |
| 33 | `2a1001f` | S3 | container | S3 · Bouton carte 2 | — | — | No public text |
| 34 | `2a1001e` | S3 | button | S3 · Bouton carte 2 | Découvrir le pôle | Explore This Area | Integrated as supplied |
| 35 | `2a10025` | S3 | container | S3 · Carte 3 — Pôle Animation Culturelle et Sociale | — | — | No public text |
| 36 | `2a10021` | S3 | heading | S3 · H3 carte 3 | Pôle Animation Culturelle et Sociale | Cultural and Social Activities | Integrated as supplied |
| 37 | `2a10022` | S3 | text-editor | S3 · Texte carte 3 | &lt;p&gt;Un pôle qui valorise la culture, les activités sociales et les initiatives collectives comme espaces de rencontre, de participation et de lien communautaire.&lt;/p&gt; | &lt;p&gt;This area promotes culture, social activities, and collective initiatives as opportunities for connection, participation, and stronger community ties.&lt;/p&gt; | Integrated as supplied |
| 38 | `2a10024` | S3 | container | S3 · Bouton carte 3 | — | — | No public text |
| 39 | `2a10023` | S3 | button | S3 · Bouton carte 3 | Découvrir le pôle | Explore This Area | Integrated as supplied |
| 40 | `2a1002e` | S4 | container | S4 — Projets et programmes | — | — | No public text |
| 41 | `2a1002c` | S4 | container | S4 · Bloc éditorial | — | — | No public text |
| 42 | `2a10028` | S4 | heading | S4 · H2 | Des actions concrètes au plus près des besoins | Practical Initiatives That Respond to Identified Needs | Integrated as supplied |
| 43 | `2a10029` | S4 | text-editor | S4 · Texte | &lt;p&gt;À travers ses projets et programmes, Amal Chabab Takaddoum met en œuvre des initiatives dans ses domaines d’intervention.&lt;/p&gt;<br>&lt;p&gt;Éducation, formation, accompagnement et animation : chaque initiative s’inscrit dans la volonté de répondre à des besoins identifiés et de favoriser la participation des personnes et des communautés.&lt;/p&gt;<br>&lt;p&gt;Découvrez les projets documentés et les programmes portés par l’association.&lt;/p&gt; | &lt;p&gt;Through its projects and programs, Association Amal Chabab Takaddoum works to carry out initiatives across its areas of work.&lt;/p&gt;<br>&lt;p&gt;Education, training, support, and community activities: each initiative reflects the association&#x27;s intention to respond to identified needs and encourage the participation of individuals and communities.&lt;/p&gt;<br>&lt;p&gt;Explore the documented projects and programs in which the association is involved.&lt;/p&gt; | Integrated as supplied |
| 44 | `2a1002b` | S4 | container | S4 · Bouton | — | — | No public text |
| 45 | `2a1002a` | S4 | button | S4 · Bouton → Projets &amp; Programmes | Voir nos projets et programmes | Explore Our Projects and Programs | Integrated as supplied |
| 46 | `2a1002d` | S4 | container | S4 · ZONE RÉSERVÉE — cartes de projets (masquée, à activer quand des fiches réelles existent) | — | — | Reserved area kept hidden (D/T/M) |
| 47 | `2a10035` | S5 | container | S5 — Actualités | — | — | No public text |
| 48 | `2a10033` | S5 | container | S5 · Bloc éditorial | — | — | No public text |
| 49 | `2a1002f` | S5 | heading | S5 · H2 | Suivre la vie associative et nos initiatives | Stay Connected with Our Community and Initiatives | Integrated as supplied |
| 50 | `2a10030` | S5 | text-editor | S5 · Texte | &lt;p&gt;Activités, événements, rencontres et nouvelles initiatives : retrouvez les actualités d’Amal Chabab Takaddoum et suivez les actions menées par l’association.&lt;/p&gt; | &lt;p&gt;Activities, events, meetings, and new initiatives: discover the latest updates from Association Amal Chabab Takaddoum and follow the work and initiatives carried out by the association.&lt;/p&gt; | Integrated as supplied |
| 51 | `2a10032` | S5 | container | S5 · Bouton | — | — | No public text |
| 52 | `2a10031` | S5 | button | S5 · Bouton → Actualités | Consulter toutes les actualités | View All Updates | Integrated as supplied |
| 53 | `2a10034` | S5 | container | S5 · ZONE RÉSERVÉE — articles WordPress réels (masquée, aucun article fictif) | — | — | Reserved area kept hidden (D/T/M) |
| 54 | `2a1003a` | S6 | container | S6 — Appel à l’action | — | — | No public text |
| 55 | `2a10036` | S6 | heading | S6 · H2 | Construisons ensemble des initiatives porteuses de sens | Let&#x27;s Build Meaningful Initiatives Together | Integrated as supplied |
| 56 | `2a10037` | S6 | text-editor | S6 · Texte | &lt;p&gt;Vous souhaitez découvrir nos activités, échanger avec notre équipe ou envisager une collaboration avec l’Association Amal Chabab Takaddoum ?&lt;/p&gt;<br>&lt;p&gt;Nous serons heureux d&#x27;échanger avec vous.&lt;/p&gt; | &lt;p&gt;Would you like to learn more about our activities, get in touch with our team, or explore opportunities to collaborate with Association Amal Chabab Takaddoum?&lt;/p&gt;<br>&lt;p&gt;We would be pleased to hear from you and exchange ideas.&lt;/p&gt; | Integrated as supplied |
| 57 | `2a10039` | S6 | container | S6 · Bouton | — | — | No public text |
| 58 | `2a10038` | S6 | button | S6 · Bouton → Contact | Nous contacter | Contact Us | Integrated as supplied |
| 59 | `2a1004c` | S7 | container | S7 — Bloc pied de page (contenu de page, pas un footer global) | — | — | No public text |
| 60 | `2a1003b` | S7 | heading | S7 · Nom de l’association | Association Amal Chabab Takaddoum | Association Amal Chabab Takaddoum | Integrated as supplied |
| 61 | `2a1003c` | S7 | text-editor | S7 · Signature | &lt;p&gt;Jeunesse · Éducation · Formation · Solidarité · Culture&lt;/p&gt; | &lt;p&gt;Youth · Education · Training · Solidarity · Culture&lt;/p&gt; | Integrated as supplied |
| 62 | `2a10049` | S7 | container | S7 · Liens (2 colonnes) | — | — | No public text |
| 63 | `2a10042` | S7 | container | S7 · Liens colonne 1 | — | — | No public text |
| 64 | `2a10041` | S7 | icon-list | S7 · Liens 1-4 | — | — | No public text |
| 65 | `2a1003d` | S7 | icon-list › item | link → /l-association/ | L’association | About the Association | Integrated as supplied (source link kept) |
| 66 | `2a1003e` | S7 | icon-list › item | link → /nos-poles/ | Nos pôles | Our Areas of Work | Integrated as supplied (source link kept) |
| 67 | `2a1003f` | S7 | icon-list › item | link → /projets-et-programmes/ | Projets et programmes | Projects and Programs | Integrated as supplied (source link kept) |
| 68 | `2a10040` | S7 | icon-list › item | link → /actualites/ | Actualités | News and Updates | Integrated as supplied (source link kept) |
| 69 | `2a10048` | S7 | container | S7 · Liens colonne 2 | — | — | No public text |
| 70 | `2a10047` | S7 | icon-list | S7 · Liens 5-8 | — | — | No public text |
| 71 | `2a10043` | S7 | icon-list › item | link → /partenaires/ | Partenaires | Partners | Integrated as supplied (source link kept) |
| 72 | `2a10044` | S7 | icon-list › item | link → /realisations/ | Réalisations | Achievements | Integrated as supplied (source link kept) |
| 73 | `2a10045` | S7 | icon-list › item | link → /publications-et-ressources/ | Publications et ressources | Publications and Resources | Integrated as supplied (source link kept) |
| 74 | `2a10046` | S7 | icon-list › item | link → /contact/ | Contact | Contact | Integrated as supplied (source link kept) |
| 75 | `2a1004a` | S7 | divider | S7 · Séparateur | — | — | No public text |
| 76 | `2a1004b` | S7 | text-editor | S7 · Mention légale | &lt;p&gt;© Association Amal Chabab Takaddoum — Tous droits réservés.&lt;/p&gt; | &lt;p&gt;© Association Amal Chabab Takaddoum — All rights reserved.&lt;/p&gt; | Integrated as supplied |
