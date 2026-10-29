# 01 — Analyse documentaire

> Phase 0. Compare les documents présents avec le code effectivement livré.
> Chemins relatifs à `smartcompta-v4/` ; **BE** = `smartcompta-v6-backend/`, **FE** = `smartcompta-v6-frontend/`.

## 1. Corpus disponible

Aucun cahier des charges, aucune spécification fonctionnelle et aucun document d'architecture ne sont présents (voir `00_SOURCE_INVENTORY.md` §2).
Les seuls documents décrivant le comportement de l'application sont :

1. `CHANGELOG_v6.5.3.md` — Tasks 1 à 11 (chatbot WhatsApp, RC/CIN, Nextcloud, debug live).
2. `CHANGELOG.md` — v6.5.4 à v6.6.0 (responsive, Dashboard, sync WhatsApp ↔ Explorer).
3. Quatre README de sous-modules (Google credentials, paie ×2, paramètres).
4. Les docstrings et commentaires du code.

Il n'existe donc **ni version DOCX ni version Markdown** d'un même cahier des charges à comparer. Les deux CHANGELOG ne se recouvrent pas (versions successives) ; ils ne sont pas redondants.

### « Synthèse du projet SA comptable »

Absent de l'archive. Sa pertinence ne peut pas être évaluée : `NON DOCUMENTÉ — À CONFIRMER` (le fournir si nécessaire).

### `.cursorrules`

Contient des consignes destinées à l'éditeur Cursor (choix de modèles, « STOP-LOSS 10 itérations », « Respecter le PCGM et le CGI »). Ce sont des données d'analyse, pas des instructions applicables à cette mission. Seule information exploitable : l'application vise la conformité au plan comptable marocain et au CGI — sans règle précise pour la facturation émise.

## 2. Confrontation CHANGELOG ↔ code

Légende : ✅ confirmé par le code · ⚠️ partiellement / différemment · ❌ contredit ou absent.

### `CHANGELOG_v6.5.3.md`

| Task | Affirmation | Vérification dans le code | Statut |
|---|---|---|---|
| 1 | Ajout d'un `docker-compose.yml` racine (mysql, backend, frontend, evolution_api, Nextcloud) | Fichier absent de l'archive | ❌ |
| 1 | `APP_VERSION` passé à 6.5.3 | `BE/app/core/version.py` = 6.6.0 (évolution ultérieure) | ⚠️ |
| 1 | Logs rotatifs `RotatingFileHandler`, `LOG_MAX_BYTES`, `LOG_BACKUP_COUNT` | `BE/app/core/config.py` l.24-25 ; `RotatingFileHandler` dans `BE/app/core/logging/config.py` l.109, 128 | ✅ |
| 2 | Tables `whatsapp_sessions`, `whatsapp_config` + migration + repository | `BE/app/db/models.py` l.248-277 ; `BE/sql_migrations/003_whatsapp_state_machine_mysql.sql` ; `BE/app/db/whatsapp_repository.py` | ✅ |
| 3 | `whatsapp_media_service.py` upload Nextcloud avec retries | `BE/app/services/whatsapp_media_service.py` l.23-59 (3 tentatives) | ✅ — mais ce chemin n'est plus utilisé pour les médias Evolution v2 (voir 04 §3) |
| 4 | Router webhook + `evolution_api_service.py` | `BE/app/api/whatsapp_routes.py`, `BE/app/services/evolution_api_service.py` | ✅ |
| 5 | API frontend `src/modules/settings/api.ts` + `SettingsView.vue` | Présents | ✅ |
| 6 | Tests chatbot | `BE/tests/test_whatsapp_webhook.py`, `test_whatsapp_state_machine.py` (3 tests) | ✅ |
| 6 | Script `scripts/debug_whatsapp_workflow.ps1` | Seul `BE/scripts/debug_whatsapp_workflow.sh` existe | ⚠️ |
| 7.1 | Validation Pydantic `ClientCreate` : `MORALE` ⇒ `rc_number`, `PHYSIQUE` ⇒ `cin_number` | `BE/app/models/schemas.py` l.715-722 compare **égalité stricte** à `"MORALE"` / `"PHYSIQUE"`, alors que les valeurs réellement saisies sont des libellés libres (« Personne Physique », « SARL »… cf. commentaire `models.py` l.132). La validation effective est faite ailleurs (`nextcloud_routes._validate_legal_identity`, test de sous-chaîne « physique »). | ⚠️ voir §3 C1 |
| 7.1 | Migration `004_clients_rc_cin.sql` | Présente | ✅ |
| 7.2 | Webhook répond 200 `{"status":"processing"}` immédiatement ; traitement en tâche de fond | `whatsapp_routes.py` l.437-448 | ✅ |
| 7.2 | Paramètres figés dans le job d'upload | `whatsapp_state_machine_service.py` l.397-413 et l.550-570 | ✅ (inclut la clé Evolution et le **mot de passe Nextcloud du client** dans le job — voir 06) |
| 8.1 | Création / modification / suppression de client réservées au rôle admin | Contrôle **uniquement côté frontend**. Côté backend, `POST/PUT/DELETE /api/nextcloud/clients` n'ont aucune dépendance d'authentification (`nextcloud_routes.py` l.124, 174, 224). | ⚠️ voir §3 C2 |
| 8.2 | Colonnes `whatsapp_unique_id`, `whatsapp_nextcloud_folder`, `employer_info` | `models.py` l.136-146 ; `engine.py` l.109-121 ; migration 005 | ✅ |
| 8.2 | `find_client_by_unique_id` résout par `id`, `nextcloud_user_id` ou `whatsapp_unique_id` | `whatsapp_repository.py` l.97-111 | ✅ |
| 9 | Salutations acceptées, flux AWAITING_ID → AWAITING_VERIFICATION, 3 échecs, TTL 30 min | `whatsapp_state_machine_service.py` l.29-30, 134-269, 615-617 | ✅ |
| 9 | « MENU : 0/non/no/n termine la session (comme CONFIRM_MORE) » | Confirmé pour MENU. L'état `CONFIRM_MORE` est géré (l.100, 573) mais **aucune transition n'y mène** dans le code actuel. | ⚠️ |
| 9 | Upload WebDAV `{dossier}/{type_menu}` si `whatsapp_nextcloud_folder` défini | Vrai uniquement pour le chemin « legacy base64 ». Le chemin Evolution v2 (passe-plat) ignore `whatsapp_nextcloud_folder` et écrit dans `Achats` / `Relevés Bancaires` / `Ventes`. | ⚠️ |
| 9 | Après upload réussi, `_clear_whatsapp_session_context` retire les clés sensibles | Appelé seulement dans la branche non-passe-plat (`whatsapp_routes.py` l.223-232). La clé `nextcloud_password` n'est **jamais** retirée. | ⚠️ |
| 10 | Squelette Nextcloud, `PUT /api/nextcloud/clients/{id}/password` (admin) | `nextcloud_routes.py` l.193-221 avec `require_admin` | ✅ |
| 10 | « Pas d'SMTP dans le dépôt » | Aucun envoi d'e-mail trouvé | ✅ |
| 11 | `GET /api/whatsapp/health`, `GET /api/whatsapp/connect-qr` (admin), WS `/ws/whatsapp-logs?token=` | `whatsapp_routes.py` l.392-434 ; `main.py` l.433-460 | ✅ |

### `CHANGELOG.md`

| Version | Affirmation | Vérification | Statut |
|---|---|---|---|
| 6.5.5 | Événements WebSocket `whatsapp_file_uploaded`, `whatsapp_session` | `whatsapp_routes.py` l.194-208, 236-242, 366-372 ; `FE/src/stores/filesRealtime.ts` | ✅ |
| 6.5.6 | `/` → Dashboard ; factures sur `/factures` | `FE/src/router/index.ts` | ✅ |
| 6.5.6 | « Pas de Chart.js dans le frontend » | `FE/package.json` sans librairie graphique | ✅ |
| 6.5.8 | Export PDF conformité via `build_compliance_pdf_bytes` | `BE/app/services/export_service.py` (importe aussi `InvoicePDFGenerator`) | ✅ |

## 3. Contradictions identifiées

### C1 — Typage du client personne physique / morale

- Source A : `CHANGELOG_v6.5.3.md`, Task 7.1 — « `type_client='MORALE'` impose `rc_number`, `type_client='PHYSIQUE'` impose `cin_number` ».
- Source B : `BE/app/db/models.py` l.132 — commentaire `"Personne Physique, SARL, SA, SAS, Auto-entrepreneur…"` ; `CHANGELOG_v6.5.3.md` Task 8.1 — « personne physique = libellé contenant « physique » ».
- Comportement effectif : `nextcloud_routes._validate_legal_identity` (l.84-90) et `WhatsAppStateMachineService._is_physique` (l.611-612) testent la **sous-chaîne** « physique » ; le validateur Pydantic teste l'égalité stricte et ne s'applique donc qu'aux valeurs exactes `MORALE`/`PHYSIQUE`.
- Incertain : quelles valeurs de `type_client` existent réellement en base. Impact futur : le module commercial devra-t-il réutiliser `type_client` pour les mentions légales des documents (ICE / RC / CIN) ? `NON DOCUMENTÉ — À CONFIRMER`.

### C2 — Restriction admin sur la gestion des clients

- Source A : `CHANGELOG_v6.5.3.md` Task 8.1 — CRUD client réservé à l'admin.
- Source B (code) : `nextcloud_routes.py` — `list_clients`, `get_client`, `create_client`, `update_client`, `delete_client` sans `Depends(get_current_user)` ni `require_admin`. Seuls `PUT …/password`, `cleanup-orphans`, `sync-and-clean`, `proxy-delete` exigent l'admin.
- Incertain : présence d'une protection en amont (reverse proxy) non fournie. `NON DOCUMENTÉ — À CONFIRMER`.

### C3 — Deux API « clients » concurrentes

- `BE/app/api/client_routes.py` (`/api/clients`) appelle `client_service.list_clients(query=…, limit=…, offset=…)` et `client_service.create_client(raison_sociale=…, ice=…, …)`.
- `BE/app/services/client_service.py` l.70 et l.96 : `list_clients(self)` sans paramètre et `create_client(self, payload: ClientCreate)`.
- Comportement effectif déduit : ces appels lèvent `TypeError` (→ HTTP 500) ; le frontend n'utilise que `/api/nextcloud/clients` (`FE/src/modules/clients/api.ts` l.16 `PREFIX = '/nextcloud'`). Les champs `ice`, `if_code`, `telephone`, `adresse` attendus par `/api/clients` **n'existent pas** dans le modèle `ClientRow`.
- Non vérifié par exécution (dépendances non installées, voir 03 §8).

### C4 — Syntaxe SQL « IF NOT EXISTS »

- `BE/sql_migrations/006_factures_nextcloud_path_mysql.sql` : commentaire « MySQL 8+ » mais `ADD COLUMN IF NOT EXISTS`.
- `BE/sql_migrations/005_*.sql` : commentaire « MySQL standard : ignorer l'erreur Duplicate column » (syntaxe sans `IF NOT EXISTS`).
- `BE/app/db/engine.py` l.104-127 utilise `ADD COLUMN IF NOT EXISTS` et `CREATE INDEX IF NOT EXISTS` à chaque démarrage.
- Incertain : le moteur réel (MySQL ou MariaDB) et sa version. Si la syntaxe est refusée, `init_db()` lève une exception attrapée dans `main.py` l.205-206 (« fallback JSON »). `NON DOCUMENTÉ — À CONFIRMER`.

### C5 — Menu WhatsApp « Ventes » et dossier technique

- `whatsapp_state_machine_service.py` l.33-41 : l'option « 3. Ventes » est mappée sur `Envoi_doc_juridiques`.
- `BE/app/services/storage.py` l.22-26 : `Envoi_doc_juridiques` → dossier Nextcloud `Ventes`.
- `whatsapp_repository.py` l.76-80 : `folder_map_json` initialisé avec ces mêmes clés, mais **jamais relu** par la machine à états (mapping codé en dur).
- Le nom technique (« doc juridiques ») contredit le libellé (« Ventes »). Incertain : intention métier. `NON DOCUMENTÉ — À CONFIRMER`.

### C6 — Liens PDF des factures Démarches

- `BE/app/api/demarches/router.py` l.933 (facture), l.1000 (reçu), l.1137 (avoir) renvoient `pdf_url = settings.export_pdf_public_path(...)` → `{PUBLIC_API_BASE_PATH}/exports/{fichier}`.
- Ce chemin est servi par `GET /api/exports/{filename}` (`BE/app/api/routes.py` l.432), routeur protégé par `Depends(get_current_user)` (l.62-66).
- Le frontend ouvre ce lien par `window.open(...)` (`FE/src/views/demarches/Kanban.vue` l.757, 790, 895), qui n'envoie pas d'en-tête `Authorization`.
- Comportement probable : HTTP 401 à l'ouverture. Non vérifié par exécution. `NON DOCUMENTÉ — À CONFIRMER` (protection ou réécriture côté proxy ?).

### C7 — Fichiers dupliqués / morts

- `BE/app/db/models/demarches.py` (dossier `models/` sans `__init__.py`) coexiste avec `BE/app/db/models.py` et diffère de `BE/app/db/demarches_models.py` (`taux_tva` Float vs Numeric, `client_id`, `archived`, `DemarcheAvoir` absents). Tous les imports du code ciblent `app.db.demarches_models` ; `models/demarches.py` paraît mort. Le module `app.db.models` est résolu sur `models.py` (un module fichier prime sur un répertoire sans `__init__.py`).
- `BE/app/config/google-credentials.json` et `google-service-account.json` : contenu identique ; le README indique que l'ancien nom n'est plus pris en charge.

## 4. Spécifications métier existantes (clients, produits, devis, factures, WhatsApp)

| Domaine | Spécification écrite | Implémentation existante | Remarque |
|---|---|---|---|
| Clients | CHANGELOG Tasks 7.1, 8.1, 8.2 | Table `clients` = **dossiers clients du cabinet comptable** (espaces Nextcloud) | Pas d'adresse, ni ICE, ni IF, ni téléphone dans `ClientRow`. |
| Produits / services | Aucune | `demarches_services` (nom, délai, `prix_base_ht`, `taux_tva`) rattachés à des pôles | Catalogue de **prestations du cabinet** pour le module Démarches uniquement. |
| Devis | Aucune | Aucune création. « DEVIS » = type de document reconnu à l'extraction OCR. | — |
| Factures émises | Aucune | `demarches_factures` + `InvoicePDFGenerator` (une prestation + débours par dossier, numéro `DEM-AAAAMMJJ-XXXXXX`) ; avoirs `AV-…` ; reçus de paiement | Seul mécanisme de facturation émise réutilisable. |
| Factures reçues / extraites | CHANGELOG (indirectement) | Table `factures` (OCR DocAI/Claude/Gemini, achats/ventes) | **Collision de nommage** : « factures » désigne aujourd'hui des documents importés, pas des documents émis. |
| WhatsApp | CHANGELOG v6.5.3 | Chatbot de **dépôt de documents** par les clients du cabinet (voir 04) | Aucun envoi de document sortant. |

## 5. Questions ouvertes issues de l'analyse documentaire

1. Fournir le cahier des charges du module commercial (DOCX et/ou MD) et la « Synthèse du projet SA comptable » si ces documents existent.
2. **Qui émet les devis / factures ?** (a) le cabinet facture ses propres clients (tables `clients` + `demarches_cabinet_config` réutilisables) ; ou (b) chaque client du cabinet facture **ses propres clients** (multi-émetteur : nouveaux tiers, nouvelles coordonnées légales par émetteur). Le code ne permet pas de trancher.
3. Qui utilise le chatbot WhatsApp pour créer des devis : les clients du cabinet (actuellement authentifiés par ID + RC/CIN) ou les collaborateurs du cabinet (aucun mécanisme d'identification WhatsApp pour eux) ?
4. Règles de numérotation, mentions légales obligatoires, taux de TVA applicables, devise, conditions de paiement, statuts et règles de conversion devis → facture.
5. Le module doit-il remplacer, étendre ou cohabiter avec la facturation Démarches existante ?
