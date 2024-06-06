import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Fonction pour charger et analyser le fichier Excel
def load_and_analyze(file):
    data = pd.read_excel(file)

    # Filtrer pour ne prendre que les 'Functional Req'
    functional_req = data[data['Req_type'] == 'Functional Req']

    # Calculer les pourcentages
    req_counts = data['Req_type'].value_counts()
    functional_req_count = req_counts.get('Functional Req', 0)  # Utiliser .get pour éviter les KeyError
    total_count = req_counts.sum()
    other_count = total_count - functional_req_count

    # Préparer les données pour le diagramme secteur
    labels = ['Functional Req', 'Other Req Types']
    sizes = [functional_req_count, other_count]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  # Séparer le premier secteur

    # Dessiner le diagramme secteur
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140)
    ax.set_title('Pourcentage des "Functional Req" parmi tous les "Req_type"')

    return fig

# Configuration du tableau de bord Streamlit
st.title('Analyse de la Traçabilité des Produits des Batteries')

# Upload du fichier Excel
uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")

if uploaded_file is not None:
    st.success('Fichier chargé avec succès')
    fig = load_and_analyze(uploaded_file)
    st.pyplot(fig)
