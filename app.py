"""
Ce script permet de selectionner un sous ensemble des donnéesn d'un data de données plus grand.
Il est écrit de sorte à pouvoir changer le fichier excel qui sert de base poour le 
data de  données 
"""
import streamlit as st 
import pandas as pd 
import warnings
import json 
from cols_to_df import cols_to_df

from streamlit_tree_select import tree_select 

#* importation du matching 

# Utile pour le récapitulatif 
f = open("cols-to-table-matching.json","r")
content = f.read()
f.close()
colsToTableMatching = json.loads(content)

#utile pour l'association tableau-colonnes
f = open("definitive-match.json","r")
content = f.read()
f.close()
matchingJson = json.loads(content) # dictionnaire [tableau -> liste colonnes]
# pour avoir des noms de tableau du style "Tableau 23"...
tables_proforma = list(map(lambda i: "Tableau "+i,list(matchingJson.keys()))) 


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
st.info("""A cause de problèmes en relation avec la taille du fichier, cette application utilise une
          une base de données réduite à 5000 lignes au lieu de 15 000.
        """)


type_dsf = st.selectbox(
     "Veuillez selectionner le type de DSF",
     ["Système Normal","Système minimal de trésorerie","DSF des banques","DSF des sociétés d'assurance"] # liste  non exhaustive.
)    

st.divider()

tables = st.multiselect(
     "Veuillez sélectionner les **Tableaux** que vous désirez:",
     tables_proforma,
     "Tableau 67"
)

#TODO: constructiion de la selection de colonnes 
selection = list()
for table in tables:# une branche pour chaque table
     list_cols = matchingJson[str(table[-2:]).strip()] # colonnes de la table courante
     selection.append(
          {
           "label": str(table), 
           "value":int(table[-2:]),
           "children": [
                {"label": col_name, "value": col_name} for col_name in list_cols
           ]
           }
     )
with st.sidebar:
     selected_cols = tree_select(selection)

st.subheader("Récapitulatif de la sélection")
st.dataframe(cols_to_df(colsToTableMatching,selected_cols["checked"]))
     
     


data,indesirable,years = chargement(1)

cols = st.multiselect(
     "Veuillez selectionnez des **colonnes** à extraire : (ces colonnes sont présentes dans tous les tableaux)",
     [
          "desigEntite"
          "num_doublons",
          "doublon_flag",
          "numerodIdent",
          "exerciceClos",
          "dureeMois"
          ],
     "doublon_flag"

     )


years = st.multiselect(
     "Veuillez sélectionner une ou plusieurs années : ",
     years,
     2021
)


extract_order = st.button("Extraire les données",
                          help="Lancer l'extraction des colonnes",
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
          use_container_width=True,
          on_click="ignore"
     )
     
# Gestion des indésirables 

st.info("Peut être ce que vous cherchez se trouve dans les données inclassables ?",
        icon="💡")

file2 = indesirable.to_csv().encode("utf-8")

st.download_button(
     "Télécharger les inclassables",
     data=file2,
     on_click="ignore",
     mime="text/csv",
     use_container_width=True,
     icon=":material/download:"
)
