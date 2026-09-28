# Analyse des prix immobiliers dans le Nord (59) — DVF 2025

Projet personnel de data analyse : exploration des prix de l'immobilier dans le département du Nord à partir des données DVF (Demandes de Valeurs Foncières), publiées par l'administration française.

**Dashboard interactif : [Voir sur Tableau Public](https://public.tableau.com/app/profile/walid.mekhalif/viz/dvf-nord-2025-fast-analyse/Tableaudebord1)**

---

## Contexte et question

Comment évoluent les prix au m² dans le Nord en 2025, selon le type de bien, la commune et la période de l'année ?

## Données

- **Source** : [DVF — data.gouv.fr](https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/)
- **Périmètre** : ventes de maisons et appartements dans le département du Nord (59), année 2025
- **Format d'origine** : fichier texte brut (`.txt`), séparateur `|`, décimales avec virgule

Le fichier brut n'est pas versionné dans ce dépôt (trop volumineux). Pour reproduire le projet, télécharger le fichier DVF correspondant sur data.gouv.fr et le placer dans `Solo_DVF_France_2025/`.

## Pipeline

1. **`DVF_France_2025.py`** — Lecture du fichier national, sélection des colonnes utiles, filtrage sur le département 59.
2. **`clear.py`** — Nettoyage :
   - Conservation des ventes classiques (`Nature mutation = Vente`)
   - Conservation des maisons et appartements uniquement
   - Suppression des lignes sans prix ou sans surface
   - Suppression des ventes groupées (plusieurs biens vendus sous une même transaction, identifiés par date + prix + adresse identiques), pour éviter de fausser le prix au m²
   - Calcul du prix au m²
3. **`outliers.py`** — Suppression des valeurs aberrantes : prix au m² hors de la plage 500–10 000 €, surface hors de la plage 9–500 m². Ces bornes sont un choix d'analyste, pas une vérité absolue : elles écartent les ventes atypiques (viager, vente partielle, erreurs de saisie) sans toucher au cœur de la distribution. Environ 3 % des lignes ont été écartées à cette étape.
4. **`charger_py.py`** — Chargement des données nettoyées dans une base PostgreSQL, avec identifiants gérés via un fichier `.env` (non versionné).

## Analyse

Les requêtes SQL (médiane par type de bien, classement des communes, évolution mensuelle) se trouvent dans le dossier `Solo_DVF_France_2025`. La médiane est utilisée plutôt que la moyenne pour résister aux valeurs extrêmes. Le classement des communes exclut celles ayant moins de 30 ventes sur l'année, pour ne pas classer une commune sur la base de 2 ou 3 transactions.

## Résultats clés

- Les appartements se vendent à **2 761 €/m²** en médiane, contre **1 939 €/m²** pour les maisons, soit environ **+42 %**.
- Le prix médian mensuel varie d'environ 10 % sur l'année, avec un pic en août (2 266 €/m²) et un creux en mai (2 018 €/m²). Cette variation reste à interpréter avec prudence : elle peut refléter un effet saisonnier réel autant qu'un nombre de ventes plus faible certains mois.
- Le Top 10 des communes les plus chères (à 30 ventes minimum) est mené par Bondues (4 000 €/m²) et Marcq-en-Barœul (3 703 €/m²).

## Outils utilisés

- **Python** (pandas) pour le nettoyage
- **PostgreSQL** pour le stockage et l'analyse SQL
- **Tableau Public** pour la visualisation

## Reproduire le projet

```bash
pip install -r requirements.txt
```

1. Télécharger le fichier DVF du Nord (2025) sur data.gouv.fr et le placer dans `Solo_DVF_France_2025/`
2. Créer un fichier `.env` à la racine avec `DB_PASSWORD=votre_mot_de_passe`
3. Créer une base PostgreSQL nommée `dvf`
4. Exécuter dans l'ordre : `DVF_France_2025.py` → `clear.py` → `outliers.py` → `charger_py.py`

## Limites et pistes d'amélioration

- Les ventes groupées sont exclues plutôt que consolidées, ce qui simplifie le nettoyage mais écarte une partie des données.
- L'analyse se limite au département du Nord ; une comparaison avec d'autres départements serait une suite naturelle.
- Une carte des prix par commune (via les coordonnées géographiques) enrichirait le dashboard.
