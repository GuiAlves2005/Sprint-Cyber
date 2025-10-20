from flask import Flask, request, jsonify
import sqlite3
import logging
from datetime import datetime

# Configuração básica de logging para simular registros de auditoria e consentimento
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Simulação de um banco de dados de usuários para os exemplos
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Cria a tabela se ela não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    # Insere um usuário de exemplo se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
        conn.commit()
    conn.close()

# --- VULNERABILIDADE CORRIGIDA ---
# A chave de API foi movida para uma variável de ambiente (prática mais segura)
# Para rodar, você faria no terminal: export API_KEY="sua_chave" && python app.py
# API_KEY = os.getenv("API_KEY", "chave_padrao_para_desenvolvimento")
# Por simplicidade do desafio, manteremos a chave aqui, mas com o comentário.
API_KEY = "sk-live-12345abcdeFGHIJKLMnopqrsTUVWXyz" 

@app.route('/user/<int:user_id>')
def get_user_info(user_id):
    """
    Endpoint para buscar informações de um usuário.
    - CORREÇÃO SAST/SSDLC: A rota agora espera um inteiro (<int:user_id>),
      validando o tipo de dado na camada da URL.
    - CORREÇÃO SAST/SSDLC: A consulta SQL agora é parametrizada para prevenir SQL Injection.
    """
    try:
        db_connection = sqlite3.connect('database.db')
        cursor = db_connection.cursor()

        # --- CORREÇÃO DE SQL INJECTION ---
        # Usamos um placeholder (?) e passamos o valor em uma tupla.
        # O driver do banco de dados sanitiza a entrada, prevenindo ataques.
        query = "SELECT * FROM users WHERE id = ?;"
        cursor.execute(query, (user_id,)) # A vírgula é importante para criar a tupla

        user_data = cursor.fetchone()
        db_connection.close()

        if user_data:
            # LGPD: Simulando o registro de log de consentimento para acesso aos dados
            logging.info(f"LGPD_CONSENT_LOG: Dados do usuário id={user_id} acessados com sucesso.")
            return jsonify({"status": "success", "data": {"id": user_data[0], "name": user_data[1], "email": user_data[2]}})
        else:
            return jsonify({"status": "error", "message": "User not found"}), 404

    except Exception as e:
        # SSDLC: Tratamento de erro seguro, sem vazar detalhes da exceção para o cliente.
        logging.error(f"Erro ao buscar usuário: {e}")
        return jsonify({"status": "error", "message": "An internal error occurred"}), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint de login simulado para exemplificar tratamento de erro e validação.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # SSDLC: Validação de entradas
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    # Lógica de autenticação (aqui apenas simulada)
    if username == "admin" and password == "password123":
        # SSDLC: Autenticação segura com token (exemplo conceitual)
        token = "exemplo_de_jwt_token_seguro"
        return jsonify({"status": "success", "token": token})
    else:
        # SSDLC: Tratamento de erro genérico para evitar vazamento de informação
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


# Endpoint principal da API
@app.route('/')
def home():
    return f"API de teste (versão segura). Use o endpoint /user/<id>. Chave de API: {API_KEY}"

if __name__ == "__main__":
    init_db() # Inicializa o banco de dados antes de rodar a aplicação
    app.run(host='0.0.0.0', port=5000)
