import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")
st.write("### 📊 Tableau de bord détaillé (Vue Pivot)")

# --- 1. Création d'un jeu de données de test (à remplacer par le tien) ---
donnees = {
    "Catégorie": ["Multimédia", "Multimédia", "Multimédia", "Alimentaire", "Alimentaire", "Cosmétique"],
    "Produit": ["PC Portable", "Smartphone", "Tablette", "Pommes", "Pâtes", "Crème"],
    "KPI_1_Ventes": [1200, 800, 400, 50, 30, 45],
    "KPI_2_Marge": [300, 200, 100, 15, 10, 25],
    "KPI_3_Defauts": [2, 5, 1, 0, 0, 1]
}
df = pd.DataFrame(donnees)

# --- 2. Configuration du tableau AgGrid ---
# On initialise le constructeur avec notre DataFrame
gb = GridOptionsBuilder.from_dataframe(df)

# A. On active le groupement sur la colonne 'Catégorie'
# hide=True permet de cacher la colonne normale puisqu'elle devient l'en-tête du groupe
gb.configure_column("Catégorie", rowGroup=True, hide=True)

# B. On configure les aggrégations pour les KPIs (pour avoir le total de la catégorie sur la ligne principale)
# Tu peux utiliser 'sum' (somme), 'avg' (moyenne), 'min', 'max', etc.
gb.configure_column("KPI_1_Ventes", aggFunc='sum')
gb.configure_column("KPI_2_Marge", aggFunc='sum')
gb.configure_column("KPI_3_Defauts", aggFunc='sum')

# C. Quelques options de design pour le confort
gb.configure_grid_options(
    groupDefaultExpanded=0, # Met 1 pour tout dérouler par défaut, ou 0 pour tout replier
    suppressAggFuncInHeader=True # Évite d'écrire "sum(KPI_1)" dans l'en-tête
)

# On compile les options
gridOptions = gb.build()

# --- 3. Affichage du tableau ---
AgGrid(
    df,
    gridOptions=gridOptions,
    height=500, # Hauteur du tableau en pixels
    fit_columns_on_grid_load=True, # Ajuste la largeur des colonnes à l'écran
    theme="alpine" # Thème clair très propre (tu peux essayer "balham" ou "streamlit")
)
