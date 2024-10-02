
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


# Função para extrair apenas o primeiro e segundo nome, ignorando preposições
def extrair_primeiro_e_segundo_nome_sem_preposicoes(nome_completo):
    partes = nome_completo.split()
    nomes_validos = []

    for parte in partes:
        # Pula preposições como "de", "do", "da", "das", "dos"
        if len(parte) > 2 or parte.lower() not in ['de', 'do', 'da', 'das', 'dos']:
            nomes_validos.append(parte)
        if len(nomes_validos) == 2:  # Pegamos apenas o primeiro e o segundo nome válido
            break

    return " ".join(nomes_validos)

# Função para criar o PDF com a lógica de pegar o primeiro e segundo nome sem preposições
def criar_pdf_por_lider():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', '', 10)
    
    for lider in lideres:
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(200, 10, f"Relatório de {lider}", ln=True, align='C')

        # Cabeçalhos do estilo Excel
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(48, 10, 'Nome', 1)
        pdf.cell(48, 10, 'Tel', 1)
        pdf.cell(48, 10, 'Nome', 1)
        pdf.cell(48, 10, 'Tel', 1)
        pdf.ln()

        # Consulta para buscar dados de cada líder
        cur.execute("SELECT nome, celular FROM cadastro_eleitoral_v6 WHERE lider = %s order by nome ASC", (lider,),)
        rows = cur.fetchall()

        # Preenchendo os dados da tabela estilo Excel, pegando apenas o primeiro e segundo nome sem preposições
        pdf.set_font('Arial', '', 10)
        for i in range(0, len(rows), 2):
            # Extrair o primeiro e segundo nome válidos, ignorando preposições
            nome1 = extrair_primeiro_e_segundo_nome_sem_preposicoes(rows[i][0]) if i < len(rows) else ''
            nome2 = extrair_primeiro_e_segundo_nome_sem_preposicoes(rows[i + 1][0]) if i + 1 < len(rows) else ''

            # Coluna 1: Nome e Telefone
            pdf.cell(48, 10, nome1, 1)
            pdf.cell(48, 10, rows[i][1] if i < len(rows) else '', 1)
            
            # Coluna 2: Nome e Telefone (para preencher lado a lado)
            pdf.cell(48, 10, nome2, 1)
            pdf.cell(48, 10, rows[i + 1][1] if i + 1 < len(rows) else '', 1)
            
            pdf.ln()

    output_path = os.path.join(os.getcwd(), "relatorios_lideres_ordem_asc.pdf")
    pdf.output(output_path)
    print(f"PDF criado com sucesso em: {output_path}")

# Chamada da função para gerar o PDF
criar_pdf_por_lider()

# Fecha a conexão com o banco de dados
cur.close()
conn.close()
