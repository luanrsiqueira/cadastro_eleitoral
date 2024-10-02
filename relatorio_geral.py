from fpdf import FPDF
import psycopg2

# Configurações da conexão ao PostgreSQL
conn = psycopg2.connect(
    dbname="cadastro_eleitoral_24",
    user="postgres",
    password="12182624",
    host="localhost",
    port="5432"
)

# Cria um cursor para executar comandos SQL
cur = conn.cursor()

# Consulta SQL para obter nome, telefone, título e seção de cada eleitor
cur.execute("""
    SELECT nome, celular, titulo_eleitoral, secao
    FROM cadastro_eleitoral_v6
    ORDER BY nome ASC
""")
results = cur.fetchall()

# Contagem total de eleitores
total_eleitores = len(results)

# Cria o PDF geral
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=7)  # Definir o tamanho da fonte

# Adicionar o título do PDF
pdf.cell(200, 10, txt="Relatório Geral de Eleitores", ln=True, align='C')
pdf.ln(10)  # Adicionar uma linha em branco

# Adicionar a contagem total de eleitores no início do PDF
pdf.set_font("Arial", size=10)
pdf.cell(200, 10, txt=f"Total de Eleitores: {total_eleitores}", ln=True, align='C')
pdf.ln(10)

# Definir a largura de cada coluna
largura_nome = 50
largura_telefone = 30
largura_titulo = 40
largura_secao = 30

# Adicionar cabeçalhos das colunas
pdf.set_font("Arial", style='B', size=7)  # Fonte em negrito para cabeçalhos
pdf.cell(largura_nome, 10, 'Nome', 1)
pdf.cell(largura_telefone, 10, 'Celular', 1)
pdf.cell(largura_titulo, 10, 'Título Eleitoral', 1)
pdf.cell(largura_secao, 10, 'Seção', 1)
pdf.ln()

# Adicionar os dados dos eleitores ao PDF
pdf.set_font("Arial", size=7)
for row in results:
    pdf.cell(largura_nome, 10, row[0], 1)
    pdf.cell(largura_telefone, 10, row[1], 1)
    pdf.cell(largura_titulo, 10, row[2], 1)
    pdf.cell(largura_secao, 10, row[3], 1)
    pdf.ln()

# Salvar o PDF em um arquivo
pdf.output("relatorio_geral_eleitores.pdf")

# Fechar a conexão com o banco de dados
cur.close()
conn.close()
