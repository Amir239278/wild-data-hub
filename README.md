# Analyse des Transactions Immobilières DVF

Ce projet analyse les données DVF (Demandes de Valeurs Foncières) de la DGFiP pour comprendre les tendances du marché immobilier.

## Structure du Projet

- `dvf.csv.gz` : Données brutes des transactions immobilières
- `analyse_dvf.py` : Script d'analyse des données
- `requirements.txt` : Dépendances Python nécessaires

## Installation

1. Créer un environnement virtuel Python :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/MacOS
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

Pour exécuter l'analyse :
```bash
python analyse_dvf.py
```

## Données

Les données DVF contiennent les informations suivantes :
- Valeur foncière
- Type de local
- Surface
- Date de mutation
- Localisation
- Et plus encore...

## Analyse

Le script `analyse_dvf.py` génère :
- Des statistiques descriptives sur les transactions
- Des visualisations de la distribution des prix
- Une analyse par type de local 