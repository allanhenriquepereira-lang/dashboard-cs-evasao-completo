import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard CS - Controle de Evasão",
    layout="wide"
)

# =========================
# LINKS CSV
# =========================
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

# =========================
# FUNÇÃO PADRÃO
# =========================
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

st.title("📊 Dashboard Estratégico - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# =====================================================
# 🔵 ABA 1 - M1
# =====================================================
with tab1:

    st.subheader("Visão Geral - Alunos M1")

    if "mes" in df_m1.columns:
        mes = st.selectbox(
            "Filtrar por Mês",
            sorted(df_m1["mes"].dropna().unique()),
            key="mes_m1"
        )
        df = df_m1[df_m1["mes"] == mes]
    else:
        df = df_m1

    total = df["contrato"].count()
    taxa_resposta = (df["resposta"].sum() / total * 100) if "resposta" in df.columns and total > 0 else 0
    taxa_historico = (df["historico"].sum() / total * 100) if "historico" in df.columns and total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total)
    col2.metric("Taxa Resposta (%)", f"{taxa_resposta:.1f}%")
    col3.metric("Taxa Histórico (%)", f"{taxa_historico:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if "justificativa" in df.columns:
            st.subheader("Distribuição por Justificativa")
            st.bar_chart(df.groupby("justificativa")["contrato"].count())

    with col2:
        if "orientador" in df.columns:
            st.subheader("Distribuição por Orientador")
            st.bar_chart(df.groupby("orientador")["contrato"].count())


# =====================================================
# 🟠 ABA 2 - 2 FALTAS
# =====================================================
with tab2:

    st.subheader("Visão Geral - Alunos 2 Faltas")

    if "mes" in df_2faltas.columns:
        mes2 = st.selectbox(
            "Filtrar por Mês",
            sorted(df_2faltas["mes"].dropna().unique()),
            key="mes_2faltas"
        )
        df2 = df_2faltas[df_2faltas["mes"] == mes2]
    else:
        df2 = df_2faltas

    total2 = df2["contrato"].count()
    taxa_retorno = (df2["retorno"].sum() / total2 * 100) if "retorno" in df2.columns and total2 > 0 else 0
    taxa_resposta2 = (df2["resposta"].sum() / total2 * 100) if "resposta" in df2.columns and total2 > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total2)
    col2.metric("Taxa Retorno (%)", f"{taxa_retorno:.1f}%")
    col3.metric("Taxa Resposta (%)", f"{taxa_resposta2:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if "resposta" in df2.columns:
            st.subheader("Distribuição Resposta")
            st.bar_chart(df2.groupby("resposta")["contrato"].count())

    with col2:
        if "retorno" in df2.columns:
            st.subheader("Distribuição Retorno")
            st.bar_chart(df2.groupby("retorno")["contrato"].count())


# =====================================================
# 🔴 ABA 3 - DESISTENTES
# =====================================================
with tab3:

    st.subheader("Visão Geral - Alunos Desistentes")

    if "mes" in df_desistentes.columns:
        mes3 = st.selectbox(
            "Filtrar por Mês",
            sorted(df_desistentes["mes"].dropna().unique()),
            key="mes_desistentes"
        )
        df3 = df_desistentes[df_desistentes["mes"] == mes3]
    else:
        df3 = df_desistentes

    total3 = df3["contrato"].count()
    taxa_hist = (df3["historico"].sum() / total3 * 100) if "historico" in df3.columns and total3 > 0 else 0
    taxa_resposta3 = (df3["resposta"].sum() / total3 * 100) if "resposta" in df3.columns and total3 > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total3)
    col2.metric("Taxa Histórico (%)", f"{taxa_hist:.1f}%")
    col3.metric("Taxa Resposta (%)", f"{taxa_resposta3:.1f}%")

    st.divider()

    if "justificativa" in df3.columns:
        st.subheader("Distribuição por Justificativa")
        st.bar_chart(df3.groupby("justificativa")["contrato"].count())
