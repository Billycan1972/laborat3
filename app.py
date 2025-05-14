import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar archivo combinado desde Dropbox
url = "https://www.dropbox.com/scl/fi/pwmcuwwj3v4i6qe5j5ozs/datos_finales.txt?rlkey=zy95sz3t34uy1quiadz4dsmtq&st=cf675r3m&dl=1"
df = pd.read_csv(url, sep='\t')

# Convertir columna 'periodo' a datetime
df['periodo'] = pd.to_datetime(df['periodo'], format='%Y%m')

# Crear una columna más legible para el producto
df['producto'] = df['product_id'].astype(str) + " - " + df['brand'] + " " + df['cat2']

# Agrupar por producto y fecha
df_prod = df.groupby(['periodo', 'producto'])['tn'].sum().reset_index()

# Título de la app
st.title("Evolución mensual de productos (con descripción)")

# Selector de producto
productos = sorted(df_prod['producto'].unique())
producto_sel = st.selectbox("Seleccioná un producto", productos)

# Filtrar y graficar
df_sel = df_prod[df_prod['producto'] == producto_sel]
fig = px.line(df_sel, x='periodo', y='tn', title=producto_sel, markers=True)

st.plotly_chart(fig, use_container_width=True)

