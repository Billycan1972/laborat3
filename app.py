import streamlit as st
import pandas as pd
import plotly.express as px

# Leer archivo desde Dropbox (descarga directa)
url = "https://www.dropbox.com/scl/fi/cu9bfsqal12y30gof2v56/sell-in.txt?rlkey=lp2t5so8x444dfk7nh23wta3h&st=xy3yh2ie&dl=1"
df = pd.read_csv(url, sep='\t')

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
