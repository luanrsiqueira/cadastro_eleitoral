import psycopg2
from fpdf import FPDF
import os
import math

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
    'Ana Carla Nunes', 'Ana Carolina', 'Ana Paula da Silva', 'Anne Taiane', 
    'Artur Lopes', 'Baidem', 'Cleidiane Paixão', 'Cleudilene Mota', 'Daine', 
    'Dudita', 'Edilson Negão', 'Eduardo', 'Elias Requel Costa', 'Faate', 
    'Flávia Gava', 'Helenio', 'Ieda', 'Ilda', 'Jackson Lima', 'Joana Lopes', 
    'Josiene Lobato', 'Keila Ribeiro', 'Laila Maciel', 'Luiz Fernando Freitas dos Santos', 
    'Lula Leal', 'Madalena', 'Maicon', 'Marcos Pereira', 'Maria Maciel', 
    'Marinaldo Caldas Ramos', 'Martha Isla', 'Matheus Andrade', 'Pastor Marcos', 
    'Patielen', 'Paulinha', 'Rafael Cohen', 'Raimundo', 'Ribamar', 'Sidney Guimarães', 
    'SOS', 'Taciana', 'Tacilene Ramos', 'Taiara', 'Valdiney Siqueira', 
    'Vinícius Santos', 'Wericley Maciel', 'Wirla'
]

# Cria a pasta onde os PDFs serão salvos
output_folder = "pdf_output"
os.makedirs(output_folder, exist_ok=True)

# Função para organizar os nomes em colunas
def organizar_em_colunas(nomes, num_colunas=2):
    linhas = math.ceil(len(nomes) / num_colunas)
    colunas = []
    
    for i in range(num_colunas):
        colunas.append(nomes[i*linhas:(i+1)*linhas])
    
    # Adicionar espaços em branco para igualar o número de linhas
    for coluna in colunas:
        while len(coluna) < linhas:
            coluna.append("")

    return colunas

# Gera o PDF para cada líder na lista
for lider in lideres:
    # Consulta SQL para obter os registros associados ao líder
    cur.execute("SELECT nome FROM cadastroeleitoral WHERE lider = %s ORDER BY nome ASC", (lider,))
    results = cur.fetchall()

    if results:
        nomes = [row[0] for row in results]
        colunas = organizar_em_colunas(nomes)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Adiciona o título com o nome do líder
        pdf.cell(200, 10, txt=f"Líder: {lider}", ln=True, align='L')
        pdf.ln(10)  # Adiciona uma linha em branco

        # Define a largura de cada coluna para duas colunas
        largura_coluna = 95

        # Adiciona os nomes em duas colunas no PDF
        for linha in zip(*colunas):
            for coluna in linha:
                pdf.cell(largura_coluna, 10, txt=coluna, border=0)
            pdf.ln(10)  # Move para a próxima linha

        # Salva o PDF na pasta especificada
        pdf_file_path = os.path.join(output_folder, f"{lider}.pdf")
        pdf.output(pdf_file_path)

        print(f"PDF gerado para o líder: {lider}")

# Fecha a conexão com o banco de dados
cur.close()
conn.close()
