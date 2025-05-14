
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Leer archivo desde Dropbox
dropbox_url = "https://www.dropbox.com/scl/fi/pwmcuwwj3v4i6qe5j5ozs/datos_finales.txt?rlkey=zy95sz3t34uy1quiadz4dsmtq&st=cf675r3m&dl=1"
r = requests.get(dropbox_url)
df = pd.read_csv(StringIO(r.text), sep='\t')

# Preprocesamiento
df = df[df['periodo'].notna()]
df = df[df['periodo'].str.len() >= 10]
df['periodo'] = pd.to_datetime(df['periodo'])
df['periodo_str'] = df['periodo'].dt.to_period('M').astype(str)

# Crear nombre descriptivo de producto
df['producto'] = df['product_id'].astype(str) + " - " + df['brand'] + " " + df['cat2']

# ---------------------------
# Visualización por producto
# ---------------------------
st.title("Evolución mensual de productos y categorías")

st.header("🔹 Evolución por producto")

df_prod = df.groupby(['periodo_str', 'producto'])['tn'].sum().reset_index()
df_prod['periodo'] = pd.to_datetime(df_prod['periodo_str'])

productos = sorted(df_prod['producto'].unique())
producto_sel = st.selectbox("Seleccioná un producto", productos)

df_prod_sel = df_prod[df_prod['producto'] == producto_sel]
df_prod_sel['tn_suavizada'] = df_prod_sel['tn'].rolling(3, center=True).mean()

fig1 = px.line(
    df_prod_sel,
    x='periodo',
    y='tn_suavizada',
    title=f"Evolución suavizada de {producto_sel}",
    markers=True
)
fig1.update_layout(xaxis_title="Mes", yaxis_title="Toneladas")
st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# Visualización por cat3
# ---------------------------
st.header("🔹 Evolución por categoría (cat3)")

cat3s = sorted(df['cat3'].dropna().unique())
cat3_sel = st.multiselect("Seleccioná una o más categorías cat3:", cat3s, default=cat3s[:5])

df_cat3 = df[df['cat3'].isin(cat3_sel)]
df_cat3 = df_cat3.groupby(['periodo_str', 'cat3'])['tn'].sum().reset_index()
df_cat3['periodo'] = pd.to_datetime(df_cat3['periodo_str'])
df_cat3['tn_suavizada'] = df_cat3.groupby('cat3')['tn'].transform(lambda x: x.rolling(3, center=True).mean())

fig2 = px.line(
    df_cat3,
    x='periodo',
    y='tn_suavizada',
    color='cat3',
    title="Evolución suavizada por categoría cat3"
)
fig2.update_layout(xaxis_title="Mes", yaxis_title="Toneladas", legend_title="cat3")
st.plotly_chart(fig2, use_container_width=True)
