# P-02 About the Association — American English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**
Deliverable: `P02_LAssociation_Amal_Chabab_Takaddoum_English_Elementor.json`
Source: `P02_LAssociation_Amal_Chabab_Takaddoum_Elementor.json` (SHA-256 `5c023191…ff64a001`). It was **not modified**: the hash is identical before and after generation.
Supplementary reference: `P02_LAssociation_Arabe_Rapport_Technique.md` (structure and link inventory only).
English content: **integrated exactly as supplied** in the task prompt. It was not retranslated or rewritten.

---

## 0. Checks performed vs. checks requiring a real import

| Check | Method | Status |
|---|---|---|
| JSON syntax | Python `json.load` | ✅ Performed |
| 7 sections, same order | Tree comparison, source ↔ English | ✅ Performed |
| 94 elements: hierarchy, types, `isInner`, child counts | Recursive node-by-node comparison | ✅ Performed (94/94) |
| Settings unchanged except public text | Key-by-key diff of every `settings` object | ✅ Performed. Only `title` (×23), `editor` (×24) and `text` (×4) differ. The heading “Initiative” is identical in both languages. Links, anchors, colors, typography and responsive values are unchanged. |
| Identifier uniqueness and non-reuse | Count, and intersection with the source | ✅ Performed. 94/94 unique; 0 French source IDs reused. |
| No collision with other project templates | Intersection with the 6 other French and 7 Arabic/English templates (14 files) | ✅ Performed (0) |
| All supplied English content integrated | Every targeted source ID consumed at build time | ✅ Performed (52/52) |
| No French public-facing text left | Search for French accented characters and common French words in all public text fields | ✅ Performed (0) |
| Anchors | `_element_id` values, and button targets ↔ anchors | ✅ Performed (2/2) |
| Image placeholders | URL and `alt` | ✅ Performed. 2/2 unchanged; `alt` empty. |
| Page settings | `page_settings` | ✅ Performed |
| Free widgets only | List of `widgetType` | ✅ Performed |
| **Import into Elementor** | — | ⛔ **Not performed** |
| **Visual rendering (desktop / tablet / mobile), overflow** | — | ⛔ **Not performed** |
| **Anchor scrolling; Polylang association; link behavior** | — | ⛔ **Not performed** |

## 1. Structure of the seven sections

| # | Section (`_title`, kept) | Background | Content |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | 2-column row (58% / 38%). Text column: H1, subtitle, text and 2 anchor buttons. Other column: image placeholder. |
| S2 | S2 — Identité | `#FFFFFF` | 2-column row (57% / 39%). Text column: H2 and a 4-paragraph text. Other column: image placeholder. |
| S3 | S3 — Mission et objectifs (anchor `#missions`) | `#F4F6F6` | Centered H2 and 5 objective cards (4 × 48% + 1 × 100%). |
| S4 | S4 — Valeurs | `#FFFFFF` | Centered header (H2 and intro) and 6 value cards (32% → 48% → 100%). |
| S5 | S5 — Organisation (anchor `#organisation`) | `#F4F6F6` | Centered header and 3 governance-body cards (33% → 48% → 100%). |
| S6 | S6 — Trois pôles | `#FFFFFF` | Centered header, 3 area cards with linked headings, and a general button. |
| S7 | S7 — Appel à l’action | `#152A33` | Centered H2, text and Contact button. |

## 2. Number and types of elements

| Type | Source | English |
|---|---|---|
| `container` | 40 | 40 |
| `heading` (1 H1, 6 H2, 17 H3) | 24 | 24 |
| `text-editor` | 24 | 24 |
| `button` | 4 | 4 |
| `image` | 2 | 2 |
| **Total** | **94** | **94** |

No element was added, removed, merged or moved.

## 3. Identifiers

**Rule (requirement 5.3, same approach as the Arabic P-02):** new identifiers were generated, and **no French source ID is reused**.
- **Format:** 7-character hexadecimal with the prefix `b8c`, from `b8c0001` to `b8c005e`.
- **Assignment:** IDs are given in depth-first tree order, so every parent-child relationship is preserved.
- **Uniqueness within the file:** **94/94**.
- **French source IDs reused:** **0**.
- **Collisions with other project templates:** **0**. This covers the French P-01, P-03, P-04, P-05, P-06 and P-11 and the Arabic P-01 to P-06 and P-11. The English P-01 is also included; it keeps the French P-01 IDs (`2a1…`).
- **Correspondence:** the full French ↔ English ID mapping is in section 10.

**Technical anchors are not identifiers and were kept exactly:** `missions` and `organisation`, on the S3 and S5 section containers.

## 4. Page settings

| Key | Source | English |
|---|---|---|
| `version` / `type` | `0.4` / `page` | identical |
| `page_settings.template` | `elementor_header_footer` | identical ✅ |
| `page_settings.hide_title` | `yes` | identical ✅ |
| `title` (template name, admin library only) | `P-02 L’association — Association Amal Chabab Takaddoum` | `P-02 L’association (EN) — Association Amal Chabab Takaddoum` |

## 5. LTR presentation

- **No direction or alignment property was added or changed.** The French source is already LTR:
  - the **9 centered** headings and texts stay centered (S3 H2; the S4, S5 and S6 headers; S7);
  - the **39 headings and texts with no alignment set** inherit start alignment, which is left in an LTR document (S1, S2 and all cards);
  - column and card order is unchanged: text on the left and image on the right in S1/S2, cards filling left to right.
- No `dir` attribute and no unknown Elementor property was introduced.
- **Manual check:** in Polylang → Languages, the English language should use left-to-right text direction (the default for `en_US`).

## 6. Responsive settings

All values are **preserved without adaptation**:
- **Typography** (desktop/tablet/mobile): H1 44/38/30; H2 34/30/26; H3 20/20/19 and 18/18/17; subtitle 20/19/17; texts 18/17/16, 17/17/16 and 16/16/15.
- **Widths:** 58/38, 57/39, 48/100, 32/48/100 and 33/48/100; custom text widths of 760 px become 100% on mobile.
- **Spacing and layout:** section paddings 96–100 / 72 / 56, card paddings, `flex_gap`, `flex_wrap` and `flex_direction_mobile: column`.

Points to watch:
- The S3 card heading “Raising Awareness of Environmental Issues and Sustainable Development” is long; it is in the full-width card.
- The S6 H2 “Three Areas of Work Supporting the Association's Mission” should be checked for line breaks on mobile.

## 7. Image placeholders

| ID (FR → EN) | Location | URL | Alt text | Status |
|---|---|---|---|---|
| `3b20008` → `b8c000b` | S1 visual column | `…/elementor/assets/images/placeholder.png` (unchanged) | empty (unchanged) | ✅ Preserved — replace with an approved image |
| `3b2000f` → `b8c0012` | S2 visual column | `…/elementor/assets/images/placeholder.png` (unchanged) | empty (unchanged) | ✅ Preserved — replace with an approved image |

No image or alt text was generated, downloaded or invented.

## 8. Anchors and internal links

### 8.1 Anchors (present in the structure)

| Button | English label | Target | Section container | `_element_id` | Check |
|---|---|---|---|---|---|
| `b8c0008` | Our Mission | `#missions` | S3 `b8c0013` | `missions` | ✅ Match |
| `b8c0009` | Our Organization | `#organisation` | S5 `b8c003c` | `organisation` | ✅ Match |

The anchor `#organisation` keeps its French spelling. It is a technical identifier, not public text.

### 8.2 Page links requiring manual Polylang association

I re-examined the French JSON. It has **five page destinations**: three linked headings in S6, the S6 general button and the S7 button. No approved English URLs were provided, so the French targets are kept. No English slug, language prefix or Polylang URL was invented. Until these links are replaced, they lead to the **French** pages.

| # | Section | Element (FR → EN ID) | English label | Kept target (FR) | English page to associate | Status |
|---|---|---|---|---|---|---|
| 1 | S6 | Heading `3b2004d` → `b8c0050` | Administration and Management | `/nos-poles/administration-et-gestion/` | P-03 (EN) | ⚠️ Unknown |
| 2 | S6 | Heading `3b20050` → `b8c0053` | Training and Integration | `/nos-poles/formation-et-integration/` | P-04 (EN) | ⚠️ Unknown |
| 3 | S6 | Heading `3b20053` → `b8c0056` | Cultural and Social Activities | `/nos-poles/animation-culturelle-et-sociale/` | P-05 (EN) | ⚠️ Unknown |
| 4 | S6 | Button `3b20057` → `b8c0059` | Explore Our Three Areas of Work | `/nos-poles/` | Areas of Work overview (EN) | ⚠️ Unknown |
| 5 | S7 | Button `3b2005c` → `b8c005e` | Contact Us | `/contact/` | P-11 Contact (EN) | ⚠️ Unknown |

## 9. Remaining manual configuration, limitations and editorial notes

### 9.1 Manual configuration

1. **Import:** Elementor → Templates → Import, then insert the template into a new page.
2. **Polylang:** assign the page to English and link it as the translation of the French P-02.
3. **Links:** replace the 5 targets in section 8.2 once the English pages exist.
4. **Images:** replace the 2 placeholders and add approved English alt text.
5. **Anchors:** after import, click both S1 buttons and check that they scroll to S3 and S5. A fixed Astra header may cover the section titles.
6. **Internal labels** (`_title`): intentionally kept in French, as allowed by criterion 7.

### 9.2 Compatibility limitations

All checks are static. Rendering, wrapping, anchor scrolling and link behavior depend on the installed Elementor, Astra and Polylang setup and were **not tested** in WordPress.

### 9.3 Editorial notes (supplied text integrated as is, for supervisor review)

| # | ID | Note |
|---|---|---|
| N1 | `3b20004` | The task prompt asks to keep the distinction between the button and the S3 heading, describing the button as a “plural” label. The supplied label **“Our Mission” is singular**, while the French “Nos missions” is plural. The distinction from “Our Mission and Objectives” (S3) is preserved; the plural is not. If a plural is intended, “Our Missions” would match the French. Nothing was changed. |
| N2 | `3b20003` | “An introduction to the association's identity and purpose.” still reads like an editorial placeholder, as noted for the French and Arabic versions. Confirm whether it should stay visible. |
| N3 | `3b2000d` | The official name is kept. “Amal for Progress” appears only in the S2 paragraph where it was supplied. |
| N4 | S3 | The objectives are phrased as statutory intentions (“seeks to”, “provided for in the bylaws”). None is presented as a current service or open program. |
| N5 | `3b20018` | “literacy” renders « lutte contre l'illettrisme ». The nuance between *illettrisme* and *analphabétisme* is not carried over, which is acceptable in English. |
| N6 | S5, S6 | Terms used: “Executive Board”, “General Assembly”, “Committees”, “bylaws” and “areas of work”. The area names match the English P-01: Administration and Management; Training and Integration; Cultural and Social Activities. |

No corrections were made.

### 9.4 Proposed SEO metadata (not injected — **proposals pending supervisor approval**)

| Field | Proposal |
|---|---|
| SEO title | About the Association \| Association Amal Chabab Takaddoum, Rabat |
| Meta description | Learn about Association Amal Chabab Takaddoum, a Moroccan nonprofit based in Rabat: its mission and objectives, values, governance, and three areas of work supporting youth and social development. |
| Slug (**unapproved proposal**) | `about-the-association` |

The proposals use wording from the supplied content only.

## 10. Translation correspondence table (all 94 elements)

The table covers all 94 elements. There are **52 public-facing text fields**: 24 headings, 24 text editors and 4 buttons. **52/52 are integrated; none is missing.** HTML is shown escaped.

| # | French source ID | New English ID | Section | Widget type | Internal label (`_title`, kept in French) | Original French content | Integrated American English content | Translation status |
|---|---|---|---|---|---|---|---|---|
| 1 | `3b2000b` | `b8c0001` | S1 | container | S1 — Bannière | — | — | No public text |
| 2 | `3b2000a` | `b8c0002` | S1 | container | S1 · Ligne 2 colonnes | — | — | No public text |
| 3 | `3b20007` | `b8c0003` | S1 | container | S1 · Colonne texte | — | — | No public text |
| 4 | `3b20001` | `b8c0004` | S1 | heading | S1 · H1 | L’association Amal Chabab Takaddoum | Association Amal Chabab Takaddoum | Integrated as supplied |
| 5 | `3b20002` | `b8c0005` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Une ambition collective au service de la jeunesse et du développement social.&lt;/p&gt; | &lt;p&gt;A shared vision for youth and social development.&lt;/p&gt; | Integrated as supplied |
| 6 | `3b20003` | `b8c0006` | S1 | text-editor | S1 · Texte | &lt;p&gt;Présentation de l&#x27;identité et de la vocation de l&#x27;association.&lt;/p&gt; | &lt;p&gt;An introduction to the association&#x27;s identity and purpose.&lt;/p&gt; | Integrated as supplied |
| 7 | `3b20006` | `b8c0007` | S1 | container | S1 · Boutons | — | — | No public text |
| 8 | `3b20004` | `b8c0008` | S1 | button | S1 · Bouton 1 → ancre #missions | Nos missions | Our Mission | Integrated as supplied |
| 9 | `3b20005` | `b8c0009` | S1 | button | S1 · Bouton 2 → ancre #organisation | Notre organisation | Our Organization | Integrated as supplied |
| 10 | `3b20009` | `b8c000a` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | No public text |
| 11 | `3b20008` | `b8c000b` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image placeholder preserved (URL and empty alt unchanged) |
| 12 | `3b20012` | `b8c000c` | S2 | container | S2 — Identité | — | — | No public text |
| 13 | `3b20011` | `b8c000d` | S2 | container | S2 · Ligne 2 colonnes | — | — | No public text |
| 14 | `3b2000e` | `b8c000e` | S2 | container | S2 · Colonne texte | — | — | No public text |
| 15 | `3b2000c` | `b8c000f` | S2 | heading | S2 · H2 | Une association ancrée dans son territoire | An Association Rooted in Its Community | Integrated as supplied |
| 16 | `3b2000d` | `b8c0010` | S2 | text-editor | S2 · Texte (4 paragraphes) | &lt;p&gt;L’Association Amal Chabab Takaddoum est une organisation associative marocaine dont le siège social est établi à Rabat. Connue en anglais sous le nom « Amal for Progress », elle inscrit son engagement dans la promotion du développement, de la culture, de l&#x27;action sociale et du sport au profit de la jeunesse.&lt;/p&gt;<br>&lt;p&gt;Son projet associatif repose sur une conviction : l&#x27;engagement des jeunes, la solidarité et la participation citoyenne constituent des leviers importants pour accompagner les dynamiques de progrès au sein de la société.&lt;/p&gt;<br>&lt;p&gt;À travers ses orientations statutaires, l&#x27;association entend contribuer à la valorisation des talents, à l&#x27;amélioration des opportunités éducatives et formatives, au renforcement des solidarités et à la participation des jeunes à la vie collective.&lt;/p&gt;<br>&lt;p&gt;Son ancrage à Rabat constitue le cadre territorial de son engagement, tout en prévoyant une ouverture à la coopération avec des associations et des organismes partageant des objectifs similaires, au niveau national et international.&lt;/p&gt; | &lt;p&gt;Association Amal Chabab Takaddoum is a Moroccan nonprofit association headquartered in Rabat. Known in English as “Amal for Progress,” its commitment is centered on promoting development, culture, social action, and sports for the benefit of young people.&lt;/p&gt;<br>&lt;p&gt;The association&#x27;s mission is grounded in the belief that youth engagement, solidarity, and civic participation are important drivers of positive change within society.&lt;/p&gt;<br>&lt;p&gt;Through the objectives set out in its bylaws, the association seeks to help develop talent, expand educational and training opportunities, strengthen solidarity, and encourage young people&#x27;s participation in community life.&lt;/p&gt;<br>&lt;p&gt;Its presence in Rabat provides the territorial foundation for its commitment, while its bylaws also provide for cooperation with associations and organizations that share similar objectives at the national and international levels.&lt;/p&gt; | Integrated as supplied |
| 17 | `3b20010` | `b8c0011` | S2 | container | S2 · Colonne visuel (image à remplacer) | — | — | No public text |
| 18 | `3b2000f` | `b8c0012` | S2 | image | S2 · IMAGE À REMPLACER — ancrage territorial à Rabat | — | — | Image placeholder preserved (URL and empty alt unchanged) |
| 19 | `3b20024` | `b8c0013` | S3 | container | S3 — Mission et objectifs (ancre #missions) | — | — | Anchor `#missions` preserved |
| 20 | `3b20013` | `b8c0014` | S3 | heading | S3 · H2 | Notre mission et nos objectifs | Our Mission and Objectives | Integrated as supplied |
| 21 | `3b20023` | `b8c0015` | S3 | container | S3 · Grille des 5 objectifs | — | — | No public text |
| 22 | `3b20016` | `b8c0016` | S3 | container | S3 · Objectif 1 — Encourager l&#x27;engagement et la part | — | — | No public text |
| 23 | `3b20014` | `b8c0017` | S3 | heading | S3 · H3 objectif 1 | Encourager l&#x27;engagement et la participation citoyenne | Encouraging Engagement and Civic Participation | Integrated as supplied |
| 24 | `3b20015` | `b8c0018` | S3 | text-editor | S3 · Texte objectif 1 | &lt;p&gt;L&#x27;association entend favoriser l&#x27;implication des jeunes dans la vie civique, encourager leurs initiatives et contribuer à la valorisation de leurs compétences, de leurs talents et de leur capacité à agir dans leur environnement.&lt;/p&gt; | &lt;p&gt;The association seeks to encourage young people&#x27;s involvement in civic life, support their initiatives, and help recognize their skills, talents, and ability to take action in their communities.&lt;/p&gt; | Integrated as supplied |
| 25 | `3b20019` | `b8c0019` | S3 | container | S3 · Objectif 2 — Promouvoir l&#x27;éducation et la forma | — | — | No public text |
| 26 | `3b20017` | `b8c001a` | S3 | heading | S3 · H3 objectif 2 | Promouvoir l&#x27;éducation et la formation | Promoting Education and Training | Integrated as supplied |
| 27 | `3b20018` | `b8c001b` | S3 | text-editor | S3 · Texte objectif 2 | &lt;p&gt;Les orientations statutaires accordent une place importante à l&#x27;éducation non formelle, à la lutte contre l&#x27;illettrisme, à la formation professionnelle et à l&#x27;accompagnement éducatif des enfants et des jeunes.&lt;/p&gt; | &lt;p&gt;The association&#x27;s statutory objectives place particular importance on non-formal education, literacy, vocational training, and educational support for children and young people.&lt;/p&gt; | Integrated as supplied |
| 28 | `3b2001c` | `b8c001c` | S3 | container | S3 · Objectif 3 — Renforcer la solidarité et l&#x27;inclu | — | — | No public text |
| 29 | `3b2001a` | `b8c001d` | S3 | heading | S3 · H3 objectif 3 | Renforcer la solidarité et l&#x27;inclusion sociale | Strengthening Solidarity and Social Inclusion | Integrated as supplied |
| 30 | `3b2001b` | `b8c001e` | S3 | text-editor | S3 · Texte objectif 3 | &lt;p&gt;L&#x27;association inscrit la solidarité et le bénévolat parmi les leviers de son action. Ses statuts prévoient également une attention aux personnes en situation de vulnérabilité et aux catégories nécessitant un accompagnement adapté, dans la limite des ressources et des conditions disponibles.&lt;/p&gt; | &lt;p&gt;The association identifies solidarity and volunteering as important drivers of its work. Its bylaws also provide for attention to people experiencing vulnerability and groups requiring appropriate support, within the limits of available resources and circumstances.&lt;/p&gt; | Integrated as supplied |
| 31 | `3b2001f` | `b8c001f` | S3 | container | S3 · Objectif 4 — Valoriser la culture, les arts et  | — | — | No public text |
| 32 | `3b2001d` | `b8c0020` | S3 | heading | S3 · H3 objectif 4 | Valoriser la culture, les arts et le sport | Promoting Culture, the Arts, and Sports | Integrated as supplied |
| 33 | `3b2001e` | `b8c0021` | S3 | text-editor | S3 · Texte objectif 4 | &lt;p&gt;La promotion des activités culturelles, artistiques, cinématographiques et sportives fait partie des domaines d&#x27;intervention prévus par les statuts. Ces activités sont envisagées comme des espaces d&#x27;expression, d&#x27;apprentissage, de rencontre et de participation.&lt;/p&gt; | &lt;p&gt;The promotion of cultural, artistic, film-related, and sports activities is among the areas of work provided for in the association&#x27;s bylaws. These activities are considered opportunities for expression, learning, connection, and participation.&lt;/p&gt; | Integrated as supplied |
| 34 | `3b20022` | `b8c0022` | S3 | container | S3 · Objectif 5 — Sensibiliser à l&#x27;environnement et  | — | — | No public text |
| 35 | `3b20020` | `b8c0023` | S3 | heading | S3 · H3 objectif 5 | Sensibiliser à l&#x27;environnement et au développement durable | Raising Awareness of Environmental Issues and Sustainable Development | Integrated as supplied |
| 36 | `3b20021` | `b8c0024` | S3 | text-editor | S3 · Texte objectif 5 | &lt;p&gt;L&#x27;association inscrit également dans ses objectifs la sensibilisation aux enjeux environnementaux et aux exigences du développement durable, à travers des initiatives et des actions adaptées.&lt;/p&gt; | &lt;p&gt;The association also includes environmental awareness and sustainable development among its objectives, through appropriate initiatives and activities.&lt;/p&gt; | Integrated as supplied |
| 37 | `3b2003b` | `b8c0025` | S4 | container | S4 — Valeurs | — | — | No public text |
| 38 | `3b20027` | `b8c0026` | S4 | container | S4 · En-tête | — | — | No public text |
| 39 | `3b20025` | `b8c0027` | S4 | heading | S4 · H2 | Les valeurs qui guident notre engagement | The Values That Guide Our Commitment | Integrated as supplied |
| 40 | `3b20026` | `b8c0028` | S4 | text-editor | S4 · Introduction | &lt;p&gt;L&#x27;action associative d&#x27;Amal Chabab Takaddoum s&#x27;appuie sur des principes qui orientent ses objectifs et son fonctionnement :&lt;/p&gt; | &lt;p&gt;Association Amal Chabab Takaddoum&#x27;s community work is guided by principles that shape its objectives and the way it operates:&lt;/p&gt; | Integrated as supplied |
| 41 | `3b2003a` | `b8c0029` | S4 | container | S4 · Grille des 6 valeurs | — | — | No public text |
| 42 | `3b2002a` | `b8c002a` | S4 | container | S4 · Valeur 1 — Citoyenneté | — | — | No public text |
| 43 | `3b20028` | `b8c002b` | S4 | heading | S4 · H3 valeur 1 | Citoyenneté | Citizenship | Integrated as supplied |
| 44 | `3b20029` | `b8c002c` | S4 | text-editor | S4 · Texte valeur 1 | &lt;p&gt;encourager la participation responsable à la vie collective.&lt;/p&gt; | &lt;p&gt;Encouraging responsible participation in community life.&lt;/p&gt; | Integrated as supplied |
| 45 | `3b2002d` | `b8c002d` | S4 | container | S4 · Valeur 2 — Égalité et justice sociale | — | — | No public text |
| 46 | `3b2002b` | `b8c002e` | S4 | heading | S4 · H3 valeur 2 | Égalité et justice sociale | Equality and Social Justice | Integrated as supplied |
| 47 | `3b2002c` | `b8c002f` | S4 | text-editor | S4 · Texte valeur 2 | &lt;p&gt;promouvoir des relations fondées sur le respect des droits et de la dignité.&lt;/p&gt; | &lt;p&gt;Promoting relationships based on respect for rights and dignity.&lt;/p&gt; | Integrated as supplied |
| 48 | `3b20030` | `b8c0030` | S4 | container | S4 · Valeur 3 — Solidarité | — | — | No public text |
| 49 | `3b2002e` | `b8c0031` | S4 | heading | S4 · H3 valeur 3 | Solidarité | Solidarity | Integrated as supplied |
| 50 | `3b2002f` | `b8c0032` | S4 | text-editor | S4 · Texte valeur 3 | &lt;p&gt;développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;Developing mutual support, volunteering, and cooperation.&lt;/p&gt; | Integrated as supplied |
| 51 | `3b20033` | `b8c0033` | S4 | container | S4 · Valeur 4 — Tolérance | — | — | No public text |
| 52 | `3b20031` | `b8c0034` | S4 | heading | S4 · H3 valeur 4 | Tolérance | Tolerance | Integrated as supplied |
| 53 | `3b20032` | `b8c0035` | S4 | text-editor | S4 · Texte valeur 4 | &lt;p&gt;favoriser le dialogue, la compréhension et le respect mutuel.&lt;/p&gt; | &lt;p&gt;Encouraging dialogue, understanding, and mutual respect.&lt;/p&gt; | Integrated as supplied |
| 54 | `3b20036` | `b8c0036` | S4 | container | S4 · Valeur 5 — Responsabilité | — | — | No public text |
| 55 | `3b20034` | `b8c0037` | S4 | heading | S4 · H3 valeur 5 | Responsabilité | Responsibility | Integrated as supplied |
| 56 | `3b20035` | `b8c0038` | S4 | text-editor | S4 · Texte valeur 5 | &lt;p&gt;inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;Making a serious and constructive approach central to commitment.&lt;/p&gt; | Integrated as supplied |
| 57 | `3b20039` | `b8c0039` | S4 | container | S4 · Valeur 6 — Initiative | — | — | No public text |
| 58 | `3b20037` | `b8c003a` | S4 | heading | S4 · H3 valeur 6 | Initiative | Initiative | Integrated as supplied (identical in both languages) |
| 59 | `3b20038` | `b8c003b` | S4 | text-editor | S4 · Texte valeur 6 | &lt;p&gt;valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;Recognizing talents, ideas, and the ability to take action.&lt;/p&gt; | Integrated as supplied |
| 60 | `3b20049` | `b8c003c` | S5 | container | S5 — Organisation (ancre #organisation) | — | — | Anchor `#organisation` preserved |
| 61 | `3b2003e` | `b8c003d` | S5 | container | S5 · En-tête | — | — | No public text |
| 62 | `3b2003c` | `b8c003e` | S5 | heading | S5 · H2 | Une organisation structurée | A Structured Organization | Integrated as supplied |
| 63 | `3b2003d` | `b8c003f` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Les statuts de l&#x27;association prévoient plusieurs instances qui contribuent à son organisation et à son fonctionnement.&lt;/p&gt; | &lt;p&gt;The association&#x27;s bylaws provide for several governing bodies that contribute to its organization and operations.&lt;/p&gt; | Integrated as supplied |
| 64 | `3b20048` | `b8c0040` | S5 | container | S5 · Grille des 3 instances | — | — | No public text |
| 65 | `3b20041` | `b8c0041` | S5 | container | S5 · Instance 1 — L&#x27;Assemblée générale | — | — | No public text |
| 66 | `3b2003f` | `b8c0042` | S5 | heading | S5 · H3 instance 1 | L&#x27;Assemblée générale | The General Assembly | Integrated as supplied |
| 67 | `3b20040` | `b8c0043` | S5 | text-editor | S5 · Texte instance 1 | &lt;p&gt;Elle constitue l&#x27;instance associative réunissant les catégories de membres prévues par les statuts. Elle intervient dans la définition des orientations générales et l&#x27;examen des rapports de l&#x27;association.&lt;/p&gt; | &lt;p&gt;The General Assembly brings together the categories of members provided for in the bylaws. It contributes to defining the association&#x27;s overall direction and reviewing its reports.&lt;/p&gt; | Integrated as supplied |
| 68 | `3b20044` | `b8c0044` | S5 | container | S5 · Instance 2 — Le Bureau exécutif | — | — | No public text |
| 69 | `3b20042` | `b8c0045` | S5 | heading | S5 · H3 instance 2 | Le Bureau exécutif | The Executive Board | Integrated as supplied |
| 70 | `3b20043` | `b8c0046` | S5 | text-editor | S5 · Texte instance 2 | &lt;p&gt;Les statuts prévoient un Bureau exécutif composé de cinq membres élus par l&#x27;Assemblée générale. Il assure notamment la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;The bylaws provide for an Executive Board composed of five members elected by the General Assembly. Its responsibilities include overseeing the organization of committees and working areas, as well as monitoring the implementation of established programs.&lt;/p&gt; | Integrated as supplied |
| 71 | `3b20047` | `b8c0047` | S5 | container | S5 · Instance 3 — Les commissions | — | — | No public text |
| 72 | `3b20045` | `b8c0048` | S5 | heading | S5 · H3 instance 3 | Les commissions | Committees | Integrated as supplied |
| 73 | `3b20046` | `b8c0049` | S5 | text-editor | S5 · Texte instance 3 | &lt;p&gt;Les commissions sont constituées selon les besoins de l&#x27;association. Elles contribuent à l&#x27;étude des programmes et au suivi des activités relevant de leurs domaines de travail.&lt;/p&gt; | &lt;p&gt;Committees are established according to the association&#x27;s needs. They contribute to reviewing programs and following up on activities within their respective areas of work.&lt;/p&gt; | Integrated as supplied |
| 74 | `3b20059` | `b8c004a` | S6 | container | S6 — Trois pôles | — | — | No public text |
| 75 | `3b2004c` | `b8c004b` | S6 | container | S6 · En-tête | — | — | No public text |
| 76 | `3b2004a` | `b8c004c` | S6 | heading | S6 · H2 | Trois pôles au service du projet associatif | Three Areas of Work Supporting the Association&#x27;s Mission | Integrated as supplied |
| 77 | `3b2004b` | `b8c004d` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires :&lt;/p&gt; | &lt;p&gt;The association&#x27;s organization is based on three complementary areas established in its bylaws:&lt;/p&gt; | Integrated as supplied |
| 78 | `3b20056` | `b8c004e` | S6 | container | S6 · Grille des 3 pôles | — | — | No public text |
| 79 | `3b2004f` | `b8c004f` | S6 | container | S6 · Carte 1 — Pôle Administration et Gestion → P-03 | — | — | No public text |
| 80 | `3b2004d` | `b8c0050` | S6 | heading | S6 · H3 carte 1 (lien P-03) | Pôle Administration et Gestion | Administration and Management | Integrated as supplied |
| 81 | `3b2004e` | `b8c0051` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt; | &lt;p&gt;This area contributes to organizing the association and supporting the operation of its organizational structure.&lt;/p&gt; | Integrated as supplied |
| 82 | `3b20052` | `b8c0052` | S6 | container | S6 · Carte 2 — Pôle Formation et Intégration → P-04 | — | — | No public text |
| 83 | `3b20050` | `b8c0053` | S6 | heading | S6 · H3 carte 2 (lien P-04) | Pôle Formation et Intégration | Training and Integration | Integrated as supplied |
| 84 | `3b20051` | `b8c0054` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt; | &lt;p&gt;This area reflects the association&#x27;s objectives relating to learning, skills development, and integration.&lt;/p&gt; | Integrated as supplied |
| 85 | `3b20055` | `b8c0055` | S6 | container | S6 · Carte 3 — Pôle Animation Culturelle et Sociale → P-05 | — | — | No public text |
| 86 | `3b20053` | `b8c0056` | S6 | heading | S6 · H3 carte 3 (lien P-05) | Pôle Animation Culturelle et Sociale | Cultural and Social Activities | Integrated as supplied |
| 87 | `3b20054` | `b8c0057` | S6 | text-editor | S6 · Texte carte 3 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;This area supports the objectives relating to culture, community activities, and social participation.&lt;/p&gt; | Integrated as supplied |
| 88 | `3b20058` | `b8c0058` | S6 | container | S6 · Bouton général | — | — | No public text |
| 89 | `3b20057` | `b8c0059` | S6 | button | S6 · Bouton → page Nos pôles | Découvrir nos trois pôles | Explore Our Three Areas of Work | Integrated as supplied |
| 90 | `3b2005e` | `b8c005a` | S7 | container | S7 — Appel à l’action | — | — | No public text |
| 91 | `3b2005a` | `b8c005b` | S7 | heading | S7 · H2 | Vous souhaitez mieux connaître notre association ? | Would You Like to Learn More About Our Association? | Integrated as supplied |
| 92 | `3b2005b` | `b8c005c` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez découvrir les missions de l&#x27;Association Amal Chabab Takaddoum, échanger avec ses représentants ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour mieux connaître vos attentes et identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;Would you like to learn more about the mission of Association Amal Chabab Takaddoum, exchange views with its representatives, or explore opportunities for collaboration?&lt;/p&gt;<br>&lt;p&gt;Let&#x27;s connect to better understand your expectations and identify opportunities for exchange.&lt;/p&gt; | Integrated as supplied |
| 93 | `3b2005d` | `b8c005d` | S7 | container | S7 · Bouton | — | — | No public text |
| 94 | `3b2005c` | `b8c005e` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | Contact Us | Integrated as supplied |
