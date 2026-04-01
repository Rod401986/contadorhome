import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Contador", layout="centered")

st.title("💰 Contador mensual")

FILE = "datos.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=["fecha", "tipo", "monto", "categoria", "nota"])
    df.to_csv(FILE, index=False)

df = pd.read_csv(FILE)

if not df.empty:
    df["fecha"] = pd.to_datetime(df["fecha"])

st.header("➕ Agregar movimiento")

with st.form("form"):
    fecha = st.date_input("Fecha", datetime.date.today())
    tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
    monto = st.number_input("Monto", min_value=0.0)
    categoria = st.text_input("Categoría")
    nota = st.text_input("Nota")

    submitted = st.form_submit_button("Guardar")

    if submitted:
        new_row = pd.DataFrame([{
            "fecha": fecha,
            "tipo": tipo,
            "monto": monto,
            "categoria": categoria,
            "nota": nota
        }])

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(FILE, index=False)
        st.success("Movimiento guardado!")

if not df.empty:
    st.header("📅 Resumen mensual")

    meses = sorted(df["fecha"].dt.to_period("M").astype(str).unique())
    mes = st.selectbox("Seleccionar mes", meses)

    df_mes = df[df["fecha"].dt.to_period("M").astype(str) == mes]

    ingresos = df_mes[df_mes["tipo"] == "Ingreso"]["monto"].sum()
    egresos = df_mes[df_mes["tipo"] == "Egreso"]["monto"].sum()

    st.write(f"Ingresos: ${ingresos}")
    st.write(f"Egresos: ${egresos}")
