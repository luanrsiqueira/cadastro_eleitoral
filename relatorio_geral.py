import psycopg2
from fpdf import FPDF
import os

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
    FROM cadastroeleitoral
    ORDER BY nome ASC
""")
results = cur.fetchall()

# Cria o PDF geral
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=7)  # Definir o tamanho da fonte

# Adicionar o título do PDF
pdf.cell(200, 10, txt="Relatório Geral de Eleitores", ln=True, align='C')
pdf.ln(10)  # Adicionar uma linha em branco

# Definir a largura de cada coluna
largura_nome = 50
largura_telefone = 30
largura_titulo = 40
largura_secao = 30

# Adicionar cabeçalhos das colunas
pdf.set_font("Arial", style='B', size=7)  # Fonte em negrito para cabeçalhos
pdf.cell(largura_nome, 10, txt="Nome", border=1, align='C')
pdf.cell(largura_telefone, 10, txt="Telefone", border=1, align='C')
pdf.cell(largura_titulo, 10, txt="Título", border=1, align='C')
pdf.cell(largura_secao, 10, txt="Seção", border=1, align='C')
pdf.ln(10)

# Resetar a fonte para os dados
pdf.set_font("Arial", size=7)

# Adicionar os dados de cada eleitor no PDF
for row in results:
    nome, celular, titulo, secao = row
    pdf.cell(largura_nome, 8, txt=nome, border=1)
    pdf.cell(largura_telefone, 8, txt=celular if celular else "Não informado", border=1)
    pdf.cell(largura_titulo, 8, txt=titulo, border=1)
    pdf.cell(largura_secao, 8, txt=secao, border=1)
    pdf.ln(8)

# Salva o PDF na pasta especificada
output_folder = "relatorios_gerais"
os.makedirs(output_folder, exist_ok=True)
pdf_file_path = os.path.join(output_folder, "relatorio_geral_eleitores.pdf")
pdf.output(pdf_file_path)

print(f"PDF geral gerado: {pdf_file_path}")

# Fecha a conexão com o banco de dados
cur.close()
conn.close()
