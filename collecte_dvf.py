import requests, hashlib, os
from datetime import datetime
import pandas as pd

# 📂 Dossier racine du script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dossier = os.path.join(BASE_DIR, "dataset")
os.makedirs(dossier, exist_ok=True)

# 🔗 URL source
url_dvf = "https://www.data.gouv.fr/fr/datasets/r/d7933994-2c66-4131-a4da-cf7cd18040a4"

# 📄 Chemins des fichiers
temp_file = os.path.join(dossier, "dvf_temp.csv.gz")
hash_file = os.path.join(dossier, "dvf_hash.txt")
log_file = os.path.join(dossier, "dvf.log")

def log(msg):
    """🧾 Ajoute un message timestampé au fichier de log"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def sha1(path):
    """🔍 Calcule le hash SHA-1 d'un fichier"""
    h = hashlib.sha1()
    try:
        with open(path, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        log(f"❌ Fichier introuvable pour le hash : {path}")
        return None

def collecter_dvf():
    log("🚀 Script collecte_dvf.py lancé...")
    log("📥 Téléchargement du fichier DVF...")

    try:
        r = requests.get(url_dvf, stream=True, timeout=30)
        if r.status_code != 200:
            log(f"❌ Erreur HTTP {r.status_code}")
            return None
    except Exception as e:
        log(f"❌ Exception lors du téléchargement : {e}")
        return None

    with open(temp_file, 'wb') as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    log(f"📁 Fichier temporaire sauvegardé sous : {temp_file}")

    nouveau_hash = sha1(temp_file)
    log(f"🔍 Nouveau hash : {nouveau_hash}")

    try:
        with open(hash_file) as f:
            ancien_hash = f.read().strip()
    except Exception:
        ancien_hash = None

    log(f"🗂️ Ancien hash : {ancien_hash if ancien_hash else 'Aucun'}")

    if nouveau_hash and nouveau_hash != ancien_hash:
        nom_fichier = f"dvf_{datetime.today().strftime('%Y%m%d')}.csv.gz"
        chemin_final = os.path.join(dossier, nom_fichier)
        os.rename(temp_file, chemin_final)
        with open(hash_file, 'w') as f:
            f.write(nouveau_hash)
        log(f"✅ Nouveau fichier détecté et sauvegardé sous {nom_fichier}")
        return chemin_final
    else:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        log("✔️ Aucun changement — fichier inchangé.")
        return None

def nettoyer_dvf(chemin_fichier):
    log("🔍 Chargement du fichier dans un DataFrame...")
    try:
        df = pd.read_csv(chemin_fichier, compression='gzip', low_memory=False, encoding='ISO-8859-1')
    except Exception as e:
        log(f"❌ Erreur lors du chargement CSV : {e}")
        return

    log(f"📊 {len(df):,} lignes brutes chargées.")

    try:
        # Étapes de nettoyage
        colonnes_supp = [
            'adresse_suffixe', 'ancien_code_commune', 'ancien_nom_commune', 'ancien_id_parcelle',
            'numero_volume', 'nature_culture_speciale', 'code_nature_culture',
            'lot1_numero', 'lot1_surface_carrez','lot2_numero', 'lot2_surface_carrez',
            'lot3_numero', 'lot3_surface_carrez', 'lot4_numero', 'lot4_surface_carrez',
            'lot5_numero', 'lot5_surface_carrez', 'nombre_lots', 'code_nature_culture_speciale',
            'surface_terrain', 'nature_culture'
        ]
        df = df.drop(columns=colonnes_supp, errors='ignore')
        df = df.dropna(subset=['valeur_fonciere', 'longitude', 'type_local'])
        df = df[df["type_local"].isin(["Maison", "Appartement"])]
        df = df[df["nature_mutation"].isin(["Vente", "Vente en l'etat futur d'achèvement"])]
        df = df.drop_duplicates()

        df_agrégé = df.groupby('id_mutation', as_index=False).agg({
            'date_mutation': 'first', 'numero_disposition': 'first', 'nature_mutation': 'first',
            'valeur_fonciere': 'first', 'adresse_numero': 'first', 'adresse_nom_voie': 'first',
            'adresse_code_voie': 'first', 'code_postal': 'first', 'code_commune': 'first',
            'nom_commune': 'first', 'code_departement': 'first', 'id_parcelle': 'first',
            'code_type_local': 'first', 'surface_reelle_bati': 'sum',
            'nombre_pieces_principales': 'sum', 'type_local': 'first',
            'longitude': 'first', 'latitude': 'first'
        })

        df_agrégé['prix_m2'] = df_agrégé['valeur_fonciere'] / df_agrégé['surface_reelle_bati']
        df_agrégé = df_agrégé[~df_agrégé['prix_m2'].isin([float('inf'), float('-inf')])]
        df_agrégé = df_agrégé[df_agrégé['prix_m2'] != 0]
        df_agrégé['prix_m2'] = df_agrégé['prix_m2'].astype(int)
        df_agrégé['date_mutation'] = pd.to_datetime(df_agrégé['date_mutation'])

        chemin_sortie = os.path.join(dossier, 'df_agrégé.csv')
        df_agrégé.to_csv(chemin_sortie, index=False)
        log(f"🧹 Fichier nettoyé et sauvegardé sous {chemin_sortie}")
    except Exception as e:
        log(f"❌ Erreur dans le nettoyage : {e}")

# 🚀 Pipeline principal
if __name__ == "__main__":
    chemin = collecter_dvf()
    if chemin:
        nettoyer_dvf(chemin)
    else:
        log("ℹ️ Aucun fichier à nettoyer — script terminé.")
