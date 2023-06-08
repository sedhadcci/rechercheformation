import pandas as pd
from fuzzywuzzy import process
import streamlit as st

@st.cache
def load_data(file):
    df = pd.read_excel(file)
    return df

def search_data(df, query, column='Compétences'):
    df_copy = df.copy()  # Crée une copie du DataFrame
    results = []
    phrases = [phrase.strip() for phrase in query.split(',')]
    for phrase in phrases:
        df_copy['Match_Score'] = df_copy[column].apply(lambda row: process.extractOne(phrase, [str(row)], score_cutoff=70))
        matched_df = df_copy[df_copy['Match_Score'].notna()]
        for i, row in matched_df.iterrows():
            result = {'Domaine': row['Domaine'], 'Nom formation': row['Nom formation'], 'Ecoles': row['Ecoles'], 'Resultat': row['Resultat']}
            results.append(result)
    return results

st.title("Moteur de recherche EXCEL")

uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    query = st.text_input("Entrer le(s) phrase(s) à rechercher, séparées par des virgules")
    if query:
        st.subheader("Résultats de recherche")
        results = search_data(df, query)
        for result in results:
            st.write(result)
