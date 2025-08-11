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



st.title("Sélecteur des données DSF")

type_dsf = st.selectbox(
     "Veuillez selectionner le type de DSF",
     ["Système Normal","Système minimal de trésorerie","DSF des banques","DSF des sociétés d'assurance"] # liste  non exhaustive.
)    

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


extract_order = st.button("Extraire les données",
                          "Lancer l'extraction des colonnes",
                          use_container_width=True)

#* Affiche  la dataFrame sélectionné
if extract_order:
     with st.spinner("extraction des données."):
          all_data = pd.read_csv("final-ref-cleaned-years-sample-version.csv")
          df = all_data[all_data["annee_exerciceClos"].isin(years)][cols]
          file = df.to_csv().encode("utf-8")
else:
     file = None 

if file is not None:
     st.download_button(
          label = "Télécharger l'extrait",
          data = file,
          mime = "text/csv",
          icon=":material/download:",
          use_container_width=True
     )


