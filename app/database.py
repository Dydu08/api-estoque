import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def init_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        with open("sql/schema.sql", "r", encoding="utf-8") as f:
            schema_script = f.read()

        for comando in schema_script.split(";"):
            comando = comando.strip()
            if comando:
                cursor.execute(comando)

        conn.commit()
        cursor.close()
        conn.close()
        print("Banco de dados e tabelas inicializados com sucesso!")
    except Exception as erro:
        print(f"Erro ao inicializar o banco de dados: {erro}")


def connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as erro:
        print(f"Erro na conexão com o MySQL: {erro}")
        return None


if __name__ == "__main__":
    init_db()

    conn = connection()
    if conn and conn.is_connected():
        print("Conexão com o MySQL realizada com sucesso!")
        conn.close()
    else:
        print("Falha ao conectar no banco de dados.")