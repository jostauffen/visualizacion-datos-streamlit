import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO
import requests

st.title("📊 Dashboard Interactivo - Ventas de Tiendas de Conveniencia")

# Opción de cargar archivo
archivo = st.file_uploader("📤 Sube tu archivo CSV (opcional, debe contener columnas 'Date', 'Total', etc.)", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    st.success("✅ Archivo cargado exitosamente")
else:
    st.info("🔁 Usando archivo por defecto desde GitHub")
    url = "https://raw.githubusercontent.com/jostauffen/visualizacion-datos-streamlit/main/data.csv"
    content = requests.get(url).content
    df = pd.read_csv(StringIO(content.decode('utf-8')))

# Procesamiento
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df['fecha_num'] = df['Date'].map(pd.Timestamp.toordinal)
df['Total'] = df['Total'].astype(float)

# Filtros dinámicos
col1, col2 = st.columns(2)
with col1:
    ciudad = st.selectbox("📍 Ciudad:", options=df['City'].unique())
with col2:
    metodo = st.selectbox("💳 Método de pago:", options=df['Payment'].unique())

df_filtrado = df[(df['City'] == ciudad) & (df['Payment'] == metodo)]

# Ventas diarias
st.subheader("📈 Ventas Diarias")
ventas_diarias = df_filtrado.groupby('Date')['Total'].sum()
fig1, ax1 = plt.subplots()
ventas_diarias.plot(ax=ax1)
ax1.set_title("Ventas Diarias")
st.pyplot(fig1)

# Boxplot
st.subheader("📦 Distribución por Línea de Producto")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.boxplot(data=df_filtrado, x='Product line', y='Total', ax=ax2)
plt.xticks(rotation=45)
st.pyplot(fig2)

# Dispersión
st.subheader("🟣 Dispersión Total vs Cantidad")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df_filtrado, x='Quantity', y='Total', hue='Gender', ax=ax3)
st.pyplot(fig3)

# Mapa de calor
st.subheader("🔥 Correlación entre variables")
fig4, ax4 = plt.subplots()
sns.heatmap(df_filtrado[['Unit price', 'Quantity', 'Total', 'gross income', 'Rating']].corr(), annot=True, cmap='coolwarm', ax=ax4)
st.pyplot(fig4)

# Gráfico 3D
st.subheader("🔮 Visualización 3D Interactiva")
fig5 = px.scatter_3d(df_filtrado, x='fecha_num', y='Quantity', z='Total', color='Product line', title='Ventas 3D')
st.plotly_chart(fig5)
