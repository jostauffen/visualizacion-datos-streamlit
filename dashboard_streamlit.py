
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from mpl_toolkits.mplot3d import Axes3D
import io

# Subir archivo
st.title("📊 Dashboard de Ventas de Tiendas de Conveniencia")

archivo = st.file_uploader("Sube tu archivo CSV (data.csv)", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)

    # Procesamiento de fecha y columnas necesarias
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    df['fecha_num'] = df['Date'].map(pd.Timestamp.toordinal)
    df['Total'] = df['Total'].astype(float)

    st.success("✅ Archivo cargado correctamente")

    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        ciudad = st.selectbox("Filtrar por ciudad:", options=df['City'].unique())
    with col2:
        metodo_pago = st.selectbox("Método de pago:", options=df['Payment'].unique())

    df_filtered = df[(df['City'] == ciudad) & (df['Payment'] == metodo_pago)]

    st.subheader("🔹 Ventas Diarias")
    ventas_diarias = df_filtered.groupby('Date')['Total'].sum()
    fig1, ax1 = plt.subplots(figsize=(10,4))
    ventas_diarias.plot(ax=ax1)
    ax1.set_title("Ventas Diarias")
    ax1.set_ylabel("Total")
    st.pyplot(fig1)

    st.subheader("🔹 Distribución por Línea de Producto")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.boxplot(data=df_filtered, x='Product line', y='Total', ax=ax2)
    plt.xticks(rotation=45)
    st.pyplot(fig2)

    st.subheader("🔹 Dispersión Total vs Cantidad")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=df_filtered, x='Quantity', y='Total', hue='Gender', ax=ax3)
    st.pyplot(fig3)

    st.subheader("🔹 Mapa de Calor de Correlación")
    fig4, ax4 = plt.subplots()
    sns.heatmap(df_filtered[['Unit price', 'Quantity', 'Total', 'gross income', 'Rating']].corr(),
                annot=True, cmap='coolwarm', ax=ax4)
    st.pyplot(fig4)

    st.subheader("🔹 Visualización 3D Interactiva")
    fig5 = px.scatter_3d(df_filtered, x='fecha_num', y='Quantity', z='Total',
                         color='Product line', title='Ventas 3D por Fecha, Cantidad y Total')
    st.plotly_chart(fig5)
else:
    st.warning("Por favor, sube un archivo CSV llamado data.csv")
