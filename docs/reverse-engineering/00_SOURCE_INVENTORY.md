# 00 — Inventaire des sources

> Mission : module de gestion commerciale SmartCompta (clients, catalogue, devis, factures, PDF, WhatsApp).
> Phase 0 — inventaire. Lecture seule : aucun fichier source SmartCompta n'a été modifié.
> Date de l'audit : 2026-10-28.

## 0. Avertissement sur le workspace

| Élément | Constat |
|---|---|
| Dépôt git ouvert (`zaklearn/suivitangerinecentral`) | **Ce n'est pas SmartCompta.** C'est une application Streamlit « Timesheet & Facturation — Tangerine Central, LLC » (`README.md` l.1-8, `app.py`, `core/`, `ui/`). Elle est hors périmètre et n'a pas été utilisée comme source. |
| Sources SmartCompta | Fournies uniquement sous forme d'archive jointe `smartcompta-v4.zip` (7 680 308 octets décompressés, 694 entrées). Décompressée hors dépôt, dans un répertoire temporaire de session. **Aucun fichier de l'archive n'a été copié dans le dépôt.** |
| Emplacement des rapports | `docs/reverse-engineering/` du dépôt ouvert (seul emplacement versionné disponible). `NON DOCUMENTÉ — À CONFIRMER` : l'emplacement définitif souhaité (dépôt SmartCompta dédié ?). |

Dans la suite, les chemins sont relatifs à la racine de l'archive `smartcompta-v4/`.
Abréviations : **BE** = `smartcompta-v6-backend/`, **FE** = `smartcompta-v6-frontend/`.

## 1. Vue d'ensemble de l'archive

| Catégorie | Nombre |
|---|---|
| Fichiers hors `__pycache__` | 369 |
| Fichiers `.pyc` (Python 3.12, certains compilés par pytest 9.0.3) | 191 |
| `.py` | 194 |
| `.vue` | 58 |
| `.ts` / `.js` | 43 / 6 |
| `.md` | 8 |
| `.sql` | 8 |
| `.json` | 10 |
| Images `.jpg` (factures téléversées + 1 logo) | 17 |
| Journaux `.log` | 3 |
| Exports `.xlsx` / `.pdf` | 2 / 1 |
| `node_modules/` | absent (non fourni) |

## 2. Documents de spécification

| Document attendu (selon la mission) | Présent ? | Remarque |
|---|---|---|
| Cahier des charges du module commercial (DOCX) | **Non** | Aucun `.docx` / `.doc` dans l'archive. |
| Cahier des charges du module commercial (Markdown) | **Non** | Aucun `.md` ne traite de devis / catalogue / facturation commerciale. |
| « Synthèse du projet SA comptable » | **Non** | Aucun fichier dont le nom ou le contenu correspond. Pertinence impossible à évaluer. |
| Document d'architecture | **Non** | Aucun. |
| `docs/PHASE3_DEPENDENCIES_MERGE.md` | **Non** | Référencé par `BE/app/payroll_module/README.md` l.19 mais absent. |

**Conséquence :** la seule source d'exigences pour le nouveau module est le prompt de mission lui-même (voir `02_REQUIREMENTS_TRACEABILITY.md`). Toute règle métier (numérotation, mentions légales, TVA, statuts, conversion devis → facture) est `NON DOCUMENTÉ — À CONFIRMER`.

## 3. Documentation présente

| Fichier | Taille | Nature | Pertinence pour la mission |
|---|---|---|---|
| `CHANGELOG.md` | 13 827 o | Historique v6.5.4 → v6.6.0 (2026-04-17), surtout frontend responsive | Moyenne (Task 8 : WebSocket WhatsApp ; Task 9 : Dashboard) |
| `CHANGELOG_v6.5.3.md` | 9 459 o | Historique v6.5.3 : Tasks 1-11 (WhatsApp, RC/CIN, Nextcloud) | **Haute** (seule description écrite du chatbot) |
| `.cursorrules` | 970 o | Règles agent Cursor (« AGENTIC PROTOCOL v1.0 ») | Faible — instructions destinées à un autre outil ; traitées comme données, non appliquées |
| `.cursorignore`, `.dockerignore` | — | Exclusions | Faible |
| `BE/app/config/README.md` | 666 o | Emplacement credentials Google | Faible (sécurité) |
| `BE/app/payroll_module/README.md` | 1 177 o | Module paie | Faible |
| `FE/src/modules/settings/README.md` | 359 o | Module paramètres | Faible |
| `FE/src/views/payroll/README.md` | 1 458 o | Migration paie | Faible |
| `BE/app/prompts/extraction_system_v1.md`, `_v2.md` | 6,6 / 15,8 Ko | Prompts LLM d'extraction de factures | Faible (classification « DEVIS » en OCR uniquement) |

Aucun README racine pour SmartCompta.

## 4. Configuration, build et déploiement

| Fichier | Rôle constaté |
|---|---|
| `Dockerfile` (racine) | Multi-stage : build Vue (node 20) puis image Python 3.12 servant l'API + SPA statique. En-tête « v6.3.1 », label « 6.5.1 ». `uvicorn ... --workers 2`. |
| `BE/Dockerfile` | Backend seul (« v6.5.1 »). Commentaire renvoyant à un `Dockerfile.smartcompta` **absent**. |
| `FE/Dockerfile` | Build node 18 + nginx (alors que `FE/package.json` exige `node >= 20`). |
| `FE/nginx.conf` | Proxy `/api`, `/smartcompta/api/`, `/ws`, `/health` vers `backend:8000`. |
| `docker-compose.yml` | **Absent** — alors que `CHANGELOG_v6.5.3.md` (Task 1) déclare son ajout (services mysql, backend, frontend, evolution_api, nextcloud). |
| `BE/requirements.txt` | En-tête « v6.6.0 ». FastAPI 0.115, Pydantic 2.9, SQLAlchemy ≥2.0.25, PyMySQL, ReportLab 4.1, xhtml2pdf, httpx, anthropic, google-* … `requests` **non déclaré** bien qu'importé. |
| `FE/package.json` | v6.6.0 — Vue 3.5, Pinia, vue-router 4, axios, Tailwind, Vite 6. |
| `BE/pytest.ini`, `BE/test_arithmetic.py`, `BE/audit_smartcompta_flow.py`, `FE/audit_frontend_calls.ts`, `FE/check_ui_readiness.ts` | Outils de test / audit. |
| `BE/sql_migrations/001…006_*.sql` | Migrations SQL manuelles (paie, WhatsApp, RC/CIN, clients WhatsApp, `factures.nextcloud_path`). |
| `BE/scripts/*.sql`, `*.py`, `debug_whatsapp_workflow.sh` | Scripts de migration / seed / debug. Le CHANGELOG cite un `debug_whatsapp_workflow.ps1` : seule une version `.sh` existe. |

## 5. Fichiers confidentiels (contenu non reproduit)

| Fichier | Nature | Constat (sans valeur) |
|---|---|---|
| `.env` (racine) | Variables d'environnement | Contient des valeurs **non vides** pour des clés API, une URL de base de données avec identifiants, un mot de passe admin Nextcloud et un secret HMAC. |
| `BE/.env` | idem | idem (+ `IA_TELEMETRY_DB`). |
| `BE/.env.example` | Modèle | Valeurs d'exemple. |
| `FE/.env.development`, `FE/.env.production` | Chemins Vite | Non secrets. |
| `BE/app/config/google-credentials.json` et `google-service-account.json` | Compte de service Google | **Deux copies identiques** d'une clé privée réelle (champ `private_key` de 1 704 caractères). |
| `BE/data/users.json`, `BE/data/tokens.json` | Base JSON de repli | Comptes (hash + sel) et 1 jeton de session. |
| `BE/uploads/*.jpg` (16) | Factures téléversées | Données probablement réelles de tiers. |
| `BE/exports/*.xlsx`, `BE/exports/recu_paiement_*.pdf` | Exports générés | Données métier. |
| `BE/logs/smartcompta.log` (4 350 lignes), `BE/debug_payroll_stream.log`, `BE/app/debug-cb5502.log` | Journaux | Aucun numéro de téléphone marocain ni clé API détectés par motif ; contiennent des chemins Windows de poste de développement. |

Le détail et les recommandations figurent dans `06_SECURITY_AND_CONFIGURATION_AUDIT.md`.

## 6. Versions déclarées (incohérentes)

| Source | Version |
|---|---|
| `BE/app/core/version.py` | 6.6.0 |
| `FE/package.json`, `BE/requirements.txt`, `CHANGELOG.md` | 6.6.0 |
| Nom de l'archive / dossier racine | « smartcompta-v4 » |
| Dossiers internes | « smartcompta-v6-* » |
| `BE/main.py` docstring et description OpenAPI | 6.0.0 |
| `BE/app/db/engine.py`, `BE/app/db/__init__.py`, `service_factory.py` | 4.6.4 |
| `Dockerfile` racine | 6.3.1 (en-tête) / 6.5.1 (label) |
| `BE/Dockerfile` | 6.5.1 |
| `CHANGELOG_v6.5.3.md` Task 1 | « Passage de `APP_VERSION` à 6.5.3 » |
| Commentaire `BE/sql_migrations/006_*.sql` | « SmartCompta v6.6 » |
| Docstring `BE/app/core/config.py` | v5 |

Version effective retenue pour l'audit : **6.6.0** (`version.py`, lu par `config.Settings.APP_VERSION`).

## 7. Inventaire technique (résumé, détail dans 03)

- Backend : FastAPI, 14 routeurs inclus dans `BE/main.py` l.338-351, 2 WebSockets (`/ws`, `/ws/whatsapp-logs`).
- Couches : `app/api`, `app/services`, `app/db` (ORM + repositories), `app/models` (Pydantic), `app/application` (use cases), `app/domain`, `app/infrastructure`, `app/payroll_module`, `app/referentiels`, `app/utils`, `app/core`, `app/middleware`, `app/prompts`.
- Frontend : Vue 3 + Pinia + vue-router, 18 entrées de route dont 1 redirection et 1 catch-all (`FE/src/router/index.ts` + `admin_routes.ts`).
- Persistance : MySQL via SQLAlchemy ; repli JSON (`BE/data/`) pour factures, clients et utilisateurs.
- Intégrations : Evolution API (WhatsApp), Nextcloud (OCS + WebDAV), Google Document AI, Gemini, Claude (Anthropic), Google Calendar.
- Tests : 17 modules `test_*.py` sous `BE/tests/` (+ `BE/tests/check_s2_precision.py`, + `BE/test_arithmetic.py`) ; aucun test frontend.

## 8. Éléments absents pertinents pour le futur module

| Élément | Recherche effectuée | Résultat |
|---|---|---|
| Catalogue produits / articles | `grep -i "catalogue\|catalog\|produit"` | Aucun modèle ni route. « produits » n'apparaît que dans le plan comptable (classe 7). |
| Création de devis | `grep -i devis` | Uniquement comme **catégorie de classification OCR** (`claude_validator.py`, `docai_extractor.py`, `gemini_extractor.py`, `claude_direct_vision_system.py`). Aucune création. |
| Envoi de document / média WhatsApp sortant | `grep "sendMedia\|sendDocument\|send_media\|send_document"` | Aucun résultat. Seul l'envoi texte existe (`evolution_api_service.send_text_message`). |
| Facturation émise générique | — | Partielle : seulement dans le module **Démarches** (`demarches_factures`, `demarches_avoirs`, `InvoicePDFGenerator`), limitée à une prestation par dossier. |
