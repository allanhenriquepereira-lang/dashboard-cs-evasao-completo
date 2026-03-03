import streamlit as st
import pandas as pd

# ==================================================
# CONFIGURAÇÃO
# ==================================================
st.set_page_config(
    page_title="Dashboard Executivo - Controle de Evasão",
    layout="wide"
)

# ==================================================
# LINKS CSV
# ==================================================
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

# ==================================================
# FUNÇÃO DE CARGA
# ==================================================
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

# ==================================================
# FUNÇÃO TAXA INTELIGENTE (FUNCIONA COM TEXTO)
# ==================================================
def calcular_taxa_texto(df, coluna):
    if coluna in df.columns and len(df) > 0:
        serie = df[coluna].astype(str).str.strip().str.lower()

        positivos = ["true", "sim", "1"]
        serie_binaria = serie.isin(positivos)

        return serie_binaria.mean() * 100

    return 0

# ==================================================
# CARREGAMENTO
# ==================================================
df_m1 = load_data(url_m1)
df_2faltas = load_data(url_2faltas)
df_desistentes = load_data(url_desistentes)

st.title("📊 Dashboard Executivo - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# ==================================================
# 🔵 M1
# ==================================================
with tab1:

    st.subheader("Indicadores Estratégicos - M1")

    if "mes" in df_m1.columns:
        mes = st.selectbox("Filtrar por Mês",
                           sorted(df_m1["mes"].dropna().unique()),
                           key="mes_m1")
        df = df_m1[df_m1["mes"] == mes]
    else:
        df = df_m1

    total = df["contrato"].nunique()

    taxa_resposta = calcular_taxa_texto(df, "resposta")
    taxa_historico = calcular_taxa_texto(df, "historico")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total)
    col2.metric("Taxa de Resposta", f"{taxa_resposta:.1f}%")
    col3.metric("Taxa de Histórico", f"{taxa_historico:.1f}%")

    st.divider()

    if total > 0 and "justificativa" in df.columns:
        st.subheader("Distribuição % por Justificativa")
        dist = df.groupby("justificativa")["contrato"].nunique() / total * 100
        st.bar_chart(dist.sort_values(ascending=False))


# ==================================================
# 🟠 2 FALTAS
# ==================================================
with tab2:

    st.subheader("Indicadores Estratégicos - 2 Faltas")

    if "mes" in df_2faltas.columns:
        mes2 = st.selectbox("Filtrar por Mês",
                            sorted(df_2faltas["mes"].dropna().unique()),
                            key="mes_2faltas")
        df2 = df_2faltas[df_2faltas["mes"] == mes2]
    else:
        df2 = df_2faltas

    total2 = df2["contrato"].nunique()

    taxa_retorno = calcular_taxa_texto(df2, "retorno")
    taxa_resposta2 = calcular_taxa_texto(df2, "resposta")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total2)
    col2.metric("Taxa de Retorno", f"{taxa_retorno:.1f}%")
    col3.metric("Taxa de Resposta", f"{taxa_resposta2:.1f}%")

    st.divider()

    if total2 > 0 and "retorno" in df2.columns:
        st.subheader("Distribuição % Retorno")
        dist = (
            df2.assign(retorno_bin=df2["retorno"].astype(str).str.lower().isin(["sim", "true"]))
            .groupby("retorno_bin")["contrato"]
            .nunique()
            / total2 * 100
        )
        st.bar_chart(dist)


# ==================================================
# 🔴 DESISTENTES
# ==================================================
with tab3:

    st.subheader("Indicadores Estratégicos - Desistentes")

    if "mes" in df_desistentes.columns:
        mes3 = st.selectbox("Filtrar por Mês",
                            sorted(df_desistentes["mes"].dropna().unique()),
                            key="mes_desistentes")
        df3 = df_desistentes[df_desistentes["mes"] == mes3]
    else:
        df3 = df_desistentes

    total3 = df3["contrato"].nunique()

    taxa_hist = calcular_taxa_texto(df3, "historico")
    taxa_resposta3 = calcular_taxa_texto(df3, "resposta")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Contratos", total3)
    col2.metric("Taxa de Histórico", f"{taxa_hist:.1f}%")
    col3.metric("Taxa de Resposta", f"{taxa_resposta3:.1f}%")

    st.divider()

    if total3 > 0 and "justificativa" in df3.columns:
        st.subheader("Distribuição % por Justificativa")
        dist = df3.groupby("justificativa")["contrato"].nunique() / total3 * 100
        st.bar_chart(dist.sort_values(ascending=False))
