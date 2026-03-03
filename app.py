import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard CS - Evasão", layout="wide")

# LINKS CSV
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df.columns = (
        df.columns
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
    )
    return df

df_m1 = load_data(url_m1)
df_2faltas = load_data(url_2faltas)
df_desistentes = load_data(url_desistentes)

st.title("📊 Dashboard CS - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# =====================
# ABA 1 - M1
# =====================
with tab1:
    st.subheader("Alunos M1")

    if "mes" in df_m1.columns:
        mes = st.selectbox("Filtrar por Mês", sorted(df_m1["mes"].dropna().unique()))
        df = df_m1[df_m1["mes"] == mes]
    else:
        df = df_m1

    total = df["contrato"].count()
    taxa_resposta = (df["resposta"].sum() / total * 100) if "resposta" in df.columns and total > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total)
    col2.metric("Taxa Resposta (%)", f"{taxa_resposta:.2f}%")

    if "justificativa" in df.columns:
        st.bar_chart(df.groupby("justificativa")["contrato"].count())

    if "orientador" in df.columns:
        st.bar_chart(df.groupby("orientador")["contrato"].count())


# =====================
# ABA 2 - 2 FALTAS
# =====================
with tab2:
    st.subheader("Alunos 2 Faltas")

    if "mes" in df_2faltas.columns:
        mes2 = st.selectbox("Filtrar por Mês", sorted(df_2faltas["mes"].dropna().unique()))
        df2 = df_2faltas[df_2faltas["mes"] == mes2]
    else:
        df2 = df_2faltas

    total2 = df2["contrato"].count()
    taxa_retorno = (df2["retorno"].sum() / total2 * 100) if "retorno" in df2.columns and total2 > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total2)
    col2.metric("Taxa Retorno (%)", f"{taxa_retorno:.2f}%")

    if "resposta" in df2.columns:
        st.bar_chart(df2.groupby("resposta")["contrato"].count())


# =====================
# ABA 3 - DESISTENTES
# =====================
with tab3:
    st.subheader("Alunos Desistentes")

    if "mes" in df_desistentes.columns:
        mes3 = st.selectbox("Filtrar por Mês", sorted(df_desistentes["mes"].dropna().unique()))
        df3 = df_desistentes[df_desistentes["mes"] == mes3]
    else:
        df3 = df_desistentes

    total3 = df3["contrato"].count()
    taxa_hist = (df3["historico"].sum() / total3 * 100) if "historico" in df3.columns and total3 > 0 else 0

    col1, col2 = st.columns(2)
    col1.metric("Total Contratos", total3)
    col2.metric("Taxa Histórico (%)", f"{taxa_hist:.2f}%")

    if "justificativa" in df3.columns:
        st.bar_chart(df3.groupby("justificativa")["contrato"].count())
