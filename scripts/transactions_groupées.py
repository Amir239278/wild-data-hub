import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de l'affichage
plt.style.use('default')
sns.set_theme()

# Lecture des données
print("Lecture du fichier DVF...")
df = pd.read_csv('dvf.csv.gz', compression='gzip', low_memory=False)

# 1. Analyse des transactions groupées
print("\nAnalyse des transactions groupées...")
# Compter le nombre de lots par transaction
grouped_transactions = df.groupby('id_mutation').size()
print(f"\nNombre total de transactions uniques : {len(grouped_transactions)}")
print(f"Nombre de transactions avec plusieurs lots : {len(grouped_transactions[grouped_transactions > 1])}")

# 2. Analyse détaillée d'une transaction groupée
# Exemple avec la transaction 2024-1218061
transaction_exemple = df[df['id_mutation'] == '2024-1218061']
print("\nAnalyse détaillée de la transaction 2024-1218061 :")
print(f"Date de mutation : {transaction_exemple['date_mutation'].iloc[0]}")
print(f"Valeur foncière totale : {transaction_exemple['valeur_fonciere'].iloc[0]:,.2f} €")
print(f"Surface totale du terrain : {transaction_exemple['surface_terrain'].iloc[0]} m²")

# Calcul des surfaces et prix
surface_totale_bati = transaction_exemple['surface_reelle_bati'].sum()
prix_m2_bati = transaction_exemple['valeur_fonciere'].iloc[0] / surface_totale_bati
prix_m2_terrain = transaction_exemple['valeur_fonciere'].iloc[0] / transaction_exemple['surface_terrain'].iloc[0]

print(f"\nSurface totale bâtie : {surface_totale_bati} m²")
print(f"Prix au m² bâti : {prix_m2_bati:,.2f} €/m²")
print(f"Prix au m² terrain : {prix_m2_terrain:,.2f} €/m²")

# 3. Analyse des types de biens dans les transactions groupées
print("\nRépartition des types de biens dans les transactions groupées :")
grouped_by_type = df[df.groupby('id_mutation')['id_mutation'].transform('count') > 1]['type_local'].value_counts()
print(grouped_by_type)

# 4. Visualisation
plt.figure(figsize=(12, 6))
grouped_by_type.plot(kind='bar')
plt.title('Répartition des types de biens dans les transactions groupées')
plt.xlabel('Type de bien')
plt.ylabel('Nombre de lots')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('repartition_types_biens.png')
plt.close()

# 5. Analyse des prix moyens par type de bien dans les transactions groupées
print("\nPrix moyens par type de bien dans les transactions groupées :")
grouped_prices = df[df.groupby('id_mutation')['id_mutation'].transform('count') > 1].groupby('type_local')['valeur_fonciere'].mean()
print(grouped_prices)

# 6. Création d'un DataFrame résumé des transactions groupées
grouped_summary = df.groupby('id_mutation').agg({
    'date_mutation': 'first',
    'valeur_fonciere': 'first',
    'surface_terrain': 'first',
    'type_local': lambda x: list(x),
    'surface_reelle_bati': 'sum'
}).reset_index()

# Calcul du prix au m²
grouped_summary['prix_m2'] = grouped_summary['valeur_fonciere'] / grouped_summary['surface_reelle_bati']

# Sauvegarde du résumé
grouped_summary.to_csv('transactions_groupées_resumé.csv', index=False)
print("\nRésumé des transactions groupées sauvegardé dans 'transactions_groupées_resumé.csv'")

# 7. Statistiques descriptives des transactions groupées
print("\nStatistiques descriptives des transactions groupées :")
print(grouped_summary[['valeur_fonciere', 'surface_terrain', 'surface_reelle_bati', 'prix_m2']].describe()) 