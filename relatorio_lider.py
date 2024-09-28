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
    'Patielen',
    'Pastor Marcos',
    'Tacilene Ramos',
    'Baidem',
    'Sidne',
    'Ana Paula da Silva',
    'Edilson',
    'Edilson Negão',
    'Flávia Gava',
    'Ana Carolina',
    'Cleidiane Paixão',
    'Jackson Lima',
    'Elias Requel Costa',
    'Artur Lopes',
    'Daine',
    'Priscila',
    'Matheus Andrade',
    'Rafael Cohen',
    'Valdiney Siqueira',
    'Keila Ribeiro',
    'Vinícius Santos',
    'Joana Lopes',
    'Raimundo',
    'Ilda',
    'Sidney Guimarães',
    'Marcos Pereira',
    'Lula Leal',
    'Ana Carla Nunes',
    'Luiz Fernando Freitas dos Santos',
    'Anne Taiane',
    'Maria Maciel',
    'Cleudilene Mota',
    'João Thiago',
    'Dudita',
    'Wivila',
    'Taciana',
    'Eduardo',
    'Josiene Lobato',
    'Marinaldo Caldas Ramos',
    'Martha Isla',
    'Taiara',
    'Laila Maciel',
    'Ribamar',
    'Faate',
    'Maicon',
    'Madalena',
    'SOS',
    'Ieda',
    'Wericley Maciel',
    'Paulinha',
    'Helenio'
]

# Cria a pasta onde os PDFs serão salvos
output_folder = "relatorios_lideres"
os.makedirs(output_folder, exist_ok=True)

# Função para organizar os nomes e telefones em colunas
def organizar_em_colunas(dados, num_colunas=2):
    linhas = math.ceil(len(dados) / num_colunas)
    colunas = []
    
    for i in range(num_colunas):
        colunas.append(dados[i*linhas:(i+1)*linhas])
    
    # Adicionar espaços em branco para igualar o número de linhas
    for coluna in colunas:
        while len(coluna) < linhas:
            coluna.append(("", ""))

    return colunas

# Gera o PDF para cada líder na lista
for lider in lideres:
    # Consulta SQL para obter os registros associados ao líder
    cur.execute("SELECT nome, celular FROM cadastroeleitoral WHERE lider = %s ORDER BY nome ASC", (lider,))
    results = cur.fetchall()

    if results:
        dados = [(row[0], row[1]) for row in results]  # Lista de tuplas (nome, celular)
        colunas = organizar_em_colunas(dados)

        pdf = FPDF(orientation='P', unit='mm', format='A4')  # Garantindo que o formato seja A4
        pdf.add_page()
        pdf.set_font("Arial", size=6)  # Diminuir o tamanho da fonte para 6

        # Adiciona o título com o nome do líder
        pdf.cell(200, 5, txt=f"Líder: {lider}", ln=True, align='L')
        pdf.ln(5)  # Adiciona uma linha em branco

        # Define a largura das colunas para caber na largura da página A4 (210mm)
        largura_nome = 70  # Largura para o nome
        largura_telefone = 30  # Largura para o telefone

        # Adiciona os cabeçalhos da tabela
        pdf.set_font("Arial", 'B', size=6)
        pdf.cell(largura_nome, 5, txt="Nome", border=1, align='C')
        pdf.cell(largura_telefone, 5, txt="Telefone", border=1, align='C')
        pdf.cell(largura_nome, 5, txt="Nome", border=1, align='C')
        pdf.cell(largura_telefone, 5, txt="Telefone", border=1, align='C')
        pdf.ln(5)

        # Adiciona os nomes e números em duas colunas no PDF com grade
        pdf.set_font("Arial", size=6)
        for linha in zip(*colunas):
            nome1, celular1 = linha[0]
            nome2, celular2 = linha[1] if len(linha) > 1 else ("", "")

            pdf.cell(largura_nome, 5, txt=nome1, border=1)
            pdf.cell(largura_telefone, 5, txt=celular1 if celular1 else "Não informado", border=1)
            pdf.cell(largura_nome, 5, txt=nome2, border=1)
            pdf.cell(largura_telefone, 5, txt=celular2 if celular2 else "Não informado", border=1)
            pdf.ln(5)  # Move para a próxima linha

        # Salva o PDF na pasta especificada
        pdf_file_path = os.path.join(output_folder, f"{lider}.pdf")
        pdf.output(pdf_file_path)

        print(f"PDF gerado para o líder: {lider}")

# Fecha a conexão com o banco de dados
cur.close()
conn.close()
