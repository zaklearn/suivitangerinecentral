# 02 — Registre et traçabilité des exigences

> Phase 0. Aucune spécification métier n'étant fournie (voir 01 §1), la source principale est le **prompt de mission** (« PROMPT MAÎTRE — SMARTCOMPTA », noté **PM**, avec son numéro de section).
> Les sources secondaires sont `CHANGELOG_v6.5.3.md` (**CL653**), `CHANGELOG.md` (**CL**) et le code (**BE**/**FE**).
> Aucune exigence n'est considérée comme satisfaite parce qu'elle figure dans un document : la colonne « Existant » reflète uniquement le code lu.

## Échelle de certitude

| Niveau | Signification |
|---|---|
| **C1 — Explicite** | Formulée explicitement dans PM. |
| **C2 — Implicite** | Découle nécessairement d'une exigence explicite. |
| **C3 — À confirmer** | Plausible, mais aucune source ne la fixe ; `NON DOCUMENTÉ — À CONFIRMER`. |

## Légende « Existant »

`ABSENT` · `PARTIEL` (mécanisme voisin réutilisable) · `EXISTANT` (prouvé par le code) · `CONTRAINTE` (exigence de méthode, pas de fonctionnalité).

## 1. Exigences fonctionnelles — Mode A (interface)

| ID | Source / emplacement | Certitude | Traduction fonctionnelle | Existant (preuve) | Vérification | Dépendances / inconnues |
|---|---|---|---|---|---|---|
| REQ-CLI-01 | PM §1 item 1 ; §3 Mode A puce 1 | C1 | Consulter, rechercher et gérer des clients (tiers facturés). | PARTIEL — table `clients` (`BE/app/db/models.py` l.118-167), UI `FE/src/views/ClientManagementView.vue`, API `/api/nextcloud/clients`. Il s'agit des **dossiers clients du cabinet**, sans adresse, ICE, IF, téléphone. | Test API CRUD + test UI de recherche. | Q-01 (qui facture qui ?). Q-02 (champs obligatoires). Risque d'incompatibilité avec `/api/clients` cassé (01 §3 C3). |
| REQ-CLI-02 | PM §3 Mode A « périmètre CRUD exact… défini après analyse » | C1 | Définir le périmètre CRUD client après validation. | — | Validation écrite du périmètre. | Q-02. |
| REQ-CAT-01 | PM §1 item 2 ; §3 Mode A puce 2 | C1 | Consulter, rechercher et gérer un catalogue de produits et services. | PARTIEL — `demarches_services` (nom, `prix_base_ht` Numeric(12,2), `taux_tva` Numeric(5,2)) et pôles (`BE/app/db/demarches_models.py` l.35-58), CRUD `/api/demarches/services`. Pas de produit, unité, référence, stock. | Test CRUD + recherche. | Q-03 (réutiliser ou créer un catalogue distinct ?). Q-06 (TVA). |
| REQ-DEV-01 | PM §1 item 3 ; §3 Mode A puce 3 | C1 | Créer, consulter, modifier et gérer des devis. | ABSENT (« DEVIS » n'existe que comme type OCR). | Tests unitaires service + API + UI. | Q-04 (statuts), Q-05 (numérotation). |
| REQ-FAC-01 | PM §1 item 4 ; §3 Mode A puce 4 | C1 | Créer, consulter, modifier et gérer des factures émises. | PARTIEL — `demarches_factures` + `POST /api/demarches/{dossier_id}/generer-facture` (`BE/app/api/demarches/router.py` l.843-948) : 1 prestation + débours par dossier, pas de lignes multiples, pas de modification. | Tests service + API + UI. | Q-05, Q-07 (modification d'une facture émise autorisée ?), collision de nom avec la table `factures` (OCR). |
| REQ-LIG-01 | PM §3 Mode A puce 5 | C1 | Sélectionner un client et **un ou plusieurs** produits pour un document. | ABSENT (Démarches : un seul service par dossier, `DemarcheDossier.service_id`). | Test création multi-lignes. | REQ-CAT-01. |
| REQ-LIG-02 | PM §3 Mode A puce 6 | C1 | Saisir les quantités et « autres informations commerciales requises ». | ABSENT | Test de validation des champs. | Q-08 (remise, unité, date de validité, conditions de paiement… non définis). |
| REQ-TOT-01 | PM §3 Mode A puce 7 | C1 | Consulter lignes, totaux et statuts. | PARTIEL — calculs HT/TVA/TTC en `Decimal` quantize 0.01 dans `generer_facture` (router l.875-885) et `InvoicePDFGenerator.generate`. Utilitaire `BE/app/utils/money.py` présent. | Tests de calcul avec cas limites d'arrondi. | Q-06 (règle d'arrondi : par ligne ou sur total ?). |
| REQ-PDF-01 | PM §1 item 5 ; §3 Mode A puce 8 | C1 | Prévisualiser et générer le PDF d'un devis / d'une facture. | PARTIEL — `InvoicePDFGenerator` ReportLab A4 (`BE/app/services/facturation_pdf.py`) : facture, avoir, reçu. Pas de modèle « devis ». | Test de génération + contrôle visuel + test de contenu (extraction texte). | Q-09 (mentions légales). |
| REQ-PDF-02 | PM §3 Mode A puce 9 | C1 | Télécharger / récupérer le document selon les mécanismes disponibles. | PARTIEL — fichiers écrits dans `BE/exports/` ; téléchargement `GET /api/exports/{filename}` authentifié ; purge automatique des exports > 7 jours au démarrage (`BE/main.py` l.242-248). | Test de téléchargement authentifié. | Rétention : un document commercial purgé après 7 jours est-il acceptable ? Q-10. Problème probable d'ouverture des liens (01 §3 C6). |
| REQ-CONV-01 | PM §3 Mode A « règles de conversion d'un devis en facture » | C1 (à définir) | Convertir un devis accepté en facture. | ABSENT | Test de conversion. | Q-04, Q-05. |

## 2. Exigences fonctionnelles — Mode B (WhatsApp)

| ID | Source / emplacement | Certitude | Traduction fonctionnelle | Existant (preuve) | Vérification | Dépendances / inconnues |
|---|---|---|---|---|---|---|
| REQ-WA-01 | PM §1 item 7 ; §3 Mode B §1 | C1 | Réutiliser le chatbot WhatsApp existant s'il est réutilisable. | EXISTANT — webhook `POST /api/whatsapp/webhook`, machine à états persistée, envoi texte Evolution API (voir 04). | Revue d'architecture + tests de non-régression du flux de dépôt. | Le menu actuel (1/2/3/0) devra être étendu sans casser le dépôt de documents. |
| REQ-WA-02 | PM §3 Mode B §2 | C1 | Le bot permet de choisir une opération. | PARTIEL — état `MENU` (`whatsapp_state_machine_service.py` l.287-319), options codées en dur. | Test de transition MENU → nouvelle opération. | Q-11 (liste des opérations WhatsApp). |
| REQ-WA-03 | PM §3 Mode B §2 | C1 | Transmettre les informations nécessaires (client, produits, quantités…). | ABSENT — seule saisie libre d'ID, RC/CIN, choix de menu. | Tests de dialogue. | Q-12 (désignation des produits par code ? recherche ?). |
| REQ-WA-04 | PM §3 Mode B §2 | C1 | Afficher un récapitulatif et demander une confirmation avant création. | ABSENT (`CONFIRM_MORE` existe mais n'est jamais atteint). | Test : aucun document créé sans confirmation explicite. | — |
| REQ-WA-05 | PM §3 Mode B §3 | C1 | Le backend exécute l'opération métier réelle. | — | Test : le bot appelle le **même service métier** que l'UI. | REQ-ARCH-01. |
| REQ-WA-06 | PM §3 Mode B §3 | C1 | Générer le PDF et le **renvoyer dans la conversation** WhatsApp. | ABSENT — `EvolutionApiService` n'a que `send_text_message`, `fetch_media`, `probe_instance`, `fetch_instance_connect_qr`. | Test avec Evolution API simulée. | Q-13 : l'endpoint Evolution d'envoi de média et son schéma ne sont **pas documentés dans les sources** ; aucune hypothèse ne sera codée sans documentation fournie. |
| REQ-WA-07 | PM §3 Mode B dernière phrase | C1 | Le chatbot ne fabrique jamais lui-même un devis / une facture. | — | Revue de code + test : aucune construction de document hors service métier. | — |
| REQ-WA-08 | PM §3 Mode B §1 | C2 | Identifier et autoriser l'utilisateur WhatsApp avant toute opération commerciale. | PARTIEL — handshake ID unique + RC/CIN (04 §2). Webhook non authentifié (06). | Tests d'autorisation négatifs. | Q-14 (rôle de l'utilisateur WhatsApp). |
| REQ-WA-09 | PM §5.2 (identifiants de conversation, erreurs, persistance, tâches asynchrones) | C2 | Rattacher chaque document produit à la conversation d'origine ; gérer erreurs et reprises. | PARTIEL — session unique par numéro, dédoublonnage en mémoire par `key.id`, verrou par numéro, tâches `asyncio.create_task`. | Tests de concurrence / doublons. | Mémoire non partagée entre les 2 workers uvicorn (06). |

## 3. Exigences d'architecture et de méthode

| ID | Source / emplacement | Certitude | Traduction | Existant | Vérification | Remarques |
|---|---|---|---|---|---|---|
| REQ-ARCH-01 | PM §1 dernier §, §3 Mode B | C1 | Réutiliser les mécanismes existants adaptés ; pas de duplication ; un seul service métier pour UI et WhatsApp. | CONTRAINTE | Revue de conception. | Candidats : `InvoicePDFGenerator`, `DemarcheCabinetConfig`, `get_session`, `require_admin`/`get_current_user`, `evolution_api_service`, machine à états. |
| REQ-ARCH-02 | PM §2 « ne pas remplacer un composant avant d'avoir compris son rôle » | C1 | Aucune réécriture du chatbot, du module Démarches ou de la table `factures`. | CONTRAINTE | Revue de diff. | — |
| REQ-SRC-01 | PM §2 | C1 | Sources fermées ; pas d'Internet ; marquer `NON DOCUMENTÉ — À CONFIRMER`. | CONTRAINTE | Revue des rapports. | Respecté : aucune ressource externe consultée. |
| REQ-DEP-01 | PM §2 | C1 | Aucune dépendance installée sans justification et autorisation. | CONTRAINTE | Revue de `requirements.txt` / `package.json`. | ReportLab, Jinja2, xhtml2pdf déjà présents. Tests non exécutés faute de dépendances installées (03 §8). |
| REQ-BIZ-01 | PM §2 dernière puce | C1 | Ne pas inventer tarifs, règles fiscales, règles de calcul, mentions légales. | CONTRAINTE | Revue. | Le code contient déjà des choix (TVA par défaut 20 %, taux 20/14/10/7/0 dans `config.TVA_RATES`, débours « exonérés ») : **à valider**, non à généraliser. |
| REQ-SEC-01 | PM §5.4 | C1 | Ne jamais divulguer ni copier les secrets ; documenter seulement les noms. | CONTRAINTE | Revue des rapports. | Voir 06. |
| REQ-TST-01 | PM §1 « tests de non-régression » | C1 | Tests de non-régression avant / après intégration. | PARTIEL — 17 modules de test backend existants (03 §8). | Exécution de la suite complète. | Environnement de test à fournir (MySQL, dépendances). |
| REQ-DOC-01 | PM §4, §5 | C1 | Produire les livrables 00 à 06. | Ce document et ses voisins. | — | Emplacement à confirmer (00 §0). |

## 4. Questions ouvertes (bloquantes pour la conception)

| ID | Question | Bloque |
|---|---|---|
| Q-01 | Émetteur des documents : le cabinet (un seul émetteur, `demarches_cabinet_config`) ou chaque client du cabinet (multi-émetteur) ? | Modèle de données entier |
| Q-02 | Champs obligatoires d'un client facturé (adresse, ICE, IF, RC, téléphone, e-mail…) ? | REQ-CLI-* |
| Q-03 | Catalogue : étendre `demarches_services` ou créer un catalogue dédié (produits + services) ? | REQ-CAT-01 |
| Q-04 | Statuts des devis et factures, transitions autorisées, conversion devis → facture (totale, partielle, multiple) ? | REQ-DEV-01, REQ-CONV-01 |
| Q-05 | Format et séquence de numérotation (continuité annuelle ? par émetteur ?). Le format `DEM-AAAAMMJJ-<hex>` actuel est aléatoire, non séquentiel. | REQ-DEV-01, REQ-FAC-01 |
| Q-06 | Taux de TVA autorisés, règle d'arrondi, devise (MAD codée en dur dans le PDF Démarches). | REQ-TOT-01 |
| Q-07 | Une facture émise peut-elle être modifiée ou seulement annulée par avoir ? | REQ-FAC-01 |
| Q-08 | « Autres informations commerciales requises » : remise, unité, validité, conditions de paiement, notes ? | REQ-LIG-02 |
| Q-09 | Mentions légales obligatoires sur devis et factures. | REQ-PDF-01 |
| Q-10 | Durée de conservation et lieu de stockage des PDF (disque local purgé à 7 jours, Nextcloud du client, autre) ? | REQ-PDF-02 |
| Q-11 | Opérations WhatsApp attendues (créer devis, créer facture, convertir, consulter, renvoyer un PDF…) ? | REQ-WA-02 |
| Q-12 | Mode de saisie des produits sur WhatsApp (code, recherche textuelle, liste numérotée) ? | REQ-WA-03 |
| Q-13 | Documentation de l'endpoint Evolution API d'envoi de document (version déployée) ? | REQ-WA-06 |
| Q-14 | Rôle et autorisations de l'utilisateur WhatsApp (client du cabinet ou collaborateur) ; correspondance numéro ↔ utilisateur ? | REQ-WA-08 |
