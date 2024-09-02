import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import streamlit as st

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

quantidade_total_eleitores = df['id'].nunique()

# Calcular a quantidade de eleitores por líder
eleitores_por_lider = df.groupby('lider')['titulo_eleitoral'].count().reset_index()
eleitores_por_lider.columns = ['lider', 'quantidade_eleitores']

# Exibir o resultado
#print(eleitores_por_lider)

# Criar filtros adicionais
bairro_filtro = df['bairro'].value_counts()
estado_civil_filtro = df['estado_civil'].value_counts()
df['idade'] = pd.to_datetime('today').year - pd.to_datetime(df['data_nascimento']).dt.year
faixa_etaria_filtro = df['idade'].value_counts(bins=[18, 25, 35, 45, 60, 100], sort=False)

# Gráfico de eleitores por líder
plt.figure(figsize=(10, 6))
plt.bar(eleitores_por_lider['lider'], eleitores_por_lider['quantidade_eleitores'], color='skyblue')
plt.title('Quantidade de Eleitores por Líder')
plt.xlabel('Líder')
plt.ylabel('Quantidade de Eleitores')
plt.xticks(rotation=90)
plt.show()

# Streamlit dashboard
st.title("Campanha Patielen")

st.metric(label="Quantidade Total de Eleitores", value=quantidade_total_eleitores)

st.subheader("Quantidade de Eleitores por Líder")
st.bar_chart(eleitores_por_lider.set_index('lider')['quantidade_eleitores'], horizontal=True)

st.subheader("Distribuição por Bairro")
st.bar_chart(bairro_filtro, horizontal=True)

st.subheader("Distribuição por Estado Civil")
st.bar_chart(estado_civil_filtro, horizontal=True)

st.subheader("Distribuição por Faixa Etária")
st.bar_chart(faixa_etaria_filtro)