import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

raiz = Path(__file__).resolve().parent.parent
caminho_schema = raiz / "sql" / "schema.sql"

def init_db():
    conn = None
    cursor = None
    
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = conn.cursor()

        with open(caminho_schema, "r", encoding="utf-8") as f:
            schema_script = f.read()

        for comando in schema_script.split(";"):
            comando = comando.strip()
            if comando:
                cursor.execute(comando)

        conn.commit()
        print("Banco de dados e tabelas inicializados com sucesso!")

    except mysql.connector.Error as erro:
        print(f"Erro ao inicializar o banco de dados: {erro}")
        
    except FileNotFoundError as erro:
        print(f"Erro ao encontrar o script do banco de dados: {erro}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


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


def criar_categoria(nome, descricao=None):
    conn = None
    cursor = None

    try:
        conn = connection()
        if conn is None:
            return None

        cursor = conn.cursor()
        sql = "INSERT INTO categorias (nome, descricao) VALUES (%s, %s)"
        cursor.execute(sql, (nome, descricao))
        conn.commit()
        return cursor.lastrowid

    except mysql.connector.Error as erro:
        print(f"Erro ao criar a categoria: {erro}")
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def criar_produto(nome, preco, quantidade, categoria_id, descricao=None):
    conn = None
    cursor = None

    try:
        conn = connection()
        if conn is None:
            return None

        cursor = conn.cursor()  
        sql = "INSERT INTO produtos(nome, descricao, preco, quantidade, categoria_id) VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, descricao, preco, quantidade, categoria_id))
        conn.commit()
        return cursor.lastrowid
    
    except mysql.connector.Error as erro:
        print(f"Erro ao criar o produto: {erro}")
        return None
    
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def listar_categorias():
    conn = None
    cursor = None

    try:
        conn = connection()
        if conn is None:
            return None
        
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT id, nome, descricao FROM categorias"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        return resultado

    except mysql.connector.Error as erro:
        print(f"Erro ao listar as categorias: {erro}")
        return None

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    init_db()
