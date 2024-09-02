import pandas as pd
import psycopg2
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx

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

# Calcular a quantidade total de eleitores
quantidade_total_eleitores = df['id'].nunique()

# Definir a meta de votos
meta_votos = 500

# Calcular a porcentagem de votos atingidos
porcentagem_atingida = (quantidade_total_eleitores / meta_votos) * 100

# Calcular quantos votos faltam para atingir a meta
votos_faltando = meta_votos - quantidade_total_eleitores
porcentagem_faltando = 100 - porcentagem_atingida

# Calcular a quantidade de eleitores por líder
eleitores_por_lider = df.groupby('lider')['id'].count().reset_index()
eleitores_por_lider.columns = ['lider', 'quantidade_eleitores']

# Calcular a quantidade total de eleitores
quantidade_total_eleitores = df['id'].nunique()

# Criar filtros adicionais
bairro_filtro = df['bairro'].value_counts()
estado_civil_filtro = df['estado_civil'].value_counts()
sexo_filtro = df['sexo'].value_counts()
situacao_emprego_filtro = df['situacao_emprego'].value_counts()
escolaridade_filtro = df['escolaridade'].value_counts()
zona_filtro = df['zona_eleitoral'].value_counts()
profissao_filtro = df['profissao'].value_counts()

# Contagem das faixas etárias
faixa_etaria_filtro = df['faixa_etaria'].value_counts()

# Definir a ordem correta das faixas etárias
ordem_faixas = ['Menor de 18', '18-25', '26-35', '36-45', '46-60', 'Acima de 60', 'Não informado']
faixa_etaria_filtro = faixa_etaria_filtro.reindex(ordem_faixas).fillna(0)

st.sidebar.image("C:\Luan_Siqueira\cadastro_eleitoral\logo_patielen.png", width=150)

# Exibir o número total de eleitores
st.metric(label="Quantidade Total de Eleitores", value=quantidade_total_eleitores)

# Exibir a barra de progresso
st.subheader("Progresso para Atingir a Meta")
st.progress(porcentagem_atingida / 100)

# Exibir a porcentagem de votos atingidos e votos faltando
st.write(f"Patielen está com **{quantidade_total_eleitores}** votos, o que representa **{porcentagem_atingida:.2f}%** da meta de {meta_votos} votos.")
st.write(f"Faltam **{votos_faltando}** votos para atingir a meta.")


# Gráfico de eleitores por líder (barra)
st.subheader("Quantidade de Eleitores por Líder")
fig_lider_bar = px.bar(eleitores_por_lider, x='lider', y='quantidade_eleitores',
                       labels={'lider': 'Líder', 'quantidade_eleitores': 'Quantidade de Eleitores'},
                       text=eleitores_por_lider['quantidade_eleitores'])
fig_lider_bar.update_traces(textangle=0)
st.plotly_chart(fig_lider_bar)

# Gráfico de eleitores por líder (pizza)
st.subheader("Distribuição de Eleitores por Líder (Gráfico de Pizza)")
fig_lider_pizza = px.pie(eleitores_por_lider, values='quantidade_eleitores', names='lider',
                         hole=0.3, labels={'quantidade_eleitores': 'Quantidade de Eleitores', 'lider': 'Líder'})
st.plotly_chart(fig_lider_pizza)

# Gráfico de distribuição por sexo
st.subheader("Distribuição por Sexo")
fig_sexo = px.pie(values=sexo_filtro.values, names=sexo_filtro.index,
                  hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Sexo'})
st.plotly_chart(fig_sexo)

# Gráfico de distribuição por situação de emprego
st.subheader("Distribuição por Situação de Emprego")
fig_emprego = px.pie(values=situacao_emprego_filtro.values, names=situacao_emprego_filtro.index,
                     hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Situação de Emprego'})
st.plotly_chart(fig_emprego)

# Gráfico de distribuição por escolaridade
st.subheader("Distribuição por Escolaridade")
fig_escolaridade = px.pie(values=escolaridade_filtro.values, names=escolaridade_filtro.index,
                          hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Escolaridade'})
st.plotly_chart(fig_escolaridade)

# Gráfico de distribuição por estado civil
st.subheader("Distribuição por Estado Civil")
fig_estado_civil = px.pie(values=estado_civil_filtro.values, names=estado_civil_filtro.index,
                          hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Estado Civil'})
st.plotly_chart(fig_estado_civil)

# Gráfico de distribuição por profissão
st.subheader("Distribuição por Profissão")
fig_profissao = px.bar(profissao_filtro, x=profissao_filtro.values, y=profissao_filtro.index, orientation='h',
                       labels={'x': 'Quantidade de Eleitores', 'y': 'Profissões'},
                       text=profissao_filtro.values)
fig_profissao.update_traces(textangle=0)
st.plotly_chart(fig_profissao)

# Gráfico de eleitores por bairro
st.subheader("Distribuição por Bairro")
fig_bairro = px.bar(bairro_filtro, x=bairro_filtro.values, y=bairro_filtro.index, orientation='h',
                    labels={'x': 'Quantidade de Eleitores', 'y': 'Bairros'},
                    text=bairro_filtro.values)
fig_bairro.update_traces(textangle=0)
st.plotly_chart(fig_bairro)

# Gráfico de pizza para distribuição por bairro
st.subheader("Distribuição por Bairro (Gráfico de Pizza)")
fig_bairro_pizza = px.pie(values=bairro_filtro.values, names=bairro_filtro.index,
                          hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Bairros'})
st.plotly_chart(fig_bairro_pizza)

# Gráfico de distribuição por faixa etária (ordenado)
st.subheader("Distribuição por Faixa Etária")
fig_faixa_etaria = px.bar(faixa_etaria_filtro, x=faixa_etaria_filtro.values, y=faixa_etaria_filtro.index, orientation='h',
                          labels={'x': 'Quantidade de Eleitores', 'y': 'Faixa Etária'},
                          text=faixa_etaria_filtro.values)
fig_faixa_etaria.update_traces(textangle=0)
st.plotly_chart(fig_faixa_etaria)

# Gráfico de pizza para distribuição por faixa etária
st.subheader("Distribuição por Faixa Etária (Gráfico de Pizza)")
fig_faixa_etaria_pizza = px.pie(values=faixa_etaria_filtro.values, names=faixa_etaria_filtro.index,
                                hole=0.3, labels={'values': 'Quantidade de Eleitores', 'names': 'Faixa Etária'})
st.plotly_chart(fig_faixa_etaria_pizza)

# Contagem de cadastros por data
cadastros_por_data = df['data_cadastro'].value_counts().sort_index()

# Gráfico de área para evolução cumulativa dos cadastros
st.subheader("Evolução Cumulativa dos Cadastros")
fig_area = px.area(cadastros_por_data, x=cadastros_por_data.index, y=cadastros_por_data.values,
                   labels={'x': 'Data de Cadastro', 'y': 'Quantidade de Cadastros'})
st.plotly_chart(fig_area)

# Agrupar os dados por bairro e faixa etária, e contar o número de eleitores
df_grouped = df.groupby(['bairro', 'faixa_etaria']).size().reset_index(name='quantidade_eleitores')

# Gráfico de barras empilhadas para distribuição de faixas etárias por bairro
st.subheader("Distribuição de Faixas Etárias por Bairro")
fig_stacked_bar = px.bar(df_grouped, x='bairro', y='quantidade_eleitores', color='faixa_etaria',
                         labels={'bairro': 'Bairro', 'quantidade_eleitores': 'Quantidade de Eleitores'},
                         barmode='stack')
st.plotly_chart(fig_stacked_bar)



