"""Módulo principal da API REST de ocorrências usando Flask e MySQL."""
from flask import Flask, jsonify, redirect
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "SenhaForte123!",
    "database": "sistemaOcorrencias",
}


@app.route("/")
def inicio():
    """Redireciona a raiz diretamente para o endpoint de ocorrências."""
    return redirect("/api/occurrences")

def obter_conexao():
    """Cria e retorna uma conexão ativa com o banco MySQL."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/api/occurrences", methods=["GET"])
def listar_ocorrencias():
    """Consulta ocorrências no MySQL e retorna no formato JSON padronizado."""
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)

        # Se suas colunas no MySQL estiverem em português, troque apenas o lado esquerdo do AS:
        # Ex: titulo AS type, descricao AS description, DATE_FORMAT(data_ocorrencia, '%Y-%m-%d') AS date
        
        cursor.execute("SELECT * FROM Ocorrencia")
        ocorrencias = cursor.fetchall()

        return jsonify(ocorrencias), 200

    except Error as erro:
        return jsonify({"erro": f"Falha ao consultar o banco: {erro}"}), 500

    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    app.run(debug=True, port=8000)