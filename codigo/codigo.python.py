from datetime import datetime
from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector

app = Flask(__name__)

# --- CONFIGURAÇÕES ---
TOKEN_SECRETO = "arduinoplayboyzin"
JSON_CREDENCIAIS = r"C:\Users\Aluno\Desktop\aula\projetotemperaturaesp-496412-776646a75384.json"

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # Coloque a sua senha do MySQL aqui
    'database': 'sintegra'
}

# --- CONEXÃO GOOGLE SHEETS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
sheet_dados = None
sheet_logs = None

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(JSON_CREDENCIAIS, scope)
    client = gspread.authorize(creds)
    planilha = client.open("TemperaturaESP")
    sheet_dados = planilha.sheet1
    sheet_logs = planilha.worksheet("Logs")
    print("✅ Google Sheets conectado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar no Google: {e}")

# --- FUNÇÕES AUXILIARES (BANCO E NUVEM) ---
def salvar_log_sheets(tipo, origem, descricao):
    """Grava uma linha na aba de Logs do Google Sheets."""
    try:
        if sheet_logs:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet_logs.append_row([agora, tipo, origem, descricao])
    except Exception as e:
        print(f"💥 Erro Sheets: {e}")

def executar_sql(query, valores=()):
    """Executa qualquer comando INSERT/UPDATE no MySQL de forma segura e limpa."""
    try:
        with mysql.connector.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, valores)
            conn.commit()
    except Exception as e:
        print(f"❌ Erro no MySQL: {e}")

# --- ROTAS ---
@app.route('/')
def home():
    return "API Híbrida Ativa na Porta 8000"

@app.route('/temperatura')
def receber():
    ip_cliente = request.remote_addr
    token_recebido = request.args.get('token')
    sensor = request.args.get('sensor')
    temperatura = request.args.get('temperatura')
    agora_sheets = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # 1. VALIDAÇÃO DE SEGURANÇA
    if token_recebido != TOKEN_SECRETO:
        msg = f"Tentativa não autorizada vinda do IP: {ip_cliente}"
        print(f"⚠️ [ALERTA] {msg}")
        salvar_log_sheets("ALERTA", "API_SEGURANCA", msg)
        executar_sql("INSERT INTO falhas (origem, erro_descricao) VALUES (%s, %s)", ("API_SEGURANCA", msg))
        return jsonify({"status": "ERRO", "mensagem": "Não autorizado"}), 401

    # 2. VALIDAÇÃO DE PARÂMETROS
    if not sensor or not temperatura:
        msg_valida = f"Dados incompletos do IP {ip_cliente}"
        print(f"⚠️ [VALIDAÇÃO] {msg_valida}")
        salvar_log_sheets("ERRO", "API_VALIDACAO", msg_valida)
        executar_sql("INSERT INTO falhas (origem, erro_descricao) VALUES (%s, %s)", ("API_VALIDACAO", msg_valida))
        return jsonify({"status": "ERRO", "mensagem": "Parâmetros ausentes"}), 400

    # 3. LOG DE REINICIALIZAÇÃO DO HARDWARE (BOOT)
    if sensor == "ESP8266_SISTEMA":
        print("🔄 [SISTEMA] O módulo ESP8266 foi reinicializado.")
        salvar_log_sheets("SISTEMA", sensor, "Dispositivo reinicializado")
        executar_sql("INSERT INTO manutencao (dispositivo) VALUES (%s)", (sensor,))
        return "Boot Registrado", 200

    # 4. PROCESSAMENTO E GRAVAÇÃO DE LEITURA NORMAL
    try:
        temp_float = float(temperatura)
        print(f"📡 {sensor} | {temp_float}°C")

        # Salvar no Google Sheets (Aba Principal)
        if sheet_dados:
            sheet_dados.append_row([sensor, temperatura, agora_sheets])

        # Salvar no MySQL (Tabela de acessos)
        executar_sql(
            "INSERT INTO acessos (sensor, temperatura, ip_origem) VALUES (%s, %s, %s)",
            (sensor, temp_float, ip_cliente)
        )

        # Verificação de Alerta Crítico por Superaquecimento
        if temp_float > 35.0:
            salvar_log_sheets("CRÍTICO", sensor, f"Superaquecimento! {temp_float}°C")
            executar_sql("INSERT INTO eventos_criticos (sensor, temperatura_critica) VALUES (%s, %s)", (sensor, temp_float))
        else:
            salvar_log_sheets("INFO", sensor, f"Leitura estável: {temp_float}°C")

        return "OK", 200

    except Exception as erro:
        msg_falha = f"Falha ao processar dados do sensor {sensor}: {erro}"
        print(f"❌ {msg_falha}")
        salvar_log_sheets("ERRO", "SISTEMA", msg_falha)
        executar_sql("INSERT INTO falhas (origem, erro_descricao) VALUES (%s, %s)", ("SISTEMA", msg_falha[:250]))
        return "ERRO", 500

if __name__ == '__main__':
    # '0.0.0.0' permite conexões locais (localhost) e externas (IP da rede do SENAI)
    app.run(host='0.0.0.0', port=8000, debug=True)



 