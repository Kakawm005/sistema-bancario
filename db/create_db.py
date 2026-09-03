import sqlite3

conexao = sqlite3.connect("banco.db")

cursor = conexao.cursor()

conexao.execute("PRAGMA foreign_keys = ON")


cursor.execute("""
    CREATE TABLE Conta (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome CHAR NOT NULL,
        senha TEXT NOT NULL,
        num_conta TEXT NOT NULL,
        num_agencia TEXT NOT NULL,
        saldo REAL DEFAULT 0
    );
""")
    
cursor.execute("""
    CREATE TABLE Extratos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_hora TEXT NOT NULL,
        tipo_transacao TEXT NOT NULL,
        valor REAL DEFAULT 0 NOT NULL,
        conta_destino id,
        conta_id INTEGER,
        FOREIGN KEY (conta_id) REFERENCES Conta(id)
    );


""")

conexao.commit()
conexao.close()