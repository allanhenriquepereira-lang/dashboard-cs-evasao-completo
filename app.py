import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Executivo - Controle de Evasão",
    layout="wide"
)

# =========================
# LINKS CSV
# =========================
url_m1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=1769040659&single=true&output=csv"
url_2faltas = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=55844215&single=true&output=csv"
url_desistentes = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTtVuYWi_7xz80PhQ0RhPlVi9ep7GsrsRIJwA8Pq7oaUj0U9KXCswHUCPCLd687ueppBXztA2YfX3R5/pub?gid=146646633&single=true&output=csv"

# =========================
# FUNÇÃO ROBUSTA
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

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip().str.lower()
            df[col] = df[col].replace({
                "true": True,
                "false": False,
                "sim": True,
                "nao": False,
                "nan": False,
                "": False
            })

    return df

df_m1 = load_data(url_m1)
df_2faltas = load_data(url_2faltas)
df_desistentes = load_data(url_desistentes)

st.title("📊 Dashboard Executivo - Controle de Evasão")

tab1, tab2, tab3 = st.tabs(["🔵 Alunos M1", "🟠 Alunos 2 Faltas", "🔴 Alunos Desistentes"])

# =====================================================
# FUNÇÃO PARA GRÁFICO PERCENTUAL
# =====================================================
def percentual_chart(df, coluna, titulo):
    if coluna in df.columns:
        total = df["contrato"].count()
        if total > 0:
            dist = df.groupby(coluna)["contrato"].count() / total * 100
            st.subheader(titulo)
            st.bar_chart(dist.sort_values(ascending=False))

# =====================================================
# 🔵 ABA M1
# =====================================================
with tab1:

    st.subheader("Indicadores - M1")

    if "mes" in df_m1.columns:
        mes = st.selectbox("Filtrar por Mês", sorted(df_m1["mes"].dropna().unique()), key="mes_m1")
        df = df_m1[df_m1["mes"] == mes]
    else:
        df = df_m1

    total = df["contrato"].count()
    taxa_resposta = (df["resposta"].sum() / total * 100) if "resposta" in df.columns and total > 0 else 0
    taxa_historico = (df["historico"].sum() / total * 100) if "historico" in df.columns and total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total)
    col2.metric("Taxa Resposta", f"{taxa_resposta:.1f}%")
    col3.metric("Taxa Histórico", f"{taxa_historico:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        percentual_chart(df, "justificativa", "Distribuição % por Justificativa")
    with col2:
        percentual_chart(df, "orientador", "Distribuição % por Orientador")


# =====================================================
# 🟠 ABA 2 FALTAS
# =====================================================
with tab2:

    st.subheader("Indicadores - 2 Faltas")

    if "mes" in df_2faltas.columns:
        mes2 = st.selectbox("Filtrar por Mês", sorted(df_2faltas["mes"].dropna().unique()), key="mes_2faltas")
        df2 = df_2faltas[df_2faltas["mes"] == mes2]
    else:
        df2 = df_2faltas

    total2 = df2["contrato"].count()
    taxa_retorno = (df2["retorno"].sum() / total2 * 100) if "retorno" in df2.columns and total2 > 0 else 0
    taxa_resposta2 = (df2["resposta"].sum() / total2 * 100) if "resposta" in df2.columns and total2 > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total2)
    col2.metric("Taxa Retorno", f"{taxa_retorno:.1f}%")
    col3.metric("Taxa Resposta", f"{taxa_resposta2:.1f}%")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        percentual_chart(df2, "retorno", "Distribuição % Retorno")
    with col2:
        percentual_chart(df2, "resposta", "Distribuição % Resposta")


# =====================================================
# 🔴 ABA DESISTENTES
# =====================================================
with tab3:

    st.subheader("Indicadores - Desistentes")

    if "mes" in df_desistentes.columns:
        mes3 = st.selectbox("Filtrar por Mês", sorted(df_desistentes["mes"].dropna().unique()), key="mes_desistentes")
        df3 = df_desistentes[df_desistentes["mes"] == mes3]
    else:
        df3 = df_desistentes

    total3 = df3["contrato"].count()
    taxa_hist = (df3["historico"].sum() / total3 * 100) if "historico" in df3.columns and total3 > 0 else 0
    taxa_resposta3 = (df3["resposta"].sum() / total3 * 100) if "resposta" in df3.columns and total3 > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Contratos", total3)
    col2.metric("Taxa Histórico", f"{taxa_hist:.1f}%")
    col3.metric("Taxa Resposta", f"{taxa_resposta3:.1f}%")

    st.divider()

    percentual_chart(df3, "justificativa", "Distribuição % por Justificativa")
