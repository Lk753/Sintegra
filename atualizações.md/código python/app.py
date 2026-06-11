import os
import socket
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector
# IMPORTAÇÃO NOVA: Recursos de segurança para senhas
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- CONFIGURAÇÕES DO SISTEMA ---
TOKEN_SECRETO = "arduinoplayboyzin"

DB_CONFIG = {
    "host": "localhost",
    "user": "miria_admin",                  
    "password": "mir0s@r0dr1",  
    "database": "sintegra"           
}

# --- CONEXÃO GOOGLE SHEETS AUTOMÁTICA ---
try:
    pasta = os.path.dirname(os.path.abspath(__file__))
    nome_base = "projetotemperaturaesp-496412-25244b1f0c91"
    json_path = os.path.join(pasta, f"{nome_base}.json")
    if not os.path.exists(json_path):
        json_path = os.path.join(pasta, nome_base)
        
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    planilha = gspread.authorize(creds).open("TemperaturaESP")
    
    sheet_dados = planilha.sheet1
    sheet_logs = planilha.worksheet("Logs")
    print("✅ Google Sheets conectado com sucesso!")
except Exception as e:
    sheet_dados = sheet_logs = None
    print(f"❌ Erro Google Sheets: {e}")

# --- FUNÇÃO AUXILIAR DE LOGS (GOOGLE SHEETS) ---
def salvar_log_sheets(tipo, origem, descricao):
    if sheet_logs:
        try:
            agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet_logs.append_row([agora, tipo, origem, descricao])
        except Exception as e:
            print(f"⚠️ Erro ao salvar log no Sheets: {e}")

# --- FUNÇÃO DO BANCO DE DADOS ---
def executar_sql(query, valores=()):
    try:
        with mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        ) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, valores)
            conn.commit()  
    except Exception as e:
        print(f"❌ ERRO NO BANCO DE DADOS MYSQL: {e}")
        print(f"🔍 QUERY TENTADA: {query}")
        print(f"📦 VALORES ENVIADOS: {valores}\n")

# ==========================================
#          ROTAS DAS PÁGINAS (HTML)
# ==========================================

@app.route('/')
@app.route('/login')
def renderizar_painel():
    return render_template('login.html')

# ==========================================
#         ROTAS DA API DO DASHBOARD
# ==========================================

# 1. ROTA DE CADASTRO (Criptografando a senha antes de salvar)
@app.route('/api/cadastro', methods=['POST'])
def api_cadastro():
    try:
        dados = request.get_json()
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')

        if not nome or not email or not senha:
            return jsonify({"erro": "Preencha todos os campos!"}), 400

        # Gerando o hash seguro da senha recebida
        senha_criptografada = generate_password_hash(senha)

        # Salvando o hash gerado no campo 'senha' do banco de dados
        query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        executar_sql(query, (nome, email, senha_criptografada))
        
        print(f"👤 [CADASTRO] Novo usuário registrado com senha criptografada: {nome}")
        return jsonify({"mensagem": "Usuário registrado com sucesso!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# 2. ROTA DE LOGIN (Validando a senha criptografada)
@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        # Buscamos os dados filtrando apenas pelo e-mail informado
        query = "SELECT nome, senha FROM usuarios WHERE email = %s"
        
        with mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"]
        ) as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, (email,))
                usuario = cursor.fetchone()

        # check_password_hash compara a senha digitada com o hash salvo no banco
        if usuario and check_password_hash(usuario['senha'], senha):
            print(f"🔓 [LOGIN] Usuário {usuario['nome']} autenticado com sucesso.")
            return jsonify({"usuario": usuario['nome']}), 200
        else:
            return jsonify({"erro": "E-mail ou senha incorretos no Banco de Dados."}), 401
    except Exception as e:
        print(f"❌ ERRO CRÍTICO NA API DE LOGIN: {e}")
        return jsonify({"erro": str(e)}), 500

# 3. ROTA DE TEMPO REAL
@app.route('/api/telemetria/atual')
def api_telemetria_atual():
    try:
        if sheet_dados:
            todas_linhas = sheet_dados.get_all_values()
            if len(todas_linhas) > 1:
                ultima = todas_linhas[-1]
                return jsonify({
                    "temperatura": float(ultima[1].replace(',', '.')),
                    "umidade": float(ultima[3].replace(',', '.')),
                    "rpm": int(ultima[4])
                })
        return jsonify({"temperatura": 0.0, "umidade": 0.0, "rpm": 0})
    except Exception:
        return jsonify({"temperatura": 0.0, "umidade": 0.0, "rpm": 0})

# 4. ROTA DE HISTÓRICO
@app.route('/api/telemetria/historico')
def api_telemetria_historico():
    try:
        lista_final = []
        if sheet_dados:
            todas_linhas = sheet_dados.get_all_values()
            linhas_dados = todas_linhas[1:]
            
            if len(linhas_dados) > 10:
                ultimas_leituras = linhas_dados[-10:]
            else:
                ultimas_leituras = linhas_dados
            
            for table_row in reversed(ultimas_leituras):
                lista_final.append({
                    "data_hora": table_row[2],
                    "temperatura": table_row[1],
                    "umidade": table_row[3],
                    "rpm": table_row[4]
                })
        return jsonify(lista_final)
    except Exception:
        return jsonify([])

# ==========================================
#          ROTA DE RECEBIMENTO DO ARDUINO
# ==========================================

@app.route('/temperatura', methods=['GET', 'POST'])
def receber():
    ip = request.remote_addr
    
    if request.is_json:
        dados_json = request.get_json() or {}
        token = dados_json.get('token')
        sensor = dados_json.get('sensor')
        temp_raw = dados_json.get('temperatura')
        umid_raw = dados_json.get('umidade', '0')
        rot_raw = dados_json.get('rotacao', '0')
    else:
        token = request.args.get('token') or request.form.get('token')
        sensor = request.args.get('sensor') or request.form.get('sensor')
        temp_raw = request.args.get('temperatura') or request.form.get('temperatura')
        umid_raw = request.args.get('umidade') or request.form.get('umidade') or '0'
        rot_raw = request.args.get('rotacao') or request.form.get('rotacao') or '0'
    
    agora_sheets = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    agora_mysql = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if token != TOKEN_SECRETO:
        msg = f"Tentativa nao autorizada do IP: {ip}"
        print(f"⚠️ [ALERTA] {msg}")
        salvar_log_sheets("ALERTA", "API_SEGURANCA", msg)
        
        query_falha = "INSERT INTO falhas (Horario, origem, erro_descricao) VALUES (%s, %s, %s)"
        executar_sql(query_falha, (agora_mysql, "API_SEGURANCA", msg))
        return jsonify({"status": "ERRO", "mensagem": "Nao autorizado"}), 401

    if sensor == "ESP8266_SISTEMA":
        desc = "Dispositivo conectado na rede via BOTAO1"
        print(f"🔄 [SISTEMA] {desc}")
        salvar_log_sheets("SISTEMA", sensor, desc)
        
        query_manutencao = "INSERT INTO manutencao (horario, equipamento, descricao, tecnico) VALUES (%s, %s, %s, %s)"
        executar_sql(query_manutencao, (agora_mysql, sensor, desc, "SISTEMA_AUTO"))
        return "Boot Registrado", 200

    if not sensor or temp_raw is None or str(temp_raw).lower() == "nan":
        msg = f"Parametros invalidos vindos do IP: {ip}. Sensor: {sensor}, Temp: {temp_raw}"
        print(f"⚠️ [VALIDACAO] {msg}")
        salvar_log_sheets("ERRO", "API_VALIDACAO", msg)
        
        query_falha = "INSERT INTO falhas (Horario, origem, erro_descricao) VALUES (%s, %s, %s)"
        executar_sql(query_falha, (agora_mysql, "API_VALIDACAO", msg))
        return jsonify({"status": "ERRO", "mensagem": "Parametros invalidos"}), 400

    try:
        temp = float(str(temp_raw).replace(',', '.'))
        umid = float(str(umid_raw).replace(',', '.'))
        rot = int(float(str(rot_raw)))
        
        print(f"📡 {sensor} | Temp: {temp}°C | Umid: {umid}% | Rotacao (A0): {rot} | {agora_sheets}")

        if sheet_dados:
            sheet_dados.append_row([sensor, temp, agora_sheets, umid, rot])

        query_acessos = "INSERT INTO acessos (horario, sensor, temperatura, ip_origem) VALUES (%s, %s, %s, %s)"
        executar_sql(query_acessos, (agora_mysql, sensor, temp, ip))

        if temp > 35.0:
            msg_critica = "Superaquecimento Detectado! Limite de 35C excedido."
            print(f"🚨 [CRÍTICO] {sensor} atingiu {temp}°C!")
            salvar_log_sheets("CRITICO", sensor, f"{msg_critica} Atual: {temp}°C")
            
            query_critico = "INSERT INTO eventos_criticos (horario, sensor, temperatura, descricao) VALUES (%s, %s, %s, %s)"
            executar_sql(query_critico, (agora_mysql, sensor, temp, msg_critica))

        return "OK", 200

    except Exception as erro:
        msg_erro = f"Erro geral no processamento do sensor: {erro}"
        print(f"❌ {msg_erro}")
        
        query_falha_ex = "INSERT INTO falhas (Horario, origem, erro_descricao) VALUES (%s, %s, %s)"
        executar_sql(query_falha_ex, (agora_mysql, "API_EXCEPTION", msg_erro))
        return "ERRO INTERNAL SERVER", 500

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_computador = s.getsockname()[0]
        s.close()
    except Exception:
        ip_computador = "localhost"

    print("\n" + "="*70)
    print("🚀 SERVIDOR IoT COMPLETO E CONFIGURADO!")
    print(f"🔗 Painel Web Local: http://localhost:8000/")
    print(f"📡 IP para colocar no código do Arduino: {ip_computador}")
    print("="*70 + "\n")

    app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)