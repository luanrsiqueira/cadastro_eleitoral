import pandas as pd
import psycopg2

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    dbname="cadastro_eleitoral_24",
    user="postgres",
    password="12182624",
    host="localhost",
    port="5432"
)

# Executar uma consulta SQL
query = "SELECT * FROM cadastro_eleitoral_v6 ORDER BY id ASC"
df = pd.read_sql(query, conn)

# Fechar a conexão
conn.close()

# Agrupar por líder e contar a quantidade de eleitores para cada líder
df_lideres = df.groupby('lider').size().reset_index(name='quantidade_eleitores')

# Ordenar pelo número de eleitores em ordem crescente
df_lideres = df_lideres.sort_values(by='quantidade_eleitores', ascending=True)

# Salvar o resultado em um novo arquivo CSV
df_lideres.to_csv("quantidade_eleitores_por_lider.csv", index=False)

# Salvar os resultados da consulta em um arquivo CSV
df.to_csv("cadastroeleitoral.csv", index=False)

