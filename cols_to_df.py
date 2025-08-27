"""
Ce programme permet de faire le récapitulatif dans l'application
streamlit.
Il fournit une fonction qui transforme une liste 
de colonne en une dataframe montrant l'appartenance de chaque colonne

"""
import pandas as pd 
import json 
import pprint

     
def cols_to_df(matching,listCols):
     """retourne un dataFrame contenant
     les tableaux contenant la liste de colonnes 
     fournies 

     Args:
         matching (dictionnaire): matching des colonnes aux tableaus
         listCols (list): liste de colonnes contenues dans le matching.
     """
     correspondances = [matching[index] for index in listCols ] # ici, les colonnes sont des indexs

     df = pd.DataFrame(
          {
               "Colonne": listCols,
               "Tableau": correspondances
          }
     ) # colonnes sélectionnées avec leur table correspondante 
     
     grouped = df.groupby("Tableau")
     
     newCols = list() # les colonnes de la dataframe finale. 
     lengths = list() # servira à determiner la dimension du tableau
     
     for tableId,group in grouped:
          
          lengths.append(group["Colonne"].shape[0])
          
     n = max(lengths)
     
     for tableId,group in grouped:
          
          n_lines = group["Colonne"].shape[0]
          colonne = pd.Series(group["Colonne"]).to_list()
          extension = ["--"] * (n - n_lines)
          
      
          newCols.append(
               {tableId:colonne + extension}
          )
          
          pprint.pprint({tableId:colonne + extension})

     final_data = {}
     
     for column in newCols:
          final_data.update(column)
     
     final_df = pd.DataFrame(
          final_data
     )
     
     return final_df
     
