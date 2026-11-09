# P-03 Administration and Management — American English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**
Deliverable: `P03_Pole_Administration_Gestion_English_Elementor.json`

> ⚠️ **Status: translation proposal pending supervisor validation.** I translated this English version myself from the French source; no English text was supplied. Translating a French proposal does **not** validate its content.

---

## 1. Objective and sources

**Objective:** an American English, LTR version of the French P-03 page. It keeps the source structure, identifiers, links, anchors and design, and its terminology matches the English P-01 and P-02.

| Source | Use | Status |
|---|---|---|
| `P03_Pole_Administration_Gestion_Elementor.json` (FR) | Structure and text to translate | ✅ Used. SHA-256 `9f135af7…a9f29e8d`; **not modified** |
| `P03_Pole_Administration_Gestion_Documentation_Technique.md` (FR) | Editorial classification § C (5 imposed / 17 validated / 24 proposals) | ⚠️ **Not received**. See section 9. |
| `P03_Pole_Administration_Gestion_Arabe_Elementor.json` | Structural cross-check | ✅ Used (same tree and IDs) |
| `P03_Pole_Administration_Gestion_Arabe_Rapport_Technique.md` | Element inventory | ✅ Used |
| English P-01 and P-02 templates | Reference terminology | ✅ Used. Shared wording was detected automatically, sentence by sentence. |

## 2. Structure of the seven sections (order preserved)

| # | Section (`_title`, kept in French) | Background | Content |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | 2 columns (58% / 38%). Left: H1, subtitle, text and 2 anchor buttons. Right: image placeholder. |
| S2 | S2 — Présentation | `#FFFFFF` | Centered H2 and 3-paragraph text (820 px) |
| S3 | S3 — Trois domaines d'intervention (anchor `#missions`) | `#F4F6F6` | Centered header and 3 cards (33% → 48% → 100%) |
| S4 | S4 — Contribution transversale (anchor `#contribution`) | `#FFFFFF` | Centered H2 and 3-paragraph text (820 px) |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | Centered header and 4 cards (48% → 48% → 100%) |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | Centered header and 2 area cards with buttons |
| S7 | S7 — Appel à l’action | `#152A33` | Centered H2, text and Contact button |

## 3. Element count and heading hierarchy

| Type | Source | English |
|---|---|---|
| `container` | 29 | 29 |
| `heading` | 16 | 16 |
| `text-editor` | 17 | 17 |
| `button` | 5 | 5 |
| `image` | 1 | 1 |
| **Total** | **68** (29 containers + 39 widgets) | **68** |

**Heading hierarchy preserved:** 1 H1, 6 H2 and 9 H3.

| Level | English headings |
|---|---|
| H1 | Administration and Management |
| H2 | An Area of Work Supporting the Association's Organization · Three Fields of Work · A Cross-Cutting Contribution to the Other Areas · The Principles That Guide Its Work · The Other Two Areas of Work · Have a Question About How the Association Works? |
| H3 | Organizing the Association's Operations · Administrative Follow-Up · Managing Necessary Resources · Responsibility · Solidarity · Initiative · Shared Governance · Training and Integration · Cultural and Social Activities |

## 4. Identifiers

**Rule (brief 5.4): the 68 source identifiers are kept unchanged.**
- **Within this file:** all 68 IDs are unique.
- **French P-03:** the IDs are identical (68/68), as intended.
- **Arabic P-03:** the IDs are identical (68/68). That file also keeps the source IDs.
- **Arabic P-02:** it shares the same 68 IDs. This collision was already documented in the Arabic P-03 report: the French P-03 source uses the same `4c3…` range that was generated for the Arabic P-02. Elementor IDs only need to be unique within a page, because generated CSS is scoped by the WordPress post ID. These are separate pages, so there is **no functional effect** unless elements from both pages are combined on one page.
- **All other templates:** no shared IDs.

## 5. Graphic and responsive settings

- **No setting was modified.** A key-by-key diff of every `settings` object shows that only `title` (×15), `editor` (×17) and `text` (×5) differ. The heading “Initiative” is identical in French and English.
- **Preserved values:**
  - **Colors:** `#F4F6F6`, `#FFFFFF`, `#152A33`, `#1F4E5F`, `#45555C`, `#E1E7E8`.
  - **Typography (desktop/tablet/mobile):** H1 44/38/30; H2 34/30/26; H3 20/20/19 and 18/18/17; texts 20/19/17, 18/17/16, 17/17/16 and 16/16/15.
  - **Widths:** 58/38, 33/48/100 and 48/48/100; 820 and 760 px, then 100% on mobile.
  - **Spacing:** paddings and `flex_gap`.
  - **Flex behavior:** `flex_wrap` and `flex_direction_mobile`.
  - **Page settings:** `template: elementor_header_footer` and `hide_title: yes`.
- **LTR:** no direction or alignment property was added, and no RTL setting exists. The 12 centered elements stay centered. The 21 headings and texts with no alignment set inherit left alignment. Column order is unchanged: text on the left, image on the right.
- **Template name** (admin library only): `P-03 Pôle Administration et Gestion (EN) — Amal Chabab Takaddoum`.
- **Image placeholder:** the Elementor native placeholder is preserved, with its URL unchanged and `alt` empty. The proposed alt text in section 7 was **not injected**.
- **No widget or feature was added.** There is no Pro widget, form, menu, header, footer or animation.

## 6. Links and anchors

| Element | English label | Target (unchanged) | Check |
|---|---|---|---|
| `4c30004` S1 button 1 | Its Fields of Work | `#missions` → S3 container `4c3001c` | ✅ Anchor present |
| `4c30005` S1 button 2 | Its Contribution | `#contribution` → S4 container `4c3001f` | ✅ Anchor present |
| `4c30036` S6 card 1 | Explore This Area | `/nos-poles/formation-et-integration/` | ⚠️ French target kept; English P-04 to be associated in Polylang |
| `4c3003b` S6 card 2 | Explore This Area | `/nos-poles/animation-culturelle-et-sociale/` | ⚠️ French target kept; English P-05 to be associated |
| `4c30042` S7 button | Contact Us | `/contact/` | ⚠️ French target kept; English Contact to be associated |

No English URL or Polylang language prefix was invented. Until the three page links are replaced, they lead to the **French** pages.

## 7. Proposed SEO metadata (not injected — **unapproved proposals**)

| Field | Proposal |
|---|---|
| SEO title | Administration and Management \| Association Amal Chabab Takaddoum |
| Meta description | The Administration and Management area of Association Amal Chabab Takaddoum supports the organization and coordination of the association's operations, administrative follow-up, and the resources it needs to function. |
| Primary keyword | association administration and management Rabat |
| Image alt text | Association Amal Chabab Takaddoum — Administration and Management |
| Slug (unapproved) | `administration-and-management` |

The meta description and alt text use the page's own wording only. They mention no accounting or financial function.

## 8. Terminology and translation choices

### 8.1 Terms aligned with the English P-01 and P-02

| French | English (this page) | Reference |
|---|---|---|
| Association Amal Chabab Takaddoum | Association Amal Chabab Takaddoum | EN P-01/P-02 (proper name kept) |
| Pôle | **area of work** / **area** | EN P-01/P-02 |
| Pôle Administration et Gestion | **Administration and Management** | EN P-01/P-02 |
| Pôle Formation et Intégration | **Training and Integration** | EN P-01/P-02 |
| Pôle Animation Culturelle et Sociale | **Cultural and Social Activities** | EN P-01/P-02 |
| statuts / orientations statutaires | bylaws / statutory objectives | EN P-02 |
| Bureau exécutif · Assemblée générale · commissions · instances | Executive Board · General Assembly · committees · governing bodies | EN P-02 |
| pôles de travail | working areas | EN P-02 (“committees and working areas”) |
| vie associative | the association's operations | EN P-01 (S3 card 1) |
| suivi administratif · moyens nécessaires | administrative follow-up · resources needed | EN P-01 (S3 card 1) |
| Découvrir le pôle · Nous contacter | Explore This Area · Contact Us | EN P-01 |
| Responsabilité / Solidarité / Initiative (texts) | identical to the EN P-02 values | EN P-02 |

### 8.2 New choices on this page — supervisor review

| # | ID | French | English | Rationale and alternatives |
|---|---|---|---|---|
| T1 | `4c30004`, `4c3000f`, `4c30010`, `4c30016` | domaine(s) d'intervention | **field(s) of work** | Since “area” is reserved for *pôle*, *domaine* needs a distinct term to avoid “areas within an area”. Alternatives: “focus areas”, “scope of work”. |
| T2 | `4c3002c` | Fonctionnement collégial | **Shared Governance** | Describes the division of roles in the French text (General Assembly → direction; Executive Board → oversight; committees → review and follow-up) without implying a different structure or a decision-making role for the area. Alternatives: “Collective Operation”, “Collegial Functioning”. **Sensitive point 3; pending validation.** |
| T3 | `4c3002d` | … au suivi des activités relevant de leurs domaines de travail | … within their respective **fields** | EN P-02 renders the same phrase as “within their respective areas of work”, which clashes with “area of work” for *pôle*. “Fields” is used here; harmonizing P-02 is recommended (not done, since P-02 was not to be modified). |
| T4 | `4c30019` | locaux, équipements et ressources | premises, equipment, and **other** resources | “Other” avoids repeating “resources: … and resources” and adds no meaning. The exclusion of accounting and financial functions is kept verbatim. **Sensitive point 2; pending validation.** |
| T5 | `4c30016` | tenue et conservation des documents associatifs | keeping and preserving the association's records | Neutral wording. It does not assign a legal custodian role. **Sensitive point 1; pending validation.** |
| T6 | `4c3001d` | transversale | cross-cutting | Standard nonprofit term. |
| T7 | `4c30001` | Pôle Administration et Gestion | Administration and Management | Same as EN P-01 S3 and EN P-02 S6 headings (no “Pôle” or “Area” prefix). |
| T8 | — | — | — | No responsibility was strengthened. The text keeps “contributes to”, “helps”, “support role” and “under the oversight of the Executive Board”. No statutory objective is presented as a completed activity. |

## 9. Editorial validation status

The French documentation § C was **not received**, so its block-level classification (5 imposed / 17 validated / 24 proposals) could not be applied as is. Its 46 blocks also do not match the 38 visible texts in the JSON. The correspondence table therefore shows an **indicative status**. It is based on an automatic comparison of each French P-03 text with the French P-01 and P-02 pages:

| Indicative status | Count |
|---|---|
| Reused verbatim from FR P-01/P-02 (likely “validated — reused”) | 19 |
| Partly reused from FR P-01/P-02 | 2 |
| New P-03 wording (imposed or proposal, per § C) | 13 |
| **Sensitive proposals flagged by the brief — NOT VALIDATED** | 4 elements (3 points) |
| **Total** | **38** |

**The three sensitive points remain proposals pending validation**, and their English translation does not validate them:
1. S3 card 2 (`4c30016`): keeping and preserving records, and monitoring administrative obligations.
2. S3 card 3 (`4c30019`): resources read as premises, equipment and resources.
3. S5 principle 4 (`4c3002c`, `4c3002d`): “Fonctionnement collégial” → “Shared Governance”.

**Supervisor action:** carry the § C classification over to the correspondence table (section 11). None of the texts should be treated as validated because of this translation.

## 10. Limitations, checks and manual integration

### 10.1 Checks performed (static, on the JSON)

- **JSON:** syntax is valid.
- **Structure:** 7 sections in source order; 68 elements with the same hierarchy, types, `isInner` and child counts.
- **Identifiers:** kept and unique (section 4).
- **Headings:** hierarchy is 1 H1, 6 H2 and 9 H3.
- **Text:** 38/38 visible texts translated, and no French public text remains (automatic search).
- **Links and anchors:** anchors match their targets, and the 5 links are unchanged.
- **Image:** the placeholder is unchanged.
- **Accounting/financial:** these terms appear only in the exclusion sentence of card 3, as in the source.

### 10.2 Not performed — to check after a real import

- Import into Elementor.
- Rendering on desktop, tablet and mobile.
- Line breaks of the longer English headings (S2 H2, S7 H2) and buttons.
- Anchor scrolling, which a fixed Astra header may affect.
- Polylang association and link behavior.
- Astra header and footer.

### 10.3 Manual integration instructions

1. Validate the English wording and the editorial statuses (sections 8 and 9).
2. Elementor → Templates → Import the JSON, then insert it into a new page.
3. Polylang: assign the page to English and link it to the French P-03 (`/nos-poles/administration-et-gestion/`).
4. Replace the 3 page links (section 6) once the English P-04, P-05 and Contact pages exist.
5. Replace the image placeholder. Add the approved alt text and SEO metadata through the usual settings, not the template.
6. Do not modify Astra, Elementor, Polylang or any global settings.

## 11. French / English correspondence table (68 elements)

ID English = ID source. HTML shown escaped.

| # | Source ID | English ID | Section | Type | `_title` (source) | French text | English text | Editorial status (indicative — § C not received) | Translation note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `4c3000b` | `4c3000b` | S1 | container | S1 — Bannière | — | — | No public text |  |
| 2 | `4c3000a` | `4c3000a` | S1 | container | S1 · Ligne 2 colonnes | — | — | No public text |  |
| 3 | `4c30007` | `4c30007` | S1 | container | S1 · Colonne texte | — | — | No public text |  |
| 4 | `4c30001` | `4c30001` | S1 | heading | S1 · H1 | Pôle Administration et Gestion | Administration and Management | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 5 | `4c30002` | `4c30002` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un pôle dédié à l&#x27;organisation et à la coordination de la vie associative.&lt;/p&gt; | &lt;p&gt;This area focuses on organizing and coordinating the association&#x27;s operations.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 6 | `4c30003` | `4c30003` | S1 | text-editor | S1 · Texte | &lt;p&gt;Il contribue au suivi administratif et à la gestion des moyens nécessaires au fonctionnement de l&#x27;association.&lt;/p&gt;<br>&lt;p&gt;Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association.&lt;/p&gt; | &lt;p&gt;It contributes to administrative follow-up and the management of the resources needed to support the association&#x27;s work.&lt;/p&gt;<br>&lt;p&gt;Its fields of work fall within the association&#x27;s statutory objectives.&lt;/p&gt; | Partly reused from FR P-01/P-02 (1/2 sentences) | EN wording partly reused from EN P-01/P-02 (1/2) |
| 7 | `4c30006` | `4c30006` | S1 | container | S1 · Boutons | — | — | No public text |  |
| 8 | `4c30004` | `4c30004` | S1 | button | S1 · Bouton 1 → ancre #missions | Ses domaines d&#x27;intervention | Its Fields of Work | Reused verbatim from FR P-01/P-02 (observed) | New EN wording |
| 9 | `4c30005` | `4c30005` | S1 | button | S1 · Bouton 2 → ancre #contribution | Sa contribution | Its Contribution | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 10 | `4c30009` | `4c30009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | No public text |  |
| 11 | `4c30008` | `4c30008` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image placeholder preserved (URL unchanged) |  |
| 12 | `4c3000e` | `4c3000e` | S2 | container | S2 — Présentation | — | — | No public text |  |
| 13 | `4c3000c` | `4c3000c` | S2 | heading | S2 · H2 | Un pôle au service de l&#x27;organisation associative | An Area of Work Supporting the Association&#x27;s Organization | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 14 | `4c3000d` | `4c3000d` | S2 | text-editor | S2 · Texte (3 paragraphes) | &lt;p&gt;Le Pôle Administration et Gestion est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt;<br>&lt;p&gt;Son rôle se situe en appui des activités portées par l&#x27;association : il contribue à l&#x27;organisation de la vie associative, au suivi administratif et à la disponibilité des moyens nécessaires à la conduite des activités.&lt;/p&gt;<br>&lt;p&gt;Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale.&lt;/p&gt; | &lt;p&gt;The Administration and Management area is one of the three areas of work established in the bylaws of Association Amal Chabab Takaddoum. It contributes to organizing the association and supporting the operation of its organizational structure.&lt;/p&gt;<br>&lt;p&gt;Its role is to support the activities carried out by the association: it contributes to organizing the association&#x27;s operations, to administrative follow-up, and to the availability of the resources needed to carry out activities.&lt;/p&gt;<br>&lt;p&gt;In accordance with the bylaws, the organization of the working areas and the monitoring of program implementation fall under the oversight of the Executive Board, elected by the General Assembly.&lt;/p&gt; | Partly reused from FR P-01/P-02 (1/5 sentences) | New EN wording |
| 15 | `4c3001c` | `4c3001c` | S3 | container | S3 — Trois domaines d&#x27;intervention (ancre #missions) | — | — | No public text |  |
| 16 | `4c30011` | `4c30011` | S3 | container | S3 · En-tête | — | — | No public text |  |
| 17 | `4c3000f` | `4c3000f` | S3 | heading | S3 · H2 | Trois domaines d&#x27;intervention | Three Fields of Work | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 18 | `4c30010` | `4c30010` | S3 | text-editor | S3 · Introduction | &lt;p&gt;Les activités du pôle s&#x27;organisent autour de trois domaines complémentaires.&lt;/p&gt; | &lt;p&gt;The area&#x27;s activities are organized around three complementary fields.&lt;/p&gt; | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 19 | `4c3001b` | `4c3001b` | S3 | container | S3 · Grille des 3 domaines | — | — | No public text |  |
| 20 | `4c30014` | `4c30014` | S3 | container | S3 · Domaine 1 — Organisation de la vie associative | — | — | No public text |  |
| 21 | `4c30012` | `4c30012` | S3 | heading | S3 · H3 domaine 1 | Organisation de la vie associative | Organizing the Association&#x27;s Operations | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 22 | `4c30013` | `4c30013` | S3 | text-editor | S3 · Texte domaine 1 | &lt;p&gt;Le pôle contribue à l&#x27;organisation et à la coordination de la vie associative. Il concourt à l&#x27;articulation entre les instances, les commissions et les pôles de travail prévus par les statuts, ainsi qu&#x27;à la continuité du fonctionnement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;The area contributes to organizing and coordinating the association&#x27;s operations. It helps connect the governing bodies, committees, and working areas provided for in the bylaws, and contributes to the continuity of the association&#x27;s work.&lt;/p&gt; | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 23 | `4c30017` | `4c30017` | S3 | container | S3 · Domaine 2 — Suivi administratif | — | — | No public text |  |
| 24 | `4c30015` | `4c30015` | S3 | heading | S3 · H3 domaine 2 | Suivi administratif | Administrative Follow-Up | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 25 | `4c30016` | `4c30016` | S3 | text-editor | S3 · Texte domaine 2 | &lt;p&gt;Le pôle contribue au suivi administratif de l&#x27;association. Ce domaine couvre la tenue et la conservation des documents associatifs, ainsi que le suivi des obligations administratives qui s&#x27;attachent à la vie de l&#x27;association.&lt;/p&gt; | &lt;p&gt;The area contributes to the association&#x27;s administrative follow-up. This field covers keeping and preserving the association&#x27;s records, as well as monitoring the administrative obligations associated with its operations.&lt;/p&gt; | **Proposal pending validation — sensitive point** (S3 card 2 — records & administrative obligations) | New EN wording |
| 26 | `4c3001a` | `4c3001a` | S3 | container | S3 · Domaine 3 — Gestion des moyens nécessaires | — | — | No public text |  |
| 27 | `4c30018` | `4c30018` | S3 | heading | S3 · H3 domaine 3 | Gestion des moyens nécessaires | Managing Necessary Resources | Reused verbatim from FR P-01/P-02 (observed) | New EN wording |
| 28 | `4c30019` | `4c30019` | S3 | text-editor | S3 · Texte domaine 3 | &lt;p&gt;Le pôle contribue à la gestion des moyens nécessaires au fonctionnement de l&#x27;association : locaux, équipements et ressources mobilisés pour la conduite des activités. Cette gestion s&#x27;entend comme un appui matériel et organisationnel, distinct des fonctions comptables et financières, qui relèvent d&#x27;un cadre propre.&lt;/p&gt; | &lt;p&gt;The area contributes to managing the resources needed for the association&#x27;s operations: premises, equipment, and other resources used to carry out its activities. This management is understood as material and organizational support, distinct from accounting and financial functions, which fall under a separate framework.&lt;/p&gt; | **Proposal pending validation — sensitive point** (S3 card 3 — premises, equipment, resources) | New EN wording |
| 29 | `4c3001f` | `4c3001f` | S4 | container | S4 — Contribution transversale (ancre #contribution) | — | — | No public text |  |
| 30 | `4c3001d` | `4c3001d` | S4 | heading | S4 · H2 | Une contribution transversale aux autres pôles | A Cross-Cutting Contribution to the Other Areas | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 31 | `4c3001e` | `4c3001e` | S4 | text-editor | S4 · Texte (3 paragraphes) | &lt;p&gt;La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités.&lt;/p&gt;<br>&lt;p&gt;En soutenant l&#x27;organisation, le suivi administratif et la disponibilité des moyens, le pôle participe à un cadre de fonctionnement commun au Pôle Formation et Intégration et au Pôle Animation Culturelle et Sociale.&lt;/p&gt;<br>&lt;p&gt;Cette fonction d&#x27;appui s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;The area&#x27;s contribution is not limited to its own scope: it also supports the conditions under which the other two statutory areas carry out their activities.&lt;/p&gt;<br>&lt;p&gt;By supporting organization, administrative follow-up, and the availability of resources, the area contributes to a shared operating framework for the Training and Integration area and the Cultural and Social Activities area.&lt;/p&gt;<br>&lt;p&gt;This support role is carried out within the framework defined by the bylaws, with the Executive Board overseeing the organization of committees and working areas, as well as monitoring the implementation of established programs.&lt;/p&gt; | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 32 | `4c30030` | `4c30030` | S5 | container | S5 — Principes de fonctionnement | — | — | No public text |  |
| 33 | `4c30022` | `4c30022` | S5 | container | S5 · En-tête | — | — | No public text |  |
| 34 | `4c30020` | `4c30020` | S5 | heading | S5 · H2 | Les principes qui guident son fonctionnement | The Principles That Guide Its Work | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 35 | `4c30021` | `4c30021` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;The area&#x27;s work is guided by the principles that shape the association&#x27;s commitment.&lt;/p&gt; | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 36 | `4c3002f` | `4c3002f` | S5 | container | S5 · Grille des 4 principes | — | — | No public text |  |
| 37 | `4c30025` | `4c30025` | S5 | container | S5 · Principe 1 — Responsabilité | — | — | No public text |  |
| 38 | `4c30023` | `4c30023` | S5 | heading | S5 · H3 principe 1 | Responsabilité | Responsibility | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 39 | `4c30024` | `4c30024` | S5 | text-editor | S5 · Texte principe 1 | &lt;p&gt;Inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;Making a serious and constructive approach central to commitment.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 40 | `4c30028` | `4c30028` | S5 | container | S5 · Principe 2 — Solidarité | — | — | No public text |  |
| 41 | `4c30026` | `4c30026` | S5 | heading | S5 · H3 principe 2 | Solidarité | Solidarity | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 42 | `4c30027` | `4c30027` | S5 | text-editor | S5 · Texte principe 2 | &lt;p&gt;Développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;Developing mutual support, volunteering, and cooperation.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 43 | `4c3002b` | `4c3002b` | S5 | container | S5 · Principe 3 — Initiative | — | — | No public text |  |
| 44 | `4c30029` | `4c30029` | S5 | heading | S5 · H3 principe 3 | Initiative | Initiative | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 45 | `4c3002a` | `4c3002a` | S5 | text-editor | S5 · Texte principe 3 | &lt;p&gt;Valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;Recognizing talents, ideas, and the ability to take action.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 46 | `4c3002e` | `4c3002e` | S5 | container | S5 · Principe 4 — Fonctionnement collégial | — | — | No public text |  |
| 47 | `4c3002c` | `4c3002c` | S5 | heading | S5 · H3 principe 4 | Fonctionnement collégial | Shared Governance | **Proposal pending validation — sensitive point** (S5 principle 4 — « Fonctionnement collégial ») | New EN wording |
| 48 | `4c3002d` | `4c3002d` | S5 | text-editor | S5 · Texte principe 4 | &lt;p&gt;Les orientations générales relèvent de l&#x27;Assemblée générale, leur supervision du Bureau exécutif, et les commissions contribuent à l&#x27;étude des programmes et au suivi des activités relevant de leurs domaines de travail.&lt;/p&gt; | &lt;p&gt;Overall direction falls to the General Assembly and its oversight to the Executive Board, while committees contribute to reviewing programs and following up on activities within their respective fields.&lt;/p&gt; | **Proposal pending validation — sensitive point** (S5 principle 4 — « Fonctionnement collégial ») | New EN wording |
| 49 | `4c3003f` | `4c3003f` | S6 | container | S6 — Les deux autres pôles | — | — | No public text |  |
| 50 | `4c30033` | `4c30033` | S6 | container | S6 · En-tête | — | — | No public text |  |
| 51 | `4c30031` | `4c30031` | S6 | heading | S6 · H2 | Les deux autres pôles | The Other Two Areas of Work | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 52 | `4c30032` | `4c30032` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires.&lt;/p&gt; | &lt;p&gt;The association&#x27;s organization is based on three complementary areas established in its bylaws.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 53 | `4c3003e` | `4c3003e` | S6 | container | S6 · Grille des 2 pôles | — | — | No public text |  |
| 54 | `4c30038` | `4c30038` | S6 | container | S6 · Carte 1 — Pôle Formation et Intégration → P-04 | — | — | No public text |  |
| 55 | `4c30034` | `4c30034` | S6 | heading | S6 · H3 carte 1 | Pôle Formation et Intégration | Training and Integration | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 56 | `4c30035` | `4c30035` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt; | &lt;p&gt;This area reflects the association&#x27;s objectives relating to learning, skills development, and integration.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 57 | `4c30037` | `4c30037` | S6 | container | S6 · Bouton carte 1 | — | — | No public text |  |
| 58 | `4c30036` | `4c30036` | S6 | button | S6 · Bouton carte 1 → P-04 | Découvrir le pôle | Explore This Area | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 59 | `4c3003d` | `4c3003d` | S6 | container | S6 · Carte 2 — Pôle Animation Culturelle et Sociale → P-05 | — | — | No public text |  |
| 60 | `4c30039` | `4c30039` | S6 | heading | S6 · H3 carte 2 | Pôle Animation Culturelle et Sociale | Cultural and Social Activities | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 61 | `4c3003a` | `4c3003a` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;This area supports the objectives relating to culture, community activities, and social participation.&lt;/p&gt; | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 62 | `4c3003c` | `4c3003c` | S6 | container | S6 · Bouton carte 2 | — | — | No public text |  |
| 63 | `4c3003b` | `4c3003b` | S6 | button | S6 · Bouton carte 2 → P-05 | Découvrir le pôle | Explore This Area | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
| 64 | `4c30044` | `4c30044` | S7 | container | S7 — Appel à l’action | — | — | No public text |  |
| 65 | `4c30040` | `4c30040` | S7 | heading | S7 · H2 | Une question sur le fonctionnement de l&#x27;association ? | Have a Question About How the Association Works? | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 66 | `4c30041` | `4c30041` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez en savoir plus sur l&#x27;organisation de l&#x27;Association Amal Chabab Takaddoum, obtenir une information d&#x27;ordre administratif ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;Would you like to learn more about how Association Amal Chabab Takaddoum is organized, obtain administrative information, or explore opportunities for collaboration?&lt;/p&gt;<br>&lt;p&gt;Let&#x27;s connect to identify opportunities for exchange.&lt;/p&gt; | Not found in FR P-01/P-02 — new P-03 wording (imposed or proposal per § C) | New EN wording |
| 67 | `4c30043` | `4c30043` | S7 | container | S7 · Bouton | — | — | No public text |  |
| 68 | `4c30042` | `4c30042` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | Contact Us | Reused verbatim from FR P-01/P-02 (observed) | EN wording identical to EN P-01/P-02 |
