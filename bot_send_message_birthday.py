from datetime import datetime, timedelta
from dotenv import load_dotenv
from urllib.parse import quote
from time import sleep
import webbrowser
import pyautogui
import psycopg2
import os
import re

load_dotenv('config.env')

# Configurações do PostgreSQL
DB_HOST = os.getenv('DB_HOST')
DB_DATABASE = os.getenv('DB_DATABASE')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Número do destinatário fixo
#telefone = '559492821276'
telefone = '559488164555'

def criar_conexao_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_DATABASE,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no banco de dados: {e}")
        return None

def obter_aniversariantes(data_inicial, data_final):
    conn = criar_conexao_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = """
            SELECT nome, data_nascimento, celular, sexo
            FROM cadastroeleitoral
            WHERE TO_CHAR(data_nascimento, 'MM-DD') BETWEEN %s AND %s
            AND celular IS NOT NULL 
            AND celular <> 'Não informado'
            ORDER BY TO_CHAR(data_nascimento, 'MM-DD') ASC
            ;
        """
        data_inicial_str = data_inicial.strftime('%m-%d')
        data_final_str = data_final.strftime('%m-%d')
        cursor.execute(query, (data_inicial_str, data_final_str))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados
    except Exception as e:
        print(f"Erro ao consultar aniversariantes: {e}")
        return []

def formatar_celular(numero):
    numero = re.sub(r'\D', '', numero)
    numero_formatado = re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', numero)
    
    return numero_formatado

def enviar_mensagem(mensagem, telefone):
    try:
        link_mensagem_whatsapp = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
        webbrowser.open(link_mensagem_whatsapp)
        sleep(15) 
        seta = pyautogui.locateCenterOnScreen('seta.png')
        if seta is not None:
            sleep(2)
            pyautogui.click(seta[0], seta[1])
            sleep(2)
            pyautogui.hotkey('ctrl', 'w')
            sleep(2)
        else:
            print("Não foi possível localizar a seta de envio no WhatsApp Web.")
    except Exception as e:
        print(f"Erro ao enviar mensagem para {telefone}: {e}")

def obter_saudacao():
    hora_atual = datetime.now().hour
    if hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    else:
        return "Boa noite"

def enviar_alerta_semanal():
    hoje = datetime.now().date()
    
    # Calcula as datas para o início (segunda-feira) e fim (domingo) da semana
    inicio_semana = hoje - timedelta(days=hoje.weekday()) 
    fim_semana = inicio_semana + timedelta(days=6)  
    
    aniversariantes = obter_aniversariantes(inicio_semana, fim_semana)
    
    if aniversariantes:
        mensagem = "🎉 *Aniversariantes da Semana* 🎉\n\n"
        for nome, data, celular, sexo in aniversariantes:
            if not celular:
                continue  # Ignora se o número de telefone estiver ausente

            primeiro_nome = nome.split()[0]
            data_aniversario = data.strftime('%d/%m')
            celular_formatado = formatar_celular(celular)
            mensagem += f"- {primeiro_nome} - {data_aniversario} - {celular_formatado}\n"
        enviar_mensagem(mensagem, telefone)
    else:
        print("Nenhum aniversariante nesta semana.")

def enviar_alerta_diario():
    hoje = datetime.now().date()
    
    aniversariantes = obter_aniversariantes(hoje, hoje)
    
    if aniversariantes:
        # Lista de aniversariantes do dia com números de telefone válidos
        lista_aniversariantes = []
        for nome, data_nascimento, celular, sexo in aniversariantes:
            if not celular or not re.search(r'\d', celular):  # Verifica se o celular está vazio ou sem números válidos
                continue  # Ignora se o número de telefone estiver ausente ou inválido

            celular_formatado = formatar_celular(celular)
            lista_aniversariantes.append(f"{nome} - Tel: {celular_formatado}")
        
        # Verifica se há aniversariantes válidos na lista antes de enviar a mensagem
        if lista_aniversariantes:
            # Construir a mensagem com todos os aniversariantes do dia
            data_aniversario = hoje.strftime("%d/%m/%Y")
            mensagem_resumo = f"🎂 *Aniversariantes de Hoje* 🎂\n\nHoje {data_aniversario} é aniversário de:\n" + "\n".join(lista_aniversariantes) + "\n\nNão esqueça de parabenizá-los!"
            enviar_mensagem(mensagem_resumo, telefone)

            # Enviar a mensagem de aviso uma vez, após os aniversariantes do dia
            mensagem_aviso = "📢 *Sugestão de mensagem para enviar ao aniversariante:*"
            enviar_mensagem(mensagem_aviso, telefone)

            saudacao = obter_saudacao()
            for nome, data_nascimento, celular, sexo in aniversariantes:
                if not celular or not re.search(r'\d', celular):  # Verifica novamente antes de enviar mensagens individuais
                    continue

                primeiro_nome = nome.split()[0]
                saudacao_completa = f"{saudacao} {primeiro_nome}, tudo bem minha amiga?" if sexo == 'Feminino' else f"{saudacao} {primeiro_nome}, tudo bem meu amigo?"
                celular_formatado = formatar_celular(celular)

                # Enviar mensagem de aniversário personalizada para cada aniversariante
                mensagem_aniversario = f"""
{saudacao_completa}

🎉 Venho hoje lhe desejar um feliz aniversário! 🎂

Que seu dia seja repleto de alegria, amor e muitas surpresas boas. Desejo a você um ano cheio de saúde, felicidade e realizações. Que todos os seus sonhos se tornem realidade!

Aproveite seu dia ao máximo!
                """
                enviar_mensagem(mensagem_aniversario, telefone)
    else:
        print("Nenhum aniversariante hoje.")


if __name__ == "__main__":
    # Verifica o dia da semana (0 = segunda-feira, 6 = domingo)
    dia_da_semana = datetime.now().weekday()
    
    # Envia alerta semanal apenas na segunda-feira
    if dia_da_semana == 0:
        enviar_alerta_semanal()
    
    # Envia alerta diário todos os dias
    enviar_alerta_diario()
