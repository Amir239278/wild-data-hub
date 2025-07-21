import streamlit as st
from estimation import estimer_depuis_adresse  # importe la fonction qui contient déjà les modèles
from streamlit_folium import st_folium
import re

# Initialisation de la session pour stocker l'historique
if "historique_estimations" not in st.session_state:
    st.session_state.historique_estimations = []

st.set_page_config(page_title="Estimation immobilière", page_icon="🏡")
departements = [
    "01 - Ain",
    "26 - Drôme",
    "31 - Haute-Garonne",
    "33 - Gironde",
    "35 - Ille-et-Vilaine",
    "38 - Isère",
    "44 - Loire-Atlantique",
    "45 - Loiret",
    "63 - Puy-de-Dôme",
    "69 - Rhône"
]

# Sidebar avec informations
with st.sidebar:
    st.markdown("### 📊 Informations")
    st.markdown("""
    - **Modèle** : IA hybride  
    - **Sources** : Données DVF (data.gouv) & Observatoire des territoires  
    - **Mise à jour** : Semestrielle 
    - **Précision** : ±15%  
    """)

    st.markdown("### 🛠️ Fonctionnalités")
    st.markdown("""
    - Estimation par adresse  
    - Analyse géographique  
    - Comparaison de prix  
    - Tendances du marché  
    """)


st.title("🏘️ Où acheter et à quel prix ?")

# Création des onglets
onglet_carte, onglet_estimation = st.tabs(["🗺️ Analyse des départements", "📊 Estimation d'une adresse"])

with onglet_estimation:
    st.markdown("Entrez les infos de votre bien immobilier pour obtenir une estimation par modèle hybride :")

    departement_selectionne = st.selectbox("🗺️​ Départements disponibles", departements)
    code_departement = departement_selectionne.split(" - ")[0]

    adresse = st.text_input("📍 Adresse complète (adresse, code postal et ville)", placeholder="Ex : 15 rue Félix Thomas, 44000 Nantes")
    # code_postal = st.text_input("🏷️ Code postal", placeholder="44000")
    match = re.search(r'\b\d{5}\b', adresse)
    code_postal = match.group() if match else None
    col1, col2 = st.columns(2)
    with col1:
        type_local = st.selectbox("🏠 Type de bien", ["Appartement", "Maison"])
    with col2:
        nb_pieces = st.number_input("🔢 Nombre de pièces", 1, 12, 3)

    surface = st.number_input("📐 Surface habitable (m²)", 10, 500, 60)

    if st.button("🔮 Estimer le bien"):
        if not adresse : # or not code_postal:
            st.warning("Merci de renseigner à la fois l'adresse complète.")
        elif not code_postal.startswith(code_departement):
            st.error(f"Le code postal doit commencer par {code_departement} (département sélectionné).")
        else:
            with st.spinner("Estimation en cours..."):
                resultat = estimer_depuis_adresse(
                    adresse_str=adresse,
                    type_local=type_local,
                    surface=surface,
                    nb_pieces=nb_pieces,
                    code_postal=code_postal
                )

            if "erreur" in resultat:
                st.error(resultat["erreur"])
            else:
                st.success("✅ Estimation réussie !")
                st.markdown(f"**📏 Prix/m² estimé** : `{format(resultat['prix_m2_estime'], ',.2f').replace(',', ' ').replace('.', ',')} €`")
                st.markdown(f"**💶 Valeur foncière estimée** : `{resultat['valeur_fonciere_estimee']:,}`".replace(",", " ") + " €")
                st.markdown(f"**📎 Fourchette de confiance** : `{resultat['fourchette'][0]:,}`".replace(",", " ") + " € – " + f"`{resultat['fourchette'][1]:,}`".replace(",", " ") + " €")
                st.markdown(f"**🗺️ Zone typologique** : `{resultat['zone'].capitalize()}`".replace("_"," "))
                st.markdown(f"**💬 Commentaire** : {resultat['commentaire']}")

                # Enregistrement dans l'historique
                st.session_state.historique_estimations.append({
                    "Adresse": adresse,
                    "Code postal": code_postal,
                    "Type": type_local,
                    "Surface": surface,
                    "Pièces": nb_pieces,
                    "Prix/m² estimé (€)": round(resultat["prix_m2_estime"], 2),
                    "Valeur foncière (€)": resultat["valeur_fonciere_estimee"],
                    "Zone": resultat["zone"].capitalize().replace("_", " ")
                })

    # Affichage de l'historique
    if st.session_state.historique_estimations:
        st.markdown("### 📜 Historique des estimations réalisées")
        st.dataframe(st.session_state.historique_estimations, use_container_width=True)

with onglet_carte:
    st.markdown("### 🗺️ Cartes d’attractivité par type de bien")

    with st.expander("🌍 Afficher la carte d’attractivité globale", expanded=True):
        with open("carte_attract_globale.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    with st.expander("🏢 Afficher la carte pour les appartements", expanded=True):
        with open("carte_attract_app.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    with st.expander("🏡 Afficher la carte pour les maisons", expanded=True):
        with open("carte_attract_maison.html", "r", encoding="utf-8") as f:
            st.components.v1.html(f.read(), height=650, scrolling=False)

    # Explication du score en bas
    st.markdown("### ℹ️ Méthodologie du rang d’attractivité")
    st.write("""
    Le **rang d’attractivité** est un indicateur calculé à partir de plusieurs critères socio-économiques et immobiliers à l’échelle départementale :

    - L'évolution de la population d'ici 2070
    - Les revenus médians
    - Et le prix moyen au m² des logements

    Les critères ne sont pas pondérés, le score est donc une moyenne simple de ces trois indicateurs.
    Ces cartes permettent ainsi d’identifier les zones les plus dynamiques ou à potentiel en France.
    """)
