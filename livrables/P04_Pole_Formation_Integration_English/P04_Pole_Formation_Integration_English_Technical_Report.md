# P-04 Training and Integration — American English Version (LTR) — Technical Report

**Association Amal Chabab Takaddoum — Rabat, Morocco**
Deliverable: `P04_Pole_Formation_Integration_English_Elementor.json`

> ⚠️ **Status: translation proposal pending supervisor validation.** This English version is a translation I prepared from the French source. Translating a French proposal does **not** validate its content.

---

## 1. Objective and sources

**Objective:** an American English, LTR version of the French P-04 page. It keeps the source structure, identifiers, links, anchors and design. Its terminology is consistent with the English P-01, P-02 and P-03.

| Source | Use | Status |
|---|---|---|
| `P04_Pole_Formation_Integration_Elementor.json` (FR) | Structure and texts to translate | ✅ Used. SHA-256 `7dd41dec…e3e6b3de`, **not modified** |
| `P04_Pole_Formation_Integration_Documentation_Technique.md` | Technical reference | ⚠️ **Not received** |
| `P04_Releve_Redactionnel.md` | Block classification (§ 0–1), historical activities (§ 2) | ⚠️ **Not received**. The classification was rebuilt from the task prompt; see section 9. |
| English P-01, P-02 and P-03 templates | Reference terminology | ✅ Used |
| Arabic P-04 template | Structural cross-check (same tree and IDs) | ✅ Used |

## 2. Structure of the seven sections (order preserved)

| # | Section (`_title`, kept in French) | Background | Content |
|---|---|---|---|
| S1 | S1 — Bannière | `#F4F6F6` | 2 columns (58% / 38%). Left: H1, subtitle, text and 2 anchor buttons. Right: image placeholder. |
| S2 | S2 — Présentation | `#FFFFFF` | Centered H2 and 3-paragraph text (820 px) |
| S3 | S3 — Domaines d'intervention (anchor `#missions`) | `#F4F6F6` | Centered header (H2 and 2-paragraph intro with guard sentence) and 4 cards (48% → 48% → 100%) |
| S4 | S4 — Contribution transversale (anchor `#contribution`) | `#FFFFFF` | Centered H2 and 3-paragraph text |
| S5 | S5 — Principes de fonctionnement | `#F4F6F6` | Centered header and 4 cards: Equality and Social Justice, Solidarity, Initiative, Responsibility |
| S6 | S6 — Les deux autres pôles | `#FFFFFF` | Centered header and 2 area cards with buttons |
| S7 | S7 — Appel à l’action | `#152A33` | Centered H2, text and Contact button |

## 3. Element count and heading hierarchy

| Type | Source | English |
|---|---|---|
| `container` | 30 | 30 |
| `heading` | 17 | 17 |
| `text-editor` | 18 | 18 |
| `button` | 5 | 5 |
| `image` | 1 | 1 |
| **Total** | **71** (30 containers + 41 widgets) | **71** |

**Heading hierarchy preserved: 1 H1, 6 H2, 10 H3.**

| Level | English headings |
|---|---|
| H1 | Training and Integration |
| H2 | An Area of Work Supporting Learning and Integration · The Area's Fields of Work · A Cross-Cutting Contribution to the Other Areas · The Principles That Guide Its Work · The Other Two Areas of Work · Have a Question About This Area's Objectives? |
| H3 | Education and Learning · Non-Formal Education and Literacy · Vocational Training and Qualifications · Social and Professional Integration · Equality and Social Justice · Solidarity · Initiative · Responsibility · Administration and Management · Cultural and Social Activities |

## 4. Identifiers

**The 71 source identifiers are kept unchanged** (brief 5.5).
- They are unique within the file (71/71).
- They are identical to the French P-04 and to the Arabic P-04, which also kept the source IDs. This is intended.
- No ID is shared with any other template.

## 5. Graphic, responsive and direction settings

- **No setting modified.** A key-by-key diff of every `settings` object shows that only the text keys differ: `title` ×16, `editor` ×18 and `text` ×5. The heading “Initiative” is the same in both languages.
- **Preserved:**
  - colors;
  - typography for desktop, tablet and mobile (H1 44/38/30; H2 34/30/26; H3 20/20/19 and 18/18/17; texts 20/19/17, 18/17/16, 17/17/16, 16/16/15);
  - widths (58/38 and 48/48/100; 820 and 780 px, reduced to 100% on mobile);
  - paddings, `flex_gap`, `flex_wrap` and `flex_direction_mobile`;
  - `template: elementor_header_footer` and `hide_title: yes`.
- **LTR:** no direction or alignment property was added, and **no RTL setting** was introduced.
  - The 12 centered elements stay centered.
  - The 23 headings and texts without an alignment setting inherit left alignment.
  - The text column stays on the left and the image on the right.
  - The source's direction-neutral layout is unchanged: symmetric spacing, no fixed left or right alignment, no absolute positioning. It is shared by all language versions.
- **Template name** (admin library only): `P-04 Pôle Formation et Intégration (EN) — Amal Chabab Takaddoum`.
- **Image placeholder:** the native Elementor placeholder is kept, with its URL unchanged and an empty `alt`. The proposed alt text in section 7 is **not injected**.
- **No added widgets or features:** no Pro widget, form, menu, header, footer or animation.

## 6. Links and anchors

| Element | English label | Target (unchanged) | Check |
|---|---|---|---|
| `5d40004` S1 button 1 | Its Fields of Work | `#missions` → S3 container `5d4001f` | ✅ Anchor present |
| `5d40005` S1 button 2 | Its Contribution | `#contribution` → S4 container `5d40022` | ✅ Anchor present |
| `5d40039` S6 card 1 | Explore This Area | `/nos-poles/administration-et-gestion/` | ⚠️ French target kept. Associate the English P-03 in Polylang. |
| `5d4003e` S6 card 2 | Explore This Area | `/nos-poles/animation-culturelle-et-sociale/` | ⚠️ French target kept. Associate the English P-05. |
| `5d40045` S7 button | Contact Us | `/contact/` | ⚠️ French target kept. Associate the English Contact page. |

No English URL or Polylang language prefix was invented. Until the three page links are replaced, they lead to the **French** pages.

## 7. Proposed SEO metadata (not injected — **unapproved proposals**)

| Field | Proposal |
|---|---|
| SEO title | Training and Integration \| Association Amal Chabab Takaddoum |
| Meta description | The Training and Integration area of Association Amal Chabab Takaddoum reflects the association's statutory objectives in education and learning, non-formal education and literacy, vocational training, and social and professional integration. |
| Primary keyword | training and integration nonprofit Rabat |
| Image alt text | Association Amal Chabab Takaddoum — Training and Integration |
| Slug (unapproved) | `training-and-integration` |

These proposals present statutory objectives, **not** an open training offer. They contain no enrollment, application or course vocabulary.

## 8. Terminology and translation choices

### 8.1 Aligned with English P-01 / P-02 / P-03

| French | English | Reference |
|---|---|---|
| Pôle Formation et Intégration / Administration et Gestion / Animation Culturelle et Sociale | Training and Integration / Administration and Management / Cultural and Social Activities | EN P-01, P-02, P-03 |
| pôle | area of work / area | EN P-01, P-02 |
| domaine(s) d'intervention | field(s) of work | EN P-03 (keeps “area” for *pôle*) |
| orientations statutaires / orientations | statutory objectives / objectives | EN P-02, P-03 |
| statuts · Bureau exécutif · Assemblée générale · commissions · pôles de travail | bylaws · Executive Board · General Assembly · committees · working areas | EN P-02, P-03 |
| éducation non formelle · lutte contre l'illettrisme · formation professionnelle · accompagnement éducatif | non-formal education · literacy · vocational training · educational support | EN P-02 |
| Sous-titre S1 (validated, P-01) | identical to EN P-01 S3 card 2 | EN P-01 |
| Texte S1 § 1, S6 card texts (validated, P-02) | identical to EN P-02 | EN P-02 |
| 4 principles (validated, P-02) | identical to EN P-02 value texts | EN P-02 |
| Ses domaines d'intervention · Sa contribution · Découvrir le pôle · Nous contacter | Its Fields of Work · Its Contribution · Explore This Area · Contact Us | EN P-03, EN P-01 |
| S2 § 3, S4 § 1 and § 3 (wording shared with P-03) | identical to EN P-03, except S4 § 3 (see T4) | EN P-03 |

### 8.2 New choices on this page (supervisor review)

| # | ID | French | English | Rationale and alternatives |
|---|---|---|---|---|
| T1 | `5d40018` | Formation professionnelle et qualification | Vocational Training and **Qualifications** | “Qualifications” renders the acquisition of skills recognition, without implying a certification offer. Alternative: “Vocational Training and Skills Qualification”. |
| T2 | `5d40016` | apprentissages conduits en dehors des cadres scolaires habituels | learning that takes place outside conventional school settings | General definition, as in the source. No program is implied. |
| T3 | `5d4001c` | L'intégration constitue la finalité… | Integration is the **goal** to which the other fields contribute | Faithful to the source. It remains an **editorial interpretation and a proposal**. |
| T4 | `5d40021` § 3 | Cette **articulation** s'exerce… | This **coordination** is carried out… | P-03 used a different French word (« fonction d'appui » → “support role”). |
| T5 | `5d40010` § 2 | les activités effectivement ouvertes à un moment donné | the activities actually available at any given time | The guard sentence is kept, and it is clear the page is not a catalog. |
| T6 | `5d40012` | Éducation et apprentissage | Education and Learning | “Learning” is preferred to “apprenticeship”, which would suggest a specific program. |
| T7 | — | — | — | Nothing was strengthened. The texts keep “reflects”, “is expected to work”, “provided for”, “viewed as” and “oversight of the Executive Board”. No objective is presented as a delivered service. |

## 9. Editorial validation status

The relevé (`P04_Releve_Redactionnel.md`) was **not received**. The classification was **rebuilt from the statuses stated in the task prompt**:
- S1 statuses are given block by block.
- S2: membership and supervision are proposals; the learning sentence and the non-formal education paragraph are validated.
- S3 and S4 card and paragraph texts are proposals; the 4 domain headings are imposed (see below).
- S5: the 4 principles are validated; the selection, H2 and intro are proposals.
- S6: the intro, card texts, area names and buttons are validated; the H2 is a proposal.
- S7: the H2 and paragraphs are proposals; the button is validated.

The French JSON contains 47 text blocks (headings, buttons and `<p>` paragraphs). Splitting S2 § 1 into its two sentences, as the prompt does, gives **48 blocks**. The resulting counts **match the relevé exactly**:

| Status | Blocks |
|---|---|
| Imposed: H1 and the 4 domain headings | **5** |
| Validated — reused from P-01/P-02 | **20** |
| **Proposals pending validation** | **23** |
| **Total** | **48** |

The **4 domain headings** were classified as imposed by deduction: the prompt says they cover the 7 orientations of the brief, and this is the only assignment consistent with the 5 imposed blocks. **To be confirmed against the relevé.**

Other points to keep in view:
- **The choice of 4 values among the 6 of P-02 is an editorial proposal.** Citizenship and Tolerance are not shown; their absence implies no institutional ranking.
- The 23 proposals remain proposals. Translating them does not validate them.

### Historical activities — explicit confirmation

These historical activities are **absent** from the English JSON, as they are from the French source:
- catering, cooking and service;
- Arabic-language learning;
- preschool education.

They appear in no visible, hidden or masked block. The conditional alternative historical block in the relevé (§ 2) was **not translated or integrated**.

An automatic search of the English JSON finds none of these terms: enroll, register, apply, application, sign up, course, session, fee, schedule, cooking, catering, Arabic, preschool. The only match for “catalog” is the guard sentence “It is not a catalog”.

## 10. Limitations, checks and manual integration

### 10.1 Checks performed (static, on the JSON)

- The JSON is valid.
- There are 7 sections in order and 71 elements with an identical hierarchy, types, `isInner` and child counts.
- The IDs are kept and unique, and the heading levels are 1 H1, 6 H2 and 10 H3.
- All visible texts are translated (39 text fields, 48 blocks), and no French public text remains (automatic search).
- The anchors match their sections, and the 5 links are unchanged.
- The image placeholder is unchanged, and no prohibited vocabulary was found.

### 10.2 Not performed — to check after a real import

- Import into Elementor.
- Rendering on desktop, tablet and mobile, including line breaks of the longer H2 and H3 headings and of the buttons.
- Anchor scrolling, since a fixed Astra header may cover the target.
- Polylang association and link behavior, and the Astra header and footer.
- **RTL reservation:** the source layout is direction-neutral and has not been tested under real RTL or LTR rendering. This English version has not been tested either.

### 10.3 Manual integration instructions

1. Validate the English wording and the 48 block statuses (sections 8, 9 and 11).
2. In Elementor → Templates, import the JSON and insert it into a new page.
3. In Polylang, assign the page to English and link it to the French P-04 (`/nos-poles/formation-et-integration/`).
4. Replace the 3 page links (section 6) once the English P-03, P-05 and Contact pages exist.
5. Replace the image placeholder. Apply the approved alt text and SEO metadata through the usual settings, not the template.
6. Do not modify Astra, Elementor, Polylang or any global settings.

## 11. Editorial tracking — 48 blocks

| Block | Element ID | Widget | French block | English block | Editorial status | Source / note |
|---|---|---|---|---|---|---|
| 1 | `5d40001` | heading | Pôle Formation et Intégration | Training and Integration | Imposed | brief |
| 2 | `5d40002` | text-editor | Un pôle orienté vers l&#x27;apprentissage, le développement des compétences et les initiatives favorisant l&#x27;intégration sociale et professionnelle. | This area focuses on learning, skills development, and initiatives that support social and professional integration. | Validated — reused | P-01 |
| 3 | `5d40003` | text-editor | Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration. | This area reflects the association&#x27;s objectives relating to learning, skills development, and integration. | Validated — reused | P-02 |
| 4 | `5d40003` | text-editor | Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association. | Its fields of work fall within the association&#x27;s statutory objectives. | **Proposal pending validation** |  |
| 5 | `5d40004` | button | Ses domaines d&#x27;intervention | Its Fields of Work | **Proposal pending validation** |  |
| 6 | `5d40005` | button | Sa contribution | Its Contribution | **Proposal pending validation** |  |
| 7 | `5d4000c` | heading | Un pôle au service de l&#x27;apprentissage et de l&#x27;intégration | An Area of Work Supporting Learning and Integration | **Proposal pending validation** |  |
| 8 | `5d4000d` (a) | text-editor | Le Pôle Formation et Intégration est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. | The Training and Integration area is one of the three areas of work established in the bylaws of Association Amal Chabab Takaddoum. | **Proposal pending validation** | membership in the three areas |
| 9 | `5d4000d` (b) | text-editor | Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration. | It reflects the association&#x27;s objectives relating to learning, skills development, and integration. | Validated — reused | P-02 |
| 10 | `5d4000d` | text-editor | Les orientations statutaires accordent une place importante à l&#x27;éducation non formelle, à la lutte contre l&#x27;illettrisme, à la formation professionnelle et à l&#x27;accompagnement éducatif des enfants et des jeunes. | The association&#x27;s statutory objectives place particular importance on non-formal education, literacy, vocational training, and educational support for children and young people. | Validated — reused | P-02 |
| 11 | `5d4000d` | text-editor | Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale. | In accordance with the bylaws, the organization of the working areas and the monitoring of program implementation fall under the oversight of the Executive Board, elected by the General Assembly. | **Proposal pending validation** | supervision |
| 12 | `5d4000f` | heading | Les domaines d&#x27;intervention du pôle | The Area&#x27;s Fields of Work | **Proposal pending validation** |  |
| 13 | `5d40010` | text-editor | Les orientations statutaires de l&#x27;association définissent les domaines dans lesquels le pôle est appelé à intervenir. | The association&#x27;s statutory objectives define the fields in which the area is expected to work. | **Proposal pending validation** |  |
| 14 | `5d40010` | text-editor | Cette page présente ces orientations. Elle ne constitue pas un catalogue : les activités effectivement ouvertes à un moment donné font l&#x27;objet d&#x27;une information distincte. | This page presents these objectives. It is not a catalog: information about the activities actually available at any given time is provided separately. | **Proposal pending validation** | S3 guard sentence — kept |
| 15 | `5d40012` | heading | Éducation et apprentissage | Education and Learning | Imposed | domain title |
| 16 | `5d40013` | text-editor | L&#x27;éducation et l&#x27;apprentissage figurent parmi les orientations statutaires du pôle. Ce domaine englobe l&#x27;accompagnement éducatif des enfants et des jeunes prévu par les statuts de l&#x27;association. | Education and learning are among the area&#x27;s statutory objectives. This field includes the educational support for children and young people provided for in the association&#x27;s bylaws. | **Proposal pending validation** | domain text |
| 17 | `5d40015` | heading | Éducation non formelle et alphabétisation | Non-Formal Education and Literacy | Imposed | domain title |
| 18 | `5d40016` | text-editor | Les statuts accordent une place à l&#x27;éducation non formelle et à la lutte contre l&#x27;illettrisme. Ce domaine désigne les apprentissages conduits en dehors des cadres scolaires habituels. | The bylaws give a place to non-formal education and literacy. This field refers to learning that takes place outside conventional school settings. | **Proposal pending validation** | domain text; 2nd sentence = general definition |
| 19 | `5d40018` | heading | Formation professionnelle et qualification | Vocational Training and Qualifications | Imposed | domain title |
| 20 | `5d40019` | text-editor | La formation professionnelle et la qualification constituent un domaine d&#x27;intervention prévu par les orientations statutaires, envisagé comme un appui au développement des compétences. | Vocational training and qualifications are a field of work provided for in the statutory objectives, viewed as a way of supporting skills development. | **Proposal pending validation** | domain text |
| 21 | `5d4001b` | heading | Intégration sociale et professionnelle | Social and Professional Integration | Imposed | domain title |
| 22 | `5d4001c` | text-editor | L&#x27;intégration constitue la finalité à laquelle les autres domaines concourent : favoriser les initiatives qui soutiennent la participation sociale et professionnelle. | Integration is the goal to which the other fields contribute: encouraging initiatives that support social and professional participation. | **Proposal pending validation** | integration as goal = editorial interpretation |
| 23 | `5d40020` | heading | Une contribution transversale aux autres pôles | A Cross-Cutting Contribution to the Other Areas | **Proposal pending validation** |  |
| 24 | `5d40021` | text-editor | La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités. | The area&#x27;s contribution is not limited to its own scope: it also supports the conditions under which the other two statutory areas carry out their activities. | **Proposal pending validation** |  |
| 25 | `5d40021` | text-editor | Les apprentissages, le développement des compétences et les initiatives d&#x27;intégration rejoignent les orientations portées par le Pôle Animation Culturelle et Sociale, tandis que le Pôle Administration et Gestion contribue à l&#x27;organisation et aux moyens nécessaires à leur conduite. | Learning, skills development, and integration initiatives connect with the objectives of the Cultural and Social Activities area, while the Administration and Management area contributes to the organization and resources needed to carry them out. | **Proposal pending validation** |  |
| 26 | `5d40021` | text-editor | Cette articulation s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis. | This coordination is carried out within the framework defined by the bylaws, with the Executive Board overseeing the organization of committees and working areas, as well as monitoring the implementation of established programs. | **Proposal pending validation** |  |
| 27 | `5d40023` | heading | Les principes qui guident son fonctionnement | The Principles That Guide Its Work | **Proposal pending validation** |  |
| 28 | `5d40024` | text-editor | Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association. | The area&#x27;s work is guided by the principles that shape the association&#x27;s commitment. | **Proposal pending validation** |  |
| 29 | `5d40026` | heading | Égalité et justice sociale | Equality and Social Justice | Validated — reused | P-02 |
| 30 | `5d40027` | text-editor | Promouvoir des relations fondées sur le respect des droits et de la dignité. | Promoting relationships based on respect for rights and dignity. | Validated — reused | P-02 |
| 31 | `5d40029` | heading | Solidarité | Solidarity | Validated — reused | P-02 |
| 32 | `5d4002a` | text-editor | Développer l&#x27;entraide, le bénévolat et la coopération. | Developing mutual support, volunteering, and cooperation. | Validated — reused | P-02 |
| 33 | `5d4002c` | heading | Initiative | Initiative | Validated — reused | P-02 |
| 34 | `5d4002d` | text-editor | Valoriser les talents, les idées et les capacités d&#x27;action. | Recognizing talents, ideas, and the ability to take action. | Validated — reused | P-02 |
| 35 | `5d4002f` | heading | Responsabilité | Responsibility | Validated — reused | P-02 |
| 36 | `5d40030` | text-editor | Inscrire l&#x27;engagement dans une démarche sérieuse et constructive. | Making a serious and constructive approach central to commitment. | Validated — reused | P-02 |
| 37 | `5d40034` | heading | Les deux autres pôles | The Other Two Areas of Work | **Proposal pending validation** |  |
| 38 | `5d40035` | text-editor | L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires. | The association&#x27;s organization is based on three complementary areas established in its bylaws. | Validated — reused | P-02 |
| 39 | `5d40037` | heading | Pôle Administration et Gestion | Administration and Management | Validated — reused | P-02 (pole name) |
| 40 | `5d40038` | text-editor | Il participe à l&#x27;organisation et au fonctionnement de la structure associative. | This area contributes to organizing the association and supporting the operation of its organizational structure. | Validated — reused | P-02 |
| 41 | `5d40039` | button | Découvrir le pôle | Explore This Area | Validated — reused | P-01 |
| 42 | `5d4003c` | heading | Pôle Animation Culturelle et Sociale | Cultural and Social Activities | Validated — reused | P-02 (pole name) |
| 43 | `5d4003d` | text-editor | Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale. | This area supports the objectives relating to culture, community activities, and social participation. | Validated — reused | P-02 |
| 44 | `5d4003e` | button | Découvrir le pôle | Explore This Area | Validated — reused | P-01 |
| 45 | `5d40043` | heading | Une question sur les orientations de ce pôle ? | Have a Question About This Area&#x27;s Objectives? | **Proposal pending validation** |  |
| 46 | `5d40044` | text-editor | Vous souhaitez en savoir plus sur les orientations du Pôle Formation et Intégration, échanger avec l&#x27;Association Amal Chabab Takaddoum ou envisager une collaboration ? | Would you like to learn more about the objectives of the Training and Integration area, exchange views with Association Amal Chabab Takaddoum, or explore opportunities for collaboration? | **Proposal pending validation** |  |
| 47 | `5d40044` | text-editor | Prenons contact pour identifier les possibilités d&#x27;échange. | Let&#x27;s connect to identify opportunities for exchange. | **Proposal pending validation** |  |
| 48 | `5d40045` | button | Nous contacter | Contact Us | Validated — reused | P-01/P-02 |

## 12. French / English correspondence table (71 elements)

English ID = source ID. HTML is shown escaped. The “Editorial status” column refers to the block numbers in section 11.

| # | Source ID | English ID | Section | Type | `_title` (source) | French text | English text | Editorial status | Translation note |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `5d4000b` | `5d4000b` | S1 | container | S1 — Bannière | — | — | No public text |  |
| 2 | `5d4000a` | `5d4000a` | S1 | container | S1 · Ligne 2 colonnes | — | — | No public text |  |
| 3 | `5d40007` | `5d40007` | S1 | container | S1 · Colonne texte | — | — | No public text |  |
| 4 | `5d40001` | `5d40001` | S1 | heading | S1 · H1 | Pôle Formation et Intégration | Training and Integration | block 1: Imposed |  |
| 5 | `5d40002` | `5d40002` | S1 | text-editor | S1 · Sous-titre | &lt;p&gt;Un pôle orienté vers l&#x27;apprentissage, le développement des compétences et les initiatives favorisant l&#x27;intégration sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;This area focuses on learning, skills development, and initiatives that support social and professional integration.&lt;/p&gt; | block 2: Validated — reused |  |
| 6 | `5d40003` | `5d40003` | S1 | text-editor | S1 · Texte | &lt;p&gt;Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt;<br>&lt;p&gt;Ses domaines d&#x27;intervention s&#x27;inscrivent dans les orientations statutaires de l&#x27;association.&lt;/p&gt; | &lt;p&gt;This area reflects the association&#x27;s objectives relating to learning, skills development, and integration.&lt;/p&gt;<br>&lt;p&gt;Its fields of work fall within the association&#x27;s statutory objectives.&lt;/p&gt; | block 3: Validated — reused; block 4: **Proposal pending validation** |  |
| 7 | `5d40006` | `5d40006` | S1 | container | S1 · Boutons | — | — | No public text |  |
| 8 | `5d40004` | `5d40004` | S1 | button | S1 · Bouton 1 → ancre #missions | Ses domaines d&#x27;intervention | Its Fields of Work | block 5: **Proposal pending validation** | “field(s)” = domaine (EN P-03 convention); “area” = pôle |
| 9 | `5d40005` | `5d40005` | S1 | button | S1 · Bouton 2 → ancre #contribution | Sa contribution | Its Contribution | block 6: **Proposal pending validation** |  |
| 10 | `5d40009` | `5d40009` | S1 | container | S1 · Colonne visuel (image à remplacer) | — | — | No public text |  |
| 11 | `5d40008` | `5d40008` | S1 | image | S1 · IMAGE À REMPLACER — visuel institutionnel | — | — | Image placeholder preserved (URL unchanged) |  |
| 12 | `5d4000e` | `5d4000e` | S2 | container | S2 — Présentation | — | — | No public text |  |
| 13 | `5d4000c` | `5d4000c` | S2 | heading | S2 · H2 | Un pôle au service de l&#x27;apprentissage et de l&#x27;intégration | An Area of Work Supporting Learning and Integration | block 7: **Proposal pending validation** |  |
| 14 | `5d4000d` | `5d4000d` | S2 | text-editor | S2 · Texte (3 paragraphes) | &lt;p&gt;Le Pôle Formation et Intégration est l&#x27;un des trois pôles statutaires de l&#x27;Association Amal Chabab Takaddoum. Il s&#x27;inscrit dans les orientations relatives à l&#x27;apprentissage, au développement des compétences et à l&#x27;intégration.&lt;/p&gt;<br>&lt;p&gt;Les orientations statutaires accordent une place importante à l&#x27;éducation non formelle, à la lutte contre l&#x27;illettrisme, à la formation professionnelle et à l&#x27;accompagnement éducatif des enfants et des jeunes.&lt;/p&gt;<br>&lt;p&gt;Conformément aux statuts, l&#x27;organisation des pôles de travail et le suivi de l&#x27;exécution des programmes relèvent de la supervision du Bureau exécutif, élu par l&#x27;Assemblée générale.&lt;/p&gt; | &lt;p&gt;The Training and Integration area is one of the three areas of work established in the bylaws of Association Amal Chabab Takaddoum. It reflects the association&#x27;s objectives relating to learning, skills development, and integration.&lt;/p&gt;<br>&lt;p&gt;The association&#x27;s statutory objectives place particular importance on non-formal education, literacy, vocational training, and educational support for children and young people.&lt;/p&gt;<br>&lt;p&gt;In accordance with the bylaws, the organization of the working areas and the monitoring of program implementation fall under the oversight of the Executive Board, elected by the General Assembly.&lt;/p&gt; | block 8: **Proposal pending validation**; block 9: Validated — reused; block 10: Validated — reused; block 11: **Proposal pending validation** |  |
| 15 | `5d4001f` | `5d4001f` | S3 | container | S3 — Domaines d&#x27;intervention (ancre #missions) | — | — | No public text |  |
| 16 | `5d40011` | `5d40011` | S3 | container | S3 · En-tête | — | — | No public text |  |
| 17 | `5d4000f` | `5d4000f` | S3 | heading | S3 · H2 | Les domaines d&#x27;intervention du pôle | The Area&#x27;s Fields of Work | block 12: **Proposal pending validation** | see T1 |
| 18 | `5d40010` | `5d40010` | S3 | text-editor | S3 · Introduction | &lt;p&gt;Les orientations statutaires de l&#x27;association définissent les domaines dans lesquels le pôle est appelé à intervenir.&lt;/p&gt;<br>&lt;p&gt;Cette page présente ces orientations. Elle ne constitue pas un catalogue : les activités effectivement ouvertes à un moment donné font l&#x27;objet d&#x27;une information distincte.&lt;/p&gt; | &lt;p&gt;The association&#x27;s statutory objectives define the fields in which the area is expected to work.&lt;/p&gt;<br>&lt;p&gt;This page presents these objectives. It is not a catalog: information about the activities actually available at any given time is provided separately.&lt;/p&gt; | block 13: **Proposal pending validation**; block 14: **Proposal pending validation** |  |
| 19 | `5d4001e` | `5d4001e` | S3 | container | S3 · Grille des 4 domaines | — | — | No public text |  |
| 20 | `5d40014` | `5d40014` | S3 | container | S3 · Domaine 1 — Éducation et apprentissage | — | — | No public text |  |
| 21 | `5d40012` | `5d40012` | S3 | heading | S3 · H3 domaine 1 | Éducation et apprentissage | Education and Learning | block 15: Imposed |  |
| 22 | `5d40013` | `5d40013` | S3 | text-editor | S3 · Texte domaine 1 | &lt;p&gt;L&#x27;éducation et l&#x27;apprentissage figurent parmi les orientations statutaires du pôle. Ce domaine englobe l&#x27;accompagnement éducatif des enfants et des jeunes prévu par les statuts de l&#x27;association.&lt;/p&gt; | &lt;p&gt;Education and learning are among the area&#x27;s statutory objectives. This field includes the educational support for children and young people provided for in the association&#x27;s bylaws.&lt;/p&gt; | block 16: **Proposal pending validation** |  |
| 23 | `5d40017` | `5d40017` | S3 | container | S3 · Domaine 2 — Éducation non formelle et alphabétisation | — | — | No public text |  |
| 24 | `5d40015` | `5d40015` | S3 | heading | S3 · H3 domaine 2 | Éducation non formelle et alphabétisation | Non-Formal Education and Literacy | block 17: Imposed |  |
| 25 | `5d40016` | `5d40016` | S3 | text-editor | S3 · Texte domaine 2 | &lt;p&gt;Les statuts accordent une place à l&#x27;éducation non formelle et à la lutte contre l&#x27;illettrisme. Ce domaine désigne les apprentissages conduits en dehors des cadres scolaires habituels.&lt;/p&gt; | &lt;p&gt;The bylaws give a place to non-formal education and literacy. This field refers to learning that takes place outside conventional school settings.&lt;/p&gt; | block 18: **Proposal pending validation** | « lutte contre l'illettrisme » → literacy (EN P-02) |
| 26 | `5d4001a` | `5d4001a` | S3 | container | S3 · Domaine 3 — Formation professionnelle et qualification | — | — | No public text |  |
| 27 | `5d40018` | `5d40018` | S3 | heading | S3 · H3 domaine 3 | Formation professionnelle et qualification | Vocational Training and Qualifications | block 19: Imposed | « qualification » → qualifications (not « certification ») |
| 28 | `5d40019` | `5d40019` | S3 | text-editor | S3 · Texte domaine 3 | &lt;p&gt;La formation professionnelle et la qualification constituent un domaine d&#x27;intervention prévu par les orientations statutaires, envisagé comme un appui au développement des compétences.&lt;/p&gt; | &lt;p&gt;Vocational training and qualifications are a field of work provided for in the statutory objectives, viewed as a way of supporting skills development.&lt;/p&gt; | block 20: **Proposal pending validation** |  |
| 29 | `5d4001d` | `5d4001d` | S3 | container | S3 · Domaine 4 — Intégration sociale et professionnelle | — | — | No public text |  |
| 30 | `5d4001b` | `5d4001b` | S3 | heading | S3 · H3 domaine 4 | Intégration sociale et professionnelle | Social and Professional Integration | block 21: Imposed |  |
| 31 | `5d4001c` | `5d4001c` | S3 | text-editor | S3 · Texte domaine 4 | &lt;p&gt;L&#x27;intégration constitue la finalité à laquelle les autres domaines concourent : favoriser les initiatives qui soutiennent la participation sociale et professionnelle.&lt;/p&gt; | &lt;p&gt;Integration is the goal to which the other fields contribute: encouraging initiatives that support social and professional participation.&lt;/p&gt; | block 22: **Proposal pending validation** | « finalité » → goal; interpretation kept as proposal |
| 32 | `5d40022` | `5d40022` | S4 | container | S4 — Contribution transversale (ancre #contribution) | — | — | No public text |  |
| 33 | `5d40020` | `5d40020` | S4 | heading | S4 · H2 | Une contribution transversale aux autres pôles | A Cross-Cutting Contribution to the Other Areas | block 23: **Proposal pending validation** |  |
| 34 | `5d40021` | `5d40021` | S4 | text-editor | S4 · Texte (3 paragraphes) | &lt;p&gt;La contribution du pôle ne se limite pas à son propre périmètre : elle concourt également aux conditions dans lesquelles les deux autres pôles statutaires conduisent leurs activités.&lt;/p&gt;<br>&lt;p&gt;Les apprentissages, le développement des compétences et les initiatives d&#x27;intégration rejoignent les orientations portées par le Pôle Animation Culturelle et Sociale, tandis que le Pôle Administration et Gestion contribue à l&#x27;organisation et aux moyens nécessaires à leur conduite.&lt;/p&gt;<br>&lt;p&gt;Cette articulation s&#x27;exerce dans le cadre défini par les statuts, le Bureau exécutif assurant la supervision de l&#x27;organisation des commissions et des pôles de travail, ainsi que le suivi de l&#x27;exécution des programmes établis.&lt;/p&gt; | &lt;p&gt;The area&#x27;s contribution is not limited to its own scope: it also supports the conditions under which the other two statutory areas carry out their activities.&lt;/p&gt;<br>&lt;p&gt;Learning, skills development, and integration initiatives connect with the objectives of the Cultural and Social Activities area, while the Administration and Management area contributes to the organization and resources needed to carry them out.&lt;/p&gt;<br>&lt;p&gt;This coordination is carried out within the framework defined by the bylaws, with the Executive Board overseeing the organization of committees and working areas, as well as monitoring the implementation of established programs.&lt;/p&gt; | block 24: **Proposal pending validation**; block 25: **Proposal pending validation**; block 26: **Proposal pending validation** | « articulation » → coordination |
| 35 | `5d40033` | `5d40033` | S5 | container | S5 — Principes de fonctionnement | — | — | No public text |  |
| 36 | `5d40025` | `5d40025` | S5 | container | S5 · En-tête | — | — | No public text |  |
| 37 | `5d40023` | `5d40023` | S5 | heading | S5 · H2 | Les principes qui guident son fonctionnement | The Principles That Guide Its Work | block 27: **Proposal pending validation** |  |
| 38 | `5d40024` | `5d40024` | S5 | text-editor | S5 · Introduction | &lt;p&gt;Le fonctionnement du pôle s&#x27;inscrit dans les principes qui orientent l&#x27;engagement de l&#x27;association.&lt;/p&gt; | &lt;p&gt;The area&#x27;s work is guided by the principles that shape the association&#x27;s commitment.&lt;/p&gt; | block 28: **Proposal pending validation** |  |
| 39 | `5d40032` | `5d40032` | S5 | container | S5 · Grille des 4 principes | — | — | No public text |  |
| 40 | `5d40028` | `5d40028` | S5 | container | S5 · Principe 1 — Égalité et justice sociale | — | — | No public text |  |
| 41 | `5d40026` | `5d40026` | S5 | heading | S5 · H3 principe 1 | Égalité et justice sociale | Equality and Social Justice | block 29: Validated — reused |  |
| 42 | `5d40027` | `5d40027` | S5 | text-editor | S5 · Texte principe 1 | &lt;p&gt;Promouvoir des relations fondées sur le respect des droits et de la dignité.&lt;/p&gt; | &lt;p&gt;Promoting relationships based on respect for rights and dignity.&lt;/p&gt; | block 30: Validated — reused |  |
| 43 | `5d4002b` | `5d4002b` | S5 | container | S5 · Principe 2 — Solidarité | — | — | No public text |  |
| 44 | `5d40029` | `5d40029` | S5 | heading | S5 · H3 principe 2 | Solidarité | Solidarity | block 31: Validated — reused |  |
| 45 | `5d4002a` | `5d4002a` | S5 | text-editor | S5 · Texte principe 2 | &lt;p&gt;Développer l&#x27;entraide, le bénévolat et la coopération.&lt;/p&gt; | &lt;p&gt;Developing mutual support, volunteering, and cooperation.&lt;/p&gt; | block 32: Validated — reused |  |
| 46 | `5d4002e` | `5d4002e` | S5 | container | S5 · Principe 3 — Initiative | — | — | No public text |  |
| 47 | `5d4002c` | `5d4002c` | S5 | heading | S5 · H3 principe 3 | Initiative | Initiative | block 33: Validated — reused |  |
| 48 | `5d4002d` | `5d4002d` | S5 | text-editor | S5 · Texte principe 3 | &lt;p&gt;Valoriser les talents, les idées et les capacités d&#x27;action.&lt;/p&gt; | &lt;p&gt;Recognizing talents, ideas, and the ability to take action.&lt;/p&gt; | block 34: Validated — reused |  |
| 49 | `5d40031` | `5d40031` | S5 | container | S5 · Principe 4 — Responsabilité | — | — | No public text |  |
| 50 | `5d4002f` | `5d4002f` | S5 | heading | S5 · H3 principe 4 | Responsabilité | Responsibility | block 35: Validated — reused |  |
| 51 | `5d40030` | `5d40030` | S5 | text-editor | S5 · Texte principe 4 | &lt;p&gt;Inscrire l&#x27;engagement dans une démarche sérieuse et constructive.&lt;/p&gt; | &lt;p&gt;Making a serious and constructive approach central to commitment.&lt;/p&gt; | block 36: Validated — reused |  |
| 52 | `5d40042` | `5d40042` | S6 | container | S6 — Les deux autres pôles | — | — | No public text |  |
| 53 | `5d40036` | `5d40036` | S6 | container | S6 · En-tête | — | — | No public text |  |
| 54 | `5d40034` | `5d40034` | S6 | heading | S6 · H2 | Les deux autres pôles | The Other Two Areas of Work | block 37: **Proposal pending validation** |  |
| 55 | `5d40035` | `5d40035` | S6 | text-editor | S6 · Introduction | &lt;p&gt;L&#x27;organisation de l&#x27;association repose sur trois pôles statutaires complémentaires.&lt;/p&gt; | &lt;p&gt;The association&#x27;s organization is based on three complementary areas established in its bylaws.&lt;/p&gt; | block 38: Validated — reused |  |
| 56 | `5d40041` | `5d40041` | S6 | container | S6 · Grille des 2 pôles | — | — | No public text |  |
| 57 | `5d4003b` | `5d4003b` | S6 | container | S6 · Carte 1 — Pôle Administration et Gestion → P-03 | — | — | No public text |  |
| 58 | `5d40037` | `5d40037` | S6 | heading | S6 · H3 carte 1 | Pôle Administration et Gestion | Administration and Management | block 39: Validated — reused |  |
| 59 | `5d40038` | `5d40038` | S6 | text-editor | S6 · Texte carte 1 | &lt;p&gt;Il participe à l&#x27;organisation et au fonctionnement de la structure associative.&lt;/p&gt; | &lt;p&gt;This area contributes to organizing the association and supporting the operation of its organizational structure.&lt;/p&gt; | block 40: Validated — reused |  |
| 60 | `5d4003a` | `5d4003a` | S6 | container | S6 · Bouton carte 1 | — | — | No public text |  |
| 61 | `5d40039` | `5d40039` | S6 | button | S6 · Bouton carte 1 → P-03 | Découvrir le pôle | Explore This Area | block 41: Validated — reused |  |
| 62 | `5d40040` | `5d40040` | S6 | container | S6 · Carte 2 — Pôle Animation Culturelle et Sociale → P-05 | — | — | No public text |  |
| 63 | `5d4003c` | `5d4003c` | S6 | heading | S6 · H3 carte 2 | Pôle Animation Culturelle et Sociale | Cultural and Social Activities | block 42: Validated — reused |  |
| 64 | `5d4003d` | `5d4003d` | S6 | text-editor | S6 · Texte carte 2 | &lt;p&gt;Il porte les orientations relatives à la culture, à l&#x27;animation et à la participation sociale.&lt;/p&gt; | &lt;p&gt;This area supports the objectives relating to culture, community activities, and social participation.&lt;/p&gt; | block 43: Validated — reused |  |
| 65 | `5d4003f` | `5d4003f` | S6 | container | S6 · Bouton carte 2 | — | — | No public text |  |
| 66 | `5d4003e` | `5d4003e` | S6 | button | S6 · Bouton carte 2 → P-05 | Découvrir le pôle | Explore This Area | block 44: Validated — reused |  |
| 67 | `5d40047` | `5d40047` | S7 | container | S7 — Appel à l’action | — | — | No public text |  |
| 68 | `5d40043` | `5d40043` | S7 | heading | S7 · H2 | Une question sur les orientations de ce pôle ? | Have a Question About This Area&#x27;s Objectives? | block 45: **Proposal pending validation** | « orientations » → objectives (EN P-02 convention) |
| 69 | `5d40044` | `5d40044` | S7 | text-editor | S7 · Texte | &lt;p&gt;Vous souhaitez en savoir plus sur les orientations du Pôle Formation et Intégration, échanger avec l&#x27;Association Amal Chabab Takaddoum ou envisager une collaboration ?&lt;/p&gt;<br>&lt;p&gt;Prenons contact pour identifier les possibilités d&#x27;échange.&lt;/p&gt; | &lt;p&gt;Would you like to learn more about the objectives of the Training and Integration area, exchange views with Association Amal Chabab Takaddoum, or explore opportunities for collaboration?&lt;/p&gt;<br>&lt;p&gt;Let&#x27;s connect to identify opportunities for exchange.&lt;/p&gt; | block 46: **Proposal pending validation**; block 47: **Proposal pending validation** |  |
| 70 | `5d40046` | `5d40046` | S7 | container | S7 · Bouton | — | — | No public text |  |
| 71 | `5d40045` | `5d40045` | S7 | button | S7 · Bouton → Contact (P-11) | Nous contacter | Contact Us | block 48: Validated — reused |  |
