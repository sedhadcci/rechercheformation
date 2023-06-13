import streamlit as st
import pandas as pd
from fuzzywuzzy import process, fuzz
import openpyxl

@st.cache
def load_data(url):
    data = pd.read_excel(url, engine='openpyxl')
    return data

def search(df, query):
    results = process.extract(query, df['Mots clés compétences'], limit=None, scorer=fuzz.token_sort_ratio)
    df['match_score'] = pd.Series([x[1] for x in results])
    matching_rows = df[df['match_score'] >= 70]
    return matching_rows

st.title("Recherche de formation")

choice = st.radio(
    "Choisissez le fichier sur lequel vous voulez effectuer la recherche",
    ('ISTEC', 'Groupe éducatif CCI'))

if choice == 'ISTEC':
    url = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/ISTEC%20recherche%20formation.xlsx'
elif choice == 'Groupe éducatif CCI':
    url = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/Groupe%20educatif%20CCI.xlsx'

df = load_data(url)

query = st.text_input("Veuillez entrer le mot-clé de compétence recherché : ")

if query:
    results = search(df, query.lower())
    results = results.set_index("Type")  # Définir 'Type' comme index.
    results = results.reindex(columns=["Ecoles", "Filières / domaine", "Formation", "Poste", "Lien"])  # Réorganiser les colonnes.
    st.write(results)
