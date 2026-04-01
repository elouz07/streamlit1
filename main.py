import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit.web import cli as stcli
from streamlit.web.cli import main
from numpy.random import default_rng as rng
from scipy.stats import pearsonr, spearmanr



df = pd.read_csv('/Users/ousmanefall/Desktop/Gomycode/python/streamlit/data/usa_mercedes_benz_prices.csv')
df.info()
df.describe()
df.isnull().sum()

#les valeurs manquantes dans les colonnes 'Rating' et 'Review Count' sont remplacées par 0
df['Rating'] = df['Rating'].fillna(0)
df['Review Count'] = df['Review Count'].fillna(0)
df.isnull().sum()

#changer le format de la colonne 'Price' en supprimant les symboles '$' et les virgules, puis convertir les valeurs en format numérique
df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '')

#les valeurs manquantes dans la colonne 'Price' sont remplacées par la médiane 
df['Price'] = pd.to_numeric(df['Price'].replace('Not Priced', np.nan))
df['Price'].fillna(df['Price'].median(), inplace=True)

# Convertir la colonne 'Price' en format numérique
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
df['Price'].unique()
#visionnage et affichage des données de la colonne price
df['Price'].describe()
df['Price']

# Convertir la colonne 'Review Count' en format numérique
df['Review Count'] = df['Review Count'].str.replace(',', '')
df['Review Count'] = pd.to_numeric(df['Review Count'], errors='coerce')
df['Review Count'].unique()
df['Review Count'].describe()
df['Review Count']

df['Review Count'] = (
    df['Review Count']
    .astype(str)
    .str.replace(',', '')
)

df['Review Count'] = pd.to_numeric(df['Review Count'], errors='coerce')

df['Review Count'].fillna(0, inplace=True)


# Export du dataset propre
df.to_csv('cleaned_mercedes_data.csv', index=False)
