import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

def load_data(url):
    data = pd.read_excel(url)
    return data

def search_data(df, query, column='Mots clés compétences'):
    df_copy = df.copy()  # Crée une copie du DataFrame
    results = []
    phrases = [phrase.strip().lower() for phrase in query.split(',')]  # Convertit chaque phrase en minuscules
    for phrase in phrases:
        df_copy['Match_Score'] = df_copy[column].apply(lambda row: fuzz.partial_ratio(phrase, str(row).lower()) if fuzz.partial_ratio(phrase, str(row).lower()) >= 70 else 0)  # Compare les phrases et les lignes en minuscules
        matched_df = df_copy[df_copy['Match_Score'] > 0]
        for i, row in matched_df.iterrows():
            result = {'Ecoles': row['Ecoles'], 'Filières / domaine': row['Filières / domaine'], 'Formation': row['Formation'], 'Poste': row['Poste'], 'Lien': row['Lien'], 'TYPE': row['TYPE']}
            results.append(result)
    return pd.DataFrame(results)  # Retourne un DataFrame au lieu d'une liste de dictionnaires

st.title("Moteur de recherche EXCEL")

url = 'https://github.com/yourusername/yourrepository/raw/main/yourfile.xlsx'  # Remplacer par l'URL de votre fichier
df = load_data(url)
query = st.text_input("Entrer le(s) phrase(s) à rechercher, séparées par des virgules")
if query:
    st.subheader("Résultats de recherche")
    results = search_data(df, query)
    st.table(results)  # Affiche les résultats dans un tableau

