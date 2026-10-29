# 06 — Audit sécurité et configuration

> Phase 1 — lecture seule. Aucun fichier `.env`, clé ou credential n'a été modifié, copié dans le dépôt ou transmis à un service externe.
> **Aucune valeur secrète n'est reproduite dans ce document** ; seules des longueurs ou la présence de champs sont mentionnées.
> **BE** = `smartcompta-v4/smartcompta-v6-backend/`, **FE** = `smartcompta-v4/smartcompta-v6-frontend/`.

## 1. Secrets présents dans l'archive livrée

| Fichier | Contenu (sans valeur) | Constat | Recommandation |
|---|---|---|---|
| `.env` (racine) et `BE/.env` | `ANTHROPIC_API_KEY` (108 car.), `GOOGLE_API_KEY` (39 car.), `DATABASE_URL` avec identifiants (76 car.), `NEXTCLOUD_ADMIN_PASS` (13 car.), `COMPLIANCE_ICS_FEED_SECRET` (48 / 39 car., valeurs différentes entre les deux fichiers) | Valeurs **réelles probables** (longueurs non conformes à des exemples). | **Révoquer et régénérer** toutes ces clés ; retirer les `.env` des archives partagées. |
| `BE/app/config/google-credentials.json` + `google-service-account.json` | Compte de service Google avec `private_key` (1 704 car.) — deux copies identiques | Clé privée exposée. | Révoquer la clé dans la console Google ; supprimer la copie obsolète. |
| `BE/data/users.json` | 3 comptes (hash SHA-256 + sel) | Hashs exposés. | Voir §3.1. |
| `BE/data/tokens.json` | 1 jeton de session | Expiré (`expires_at` = 2026-03-27) ; utilisé seulement en mode repli JSON. | Purger. |
| `BE/app/services/auth.py` l.151-188 | Mots de passe des comptes par défaut `admin`, `comptable`, `demo` **codés en dur** | Créés automatiquement au démarrage s'ils n'existent pas. | Supprimer le seed en production ou forcer le changement au premier login. |
| Table `whatsapp_config.evolution_api_key` | Stockée en clair en base | Masquée en lecture API (`"***"`, `settings_routes.py` l.240). | Chiffrement au repos : `NON DOCUMENTÉ — À CONFIRMER`. |
| Table `clients.nextcloud_password` | Mot de passe Nextcloud de chaque client en clair | **Renvoyé par `GET /api/nextcloud/clients` sans authentification** (schéma `Client`, `schemas.py` l.672). Copié dans `whatsapp_sessions.context_json`. | Critique — voir §2. |
| `BE/uploads/*.jpg` (16), `BE/exports/*` | Documents de tiers | Données personnelles / commerciales. | Exclure des archives. |

`.dockerignore` n'exclut **ni `.env`, ni `app/config/*.json`, ni `data/`, ni `uploads/`, ni `logs/`** : ils sont copiés dans l'image Docker (`COPY smartcompta-v6-backend/ .`, `Dockerfile` racine).
`.cursorignore` exclut `data/` et `uploads/` mais pas `.env`.

Journaux (`BE/logs/smartcompta.log`, `BE/debug_payroll_stream.log`, `BE/app/debug-cb5502.log`) : recherche par motifs — aucun numéro marocain `2126/2127…`, aucune clé API ; occurrences de « password » limitées à des messages d'erreur HTTP. Ils contiennent des chemins de poste de développement Windows.

## 2. Contrôle d'accès des routes

Méthode : recherche de `get_current_user`, `require_admin`, `get_admin_user`, `finops_read_access`, `verify_token` par fichier, puis lecture des déclarations de routeurs (03 §3).

| Surface | Authentification | Gravité | Commentaire |
|---|---|---|---|
| `GET/POST/PUT/DELETE /api/nextcloud/clients[/{id}]` | **Aucune** | **Critique** | Lecture de tous les clients avec RC, CIN, ID WhatsApp et **mot de passe Nextcloud** ; création / suppression de comptes Nextcloud. Contredit CHANGELOG v6.5.3 Task 8.1. |
| `/api/demarches/*` (tout le routeur, dont `setup-db`, `patch-db-tva`, `config-facture`, génération de factures) | **Aucune** | **Haute** | Le module de facturation existant est public. |
| `POST /api/whatsapp/webhook` | **Aucune**, sans signature | **Haute** | Usurpation de n'importe quel numéro. |
| `/api/clients/*`, `/api/extract/*`, `/api/bank-statements/*`, `/api/upload-async`, `/api/jobs` | Aucune | Haute | Upload, lecture, suppression, export de documents. |
| `/api/extract/exports/{f}`, `/api/clients/{id}/exports/{f}` | Aucune | Haute | Téléchargement de tout fichier d'`exports/` par nom (filtre `..` et `/`). |
| `GET /uploads/*` (StaticFiles) | Aucune | Haute | Factures téléversées et logos accessibles par nom de fichier (préfixe aléatoire de 12 hex). |
| `POST /api/settings/db/init`, `/db/test`, `/nextcloud/test`, `GET /config` | Aucune | Moyenne | `GET /config` masque le mot de passe de la base. |
| `/api/compliance/*` (sauf `calendar/feed-url`, `google-sync`) | Aucune | Moyenne | `feed.ics` protégé par HMAC selon la description (`COMPLIANCE_ICS_FEED_SECRET`). |
| WS `/ws` | Aucune | Moyenne | Diffuse les événements d'upload WhatsApp (numéro de téléphone inclus). |
| `GET /api/invoices/{id}/preview` | Aucune (volontaire, « UUID for security ») | Basse | Sécurité par identifiant non devinable. |
| `/api` (routes.py), `/api/payroll`, `/api/auth/users*`, `/api/admin/*`, `/api/settings/integrations`, `/api/whatsapp/health`, `/connect-qr`, WS `/ws/whatsapp-logs` | Oui | — | — |

Une protection en amont (reverse proxy d'authentification) n'est **pas présente dans les sources** : `FE/nginx.conf` relaie `/api` sans contrôle. Existence ailleurs : `NON DOCUMENTÉ — À CONFIRMER`.

## 3. Authentification et sessions

| Point | Constat (prouvé) | Fichier |
|---|---|---|
| Hash des mots de passe | `sha256(salt + password + salt)`, une seule itération | `BE/app/services/auth.py` l.199-202 |
| Jetons | Opaques, stockés en base (`tokens`) ou JSON, validité 7 jours, révocables (logout) | `auth.py` l.78, 249 |
| Transport du jeton | En-tête `Authorization: Bearer` ; **query string** pour `/ws/whatsapp-logs` | `auth_routes.py` l.68-88 ; `main.py` l.437 |
| Stockage côté navigateur | `localStorage` (`smartcompta_token`, `smartcompta_user`) | `FE/src/shared/services/http.ts` |
| Rôles | `admin`, `comptable`, `user` + drapeaux `can_*` ; `require_permission` défini mais **non utilisé** par les routeurs métier lus | `auth_routes.py` l.97-110 |
| Rôle admin côté UI | Garde `requiresAdmin` (frontend) — non répliquée systématiquement côté backend | `FE/src/router/index.ts` |

## 4. Configuration

### 4.1 Variables d'environnement (noms et rôle)

| Variable | Rôle établi | Défini dans |
|---|---|---|
| `ANTHROPIC_API_KEY` | Clé API Claude | `.env`, `BE/.env`, `.env.example` |
| `GOOGLE_API_KEY` | Clé Gemini (`effective_gemini_api_key`) | idem |
| `GOOGLE_APPLICATION_CREDENTIALS` | Chemin du JSON compte de service | `.env`, `BE/.env` |
| `GOOGLE_DOCAI_PROJECT_ID`, `GOOGLE_DOCAI_PROCESSOR_ID`, `GOOGLE_DOCAI_BANK_PROCESSOR_ID`, `GOOGLE_DOCAI_LOCATION`, `GOOGLE_DOCAI_TIMEOUT` | Document AI | idem |
| `GOOGLE_CALENDAR_DELEGATED_SUBJECT` | Calendrier cible | `.env`, `BE/.env` |
| `DATABASE_URL` | Connexion MySQL principale | idem |
| `IA_TELEMETRY_DB` | Base de télémétrie | `BE/.env` |
| `NEXTCLOUD_URL`, `NEXTCLOUD_ADMIN_USER`, `NEXTCLOUD_ADMIN_PASS`, `NEXTCLOUD_USE_SSL`, `NEXTCLOUD_QUOTA_DEFAULT` | Nextcloud | idem |
| `COMPLIANCE_ICS_FEED_SECRET` | HMAC des flux ICS | `.env`, `BE/.env` |
| `PUBLIC_API_ORIGIN`, `PUBLIC_API_BASE_PATH`, `PUBLIC_APP_ORIGIN` | Construction des URL publiques (PDF, ICS, reset) | `.env`, `BE/.env`, `Dockerfile` (ARG) |
| `DEBUG`, `HOST`, `PORT`, `CORS_ORIGINS` | Serveur | idem |
| `LOG_LEVEL`, `LOG_FORMAT`, `LOG_FILE`, `LOG_MAX_BYTES`, `LOG_BACKUP_COUNT`, `WORKERS`, `PASSWORD_RESET_UI_PATH`, `SMARTCOMPTA_COMPLIANCE_PATH` | Déclarés dans `config.Settings` avec valeur par défaut | `BE/app/core/config.py` |
| `VITE_APP_BASE_PATH`, `VITE_APP_API_BASE`, `VITE_PAYROLL_API_PREFIX` | Chemins frontend | `FE/.env.*`, `Dockerfile` (ARG) |

Aucune variable n'existe pour Evolution API : sa configuration est **en base** (`whatsapp_config`), éditable par l'admin.
Le futur module ne requiert, à ce stade, aucune nouvelle variable ; toute variable ajoutée devra être documentée ici.

### 4.2 Points de configuration à risque

| Point | Constat |
|---|---|
| CORS | `allow_credentials=True`, méthodes et en-têtes `*`, origines depuis `CORS_ORIGINS` (`main.py` l.306-312). |
| `DEBUG` | Si vrai, le détail des exceptions est renvoyé au client (`main.py` l.503). |
| `uvicorn --workers 2` | État en mémoire non partagé (jobs, verrous WhatsApp, dédoublonnage, connexions WebSocket). Un événement WebSocket émis par un worker n'atteint que les clients connectés à ce worker [conception PROUVÉE ; impact réel non mesuré]. |
| Écritures de debug | Chemins Windows codés en dur (`BE/app/db/models.py` l.102, `BE/app/models/schemas.py` l.186, 243) : écriture silencieusement ignorée sous Linux, mais exécutée à chaque désérialisation. |
| `.dockerignore` | Voir §1. |

## 5. Validation des entrées et fichiers

| Point | Constat |
|---|---|
| Webhook WhatsApp | `dict[str, Any]` sans schéma. |
| Médias WhatsApp | Liste blanche d'extensions (sur le nom fourni ou déduit du MIME) et taille ≤ 15 Mo ; pas de contrôle du contenu réel. |
| Noms de fichiers d'export | Filtre `..`, `/`, `\` (`routes.py` l.437) ; `client_routes.py` l.465 ne filtre pas `\`. |
| Logo cabinet | `_resolve_logo_path` borne le chemin à `UPLOAD_DIR` / `BASE_DIR`, sauf chemin **absolu** accepté tel quel (`facturation_pdf.py` l.71-73) — `logo_url` étant modifiable sans authentification (`PUT /api/demarches/config-facture`), tout fichier image lisible du serveur peut être inséré dans un PDF [PROUVÉ par lecture ; non exécuté]. |
| Messages d'erreur | Certains détails techniques (chemin distant, message HTTP Evolution) sont envoyés à l'utilisateur WhatsApp. |

## 6. Synthèse des risques à traiter avant ou pendant l'intégration

| Priorité | Action recommandée (non réalisée — lecture seule) |
|---|---|
| P0 | Révoquer / régénérer toutes les clés et mots de passe présents dans l'archive (§1). |
| P0 | Protéger `/api/nextcloud/clients*` et `/api/demarches/*` par authentification + rôle ; ne plus exposer `nextcloud_password` dans les réponses. |
| P0 | Authentifier le webhook WhatsApp (secret partagé / jeton fourni par Evolution — mécanisme exact `NON DOCUMENTÉ — À CONFIRMER`). |
| P1 | Retirer `nextcloud_password` de `whatsapp_sessions.context_json` (ou le lire au moment de l'upload). |
| P1 | Corriger la priorité d'opérateurs de `_handle_verification` (04 WA-D4). |
| P1 | Exclure `.env`, credentials, `data/`, `uploads/`, `logs/`, `exports/` de l'image Docker et des archives. |
| P2 | Remplacer `sha256` simple par un algorithme de dérivation adapté ; supprimer les comptes par défaut. |
| P2 | Authentifier `/ws` ; ne pas transmettre le numéro de téléphone dans les diffusions. |
| P2 | Déclarer `requests` dans `requirements.txt` ou migrer vers `httpx` (déjà déclaré). |

Ces actions sortent du périmètre strict « lecture seule » de la Phase 1 et nécessitent une autorisation explicite. Le nouveau module commercial **ne doit pas** être exposé tant que P0 n'est pas traité, car il ajouterait des données de facturation à une surface API aujourd'hui partiellement publique.
