import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Dashboard Executivo - Controle de Evasão",
    layout="wide"
)

# ==========================================
# LINKS CSV
# ==========================================
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

# ==========================================
# FUNÇÃO ROBUSTA DE CARREGAMENTO
# ==========================================
@st.cache_data(ttl=60)
def load_data(url):
    df = pd.read_csv(url)

    # Limpeza de colunas
    df.columns = df.columns.str.strip()
    df.columns = (
        df.columns
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
    )

    return df

# ==========================================
# FUNÇÃO SEGURA PARA CÁLCULO DE TAXA
# ==========================================
def calcular_taxa(df, coluna):
    if coluna in df.columns and len(df) > 0:
        return (
            pd.to_numeric(df[coluna], errors="coerce")
            .fillna(0)
            .astype(float)
            .mean() * 100
        )
    return 0

# ==========================================
# CARREGAMENTO DOS DADOS
# ==========================================
df_m1 = load_data(url_m1)
df_2faltas = load_data(url_2faltas)
df_desistentes = load_data(url_desistentes)

st.title("📊 Dashboard Executivo - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# =====================================================
# 🔵 ABA M1
# =====================================================
with tab1:

    st.subheader("Indicadores Estratégicos - M1")

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
    taxa_resposta = calcular_taxa(df, "resposta")
    taxa_historico = calcular_taxa(df, "historico")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total)
    col2.metric("Taxa de Resposta", f"{taxa_resposta:.1f}%")
    col3.metric("Taxa de Histórico", f"{taxa_historico:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if "justificativa" in df.columns and total > 0:
            st.subheader("Distribuição % por Justificativa")
            dist = df.groupby("justificativa")["contrato"].count() / total * 100
            st.bar_chart(dist.sort_values(ascending=False))

    with col2:
        if "orientador" in df.columns and total > 0:
            st.subheader("Distribuição % por Orientador")
            dist = df.groupby("orientador")["contrato"].count() / total * 100
            st.bar_chart(dist.sort_values(ascending=False))


# =====================================================
# 🟠 ABA 2 FALTAS
# =====================================================
with tab2:

    st.subheader("Indicadores Estratégicos - 2 Faltas")

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
    taxa_retorno = calcular_taxa(df2, "retorno")
    taxa_resposta2 = calcular_taxa(df2, "resposta")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total2)
    col2.metric("Taxa de Retorno", f"{taxa_retorno:.1f}%")
    col3.metric("Taxa de Resposta", f"{taxa_resposta2:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if "retorno" in df2.columns and total2 > 0:
            st.subheader("Distribuição % Retorno")
            dist = df2.groupby("retorno")["contrato"].count() / total2 * 100
            st.bar_chart(dist)

    with col2:
        if "resposta" in df2.columns and total2 > 0:
            st.subheader("Distribuição % Resposta")
            dist = df2.groupby("resposta")["contrato"].count() / total2 * 100
            st.bar_chart(dist)


# =====================================================
# 🔴 ABA DESISTENTES
# =====================================================
with tab3:

    st.subheader("Indicadores Estratégicos - Desistentes")

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
    taxa_hist = calcular_taxa(df3, "historico")
    taxa_resposta3 = calcular_taxa(df3, "resposta")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total3)
    col2.metric("Taxa de Histórico", f"{taxa_hist:.1f}%")
    col3.metric("Taxa de Resposta", f"{taxa_resposta3:.1f}%")

    st.divider()

    if "justificativa" in df3.columns and total3 > 0:
        st.subheader("Distribuição % por Justificativa")
        dist = df3.groupby("justificativa")["contrato"].count() / total3 * 100
        st.bar_chart(dist.sort_values(ascending=False))
