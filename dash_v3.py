import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("cadastroeleitoral.csv")

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
meta_votos = 1500

# Calcular a quantidade total de eleitores (sem filtros)
quantidade_total_eleitores = df['id'].nunique()

# Calcular a porcentagem de votos atingidos em relação ao total de eleitores
porcentagem_atingida = (quantidade_total_eleitores / meta_votos) * 100

# Carregar a logo na barra lateral
st.sidebar.image("logo_patielen.png", width=200)

# Aplicar os filtros
df_filtered = df.copy()
selected_bairro = st.sidebar.multiselect("Selecione o Bairro", options=sorted(df['bairro'].unique()))
selected_faixa_etaria = st.sidebar.multiselect("Selecione a Faixa Etária", options=df['faixa_etaria'].unique())
selected_sexo = st.sidebar.multiselect("Selecione o Gênero", options=df['sexo'].unique())
selected_emprego = st.sidebar.multiselect("Selecione a Situação de Emprego", options=df['situacao_emprego'].unique())
selected_escolaridade = st.sidebar.multiselect("Selecione a Escolaridade", options=df['escolaridade'].unique())
selected_secao = st.sidebar.multiselect("Selecione a Seção Eleitoral", options=sorted(df["secao"].unique()))
selected_lider = st.sidebar.multiselect("Selecione o Líder", options=sorted(df['lider'].unique()))

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
if selected_lider:
    df_filtered = df_filtered[df_filtered['lider'].isin(selected_lider)]

# Recalcular a quantidade total de eleitores após filtros
quantidade_eleitores_filtrados = df_filtered['id'].nunique()

# Calcular quantos votos faltam para atingir a meta
votos_faltando = meta_votos - quantidade_total_eleitores

st.image("logo_patielen.png", width=100)

# Exibir a barra de progresso
st.subheader("Progresso para Atingir a Meta")
st.progress(porcentagem_atingida / 100)

# Exibir a porcentagem de votos atingidos e votos faltando
st.write(f"Patielen está com **{quantidade_total_eleitores}** votos, o que representa **{porcentagem_atingida:.2f}%** da meta de {meta_votos} votos.")
st.write(f"Faltam **{votos_faltando}** votos para atingir a meta.")

# Exibir o número total de eleitores (baseado em filtros)
st.metric(label="Quantidade Total de Eleitores", value=quantidade_eleitores_filtrados)

if selected_secao:
    # Filtrar os eleitores da seção selecionada
    eleitores_filtrados = df[df["secao"].isin(selected_secao)][["nome", "titulo_eleitoral"]]
    
    # Colocar a tabela logo abaixo da quantidade total de eleitores
    st.write("Eleitores nesta seção:")
    st.dataframe(eleitores_filtrados)

# Gráfico de distribuição por líder
st.subheader("Distribuição por Líder")
lider_counts = df_filtered['lider'].value_counts().reset_index()
lider_counts.columns = ['Líder', 'Count']
fig_lider = px.bar(lider_counts, x='Count', y='Líder', orientation='h', 
                   labels={'Líder': 'Líder', 'Count': 'Eleitores'})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_lider.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

# Adicionar as quantidades no final das barras
fig_lider.update_traces(texttemplate='%{x}', textposition='outside')

st.plotly_chart(fig_lider)

# Gráfico de eleitores por bairro
st.subheader("Distribuição por Bairro")
bairro_counts = df_filtered['bairro'].value_counts().reset_index()
bairro_counts.columns = ['Bairro', 'Count']
fig_bairro = px.bar(bairro_counts, x='Count', y='Bairro', orientation='h', 
                    labels={'Bairro': 'Bairro', 'Count': 'Eleitores'})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_bairro.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

# Adicionar as quantidades no final das barras
fig_bairro.update_traces(texttemplate='%{x}', textposition='outside')

st.plotly_chart(fig_bairro)

# Gráfico de distribuição por faixa etária
st.subheader("Distribuição por Faixa Etária")
faixa_counts = df_filtered['faixa_etaria'].value_counts().reindex(['Menor de 18', '18-25', '26-35', '36-45', '46-60', 'Acima de 60', 'Não informado']).reset_index()
faixa_counts.columns = ['Faixa Etária', 'Count']
fig_faixa_etaria = px.bar(faixa_counts, x='Count', y='Faixa Etária', orientation='h', 
                          labels={'Faixa Etária': 'Faixa Etária', 'Count': 'Eleitores'})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_faixa_etaria.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

# Adicionar as quantidades no final das barras
fig_faixa_etaria.update_traces(texttemplate='%{x}', textposition='outside')

st.plotly_chart(fig_faixa_etaria)

# Gráfico de distribuição por situação de emprego
st.subheader("Distribuição por Situação de Emprego")
emprego_counts = df_filtered['situacao_emprego'].value_counts().reset_index()
emprego_counts.columns = ['Situação de Emprego', 'Count']
fig_emprego = px.bar(emprego_counts, x='Count', y='Situação de Emprego', orientation='h', 
                     labels={'Situação de Emprego': 'Situação de Emprego', 'Count': 'Eleitores'})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_emprego.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

# Adicionar as quantidades no final das barras
fig_emprego.update_traces(texttemplate='%{x}', textposition='outside')

st.plotly_chart(fig_emprego)

# Gráfico de distribuição por escolaridade
st.subheader("Distribuição por Escolaridade")
escolaridade_counts = df_filtered['escolaridade'].value_counts().reset_index()
escolaridade_counts.columns = ['Escolaridade', 'Count']
fig_escolaridade = px.bar(escolaridade_counts, x='Count', y='Escolaridade', orientation='h', 
                          labels={'Escolaridade': 'Escolaridade', 'Count': 'Eleitores'})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_escolaridade.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

# Adicionar as quantidades no final das barras
fig_escolaridade.update_traces(texttemplate='%{x}', textposition='outside')

st.plotly_chart(fig_escolaridade)

# Gráfico de Treemap para Seção Eleitoral com Eleitores
st.subheader("Distribuição por Seção Eleitoral (Treemap)")
secao_counts = df_filtered['secao'].value_counts().reset_index()
secao_counts.columns = ['Seção Eleitoral', 'Eleitores']
fig_treemap = px.treemap(secao_counts, 
                         path=['Seção Eleitoral'], 
                         values='Eleitores',
                         labels={'Seção Eleitoral': 'Seção Eleitoral', 'Eleitores': 'Eleitores'},
                         color='Eleitores',
                         hover_data={'Eleitores': True})

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_treemap.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

st.plotly_chart(fig_treemap)

# Gráfico de distribuição por sexo
st.subheader("Distribuição por Gênero")
fig_sexo = px.pie(df_filtered, names='sexo', title='Distribuição por Gênero')

# Ajustar layout para exibir corretamente em dispositivos móveis
fig_sexo.update_layout(
    autosize=True,
    margin=dict(l=0, r=0, t=30, b=30),
    height=300
)

st.plotly_chart(fig_sexo)