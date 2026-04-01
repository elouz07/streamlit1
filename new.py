import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import streamlit as st

# -----------------------------
# CONFIGURATION PAGE
# -----------------------------
st.set_page_config(
    page_title="Mercedes Dashboard",
    page_icon="🛞",  
    layout="wide"
)

# -----------------------------
# CHARGEMENT DES DONNEES
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('/Users/ousmanefall/Desktop/Gomycode/python/streamlit/data/cleaned_mercedes_data.csv')
    return df

df = load_data()

# -----------------------------
# SIDEBAR - FILTRES
# -----------------------------
st.sidebar.title("🔎 Filtres dynamiques")

# Colonnes numériques
numeric_cols = df.select_dtypes(include=np.number).columns
numeric_filters = {}
for col in numeric_cols:
    min_val, max_val = float(df[col].min()), float(df[col].max())
    numeric_filters[col] = st.sidebar.slider(
        f"{col}",
        min_val,
        max_val,
        (min_val, max_val)
    )

# Colonnes catégorielles
categorical_cols = df.select_dtypes(include='object').columns
categorical_filters = {}
for col in categorical_cols:
    options = df[col].unique()
    selected = st.sidebar.multiselect(f"{col}", options)
    if selected:
        categorical_filters[col] = selected

# -----------------------------
# APPLICATION DES FILTRES
# -----------------------------
df_filtered = df.copy()

# Appliquer les filtres numériques
for col, (low, high) in numeric_filters.items():
    df_filtered = df_filtered[(df_filtered[col] >= low) & (df_filtered[col] <= high)]

# Appliquer les filtres catégoriels
for col, selected in categorical_filters.items():
    df_filtered = df_filtered[df_filtered[col].isin(selected)]

# -----------------------------
# HEADER ET METRICS
# -----------------------------
st.title("🛞 Mercedes-Benz Dashboard Ultime")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("💰 Prix moyen", f"{df_filtered['Price'].mean():,.0f}" if 'Price' in df_filtered.columns else "N/A")
col2.metric("📊 Médiane", f"{df_filtered['Price'].median():,.0f}" if 'Price' in df_filtered.columns else "N/A")
col3.metric("⭐ Rating moyen", f"{df_filtered['Rating'].mean():.2f}" if 'Rating' in df_filtered.columns else "N/A")
col4.metric("📝 Total reviews", f"{int(df_filtered['Review Count'].sum())}" if 'Review Count' in df_filtered.columns else "N/A")
col5.metric("🚗 Total véhicules", len(df_filtered))

st.markdown("---")

# -----------------------------
# STATISTIQUES
# -----------------------------
st.subheader("📈 Statistiques descriptives")
if len(numeric_cols) > 0:
    st.dataframe(df_filtered[numeric_cols].describe().style.format("{:.2f}"))
else:
    st.write("Aucune colonne numérique disponible.")

st.markdown("---")

# -----------------------------
# HISTOGRAMMES + BOXPLOTS POUR TOUTES LES COLONNES NUMERIQUES
# -----------------------------
st.subheader("📊 Histogrammes et Boxplots")

for col in numeric_cols:
    st.markdown(f"### {col}")
    col1, col2 = st.columns(2)
    with col1:
        fig_hist = px.histogram(
            df_filtered,
            x=col,
            nbins=30,
            title=f"Distribution de {col}",
            color_discrete_sequence=["#1f77b4"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    with col2:
        fig_box = px.box(
            df_filtered,
            y=col,
            title=f"Boxplot de {col}",
            color_discrete_sequence=["#ff7f0e"]
        )
        st.plotly_chart(fig_box, use_container_width=True)

# -----------------------------
# Scatter Price vs Rating
# -----------------------------
if 'Price' in df_filtered.columns and 'Rating' in df_filtered.columns:
    st.subheader("Prix vs Rating")
    df_sample = df_filtered.sample(min(len(df_filtered), 1000))
    fig_scatter = px.scatter(
        df_sample,
        x="Price",
        y="Rating",
        size="Review Count" if 'Review Count' in df_sample.columns else None,
        color="Rating",
        hover_data=["Name"] if 'Name' in df_sample.columns else None,
        title="Prix vs Rating"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# -----------------------------
# Top 10 voitures
# -----------------------------
if 'Rating' in df_filtered.columns and 'Name' in df_filtered.columns:
    st.subheader("Top 10 voitures les mieux notées")
    top_cars = df_filtered.sort_values(by="Rating", ascending=False).head(10)
    fig_top = px.bar(
        top_cars,
        x="Rating",
        y="Name",
        orientation="h",
        color_discrete_sequence=["#2ca02c"],
        title="Top 10 voitures"
    )
    st.plotly_chart(fig_top, use_container_width=True)

# -----------------------------
# Heatmap des corrélations
# -----------------------------
st.subheader("Heatmap des corrélations")
if len(numeric_cols) > 1:
    corr_matrix = df_filtered[numeric_cols].corr()
    fig_corr = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=list(corr_matrix.columns),
        y=list(corr_matrix.index),
        colorscale='Viridis',
        showscale=True
    )
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.write("Pas assez de colonnes numériques pour la heatmap.")

st.markdown("---")

# -----------------------------
# TABLEAU FILTRE
# -----------------------------
st.subheader("📋 Données filtrées")
st.dataframe(df_filtered)

# -----------------------------
# TELECHARGEMENT CSV
# -----------------------------
st.download_button(
    "📥 Télécharger les données filtrées",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_mercedes_data.csv"
)