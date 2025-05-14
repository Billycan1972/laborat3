import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el dataset original
url = 'https://drive.google.com/uc?id=1m6UZRFjRYSIFMP_a4_Ck3cloeSTfv20k'
df = pd.read_csv(url, sep='\t')

df['periodo'] = pd.to_datetime(df['periodo'], format='%Y%m')

# Agrupación por mes y producto
df_prod = df.groupby(['periodo', 'product_id'])['tn'].sum().reset_index()

# Sidebar con selección de producto
productos = sorted(df_prod['product_id'].unique())
producto_sel = st.selectbox("Seleccioná un producto", productos)

# Filtrar y graficar
df_sel = df_prod[df_prod['product_id'] == producto_sel]
fig = px.line(df_sel, x='periodo', y='tn', title=f'Evolución producto {producto_sel}', markers=True)

st.plotly_chart(fig, use_container_width=True)
