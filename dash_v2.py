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
query = "SELECT * FROM cadastroeleitoral ORDER BY id ASC"
df = pd.read_sql(query, conn)

# Fechar a conexão
conn.close()

# Salvar os resultados da consulta em um arquivo CSV
df.to_csv("cadastroeleitoral.csv", index=False)

