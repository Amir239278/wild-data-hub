import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de l'affichage
plt.style.use('default')
sns.set_theme()

# Lecture des données
print("Lecture du fichier DVF...")
df = pd.read_csv('data/raw/dvf.csv.gz', compression='gzip', low_memory=False)

# ... existing code ...

grouped_summary = df.groupby('id_mutation').agg({
    'date_mutation': 'first',
    'valeur_fonciere': 'first',
    'surface_terrain': 'first',
    'type_local': lambda x: list(x),
    'surface_reelle_bati': 'sum'
}).reset_index()

# Sauvegarde du résumé
grouped_summary.to_csv('data/processed/transactions_groupées_resumé.csv', index=False)
print("\nRésumé des transactions groupées sauvegardé dans 'data/processed/transactions_groupées_resumé.csv'")

# ... existing code ... 