import os
import sqlite3

# --- VULNERABILIDADE 1: Senha "Hardcoded" ---
# Senhas, chaves de API e outros segredos nunca devem ser colocados diretamente no código.
# Semgrep irá detectar isso como um risco de segurança.
API_KEY = "sk-live-12345abcdeFGHIJKLMnopqrsTUVWXyz" 

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Função de login (apenas para exemplo)
def login(user):
    print(f"Usuário {user.username} logado com a chave: {API_KEY}")

# --- VULNERABILIDADE 2: Injeção de SQL (SQL Injection) ---
# A função abaixo constrói uma consulta SQL diretamente com a entrada do usuário.
# Um invasor poderia manipular o 'user_id' para roubar ou apagar dados.
# Por exemplo, se user_id for "123 OR 1=1", a consulta pode retornar todos os usuários.
def get_user_info(db_connection, user_id):
    # FORMA VULNERÁVEL:
    query = "SELECT * FROM users WHERE id = '" + user_id + "';"
    
    print(f"Executando consulta perigosa: {query}")
    
    cursor = db_connection.cursor()
    # A linha abaixo é onde a vulnerabilidade é executada.
    cursor.execute(query) 
    
    return cursor.fetchone()

# Função principal para simular a execução
def main():
    print("Iniciando a aplicação de teste...")
    
    # Simula o login
    test_user = User("admin", "password123")
    login(test_user)
    
    # Simula a conexão com um banco de dados em memória
    conn = sqlite3.connect(':memory:')
    
    # Simula uma busca vulnerável no banco de dados
    print("\nTestando a busca de usuário vulnerável:")
    get_user_info(conn, "105") # Busca normal
    get_user_info(conn, "105' OR '1'='1") # Simula um ataque de SQL Injection

if __name__ == "__main__":
    main()
