# P-06 Projects and Programs — English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**

Deliverables:
- `P06_Projets_Programmes_English_Elementor.json`
- `P06_Projets_Programmes_English_Correspondence_Table.md`
- this report

> ⚠️ **No import, visual test, responsive test or publication was carried out.** All checks are static checks on the JSON files.

---

## 1. Purpose and scope

The goal is an English (LTR) version of the French P-06 page. It uses the English copy supplied in the task prompt (§ 4.2). Structure, IDs, links, styling and page settings stay the same as the source.

The page remains a general presentation page. It is **not** a project catalog: no cards, listings, statistics or new calls to action were added.

## 2. Source files available and consulted

| File | Use | Status |
|---|---|---|
| `P06_Projets_Programmes_Elementor.json` (FR) | Authoritative structure and text | ✅ Used. SHA-256 `95ca36d6…e4816e1d`. **Not modified** (hash identical before and after). |
| English P-01 and P-02 templates and reports | Terminology consistency check | ✅ Consulted only. No wording was taken from them. |
| English P-03, P-04 and P-05 templates | Terminology check | ✅ Consulted only |
| Arabic P-06 template | Cross-check of IDs and collisions | ✅ Consulted only |
| Integrated project handover document v2.1 | Context | ⚠️ Not available in this session |

## 3. Missing P-06 documentation and its consequences

No P-06-specific technical documentation or editorial review sheet was identified. As a result:
- The **institutional approval status** of the P-06 texts is **not documented**. Every text block is recorded as *Source JSON — institutional approval status not documented*.
- No count of imposed, validated or proposed blocks is asserted.
- No P-06 arbitration list was reconstructed from other pages.
- Nothing was inferred or added from other pages.

## 4. Translation methodology

- The supplied English copy was integrated **block by block, exactly as supplied**. There was no retranslation, rewording or spelling change. The copy already uses American spelling.
- Each paragraph stays in the same `<p>` position as in the source.
- Editorial concerns are **reported, not corrected** (§ 5.2 and § 11).

## 5. English terminology choices

### 5.1 Applied (from task prompt § 4.3)

| French | English |
|---|---|
| Projets et programmes / Projet / Programme | Projects and Programs / Project / Program |
| Engagement associatif | Association's commitment |
| Domaines d'intervention | Areas of work |
| Éducation, formation, accompagnement, animation | Education, training, support, community engagement |
| Besoins identifiés | Identified needs |
| Participation des personnes et des communautés | Participation of individuals and communities |
| Projets réalisés / documentés | Projects implemented / documented projects |
| Programmes portés par l'association | Programs supported by the association |
| Nous contacter | Contact Us |

Projects, programs, initiatives and activities are kept as distinct concepts, as in the source.

### 5.2 Consistency with the English P-01 to P-05 (reported, not changed)

Three P-06 texts repeat French wording that also appears in P-01. Their supplied English differs from the English P-01 wording:

| P-06 element | French (identical to P-01) | P-06 English (supplied, integrated) | English P-01 wording |
|---|---|---|---|
| `e5c0004` §1 | À travers ses projets et programmes, Amal Chabab Takaddoum met en œuvre des initiatives dans ses domaines d'intervention. | Through its projects and programs, Amal Chabab Takaddoum implements initiatives in its areas of work. | Through its projects and programs, Association Amal Chabab Takaddoum works to carry out initiatives across its areas of work. |
| `e5c0004` §2 | Éducation, formation, accompagnement et animation : chaque initiative s'inscrit dans la volonté de répondre à des besoins identifiés… | Education, training, support and community engagement: each initiative reflects the commitment to responding to identified needs… | Education, training, support, and community activities: each initiative reflects the association's intention to respond to identified needs… |
| `e5c0007` | Découvrez les projets documentés et les programmes portés par l'association. | Explore the documented projects and programs supported by the association. | Explore the documented projects and programs in which the association is involved. |
| `e5c000c` | Vous souhaitez découvrir nos activités, échanger avec notre équipe ou envisager une collaboration… / Nous serons heureux d'échanger avec vous. | …exchange ideas with our team or explore opportunities for collaboration with… / We would be delighted to hear from you. | …get in touch with our team, or explore opportunities to collaborate with… / We would be pleased to hear from you and exchange ideas. |

Other terminology differences:
- **« Animation »** is rendered as *community engagement* here. Elsewhere it is *community activities* (English P-01, P-02) or *Engagement* (English P-05).
- **Association name:** “Amal Chabab Takaddoum” appears without “Association” in `e5c0004` §1, matching the French source. English P-01 adds “Association”.
- **Serial (Oxford) comma:** the supplied copy does not use it, while the English P-01 to P-04 do.
- **Areas of work:** consistent with English P-01 and P-02. English P-05 uses *areas of intervention*.

**Supervisor decision needed:** either align P-06 with the English P-01 wording for the shared sentences, or keep the P-06 wording.

## 6. Four-section structure (source order)

| Section | `_title` (kept) | Background | Content |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | H1 *Projects and Programs* (no subtitle, paragraph, button or image in the source, and none added) |
| S2 | S2 — Présentation | `#FFFFFF` | H2 and 2 paragraphs |
| S3 | S3 — Portefeuille de projets | `#F4F6F6` | H2, 1 paragraph and the archive button |
| S4 | S4 — Appel à l’action | `#152A33` | H2, 2 paragraphs and the Contact button |

No section was added to match the seven-section structure of P-01 to P-05.

## 7. Element and widget counts

| Type | Source | English |
|---|---|---|
| Root sections | 4 | 4 |
| Containers | 6 | 6 |
| Heading (1 H1, 3 H2) | 4 | 4 |
| Text editor | 3 | 3 |
| Button | 2 | 2 |
| **Elements** | **15** | **15** |

Hierarchy, types, `isInner` values and child counts are identical, checked node by node. No element was added, deleted, merged or reordered.

## 8. ID preservation and uniqueness

- **All 15 IDs are preserved** in source order: `e5c0002`, `e5c0001`, `e5c0005`, `e5c0003`, `e5c0004`, `e5c000a`, `e5c0006`, `e5c0007`, `e5c0009`, `e5c0008`, `e5c000f`, `e5c000b`, `e5c000c`, `e5c000e`, `e5c000d`.
- **Unique:** 15/15. No duplicates and none missing.
- **Shared** with the French P-06 only, which is intended. The Arabic P-06 uses its own `f6a…` range. No ID is shared with any other template.

## 9. Link and destination verification

| Location | English label | Target | Check |
|---|---|---|---|
| S3 button `e5c0008` | Discover All Our Projects | `/category/projets-programmes/` | ✅ Unchanged. Category archive. |
| S4 button `e5c000d` | Contact Us | `/contact/` | ✅ Unchanged |

- **Two distinct destinations:** the proposed P-06 page path is `/projets-et-programmes/`, while `/category/projets-programmes/` is the archive. The source JSON has no permalink field, and none was added.
- No English prefix or Polylang URL was invented.
- The archive button stays a browsing call to action, not a registration call to action.
- Until the Polylang association is done, both buttons lead to the **French** archive and Contact page.

## 10. Style and responsive preservation

- **Key-by-key diff:** only the text keys differ (`title` ×4, `editor` ×3, `text` ×2). Every other setting is identical.
- **Backgrounds:** unchanged (`#F4F6F6`, `#FFFFFF`, `#F4F6F6`, `#152A33`).
- **Typography and layout:** unchanged. This covers font sizes and their responsive variants, weights, line heights, text colors, custom widths (820, 780 and 760 px, reduced to 100% on mobile), paddings and button styles.
- **Page settings:** `template: elementor_header_footer` and `hide_title: yes` are unchanged.
- **Alignment and direction:** all 7 headings and texts are **centered** in the source and stay centered. No direction or alignment property was added.
- **Template name** (admin library only): `P-06 Projets et programmes (EN) — Association Amal Chabab Takaddoum`.
- **Additions:** none. No image, icon, form, catalog, card, extra widget, Pro widget, animation, header, menu or footer.

## 11. Editorial status limitations and open points

All 9 text blocks are recorded as *Source JSON — institutional approval status not documented*. They are **not** classified as imposed, validated or approved.

Points kept open for the supervisor:
1. The formal approval status of the P-06 source texts is not documented in any P-06-specific file.
2. No P-06 editorial review sheet or technical documentation was identified.
3. The proposed English page permalink must be checked against the site's language and URL conventions.
4. The archive target `/category/projets-programmes/` must remain distinct from the P-06 page path.
5. The SEO proposals (§ 12) require approval.
6. The final English terminology must be checked against the approved English P-01 to P-05, especially the wording differences in § 5.2.

Additional translation points flagged for review (source wording preserved):

| Element | Point |
|---|---|
| `e5c000c` §2 | « Nous serons heureux **d'échanger** avec vous » is rendered as “We would be delighted **to hear from you**”, which softens the idea of exchange. A closer option: “We would be pleased to hear from you and exchange ideas.” (wording used in English P-01). |
| `e5c0006` | “Projects Implemented by the Association” is faithful to « réalisés ». The page names no project and claims no completion or evaluation. |
| `e5c0003` | “Our Association's Commitment” adds the first-person possessive; the French reads « l'engagement associatif ». |

## 12. SEO proposals (not injected into the JSON)

| SEO element | Proposed value | Status |
|---|---|---|
| Page title | Projects and Programs | Translation proposal |
| Permalink | `/projets-et-programmes/` | To confirm against the site's URL conventions |
| Main keyword | Projects and Programs | Proposal |
| SEO title | Projects and Programs – Amal Chabab Takaddoum | Proposal |
| Meta description | Explore the projects and programs of Amal Chabab Takaddoum and learn how its initiatives support education, training, community engagement and participation. | Proposal |
| Category | Projects and Programs | Translation proposal. The source archive category is `/category/projets-programmes/`; the English category must be created and linked in Polylang manually. |

## 13. Tests performed and not performed

**Performed (static, on the JSON):**
- JSON syntax.
- Structure: 4 sections in order and 15 elements with identical hierarchy, types, `isInner` values and child counts. Heading levels: 1 H1 and 3 H2.
- IDs preserved, unique and in source order.
- Key-by-key settings diff, limited to the text keys.
- Backgrounds and page settings.
- Both link targets unchanged.
- All 9 supplied texts integrated.
- Automatic search: no French public text and no British spelling.
- Search for unwanted claims: no match for register, apply, enroll, book, catalog, completed, currently, active, partner, donor, funding or result.

**Not performed:**
- Elementor import.
- Rendering on desktop, tablet and mobile.
- Polylang association and behavior of the archive and Contact links.
- Display of the English category archive.
- Astra header and footer.

## 14. Known limitations and risks

- **Inconsistent wording across pages:** three texts share French wording with P-01 but have different English wording (§ 5.2).
- **Links lead to French pages** until the Polylang association is made. The English archive category may not exist yet.
- **Approval status unknown:** the P-06 texts have no documented approval status.
- **Rendering untested:** in particular, check wrapping of the S2 H2 on mobile.

## 15. Statement

**No import, publication or deployment was carried out.** WordPress, Elementor, Astra, Polylang and all global settings are unchanged. No project or program was created in WordPress. The French P-06 and the P-01 to P-05 pages (all languages) were not modified. The supervisor keeps exclusive authority over validation and implementation.
