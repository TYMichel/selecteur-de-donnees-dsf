"""
Ce script permet de selectionner un sous ensemble des donnéesn d'un data de données plus grand.
Il est écrit de sorte à pouvoir changer le fichier excel qui sert de base poour le 
data de  données 
"""
import streamlit as st 
import pandas as pd 
import warnings

warnings.filterwarnings("ignore")
#! Version avec une base de données réduites. "final-ref-cleaned-sample-version.csv"
@st.cache_data
def chargement(n=1):
     with st.spinner("Chargement des tables"):
          data = pd.read_csv("final-ref-cleaned-years-sample-version.csv",on_bad_lines="skip",low_memory=False,nrows=n) # base de données 
          indesirable = pd.read_csv("final-ref-indesirable-years.csv",on_bad_lines="skip",low_memory=False) # les années d'exercice clos ne sont pas identifiables.
          years = pd.read_csv("final-ref-cleaned-years-sample-version.csv",header=0,usecols=["annee_exerciceClos"])
          years = years["annee_exerciceClos"].unique()

     return data,indesirable,years



st.title("Sélecteur des données DSF Normal")
st.divider()
st.info("""A cause de problèmes en relation avec la taille du fichier, cette application utilise une
          une base de données réduite à 5000 lignes au lieu de 15 000.
        """)

data,indesirable,years = chargement(1)

cols = st.multiselect(
     "Veuillez selectionnez des **colonnes** à extraire :",
     list(data.columns),
     "doublon_flag"

     )


years = st.multiselect(
     "Veuillez sélectionner une ou plusieurs années : ",
     years,
     2021
)


afficher_data = st.button("Afficher la sélection",
                          type='primary',
                          help="Afficher les colonnes et années **sélectionnées**",
                          use_container_width=True)


#* Affiche  la dataFrame sélectionné
if afficher_data:
     all_data = pd.read_csv("final-ref-cleaned-years-sample-version.csv")
     df = all_data[all_data["annee_exerciceClos"].isin(years)][cols]
     st.dataframe(df)
     
st.divider()

show_indesirable = st.button("Afficher les indésirables",
                             help="Ce sont les lignes avec des dates illisibles",
                             use_container_width=True
                             )

if show_indesirable:
     st.dataframe(indesirable)
     st.write(f"Nombre d'indésirables: {indesirable.shape[0]}")