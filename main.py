from db.create_db import inicializar_banco
from db.query import Main


if __name__ == "__main__":
    try:
        inicializar_banco()
        Main()
    except (EOFError, KeyboardInterrupt):
        print("\nPrograma encerrado.")
