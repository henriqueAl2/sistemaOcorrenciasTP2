"""Flask application for the occurrence API and admin/report pages."""

from __future__ import annotations

import math
import os
import secrets

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, session, url_for
from mysql.connector import Error

if __package__:
    from .admin_reports import register_admin_reports
    from .database import get_db_connection
else:
    from admin_reports import register_admin_reports
    from database import get_db_connection


load_dotenv()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.getenv("ALERTADF_SECRET_KEY") or secrets.token_hex(32),
    ADMIN_PASSWORD_HASH=os.getenv("ALERTADF_ADMIN_PASSWORD_HASH", ""),
    DB_HOST=os.getenv("ALERTADF_DB_HOST", "127.0.0.1"),
    DB_PORT=int(os.getenv("ALERTADF_DB_PORT", "3306")),
    DB_NAME=os.getenv("ALERTADF_DB_NAME", "sistemaOcorrencias"),
    DB_USER=os.getenv("ALERTADF_DB_USER", "root"),
    DB_PASSWORD=os.getenv("ALERTADF_DB_PASSWORD", ""),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)
register_admin_reports(app, register_home=False)


@app.route("/")
def inicio():
    """Abre o painel de relatórios depois do login administrativo."""
    endpoint = "reports.index" if session.get("is_admin") else "login"
    return redirect(url_for(endpoint))


def obter_conexao():
    """Cria e retorna uma conexão ativa com o banco MySQL."""
    return get_db_connection()


def _coordenada_numerica(valor, minimo, maximo):
    """Converte as coordenadas armazenadas como texto para números do mapa."""
    try:
        coordenada = float(valor)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(coordenada) or not minimo <= coordenada <= maximo:
        return None
    return coordenada


@app.route("/api/occurrences", methods=["GET"])
def listar_ocorrencias():
    """Retorna os campos necessários para o mapa, sem expor dados do usuário."""
    conexao = None
    cursor = None
    try:
        conexao = obter_conexao()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            """SELECT CONCAT(o.idOcorrencia, ':', o.tipoOcorrencia_idtipoOcorrencia) AS id,
                      t.nome AS type,
                      o.descricao AS description,
                      DATE_FORMAT(COALESCE(o.hora, TIMESTAMP(o.data)), '%Y-%m-%dT%H:%i:%s') AS date,
                      l.latitude AS latitude,
                      l.longitude AS longitude
               FROM Ocorrencia o
               JOIN tipoOcorrencia t
                 ON t.idtipoOcorrencia = o.tipoOcorrencia_idtipoOcorrencia
               JOIN Local l ON l.codigo = o.Local_codigo
               ORDER BY COALESCE(o.hora, TIMESTAMP(o.data)) DESC, o.idOcorrencia DESC"""
        )
        ocorrencias = cursor.fetchall()
        for ocorrencia in ocorrencias:
            ocorrencia["latitude"] = _coordenada_numerica(ocorrencia["latitude"], -90, 90)
            ocorrencia["longitude"] = _coordenada_numerica(ocorrencia["longitude"], -180, 180)
        return jsonify(ocorrencias), 200
    except (Error, ConnectionError):
        app.logger.exception("Falha ao consultar as ocorrências.")
        return jsonify({"erro": "Falha ao consultar o banco de dados."}), 503
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8000")),
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
