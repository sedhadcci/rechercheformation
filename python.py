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
        
    df[column] = df[column].apply(lambda x: str(x).lower())
    return df[df[column].str.contains('|'.join(query))][result_columns]

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
