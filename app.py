import streamlit as st
from estimation import estimer_depuis_adresse  # importe la fonction qui contient déjà les modèles

st.set_page_config(page_title="Estimation immobilière", page_icon="🏡")

st.title("🏘️ Estimation immobilière intelligente")
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
            st.markdown(f"**📏 Prix/m² estimé** : `{resultat['prix_m2_estime']:.2f} €`")
            st.markdown(f"**💶 Valeur foncière estimée** : `{resultat['valeur_fonciere_estimee']:,} €`")
            st.markdown(f"**📎 Fourchette de confiance** : `{resultat['fourchette'][0]:,} € – {resultat['fourchette'][1]:,} €`")
            st.markdown(f"**🗺️ Zone typologique** : `{resultat['zone']}`")
            st.markdown(f"**💬 Commentaire** : {resultat['commentaire']}")
