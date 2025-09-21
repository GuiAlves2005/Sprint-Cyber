from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

API_KEY = "sk-live-12345abcdeFGHIJKLMnopqrsTUVWXyz" 

# Cria um endpoint /user/<user_id> que é vulnerável a DAST e SAST
@app.route('/user/<user_id>')
def get_user_info(user_id):
    try:
        # Conexão com um banco de dados em memória
        db_connection = sqlite3.connect(':memory:')
        cursor = db_connection.cursor()

        # Consulta vulnerável 
        query = "SELECT * FROM users WHERE id = '" + user_id + "';"
        cursor.execute(query) 

        user_data = cursor.fetchone()
        db_connection.close()

        if user_data:
            return jsonify({"status": "success", "data": user_data})
        else:
            # Usa um status code correto para "Não Encontrado"
            return jsonify({"status": "error", "message": "User not found"}), 404

    except Exception as e:
        # Retorna um erro 500 caso algo dê errado
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint principal da API
@app.route('/')
def home():
    return f"API de teste vulnerável. Use o endpoint /user/<id>. Chave de API: {API_KEY}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
