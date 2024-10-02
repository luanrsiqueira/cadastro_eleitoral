
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

# Lista de nomes dos líderes
lideres = [
    "Ana Carla Lopes", "Ana Carla Nunes", "Ana Carolina", "Ana Paula da Silva", 
    "Anne Taiane", "Artur Lopes", "Baidem", "Cleidiane Paixão", "Cleudilene Mota", 
    "Daine", "Dudita", "Edilson", "Edilson Negão", "Eduardo", "Elias Requel Costa", 
    "Faate", "Flávia Gava", "Helenio", "Ieda", "Ilda", "Jackson Lima", "Joana Lopes", 
    "João Thiago", "Jordana", "Josiene Lobato", "Keila Ribeiro", "Laila Maciel", 
    "Luiz Fernando Freitas dos Santos", "Lula Leal", "Madalena", "Maicon", "Marcos Pereira", 
    "Maria Maciel", "Marinaldo Caldas Ramos", "Martha Isla", "Matheus Andrade", 
    "Pastor Marcos", "Paulinha", "Priscila", "Rafael Cohen", "Raimunda", "Raimundo", 
    "Ribamar", "Ronilson", "Sidne", "Sidney Guimarães", "SOS", "Taciana", 
    "Tacilene Ramos", "Taiara", "Valdiney Siqueira", "Vanuza Costa", "Vinícius Santos", 
    "Wericley Maciel", "Wivila", "Zilzane de Sousa"
]

# Função para criar o PDF com colunas e formato de tabela
def criar_pdf_por_lider():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 10)
    
    for lider in lideres:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, f"Relatório de {lider}", ln=True, align='C')

        # Cabeçalhos da tabela
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(90, 10, 'Nome', 1)
        pdf.cell(90, 10, 'Telefone', 1)
        pdf.ln()

        # Consulta para buscar dados de cada líder
        cur.execute("SELECT nome, celular FROM cadastro_eleitoral_v2 WHERE lider = %s", (lider,))
        rows = cur.fetchall()

        # Preenchendo os dados da tabela
        pdf.set_font('Arial', '', 10)
        for row in rows:
            pdf.cell(90, 10, row[0], 1)  # Nome
            pdf.cell(90, 10, row[1], 1)  # Telefone
            pdf.ln()

    output_path = os.path.join(os.getcwd(), "relatorio_lideres_tabela_formatada.pdf")
    pdf.output(output_path)
    print(f"PDF criado com sucesso em: {output_path}")

# Chamada da função para gerar o PDF
criar_pdf_por_lider()

# Fecha a conexão com o banco de dados
cur.close()
conn.close()
