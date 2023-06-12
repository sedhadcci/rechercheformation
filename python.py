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
    phrases = [phrase.strip() for phrase in query.split(',')]
    for phrase in phrases:
        df_copy['Match_Score'] = df_copy[column].apply(lambda row: fuzz.partial_ratio(phrase, str(row)) if fuzz.partial_ratio(phrase, str(row)) >= 70 else 0)
        matched_df = df_copy[df_copy['Match_Score'] > 0]
        for i, row in matched_df.iterrows():
            result = {'Ecoles': row['Ecoles'], 'Filières / domaine': row['Filières / domaine'], 'Formation': row['Formation'], 'Poste': row['Poste'], 'Lien': row['Lien']}
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
