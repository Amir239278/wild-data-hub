# Analyse des Transactions Immobilières (DVF)

Ce projet vise à analyser les transactions immobilières issues du fichier DVF (Demandes de Valeurs Foncières) en France.

## Structure du projet

```
Projet-3/
│
├── data/
│   ├── raw/                # Données brutes (ex: dvf.csv.gz)
│   └── processed/          # Résultats d'analyse (transactions_groupées_resumé.csv)
│
├── notebooks/              # Notebooks Jupyter pour exploration
│
├── scripts/                # Scripts Python pour traitement et analyse
│   └── transactions_groupées.py
│
├── rapports/               # Graphiques, rapports, visualisations
│
├── README.md               # Présentation du projet
└── requirements.txt        # Dépendances Python
```

## Lancer l'analyse

1. Placez le fichier `dvf.csv.gz` dans `data/raw/`.
2. Exécutez le script principal :
   ```bash
   python3 scripts/transactions_groupées.py
   ```
3. Les résultats seront générés dans `data/processed/` et les graphiques dans `rapports/`.

## Dépendances
- pandas
- numpy
- matplotlib
- seaborn

Installez-les avec :
```bash
pip install -r requirements.txt
```

## Objectif
- Nettoyer et structurer les données DVF
- Analyser les transactions groupées (ventes en bloc)
- Générer des statistiques et des visualisations

## Auteur
Meraka Amir 