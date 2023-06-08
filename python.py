import pandas as pd
from fuzzywuzzy import process
import streamlit as st

@st.cache
def load_data(file):
    df = pd.read_excel(file)
    return df

def search_data(df, query, columns):
    results = []
    for col in columns:
        matches = process.extractBests(query, df[col], score_cutoff=70)
        results.extend(matches)
    return results

st.title("Moteur de recherche EXCEL")

uploaded_file = st.file_uploader("Choisir un fichier Excel", type="xlsx")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    query = st.text_input("Entrer le(s) mot(s) clé(s)")
    if query:
        st.subheader("Résultats de recherche")
        columns = ["Compétences", "Domaine", "Nom formation", "Ecoles"]
        results = search_data(df, query, columns)
        for result in results:
            st.write(result)
