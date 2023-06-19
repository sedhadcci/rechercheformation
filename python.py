import streamlit as st
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

@st.cache(allow_output_mutation=True)
def load_data(url):
    data = pd.read_excel(url, engine='openpyxl')
    return data

def search_data(df, query, column='Mots clés compétences', result_columns=None):
    if result_columns is None:
        result_columns = ['TYPE', 'Ecoles', 'Filières / domaine', 'Formation', 'Poste', 'Lien']

    matched_indexes = []
    for keyword in query:
        matches = process.extract(keyword, df[column], scorer=fuzz.token_set_ratio)
        for match in matches:
            if match[1] >= 70:
                matched_indexes.extend(df[df[column] == match[0]].index.tolist())
    return df.loc[matched_indexes, result_columns]

url_istec = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/ISTEC%20recherche%20formation.xlsx'
url_cci = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/Groupe%20educatif.xlsx'
url_Ferrandi = 'https://raw.githubusercontent.com/sedhadcci/rechercheformation/main/Ferrandi%20mots%20cles.xlsx'

file_choice = st.radio("Choisissez un fichier pour effectuer la recherche:", ('ISTEC', 'Groupe éducatif CCI' , 'Ferrandi'))

if file_choice == 'ISTEC':
    url = url_istec
elif file_choice == 'Groupe éducatif CCI':
    url = url_cci
elif file_choice == 'Ferrandi':
    url = url_Ferrandi

df = load_data(url)

query = st.text_input('Entrez votre recherche ici:')
query = [i.lower() for i in query.split(",")]

if st.button('Rechercher'):
    results = search_data(df, query)
    st.write(results)
