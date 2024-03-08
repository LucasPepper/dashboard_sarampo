import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df_casos = pd.read_csv("casos_sarampo.csv", decimal = ',') # Casos confirmados de Sarampo no Brasil (1990 a 2022)
df_triplice_regioes = pd.read_csv("https://raw.githubusercontent.com/LucasPepper/cobertura_vacinal/main/cpnibr17092152690.csv", encoding = 'latin', sep = ';', decimal = ',') # sarampo , caxumba e rubéola
df_triplice_estados = pd.read_csv("https://raw.githubusercontent.com/LucasPepper/cobertura_vacinal/main/triplice%20viral%20estados%20regioes.csv", encoding = 'latin', sep = ';', decimal = ',') # sarampo , caxumba e rubéola

df = df_casos

# Removendo espaços dos índices
df.index = df.index.map(lambda x: str(x).strip())

col1, col2  = st.columns(2)
col3, col4  = st.columns(2)

df.index = df["Ano"]

# Gráfico 1 - Casos Anuais
# Ano
ano_filtro = st.sidebar.selectbox("Ano - Gráfico 1 (Casos Anuais)", df.index)
df_filtered_ano = df.loc[ano_filtro]

# Filtro Ano
fig_ano = px.bar(df_filtered_ano[1:], title="Casos Anuais de Sarampo (Filtrados por Ano)", text="value")
col1.plotly_chart(fig_ano, use_container_width=True)


# Gráfico 2 - Casos Anuais
# UF/Região
uf_filtro = st.sidebar.selectbox("UF/Região - Gráfico 2 (Casos Anuais)", df.columns[1:])
df_filtered_uf = df[uf_filtro]

# Filtro Região
fig_regiao = px.bar(df_filtered_uf, title="Casos Anuais de Sarampo (Filtrados por UF/Região)", text="value")
col2.plotly_chart(fig_regiao, use_container_width=True)

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

# fill in those three columns with respective metrics or KPIs
kpi1.metric(
    label="Regiões que alcançaram a Meta % CV desde 2017📉",
    value=0,
)

kpi2.metric(
    label="Média % CV do Brasil em 2021 (vs 2022)📈",
    value=74.94,
    delta=round(80.70 - 74.94, 2)
)

kpi3.metric(
    label="Casos anuais de Sarampo no Brasil em 2021 (vs 2022)📉",
    value=41,
    delta=676 - 41 
)


# Gráfico 3 - CV
df_triplice_regioes = df_triplice_regioes.drop(columns=" Total")
df_cv = pd.merge(df_triplice_estados, df_triplice_regioes, on="Ano")
df_cv.index = df_cv["Ano"]
df_cv = df_cv.drop(index= df_cv.index[-1])
df_cv = df_cv.drop(index= df_cv.index[0])
df_cv['Ano'] = df_cv['Ano'].astype(int)
df_cv.columns = df_cv.columns.map(lambda x: str(x).strip())
#df_cv = df_cv.drop(columns=["Total_x"])

# Mudando a ordem das colunas Regiões
nova_ordem_colunas = ["Ano", "1 Região Norte", "RO", "AC", "AM", "RR", "PA", "AP", "TO",
                      "2 Região Nordeste", "MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA",
                      "3 Região Sudeste", "MG", "ES", "RJ", "SP",
                      "4 Região Sul", "PR", "SC", "RS",
                      "5 Região Centro-Oeste","MS", "MT", "GO", "DF", "Total"]

df_cv = df_cv[nova_ordem_colunas]

df_cv = df_cv.rename(columns={"1 Região Norte": "Norte", "2 Região Nordeste": "Nordeste",
                               "3 Região Sudeste": "Sudeste", "4 Região Sul": "Sul",
                                 "5 Região Centro-Oeste": "Centro-Oeste", "Total": "Total_Brasil"})

# Ano
ano_cv_filtro = st.sidebar.selectbox("Ano - Gráfico 3 (CV %)", df_cv.index)
df_cv_filtered_ano = df_cv.loc[ano_cv_filtro]

# Filtro Ano
fig_cv_ano = px.bar(df_cv_filtered_ano[1:], title="CV (%) Anual D1 Tríplice Viral (Filtrada por Ano)", text="value")
fig_cv_ano.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Meta OMS 95%", annotation_position="top left")
col3.plotly_chart(fig_cv_ano, use_container_width=True)


# Gráfico 4 - CV
# UF/Região
uf_cv_filtro = st.sidebar.selectbox("UF/Região - Gráfico 4 (CV %)", df_cv.columns[1:])
df_cv_filtered_uf = df_cv[uf_cv_filtro]


# Filtro UF/Região
fig_regiao = px.bar(df_cv_filtered_uf, title="CV (%) Anual D1 Tríplice Viral (Filtrada por UF/Região)", text="value")
fig_regiao.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Meta OMS 95%", annotation_position="top right")
col4.plotly_chart(fig_regiao, use_container_width=True)




# Visão detalhada dos Datasets
# CV
st.markdown("### Visão Detalhada do Dataset - % CV")
st.dataframe(df_cv)

# Casos Anuais
st.markdown("### Visão Detalhada do Dataset - Casos Anuais de Sarampo")
st.dataframe(df_casos)
