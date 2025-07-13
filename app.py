import streamlit as st
from estimation import estimer_depuis_adresse  # importe la fonction qui contient déjà les modèles
from streamlit_folium import st_folium

st.set_page_config(page_title="Estimation immobilière", page_icon="🏡")

st.title("🏘️ Où acheter et à quel prix ?")

# Création des onglets
onglet_carte, onglet_estimation = st.tabs(["🗺️ Analyse des départements", "📊 Estimation d'une adresse"])

with onglet_estimation:
    st.markdown("Entrez les infos de votre bien immobilier pour obtenir une estimation par modèle hybride :")

    adresse = st.text_input("📍 Adresse complète", placeholder="Ex : 15 rue Félix Thomas, Nantes")
    code_postal = st.text_input("🏷️ Code postal", placeholder="44000")

    col1, col2 = st.columns(2)
    with col1:
        type_local = st.selectbox("🏠 Type de bien", ["Appartement", "Maison"])
    with col2:
        nb_pieces = st.number_input("🔢 Nombre de pièces", 1, 12, 3)

    surface = st.number_input("📐 Surface habitable (m²)", 10, 500, 60)

    if st.button("🔮 Estimer le bien"):
        if not adresse or not code_postal:
            st.warning("Merci de renseigner à la fois l'adresse et le code postal.")
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
    st.markdown("### ℹ️ Méthodologie du score d’attractivité")
    st.write("""
    Le **score d’attractivité** est un indicateur calculé à partir de plusieurs critères socio-économiques et immobiliers à l’échelle départementale :

    - L'évolution de la population d'ici 2070
    - Les revenus médians
    - Et le prix moyen au m² des logements

    Les critères ne sont pas pondérés, le score est donc une moyenne simple de ces trois indicateurs.
    Ces cartes permettent ainsi d’identifier les zones les plus dynamiques ou à potentiel en France.
    """)
