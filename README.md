# Timesheet & Facturation — Tangerine Central, LLC

Application Streamlit multi-utilisateurs qui remplace les deux fichiers Excel
(Timesheet + Invoice) de Tangerine Central : chaque expert saisit son
timesheet, l'app calcule via son TJM, génère le **timesheet** et la **facture**
au format Excel **identique aux modèles d'origine** (+ PDF), stocke tout en
MySQL, affiche un dashboard et offre au deputy manager une supervision avec
alertes d'épuisement.

## Démarrage

```bash
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # puis renseigner
streamlit run app.py
```

Au premier lancement, `bootstrap()` crée les tables manquantes, la ligne de
configuration, et — si la table `users` est vide — l'administrateur initial
décrit dans `[bootstrap_admin]`, avec changement de mot de passe forcé.

La génération PDF repose sur **LibreOffice headless** (`soffice`). Sans lui,
le téléchargement Excel reste disponible et l'app le signale.

### Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Les tests tournent sur SQLite jetable, sans service externe ; le code de
production ne contient aucune branche spécifique à SQLite, seule l'URL change
(`APP_DATABASE_URL`). Les tests PDF se désactivent d'eux-mêmes si LibreOffice
ou `pdftotext` sont absents.

## Architecture

```
app.py                     porte d'accès + navigation par rôle
core/
  models.py                11 tables ORM                        (M6)
  db.py                    engine Aiven SSL, sessions, bootstrap(M6)
  integrity.py             les 5 règles d'intégrité             (M6)
  security.py  auth.py     bcrypt, matrice de permissions       (M1)
  audit.py                 journalisation audit_log
  config_service.py        paramètres, projets, allocations     (M2)
  entries_service.py       saisie et verrouillage               (M3)
  timesheet_export.py      remplissage du modèle timesheet      (M4)
  invoice_service.py       cycle de vie des factures            (M5)
  invoice_export.py        remplissage du modèle facture        (M5)
  metrics_service.py       agrégations SQL du dashboard         (M7)
  alerts_service.py        consommation, seuils, alertes        (M8)
  xlsx_utils.py            insertion de lignes, tables, fusions
  pdf.py                   conversion xlsx → pdf (LibreOffice)
ui/                        un module Streamlit par écran
templates/                 les deux modèles Excel d'origine
```

## Les décisions structurantes, et où elles vivent dans le code

| Décision | Implémentation |
|---|---|
| MySQL Aiven, SSL obligatoire | `core/db.py` — CA écrit depuis `st.secrets`, `connect_args={"ssl": {"ca": …}}` |
| Jour **ou** heure, aucune conversion en facturation | `montant = quantite × taux_applique`, `core/entries_service.py` |
| TJM par expert, figé à la saisie | `entries.taux_applique`, snapshot pris dans `creer_entree()` |
| USD | `config.devise`, non modifiable en v1 |
| Rendu Excel identique, par remplissage | `core/xlsx_utils.py` ouvre le modèle, n'écrit que des valeurs |
| Option C | `entries.heures_par_jour_snap`, figé si `unite=jour` |
| Une ligne LABOR par entrée | `invoice_service.lignes_labor_brouillon()`, sans regroupement |

Modifier `heures_par_jour` (M2) ou un TJM ne retouche **aucune** entrée
existante : chaque entrée porte ses propres valeurs figées. C'est vérifié par
`test_snapshots_survivent_au_changement_de_config`.

## Trois formules fausses du modèle de facture, corrigées

Le modèle `TangerineCentral_InvoiceTemplate_Aug26.xlsx` produit, tel quel, une
facture arithmétiquement incorrecte. Observé en PDF avant correction :
`Hours 8 × Rate $100 = $750`, montant ODC vide, et **Total $4 700 au lieu de
$2 500**. Les trois correctifs sont dans `core/invoice_export.py` :

| Cellule | Dans le modèle | Conséquence | Correctif |
|---|---|---|---|
| `G27:G29` Amount ODC | référence `InvoiceDetails[[#This Row],[Hours]]`, hors du tableau LABOR | montant ODC vide | `=E{r}*F{r}` |
| `G30` sous-total ODC | `SUM(InvoiceDetails[Amount])`, la colonne du tableau **LABOR** | sous-total ODC = sous-total LABOR, donc `Total = G24+G30` compte le labor deux fois | `=SUM(G{premiere}:G{derniere})` sur la plage ODC |
| colonne `Hours` / `Units` | format `0` | une quantité de 7,5 s'affiche « 8 » en regard d'un montant calculé sur 7,5 | format `#,##0.##` (les entiers restent des entiers) |

Le premier point est signalé par le cahier des charges (§5.5) ; les deux
autres ont été trouvés en inspectant le modèle. Chacun a son test de
non-régression dans `tests/test_m5_facturation.py`, et le test PDF vérifie les
montants de bout en bout.

Hors ces trois points, **aucune cellule du modèle n'est restylée** :
`tests/test_m4_timesheet.py::test_fidelite_de_style` compare police, graisse,
fond, bordures, alignement, retour à la ligne et format de nombre de chaque
cellule du modèle avec celle du fichier produit, débordement inclus, et exige
zéro écart.

### Une seule entorse volontaire à la fidélité, côté timesheet

La colonne `Date` du modèle est au format `General` : une date y apparaîtrait
en numéro de série (`46296`). Le format `mm/dd/yyyy` est donc posé sur les
cellules de données de la colonne A. C'est la seule différence de style
mesurée avec le modèle.

## Numérotation des factures — un point à confirmer

Le cahier des charges demande le format `{prefixe}-{AAAA}-{seq:03d}` avec une
**séquence par expert et par année**, et `invoices.numero` UNIQUE. Ces trois
exigences sont incompatibles : sous un préfixe commun, deux experts obtiennent
`TC-2026-001` la même année et la contrainte d'unicité saute.

Deux modes sont donc implémentés, dans `config.mode_numerotation` :

* **`par_expert`** (défaut) — `{prefixe}-{code}-{AAAA}-{seq:03d}`, par exemple
  `TC-JD-2026-001`. Le code vient de `users.code_facture`, dérivé des
  initiales à la création et modifiable par l'admin. Chaque expert a sa série,
  et les numéros restent uniques.
* **`globale`** — `{prefixe}-{AAAA}-{seq:03d}`, la forme littérale du cahier
  des charges, avec une seule séquence pour tous les experts.

Le mode se change dans Configuration → Paramètres généraux. Le préfixe par
défaut est `TC`.

Deux champs ont été ajoutés au schéma M6 pour cela : `users.code_facture` et
`config.mode_numerotation`.

## Entrées rattachées à une facture

Le cahier des charges dit trois choses : la sélection porte sur les entrées
`invoice_id IS NULL` (§5.1.1), l'émission renseigne `invoice_id` (§5.1.2), et
annuler un brouillon « libère les entrées » (§5.1), tandis que M3 précise que
les entrées en brouillon « restent modifiables ». Lecture retenue, seule
cohérente avec les quatre phrases :

* la sélection dans un brouillon pose déjà `invoice_id` — c'est ce qui donne
  un sens à « libérer les entrées » à l'annulation ;
* une entrée rattachée à un **brouillon** reste modifiable, et le brouillon est
  recalculé ;
* une entrée rattachée à une facture **émise** est verrouillée.

Les lignes ODC vivent dans `invoice_odc` dès le brouillon : elles n'ont pas
d'autre support. Elles se figent à l'émission comme les lignes LABOR.

## Points remarqués, sans modification du code

* **`E24` additionne des heures et des jours.** La colonne `Hours` du modèle
  reçoit la quantité telle quelle, heures ou jours selon l'unité (décision 2).
  Le sous-total `E24` du modèle en fait donc une somme de grandeurs
  hétérogènes : `7,5 h + 2 j` s'affiche `9,5`. Les montants, eux, sont justes.
  À confirmer : faut-il laisser ce sous-total, ou le vider ?
* **`G32` (Advance) est au format `General`** dans le modèle : une avance de
  250 s'affiche `250` et non `$250.00`, à côté de montants en devise. Laissé
  tel quel par fidélité.
* **Le modèle de timesheet n'est pas en « ajuster à la page »** : 35 entrées
  donnent 7 pages en PDF. C'est le réglage d'impression du modèle d'origine.
* **Le tableau Excel du timesheet (`A8:E48`) couvre les lignes de signature.**
  Sans conséquence, mais c'est pourquoi sa référence est étendue de la même
  hauteur que les lignes insérées.

## Concurrence

Les écritures passent par `get_session()`, qui commite en sortie normale et
annule sur exception. `entries` et `invoices` portent `updated_at` géré par la
base. L'attribution d'un numéro de facture se fait dans la transaction
d'émission, avec reprise sur `IntegrityError` : deux émissions simultanées ne
produisent pas deux fois le même numéro, la seconde prend le suivant.

## Sécurité

* Mots de passe hachés **bcrypt coût 12** (`passlib`), jamais en clair en base,
  en logs ni en code. Au-delà de 72 octets le mot de passe est refusé plutôt
  que tronqué silencieusement par bcrypt.
* Échec de connexion : message générique, sans distinction entre email
  inconnu, compte désactivé et mot de passe faux. Vérification à vide sur un
  email inconnu, pour que le temps de réponse ne renseigne pas non plus.
* Compteur d'échecs en session, blocage au-delà de 5 tentatives.
* **Cloisonnement au niveau requête** : `auth.perimetre_user_id()` donne le
  filtre `user_id` à appliquer ; un expert ne peut pas charger les données
  d'un autre, même en forçant l'interface. Les panneaux non autorisés ne sont
  pas construits, pas seulement masqués.
* Aucun compte n'est supprimé : il est désactivé (`actif=0`), et le dernier
  administrateur actif ne peut pas l'être.
* `audit_log` filtre les champs sensibles avant écriture.
* Secrets uniquement via `st.secrets`, et `.streamlit/secrets.toml` est
  dans `.gitignore`.

## Couverture des critères d'acceptation

| Module | Fichier de tests |
|---|---|
| M6 — bootstrap, snapshots, intégrité | `tests/test_m6_db_integrity.py` |
| M1 — gate, rôles, cloisonnement, mots de passe | `tests/test_m1_auth.py` |
| M2 / M3 — config, allocations, saisie, verrouillage | `tests/test_m2_m3_saisie.py` |
| M4 — fidélité, formule `SUBTOTAL`, débordement | `tests/test_m4_timesheet.py` |
| M5 — cycle de vie, numérotation, rendu, correctifs | `tests/test_m5_facturation.py` |
| M7 / M8 — métriques, seuils, alertes, extras | `tests/test_m7_m8_supervision.py` |
| PDF de bout en bout | `tests/test_pdf.py` |
| Démarrage de l'app et gating par rôle | `tests/test_app_smoke.py` |

`tests/test_app_smoke.py` exécute réellement `app.py` avec le harnais de test
de Streamlit : il vérifie que la porte d'accès bloque sans connexion, que
chaque rôle ne voit que ses écrans, et que **chacun des huit écrans se rend
sans exception**.
