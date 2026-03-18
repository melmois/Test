import streamlit as st
import pandas as pd
import numpy as np
import plotly as px

# Configuration de la page
st.set_page_config(page_title="Tableau de Bord V2", page_icon="🚀")
st.title("🚀 Suivi des Ventes - Version Avancée")

# 1. Génération des données (toujours avec notre cache en mémoire !)
@st.cache_data
def charger_donnees():
    np.random.seed(42)
    # On génère des dates du 1er janvier 2024 au 9 avril 2024 (100 jours)
    dates = pd.date_range(start="2024-01-01", periods=100)
    categories = ['Ordinateurs', 'Smartphones', 'Accessoires', 'Écrans']
    
    data = {
        'Date': dates,
        'Catégorie': np.random.choice(categories, 100),
        'Quantité Vendue': np.random.randint(1, 15, 100),
        'Chiffre d\'Affaires (€)': np.random.randint(50, 1500, 100)
    }
    return pd.DataFrame(data)

df = charger_donnees()

# --- BARRE LATÉRALE (LES FILTRES) ---
st.sidebar.header("🛠️ Filtres multiples")

# Filtre 1 : Le choix multiple (Multiselect)
toutes_les_categories = list(df['Catégorie'].unique())
categories_choisies = st.sidebar.multiselect(
    "1. Choisissez vos catégories :",
    options=toutes_les_categories,
    default=toutes_les_categories # Par défaut, on sélectionne toutes les catégories
)

# Filtre 2 : La sélection de dates (Date input)
# On récupère la date minimum et maximum de notre base de données
date_min = df['Date'].min().date()
date_max = df['Date'].max().date()

dates_choisies = st.sidebar.date_input(
    "2. Sélectionnez une période :",
    value=(date_min, date_max), # Par défaut, on sélectionne toute la période
    min_value=date_min,
    max_value=date_max
)

# --- FILTRAGE DES DONNÉES (Le cœur du moteur) ---

# Étape A : On filtre d'abord par catégories grâce à la fonction .isin() de Pandas
# (Cela signifie : "Garde les lignes où la catégorie EST DANS la liste des choix")
df_filtre = df[df['Catégorie'].isin(categories_choisies)]

# Étape B : On filtre ensuite par date
# Le date_input renvoie parfois 1 seule date (si l'utilisateur est en train de cliquer)
# ou 2 dates (début et fin). On vérifie donc qu'il y en a bien 2 avant de filtrer.
if len(dates_choisies) == 2:
    date_debut, date_fin = dates_choisies
    # On convertit les dates pour que Pandas les comprenne bien
    date_debut = pd.to_datetime(date_debut)
    date_fin = pd.to_datetime(date_fin)
    
    # On ne garde que les lignes entre la date de début ET (&) la date de fin
    df_filtre = df_filtre[(df_filtre['Date'] >= date_debut) & (df_filtre['Date'] <= date_fin)]

# --- AFFICHAGE DES RÉSULTATS ---

# Si l'utilisateur a tout décoché, le tableau est vide. On affiche un petit message sympa.
if df_filtre.empty:
    st.warning("⚠️ Aucune donnée ne correspond à vos filtres. Essayez de sélectionner au moins une catégorie.")
else:
    # Les indicateurs clés
    col1, col2 = st.columns(2)
    col1.metric("Ventes Totales", f"{df_filtre['Quantité Vendue'].sum()} unités")
    col2.metric("Chiffre d'Affaires", f"{df_filtre['Chiffre d\'Affaires (€)'].sum()} €")

    st.subheader("Aperçu des données")
    st.dataframe(df_filtre.head())

    st.subheader("Évolution du Chiffre d'Affaires")
    # On prépare proprement les données pour Plotly (.reset_index() transforme la Série en vrai Tableau)
    donnees_graphique = df_filtre.groupby('Date')['Chiffre d\'Affaires (€)'].sum().reset_index()

    # On crée un beau graphique avec Plotly Express
    fig = px.line(
        donnees_graphique, 
        x='Date', 
        y='Chiffre d\'Affaires (€)', 
        markers=True, # Ajoute des petits points sur la courbe
        color_discrete_sequence=['#FF4B4B'] # La couleur rouge de Streamlit !
    )

    # On demande à Streamlit d'afficher ce graphique Plotly
    st.plotly_chart(fig, use_container_width=True)
