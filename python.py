import streamlit as st
import pandas as pd
from fuzzywuzzy import process, fuzz
import openpyxl
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

@st.cache
@st.cache(allow_output_mutation=True)
def load_data(url):
    data = pd.read_excel(url, engine='openpyxl')
    return data

def search(df, query):
    results = process.extract(query, df['Mots clés compétences'], limit=None, scorer=fuzz.token_sort_ratio)
    df['match_score'] = pd.Series([x[1] for x in results])
    matching_rows = df[df['match_score'] >= 70]
    return matching_rows
def search_data(df, query, column='Mots clés compétences', result_columns=None):
    if result_columns is None:
        result_columns = ['TYPE', 'Ecoles', 'Filières / domaine', 'Formation', 'Poste', 'Lien']

st.title("Recherche de formation")
    matched_indexes = []
    for keyword in query:
        matches = process.extract(keyword, df[column], scorer=fuzz.token_set_ratio)
        for match in matches:
            if match[1] >= 70:
                matched_indexes.extend(df[df[column] == match[0]].index.tolist())
    return df.loc[matched_indexes, result_columns]

choice = st.radio(
    "Choisissez le fichier sur lequel vous voulez effectuer la recherche",
    ('ISTEC', 'Groupe éducatif CCI'))
url_istec = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/ISTEC%20recherche%20formation.xlsx'
url_cci = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/Groupe%20educatif%20CCI.xlsx'

if choice == 'ISTEC':
    url = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/ISTEC%20recherche%20formation.xlsx'
elif choice == 'Groupe éducatif CCI':
    url = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/Groupe%20educatif%20CCI.xlsx'
file_choice = st.radio("Choisissez un fichier pour effectuer la recherche:", ('ISTEC', 'Groupe éducatif CCI'))

if file_choice == 'ISTEC':
    url = url_istec
elif file_choice == 'Groupe éducatif CCI':
    url = url_cci

df = load_data(url)

query = st.text_input("Veuillez entrer le mot-clé de compétence recherché : ")
query = st.text_input('Entrez votre recherche ici:')
query = [i.lower() for i in query.split(",")]

if query:
    results = search(df, query.lower())
    results = results.set_index("Type")  # Définir 'Type' comme index.
    results = results.reindex(columns=["Ecoles", "Filières / domaine", "Formation", "Poste", "Lien"])  # Réorganiser les colonnes.
if st.button('Rechercher'):
    results = search_data(df, query)
    st.write(results)
