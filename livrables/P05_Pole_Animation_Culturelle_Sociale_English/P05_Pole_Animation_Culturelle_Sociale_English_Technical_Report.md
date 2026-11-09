# P-05 Cultural and Social Engagement Department — English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**
Deliverables:
- `P05_Pole_Animation_Culturelle_Sociale_English_Elementor.json`
- `P05_Pole_Animation_Culturelle_Sociale_English_Correspondence_Table.md`
- this report

> ⚠️ **No import, visual test, responsive test, RTL test or publication was carried out.** All checks below are static checks on the JSON files.

---

## 1. Purpose and source files

**Purpose:** an English, LTR version of the French P-05 page. It uses the English copy supplied in the task prompt (§ 4.2) and keeps the structure, IDs, links, anchors, styling and editorial statuses unchanged.

| Source | Use | Status |
|---|---|---|
| `P05_Pole_Animation_Culturelle_Sociale_Elementor.json` | Structure and French text | ✅ Used. SHA-256 `7dcd0146…32c7c5c0`; **not modified** |
| `P05_Pole_Animation_Culturelle_Sociale_Documentation_Technique.md` | Technical reference | ⚠️ **Not received** in this session |
| `P05_Releve_Redactionnel.md` | 45-block classification and 7 arbitration points | ⚠️ **Not received**. Statuses are taken from the labels in the task prompt § 4.2. See § 9. |
| `P03_Pole_Administration_Gestion_Elementor.json` (FR) | Style-fingerprint reference | ✅ Used for comparison only; not modified |
| English P-01 and P-02 (validated references) | Terminology comparison | ✅ Used for comparison only; **no wording was changed because of them** (see § 2.3) |
| English P-03 and P-04 | Not used as an editorial source, as instructed | Consulted only to report naming discrepancies |

## 2. Translation methodology and terminology choices

### 2.1 Method

- **Text:** the English copy in § 4.2 was integrated **block by block, as supplied**. No retranslation, no rewording, no addition.
- **Sentence-level blocks:** when one Elementor paragraph holds two blocks with different statuses (S2 § 1, S3 card 3), the two sentences are joined in a single `<p>`, exactly as in the French source.
- **Spelling normalization:** rule 4.1 requires American spelling, but the supplied copy uses British forms. These were normalized, and **only these**; no wording or meaning was changed:

| Element | Supplied | Integrated |
|---|---|---|
| `6e5000d` § 3 | organisation, programme | organization, program |
| `6e50010` | organised | organized |
| `6e5001e` § 2, § 3 | organisation (×2), programmes | organization, programs |
| `6e5002a` | Recognising | Recognizing |
| `6e5002d` | programmes | programs |
| `6e50032` | organisation | organization |
| `6e50035` | organisation | organization |

Each normalization is also marked in the correspondence table. To revert to the supplied spelling, these 10 words are the only changes.

### 2.2 Terminology applied (as supplied, § 4.3)

| French | English |
|---|---|
| Pôle Animation Culturelle et Sociale | Cultural and Social Engagement Department |
| Pôle Administration et Gestion | Administration and Management Department |
| Pôle Formation et Intégration | Training and Integration Department |
| Animation | Engagement |
| Participation sociale | Social Participation |
| Fonctionnement collégial | Collegial Functioning |
| Bureau exécutif / Assemblée générale | Executive Board / General Assembly |
| Orientations statutaires / statuts | Statutory orientations / statutes |
| Domaines d'intervention | Areas of intervention |

### 2.3 ⚠️ Terminology discrepancies with the English P-01 to P-04 — reported, not changed

The prompt says the department names “must remain consistent with the P01–P04 English pages”. It also says that if a validated P-01 or P-02 English version uses a different equivalent, the discrepancy must be **reported rather than silently changed**. The supplied P-05 copy does differ:

| Concept | P-05 (supplied, integrated) | EN P-01 / P-02 (validated) | EN P-03 / P-04 (unvalidated) |
|---|---|---|---|
| *Pôle* | **Department** | **area of work / area** | area of work / area |
| Pôle Animation Culturelle et Sociale | **Cultural and Social Engagement Department** | **Cultural and Social Activities** | Cultural and Social Activities |
| Pôle Administration et Gestion | Administration and Management **Department** | Administration and Management | Administration and Management |
| Pôle Formation et Intégration | Training and Integration **Department** | Training and Integration | Training and Integration |
| *Animation* | Engagement | community activities (EN P-02) | community activities |
| statuts | **statutes** | **bylaws** | bylaws |
| orientations statutaires | statutory orientations | statutory objectives (EN P-02) | statutory objectives |
| domaines d'intervention | areas of intervention | — | **fields of work** |
| « Découvrir le pôle » | Discover the Department | **Explore This Area** (EN P-01) | Explore This Area |
| « Sa contribution » | **Our** Contribution | — | Its Contribution |
| « Fonctionnement collégial » | Collegial Functioning | — | Shared Governance (EN P-03) |
| supervision du Bureau exécutif | supervision | oversight (EN P-02) | oversight |

**Validated texts with different English wording:** these blocks are labeled “validated / reused”, but their English text differs from the existing English version of the same validated French text:

| Element | P-05 supplied English | Existing English version |
|---|---|---|
| `6e50002` subtitle | A department that values culture, social activities and collective initiatives as spaces for connection, participation and community ties. | EN P-01 S3 card 3: “This area promotes culture, social activities, and collective initiatives as opportunities for connection, participation, and stronger community ties.” |
| `6e50024` Responsibility | Making a commitment through a serious and constructive approach. | EN P-02: “Making a serious and constructive approach central to commitment.” |
| `6e50027` Solidarity | Promoting mutual support, volunteering and cooperation. | EN P-02: “Developing mutual support, volunteering, and cooperation.” |
| `6e5002a` Initiative | Recognizing talents, ideas and the capacity to take action. | EN P-02: “Recognizing talents, ideas, and the ability to take action.” |
| `6e50035` Administration card | It contributes to the organization and functioning of the association. | EN P-02: “This area contributes to organizing the association and supporting the operation of its organizational structure.” |
| `6e5003a` Training card | It supports the orientations relating to learning, skills development and integration. | EN P-02: “This area reflects the association's objectives relating to learning, skills development, and integration.” |

**Punctuation:** the supplied copy does not use the serial (Oxford) comma; the English P-01 to P-04 do. It was left as supplied.

**Supervisor decision needed:** choose one terminology set for all English pages (*Department* vs. *area of work*, *statutes* vs. *bylaws*, the department names and the button label), then harmonize either P-05 or P-01 to P-04 accordingly. **No other page was modified.**

## 3. Complete structural inventory

| Item | Source | English |
|---|---|---|
| Root sections | 7 | 7 |
| Elements | 68 | 68 |
| Containers | 29 | 29 |
| Widgets | 39 | 39 |
| — heading | 16 | 16 |
| — text-editor | 17 | 17 |
| — button | 5 | 5 |
| — image | 1 | 1 |
| Heading levels | 1 H1 · 6 H2 · 9 H3 | 1 H1 · 6 H2 · 9 H3 |

No element was added, deleted, merged or reordered.

## 4. Section-by-section description

| Section | `_title` (kept in French) | Background | English content |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | H1 *Cultural and Social Engagement Department*; subtitle; 2 paragraphs; buttons *Areas of Intervention* (`#missions`) and *Our Contribution* (`#contribution`); image placeholder |
| S2 | S2 — Présentation | `#FFFFFF` | H2 *A Department Dedicated to Culture and Social Participation*; 3 paragraphs |
| S3 | S3 — Trois domaines d'intervention (anchor `#missions`) | `#F4F6F6` | H2 *Three Areas of Intervention*; intro; cards in order: **Culture**, **Engagement**, **Social Participation** |
| S4 | S4 — Contribution transversale (anchor `#contribution`) | `#FFFFFF` | H2 *A Cross-Cutting Contribution to the Other Departments*; 3 paragraphs |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | H2 *The Principles That Guide Its Work*; intro; cards in order: **Responsibility**, **Solidarity**, **Initiative**, **Collegial Functioning** |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | H2 *The Other Two Departments*; intro; 2 cards with *Discover the Department* |
| S7 | S7 — Appel à l’action | `#152A33` | H2 *Questions About This Department's Areas of Work?*; 2 paragraphs; *Contact Us* |

## 5. Element and widget counts

See § 3. Only the text keys changed: `title` ×14, `editor` ×17 and `text` ×5. The headings “Culture” and “Initiative” are the same in both languages.

## 6. ID preservation and uniqueness

- **All 68 IDs are preserved** and appear in the same order as in the source (`6e5…`). They were not regenerated.
- **Unique:** 68 of 68.
- **Shared IDs:** the 68 IDs are shared with the French P-05 and with the Arabic P-05, which also keeps the source IDs. This is intended. They are shared with no other template.

## 7. Navigation and link verification

| Location | English label | Target | Check |
|---|---|---|---|
| S1 button 1 `6e50004` | Areas of Intervention | `#missions` | ✅ Anchor on the S3 container `6e5001c` |
| S1 button 2 `6e50005` | Our Contribution | `#contribution` | ✅ Anchor on the S4 container `6e5001f` |
| S6 card 1 `6e50036` | Discover the Department | `/nos-poles/administration-et-gestion/` | ✅ Unchanged · ⚠️ English page to be associated in Polylang |
| S6 card 2 `6e5003b` | Discover the Department | `/nos-poles/formation-et-integration/` | ✅ Unchanged · ⚠️ English page to be associated |
| S7 `6e50042` | Contact Us | `/contact/` | ✅ Unchanged · ⚠️ English page to be associated |

No English prefix, Polylang URL or new URL structure was created. Until the three page links are replaced, they lead to the French pages.

## 8. Style and responsive preservation

- **Key-by-key diff:** every setting other than the text keys is identical to the French P-05.
- **Style fingerprint:** compared with the French **P-03**, the shape of the tree and every non-text setting are **identical** across the 7 sections. The zero-difference result documented for P-05 is therefore maintained.
- **Colors present:** `#1F4E5F`, `#152A33`, `#45555C`, `#F4F6F6`, `#FFFFFF`, `#E1E7E8`, `#C7D2D6`, and the transparent `#00000000` used by the outline button. No new color was introduced.
- **Unchanged layout values:**
  - typography for desktop, tablet and mobile;
  - weights and line heights;
  - margins, paddings and card radii;
  - widths (58/38, 33/48/100, 48/48/100, 820 and 760 px → 100% on mobile);
  - `flex_wrap` and `flex_direction_mobile`.
- **Unchanged page settings:** `template: elementor_header_footer` and `hide_title: yes`.
- **Alignment and direction:** no direction or alignment property was added, and there is no RTL setting. The 12 centered elements stay centered. The 21 others inherit LTR start alignment.
- **Image placeholder:** kept in S1, with its URL unchanged. The `alt` field stays **empty**, and the proposed alt text (§ 11) is **not injected**.
- **No additions:** no header, menu, footer, form, plugin, Pro widget or animation.
- **Template name** (admin library only): `P-05 Pôle Animation Culturelle et Sociale (EN) — Amal Chabab Takaddoum`.

## 9. Editorial status distribution

The statuses come from the labels in task prompt § 4.2. The relevé itself was not received.

| Status | Prompt § 2.2 (relevé) | Labels in § 4.2 (applied) |
|---|---|---|
| Imposed | 13 | **14** |
| Validated / Reused | 15 | **15** |
| Proposal to Validate | 17 | **17** |
| **Total** | **45** | **46** |

⚠️ **Count discrepancy:** the copy in § 4.2 labels **46** blocks, 14 of them imposed, while the relevé totals are 45 blocks with 13 imposed. The 14 imposed blocks are:
- the H1;
- the 2 S1 buttons;
- S2 § 2;
- the S3 H2 and the 3 card headings;
- the second sentence of S3 card 3;
- the S4 H2 and the S6 H2;
- the 2 S6 buttons;
- the S7 button.

One of these is probably counted differently in the relevé, for example the two identical S6 buttons counted as one block. **No block was reclassified.** The 15 validated and 17 proposal blocks match the relevé exactly. The supervisor should reconcile the imposed blocks against the relevé.

**The 17 proposals remain proposals.** Their translation does not validate them. They include “Collegial Functioning” (heading and text), both Executive Board paragraphs (S2 § 3 and S4 § 3), and the S7 call to action.

Full block-level list: correspondence table, part B.

## 10. Editorial arbitration points kept for the supervisor

| # | Point | Treatment in this version |
|---|---|---|
| 1 | Approval, correction or replacement of the 17 proposed blocks | Kept as proposals; translated as supplied |
| 2 | Proposed principle “Collegial Functioning” | Kept as a proposal (`6e5002c`, `6e5002d`); not presented as an approved statutory principle |
| 3 | Keeping “sports” in the Culture card | **Kept**: validated P-02 formulation describing the statutory scope, not a department activity |
| 4 | Executive Board wording differs from the statutes (S2 § 3, S4 § 3) | Source wording translated faithfully; **not corrected** |
| 5 | Pending correction on document-keeping responsibilities in P-03 | **P-03 not modified** |
| 6 | Ideological references and statutory formulations excluded from P-05 | Still excluded; nothing reintroduced |
| 7 | Approval of the SEO proposals | Proposals only (§ 11) |

Additional points raised by this translation:
- **8:** the terminology alignment with the English P-01 to P-04 (§ 2.3).
- **9:** the 45/46 and 13/14 block count (§ 9).
- **10:** “Our Contribution” vs. French « Sa contribution », which means “its contribution”.

Inputs the supervisor may request separately and that **were not created or substituted**: the official logo or visual identity, and the institutional image for the department.

## 11. SEO proposals (not injected into the JSON)

| SEO element | Proposed English value | Status |
|---|---|---|
| Permalink | `/nos-poles/animation-culturelle-et-sociale/` | Imposed (unchanged) |
| Main keyword | Cultural and Social Engagement Department | Proposal |
| SEO title | Cultural and Social Engagement Department – Amal Chabab Takaddoum | Proposal |
| Meta description | Discover the Cultural and Social Engagement Department of Amal Chabab Takaddoum, its statutory orientations in culture, engagement and social participation, and its contribution to the association. | Proposal |
| Image alt text | Cultural and Social Engagement Department of Association Amal Chabab Takaddoum | Proposal |
| WordPress page title | Cultural and Social Engagement Department | Translation of the source title |

Notes for the supervisor:
- The proposed SEO title and meta description use “Amal Chabab Takaddoum” without “Association”, as supplied.
- The permalink stays French. The English URL depends on the Polylang configuration.

## 12. Tests performed and not performed

**Performed (static, on the JSON):**
- **Structure:** JSON syntax; 7 sections in order; 68 elements with the same hierarchy, types, `isInner` and child counts; heading levels 1/6/9; S3 and S5 card order.
- **Identifiers:** preserved, unique and in source order.
- **Settings:** key-by-key diff limited to the text keys; style-fingerprint comparison with the French P-03.
- **Navigation:** both anchors match their targets; the 5 targets are unchanged.
- **Text:** all 46 supplied blocks integrated; automatic search shows no French text and no remaining British spelling.
- **Prohibited content:** automatic search for festival, seminar, exhibition, workshop, camp, theatre/theater, academy, club, tournament, performance, concert, internship, register, apply, enrol/enroll, book, admission, catalog and available found **0** matches.

**Not performed:**
- Elementor import.
- Rendering on desktop, tablet and mobile, including line breaks of the long H1 and S2/S4 H2.
- Anchor scrolling under a fixed Astra header.
- Polylang association and link behavior.
- Astra header and footer.
- Any RTL or LTR rendering test.

## 13. Known limitations and risks

- **Terminology mismatch:** if published unchanged, P-05 would name the departments differently from the English P-01 to P-04 (§ 2.3). This is the main editorial risk.
- **Status traceability:** statuses come from the task prompt, not from the relevé, which was not received. The imposed-block count differs by one (§ 9).
- **Spelling:** spelling was normalized to American English (§ 2.1). This is reversible.
- **Untested rendering:** rendering is untested, and the H1 (41 characters) and some H2 headings may wrap differently from the French.
- **Links:** the links lead to the French pages until the Polylang association is done.

## 14. Statement

**No import, publication or deployment was carried out.**
- No change was made to WordPress, Elementor, Astra, Polylang or global settings.
- The French P-05 and the P-01 to P-04 pages, in every language, were not modified.

The supervisor retains exclusive authority over validation and implementation.
