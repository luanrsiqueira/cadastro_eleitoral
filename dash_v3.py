import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    dbname="cadastro_eleitoral_24",
    user="postgres",
    password="12182624",
    host="localhost",
    port="5432"
)

# Executar uma consulta SQL
query = "SELECT * FROM cadastroeleitoral"
df = pd.read_sql(query, conn)

# Fechar a conexão
conn.close()

# Calcular a idade
df['idade'] = pd.to_datetime('today').year - pd.to_datetime(df['data_nascimento']).dt.year

# Definir as faixas etárias
def faixa_etaria(idade):
    if idade < 18:
        return 'Menor de 18'
    elif 18 <= idade <= 25:
        return '18-25'
    elif 26 <= idade <= 35:
        return '26-35'
    elif 36 <= idade <= 45:
        return '36-45'
    elif 46 <= idade <= 60:
        return '46-60'
    elif idade > 60:
        return 'Acima de 60'
    else:
        return 'Não informado'

# Aplicar a função de faixa etária
df['faixa_etaria'] = df['idade'].apply(faixa_etaria)

# Definir a meta de votos
meta_votos = 500

# Calcular a quantidade total de eleitores (sem filtros)
quantidade_total_eleitores = df['id'].nunique()

# Calcular a porcentagem de votos atingidos em relação ao total de eleitores
porcentagem_atingida = (quantidade_total_eleitores / meta_votos) * 100

# Carregar a logo na barra lateral
st.sidebar.image("C:/Luan_Siqueira/cadastro_eleitoral/logo_patielen.png", width=200)

# Aplicar os filtros
df_filtered = df.copy()
selected_bairro = st.sidebar.multiselect("Selecione o Bairro", options=sorted(df['bairro'].unique()))
selected_faixa_etaria = st.sidebar.multiselect("Selecione a Faixa Etária", options=df['faixa_etaria'].unique())
selected_sexo = st.sidebar.multiselect("Selecione o Gênero", options=df['sexo'].unique())
selected_emprego = st.sidebar.multiselect("Selecione a Situação de Emprego", options=df['situacao_emprego'].unique())
selected_escolaridade = st.sidebar.multiselect("Selecione a Escolaridade", options=df['escolaridade'].unique())
selected_secao = st.sidebar.multiselect("Selecione a Seção Eleitoral", options=sorted(df['secao'].unique()))

if selected_bairro:
    df_filtered = df_filtered[df_filtered['bairro'].isin(selected_bairro)]
if selected_faixa_etaria:
    df_filtered = df_filtered[df_filtered['faixa_etaria'].isin(selected_faixa_etaria)]
if selected_sexo:
    df_filtered = df_filtered[df_filtered['sexo'].isin(selected_sexo)]
if selected_emprego:
    df_filtered = df_filtered[df_filtered['situacao_emprego'].isin(selected_emprego)]
if selected_escolaridade:
    df_filtered = df_filtered[df_filtered['escolaridade'].isin(selected_escolaridade)]
if selected_secao:
    df_filtered = df_filtered[df_filtered['secao'].isin(selected_secao)]

# Recalcular a quantidade total de eleitores após filtros
quantidade_eleitores_filtrados = df_filtered['id'].nunique()

# Calcular quantos votos faltam para atingir a meta
votos_faltando = meta_votos - quantidade_total_eleitores

# Exibir a barra de progresso
st.subheader("Progresso para Atingir a Meta")
st.progress(porcentagem_atingida / 100)

# Exibir a porcentagem de votos atingidos e votos faltando
st.write(f"Patielen está com **{quantidade_total_eleitores}** votos, o que representa **{porcentagem_atingida:.2f}%** da meta de {meta_votos} votos.")
st.write(f"Faltam **{votos_faltando}** votos para atingir a meta.")

# Exibir o número total de eleitores (baseado em filtros)
st.metric(label="Quantidade Total de Eleitores", value=quantidade_eleitores_filtrados)

# Gráfico de eleitores por bairro
st.subheader("Distribuição por Bairro")
fig_bairro = px.bar(df_filtered['bairro'].value_counts(), orientation='h', 
                    labels={'index': 'Bairro', 'value': 'Quantidade de Eleitores'})
st.plotly_chart(fig_bairro)

# Gráfico de distribuição por faixa etária
st.subheader("Distribuição por Faixa Etária")
fig_faixa_etaria = px.bar(df_filtered['faixa_etaria'].value_counts().reindex(['Menor de 18', '18-25', '26-35', '36-45', '46-60', 'Acima de 60', 'Não informado']), 
                          orientation='h', labels={'index': 'Faixa Etária', 'value': 'Quantidade de Eleitores'})
st.plotly_chart(fig_faixa_etaria)

# Gráfico de distribuição por situação de emprego
st.subheader("Distribuição por Situação de Emprego")
fig_emprego = px.bar(df_filtered['situacao_emprego'].value_counts(), orientation='h', 
                     labels={'index': 'Situação de Emprego', 'value': 'Quantidade de Eleitores'})
st.plotly_chart(fig_emprego)

# Gráfico de distribuição por escolaridade
st.subheader("Distribuição por Escolaridade")
fig_escolaridade = px.bar(df_filtered['escolaridade'].value_counts(), orientation='h', 
                          labels={'index': 'Escolaridade', 'value': 'Quantidade de Eleitores'})
st.plotly_chart(fig_escolaridade)

# Gráfico de Treemap para Seção Eleitoral com Quantidade de Eleitores
st.subheader("Distribuição por Seção Eleitoral (Treemap)")
secao_counts = df_filtered['secao'].value_counts().reset_index()
secao_counts.columns = ['Seção Eleitoral', 'Quantidade de Eleitores']
fig_treemap = px.treemap(secao_counts, 
                         path=['Seção Eleitoral'], 
                         values='Quantidade de Eleitores',
                         labels={'Seção Eleitoral': 'Seção Eleitoral', 'Quantidade de Eleitores': 'Quantidade de Eleitores'},
                         color='Quantidade de Eleitores',
                         hover_data={'Quantidade de Eleitores': True})
st.plotly_chart(fig_treemap)

# Gráfico de distribuição por sexo
st.subheader("Distribuição por Gênero")
fig_sexo = px.pie(df_filtered, names='sexo', title='Distribuição por Gênero')
st.plotly_chart(fig_sexo)
