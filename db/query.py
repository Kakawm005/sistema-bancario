import hashlib
import hmac
import re
import secrets
import sys
from datetime import datetime
from decimal import Decimal
from getpass import getpass

from db.create_db import conectar

ITERACOES_SENHA = 600_000
SALDO_MAXIMO = 999_999_999_999.99


def Main():
    while True:
        print("\nSistema Bancário\n1. Criar conta\n2. Entrar\n3. Sair")
        resposta = input("Opção: ").strip()
        if resposta == "1":
            CriarConta()
        elif resposta == "2":
            conta_id = EntrarConta()
            if conta_id is not None and Home(conta_id) == "stop":
                return
        elif resposta == "3":
            return
        else:
            print("Opção inválida.")


def Home(conta_id):
    while True:
        print(
            "\nMinha conta\n1. Consultar saldo\n2. Consultar extrato"
            "\n3. Sacar\n4. Depositar\n0. Voltar ao menu inicial\n12. Sair"
        )
        resposta = input("Opção: ").strip()
        if resposta == "1":
            ConsultarSaldo(conta_id)
        elif resposta == "2":
            ConsultarExtrato(conta_id)
        elif resposta == "3":
            Saque(conta_id)
        elif resposta == "4":
            Deposito(conta_id)
        elif resposta == "0":
            return
        elif resposta == "12":
            return "stop"
        else:
            print("Opção inválida.")


def ler_senha():
    if sys.stdin.isatty():
        return getpass("Senha: ")
    return input("Senha: ")


def codificar_senha(senha, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    hash_senha = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), bytes.fromhex(salt), ITERACOES_SENHA
    )
    return f"pbkdf2_sha256${salt}${hash_senha.hex()}"


def CriarConta():
    nome = input("Nome: ").strip()
    senha = ler_senha()
    num_conta = input("Número da conta: ").strip()
    num_agencia = input("Número da agência: ").strip()
    if not all((nome, senha.strip(), num_conta, num_agencia)):
        print("Preencha todos os campos.")
        return

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            INSERT INTO Conta (nome, senha, num_conta, num_agencia)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM Conta WHERE num_conta = ?)
            """,
            (nome, codificar_senha(senha), num_conta, num_agencia, num_conta),
        )
    if cursor.rowcount == 0:
        print("Já existe uma conta com esse número.")
        return
    print("Conta criada com sucesso.")


def EntrarConta():
    num_conta = input("Número da conta: ").strip()
    senha = ler_senha()
    with conectar() as conexao:
        contas = conexao.execute(
            "SELECT id, nome, senha FROM Conta WHERE num_conta = ? ORDER BY id",
            (num_conta,),
        ).fetchall()
        for conta_id, nome, senha_salva in contas:
            hash_salvo = re.fullmatch(r"pbkdf2_sha256\$([0-9a-f]{32})\$[0-9a-f]{64}", senha_salva)
            if hash_salvo:
                senha_digitada = codificar_senha(senha, hash_salvo[1])
            else:
                senha_digitada = senha
            if not hmac.compare_digest(senha_digitada.encode("utf-8"), senha_salva.encode("utf-8")):
                continue
            if not hash_salvo:
                conexao.execute(
                    "UPDATE Conta SET senha = ? WHERE id = ? AND senha = ?",
                    (codificar_senha(senha), conta_id, senha_salva),
                )
            print(f"Bem-vindo, {nome}!")
            return conta_id

    print("Conta ou senha inválida.")
    return None


def formatar_valor(valor):
    return f"R$ {valor:.2f}".replace(".", ",")


def ConsultarSaldo(conta_id):
    with conectar() as conexao:
        saldo, = conexao.execute("SELECT saldo FROM Conta WHERE id = ?", (conta_id,)).fetchone()
    print(f"Saldo: {formatar_valor(saldo)}")
    return saldo


def ler_valor(prompt):
    entrada = input(prompt).strip()
    if re.fullmatch(r"[0-9]+(?:[.,][0-9]{1,2})?", entrada):
        valor = Decimal(entrada.replace(",", "."))
        if 0 < valor <= Decimal(str(SALDO_MAXIMO)):
            return float(valor)
    print("Informe um valor positivo com até duas casas decimais dentro do limite da conta.")
    return None


def CriarExtrato(conexao, tipo_transacao, valor, conta_id):
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conexao.execute(
        "INSERT INTO Extratos (data_hora, tipo_transacao, valor, conta_id) VALUES (?, ?, ?, ?)",
        (data_hora, tipo_transacao, valor, conta_id),
    )


def Saque(conta_id):
    valor = ler_valor("Valor do saque: ")
    if valor is None:
        return
    with conectar() as conexao:
        cursor = conexao.execute(
            "UPDATE Conta SET saldo = ROUND(saldo - ?, 2) WHERE id = ? AND saldo >= ?",
            (valor, conta_id, valor),
        )
        if cursor.rowcount == 0:
            print("Saldo insuficiente.")
            return
        CriarExtrato(conexao, "Saque", valor, conta_id)
    print("Saque realizado com sucesso.")


def Deposito(conta_id):
    valor = ler_valor("Valor do depósito: ")
    if valor is None:
        return
    with conectar() as conexao:
        cursor = conexao.execute(
            "UPDATE Conta SET saldo = ROUND(saldo + ?, 2) WHERE id = ? AND ROUND(saldo + ?, 2) <= ?",
            (valor, conta_id, valor, SALDO_MAXIMO),
        )
        if cursor.rowcount == 0:
            print(f"O saldo ultrapassaria o limite de {formatar_valor(SALDO_MAXIMO)}.")
            return
        CriarExtrato(conexao, "Depósito", valor, conta_id)
    print("Depósito realizado com sucesso.")


def ConsultarExtrato(conta_id):
    with conectar() as conexao:
        transacoes = conexao.execute(
            """
            SELECT data_hora, tipo_transacao, valor FROM Extratos
            WHERE conta_id = ? ORDER BY id DESC
            """,
            (conta_id,),
        ).fetchall()
    if not transacoes:
        print("Nenhuma movimentação no extrato.")
    for data_hora, tipo, valor in transacoes:
        print(f"{data_hora} | {tipo} | {formatar_valor(valor)}")
    return transacoes
