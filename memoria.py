# memoria.py
import sqlite3
from datetime import datetime

DB = "memoria.db"

def inicializar_banco():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telefone TEXT,
                mensagem_usuario TEXT,
                resposta_ia TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def salvar_interacao(telefone, mensagem_usuario, resposta_ia):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO historico (telefone, mensagem_usuario, resposta_ia)
            VALUES (?, ?, ?)
        ''', (telefone, mensagem_usuario, resposta_ia))
        conn.commit()

def recuperar_historico(telefone, limite=10):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT mensagem_usuario, resposta_ia FROM historico
            WHERE telefone = ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (telefone, limite))
        return c.fetchall()
