from contextlib import contextmanager
import os
from typing import Generator
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("ALERTADF_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("ALERTADF_DB_PORT", "3306")),
    "user": os.getenv("ALERTADF_DB_USER", "root"),
    "password": os.getenv("ALERTADF_DB_PASSWORD", ""),
    "database": os.getenv("ALERTADF_DB_NAME", "sistemaOcorrencias"),
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
    "autocommit": False,
}


def get_db_connection() -> MySQLConnection:
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as err:
        raise ConnectionError(f"Erro ao conectar ao banco de dados MySQL: {err}") from err


@contextmanager
def get_db_cursor(dictionary: bool = True, commit: bool = False) -> Generator:
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=dictionary)
    try:
        yield cursor
        if commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def testar_conexao() -> bool:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT DATABASE() AS banco_ativo;")
        resultado = cursor.fetchone()
        return bool(resultado and resultado.get("banco_ativo"))

