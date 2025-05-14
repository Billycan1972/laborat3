import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Cargar archivo desde Google Drive
url = "https://drive.google.com/uc?id=1m6UZRFjRYSIFMP_a4_Ck3cloeSTfv20k"
r = requests.get(url)
df = pd.read_csv(StringIO(r.text), sep='\t')
st.write("Columnas disponibles:", df.columns.tolist())
st.dataframe(df.head())


# Convertir columna 'periodo' a datetime
df['periodo'] = pd.to_datetime(df['periodo'], format='%Y%m')

# Agrupar por producto y fecha
df_prod = df.groupby(['periodo', 'product_id'])['tn'].sum().reset_index()

# Título
st.title("Evolución mensual de productos")

# Selector de producto
productos = sorted(df_prod['product_id'].unique())
producto_sel = st.selectbox("Seleccioná un producto", productos)

# Filtrar y graficar
df_sel = df_prod[df_prod['product_id'] == producto_sel]
fig = px.line(df_sel, x='periodo', y='tn', title=f'Producto {producto_sel}', markers=True)

st.plotly_chart(fig, use_container_width=True)

