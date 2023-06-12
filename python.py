import pandas as pd
from fuzzywuzzy import fuzz
import streamlit as st

@st.cache
def load_data(file):
    df = pd.read_excel(file)
    return df

def search_data(df, query, column='Mots clés compétences'):
    df_copy = df.copy()  # Crée une copie du DataFrame
    results = []
    phrases = [phrase.strip().lower() for phrase in query.split(',')]  # Convertit les phrases de recherche en minuscules
    for phrase in phrases:
        df_copy['Match_Score'] = df_copy[column].apply(lambda row: 100 if phrase == str(row).lower() else (fuzz.partial_ratio(phrase, str(row).lower()) if fuzz.partial_ratio(phrase, str(row).lower()) >= 70 else 0))  # Vérifie d'abord la correspondance exacte, puis compare la similarité
        matched_df = df_copy[df_copy['Match_Score'] > 0]
        for i, row in matched_df.iterrows():
            result = {'Ecoles': row['Ecoles'], 'Filières / domaine': row['Filières / domaine'], 'Formation': row['Formation'], 'Poste': row['Poste'], 'Lien': row['Lien']}
            results.append(result)
    return pd.DataFrame(results)

st.title("Moteur de recherche EXCEL")

uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    query = st.text_input("Entrer le(s) phrase(s) à rechercher, séparées par des virgules")
    if query:
        st.subheader("Résultats de recherche")
        results = search_data(df, query)
        st.table(results)
