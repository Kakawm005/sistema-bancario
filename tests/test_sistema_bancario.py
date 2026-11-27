import sqlite3
import subprocess
import sys
import unittest
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

MAIN = Path(__file__).resolve().parents[1] / "main.py"


class TestSistemaBancario(unittest.TestCase):
    def setUp(self):
        pasta = self.enterContext(TemporaryDirectory())
        self.pasta = Path(pasta)
        self.banco = self.pasta / "banco.db"

    def executar(self, *respostas):
        resultado = subprocess.run(
            [sys.executable, "-X", "utf8", str(MAIN)],
            cwd=self.pasta,
            input="\n".join(respostas) + "\n",
            capture_output=True,
            encoding="utf-8",
            timeout=15,
        )
        self.assertEqual(resultado.returncode, 0, resultado.stderr)
        return resultado.stdout

    def test_fluxo_com_duas_contas_e_persistencia(self):
        saida = self.executar(
            "9", "1", "Ana", "demo-ana", "101", "0001",
            "1", "Bruno", "demo-bruno", "102", "0001",
            "2", "101", "senha-errada", "2", "101", "demo-ana",
            "1", "2", "4", "100,50", "3", "30.25", "1", "2", "0",
            "2", "102", "demo-bruno", "1", "2", "12",
        )
        for mensagem in (
            "Opção inválida.",
            "Conta ou senha inválida.",
            "Saldo: R$ 70,25",
            "Depósito | R$ 100,50",
            "Saque | R$ 30,25",
        ):
            self.assertIn(mensagem, saida)
        self.assertEqual(saida.count("Saldo: R$ 0,00"), 2)
        self.assertEqual(saida.count("Nenhuma movimentação no extrato."), 2)

        saida = self.executar("2", "101", "demo-ana", "1", "2", "12")
        self.assertIn("Saldo: R$ 70,25", saida)
        self.assertLess(saida.index("Saque |"), saida.index("Depósito |"))

    def test_rejeita_duplicata_e_valores_invalidos(self):
        saida = self.executar(
            "1", "Ana", "demo", "101", "0001",
            "1", "Outra pessoa", "outra-senha", "101", "0002",
            "2", "101", "demo", "4", "10",
            "3", "11", "3", "-5", "4", "NaN", "4", "0", "4", "1,001", "1", "12",
        )
        self.assertIn("Já existe uma conta com esse número.", saida)
        self.assertIn("Saldo insuficiente.", saida)
        self.assertEqual(saida.count("Informe um valor positivo"), 4)
        self.assertIn("Saldo: R$ 10,00", saida)
        with closing(sqlite3.connect(self.banco)) as conexao:
            self.assertEqual(conexao.execute("SELECT COUNT(*) FROM Conta").fetchone(), (1,))
            self.assertEqual(conexao.execute("SELECT COUNT(*) FROM Extratos").fetchone(), (1,))

    def test_converte_senha_antiga_ao_entrar(self):
        self.executar("3")
        with closing(sqlite3.connect(self.banco)) as conexao, conexao:
            conexao.execute(
                "INSERT INTO Conta (nome, senha, num_conta, num_agencia, saldo) VALUES (?, ?, ?, ?, ?)",
                ("Conta antiga", "demonstração", "123", "0001", 42.50),
            )

        saida = self.executar("2", "123", "demonstração", "1", "12")
        self.assertIn("Saldo: R$ 42,50", saida)
        with closing(sqlite3.connect(self.banco)) as conexao:
            senha, = conexao.execute("SELECT senha FROM Conta").fetchone()
        self.assertTrue(senha.startswith("pbkdf2_sha256"))
        self.assertIn("Bem-vindo, Conta antiga!", self.executar("2", "123", "demonstração", "12"))
