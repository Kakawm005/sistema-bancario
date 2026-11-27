import sqlite3
from contextlib import closing, contextmanager

ARQUIVO_BANCO = "banco.db"


@contextmanager
def conectar():
    with closing(sqlite3.connect(ARQUIVO_BANCO)) as conexao:
        conexao.execute("PRAGMA foreign_keys = ON")
        with conexao:
            yield conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS Conta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                num_conta TEXT NOT NULL,
                num_agencia TEXT NOT NULL,
                saldo REAL NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS Extratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                tipo_transacao TEXT NOT NULL,
                valor REAL NOT NULL,
                conta_destino INTEGER,
                conta_id INTEGER NOT NULL,
                FOREIGN KEY (conta_id) REFERENCES Conta(id)
            );
        """)


if __name__ == "__main__":
    inicializar_banco()
