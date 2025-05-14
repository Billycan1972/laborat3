import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Leer archivo combinado desde Dropbox con requests (evita error SSL)
dropbox_url = "https://www.dropbox.com/scl/fi/pwmcuwwj3v4i6qe5j5ozs/datos_finales.txt?rlkey=zy95sz3t34uy1quiadz4dsmtq&st=cf675r3m&dl=1"
r = requests.get(dropbox_url)
df = pd.read_csv(StringIO(r.text), sep='\t')

# Limpiar valores vacíos o no válidos en la columna periodo
df = df[df['periodo'].notna()]
df = df[df['periodo'].str.len() >= 10]

# Convertir a datetime y luego a periodo mensual
df['periodo'] = pd.to_datetime(df['periodo'])
df['periodo'] = df['periodo'].dt.to_period('M')


# Crear nombre descriptivo de producto
df['producto'] = df['product_id'].astype(str) + " - " + df['brand'] + " " + df['cat2']

# Agrupar por mes y producto
df_prod = df.groupby(['periodo', 'producto'])['tn'].sum().reset_index()

# Convertir periodo a string para graficar
df_prod['periodo_str'] = df_prod['periodo'].astype(str)

# Título
st.title("Evolución mensual de productos")

# Selector de producto
productos = sorted(df_prod['producto'].unique())
producto_sel = st.selectbox("Seleccioná un producto", productos)

# Filtrar y graficar
df_sel = df_prod[df_prod['producto'] == producto_sel]
fig = px.line(df_sel, x='periodo_str', y='tn', title=producto_sel, markers=True)

st.plotly_chart(fig, use_container_width=True)


