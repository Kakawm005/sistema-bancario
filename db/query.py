import sqlite3
from time import sleep
import os
from datetime import datetime


def Main():
    while True:
        print('****************************')
        sleep(0.5)
        print('*****SELECIONE*UMA*OPÇÃO****')
        sleep(0.5)
        print('****************************')       
        print('****************************')
        sleep(0.5)
        print('*******1- *CRIAR*CONTA******')
        sleep(0.5)
        print('****************************')       
        print('****************************')
        sleep(0.5)
        print('*********2*-*ENTRAR*********')
        sleep(0.5)
        print('****************************')     
        print('****************************')
        sleep(0.5)
        print('**********3*-*SAIR**********')
        sleep(0.5)
        print('****************************')     
        resposta = str(input('R:'))  
        if resposta == "1":
            CriarConta()
        elif resposta == "2":
            id = EntrarConta()
        elif resposta == "3":
            break
        else:
            ErroMensager()

        if id:
            retorno = Home(id)
            if retorno == "stop":
                break


def Home(id):
    while True:
        print('****************************')
        sleep(0.3)
        print('****1*-*CONSULTAR*SALDO*****')
        sleep(0.3)
        print('****************************') 
        sleep(0.3) 
        print('****************************')
        sleep(0.3)
        print('***2*-*CONSULTAR*EXTRATO****')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('*********3*-*SAQUES*********')
        sleep(0.3)
        print('****************************')  
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('********4*-*DEPÓSITOS*******')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('*****5*-*TRANSFERÊNCIAS*****')
        sleep(0.3)
        print('****************************') 
        sleep(0.3) 
        print('****************************')
        sleep(0.3)
        print('*******6*-*PAGAMENTOS*******')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('**********7*-*PIX***********')
        sleep(0.3)
        print('****************************')  
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('******8*-*EMPRÉSTIMOS*******')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('*********9*-*CARTÕES********')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('***10*-*CONTA*E*SEGURANÇA***')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****************************')
        sleep(0.3)
        print('****11*-*OUTROS*SERVIÇOS****')
        sleep(0.3)
        print('****************************')
        print('****************************')
        sleep(0.3)
        print('*********12*-*SAIR**********')
        sleep(0.3)
        print('****************************')
        resposta = str(input("R:"))
        os.system("cls")
        if resposta == '1':
            ConsultarSaldo(id)
        elif resposta == '2':
            ConsultarExtrato(id)
        elif resposta == '3':
            Saque(id)
        elif resposta == '4':
            Deposito(id)
        elif resposta == '5':
            erro404()
        elif resposta == '6':
            erro404()
        elif resposta == '7':
            erro404()
        elif resposta == '8':
            erro404()
        elif resposta == '9':
            erro404()
        elif resposta == '10':
            erro404()
        elif resposta == '11':
            erro404()
        elif resposta == '12':
            return "stop"
        else:
            ErroMensager()
    
    

def erro404():
    print('****************************')
    sleep(0.5)
    print('ESSA*PÁGINA*NÃO*EXISTE*AINDA')
    sleep(0.5)
    print('****************************')
    return None


def ErroMensager():
    print('****************************')
    sleep(0.5)
    print('DIGITE*OS*DADOS*CORRETAMENTE')
    sleep(0.5)
    print('****************************')
    return None


def CriarConta():
    try:
        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        print('****************************')
        sleep(0.5)
        print('******DIGITE*O*SEU*NOME*****')
        sleep(0.5)
        print('****************************')
        nome = str(input('R:'))
        if not nome:
            ErroMensager()
            return False
        os.system("cls")
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        print('******DIGITE*SUA*SENHA******')
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        senha = str(input('R:'))
        if not senha:
            ErroMensager()
            return False
        os.system("cls")
        print('****************************')
        sleep(0.5)
        print('**DIGITE*O*NUMERO*DA*CONTA**')
        sleep(0.5)
        print('****************************')
        num_conta = str(input('R:'))
        if not num_conta:
            ErroMensager()
            return False
        os.system("cls")
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        print('*DIGITE*O*NUMERO*DA*AGÊNCIA*')
        sleep(0.5)
        print('****************************')
        num_agencia = str(input('R:'))
        if not num_agencia:
            ErroMensager()
            return False
        sleep(0.5)
        cursor.execute(
            "INSERT INTO Conta (nome, senha, num_conta, num_agencia) VALUES (?, ?, ?, ?)",
            (nome, senha, num_conta, num_agencia)
        )
        conexao.commit()
        conexao.close()
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        print('**CONTA*CRIADA*COM*SUCESSO**')
        sleep(0.5)
        print('****************************')
    except:
        ErroMensager()
        return False


def EntrarConta():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    print('****************************')
    sleep(0.5)
    print('**DIGITE*O*NUMERO*DA*CONTA**')
    sleep(0.5)
    print('****************************')
    sleep(0.5)
    num_conta = str(input('R:'))
    os.system("cls")
    print('****************************')
    sleep(0.5)
    print('******DIGITE*SUA*SENHA******')
    sleep(0.5)
    print('****************************')
    sleep(0.5) 
    senha = str(input('R:'))
    os.system("cls")
    cursor.execute(
        """
            SELECT id, nome FROM Conta
            WHERE num_conta = ?
            AND senha = ?
        """,
        (num_conta, senha)
    )
    try:
        id, nome = cursor.fetchall()[0]
        if id and nome:
            print('****************************')
            sleep(0.5)
            print(f'*BEM VINDO DE VOLTA {nome.upper()}*')
            sleep(0.5)
            print('****************************')
            sleep(0.5)
            return id
        else:
            print('****************************')
            sleep(0.5)
            print('****CONTA*NÃO*ENCONTRADA****')
            sleep(0.5)
            print('****************************')
            sleep(0.5)
            conexao.close()
            return False
    except IndexError:
        print('****************************')
        sleep(0.5)
        print('****CONTA*NÃO*ENCONTRADA****')
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        conexao.close()
        return False


def CriarExtrato(tipo_transacao, valor, conta_id):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    data_hora = datetime.now().strftime("%I:%M - %d/%m/%Y")

    cursor.execute(
        "INSERT INTO Extratos (data_hora, tipo_transacao, valor, conta_id) VALUES (?, ?, ?, ?)",
        (data_hora, tipo_transacao, valor, conta_id)
    )
    conexao.commit()
    conexao.close()


def ConsultarSaldo(id):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT saldo FROM Conta
            WHERE id = ?
        """,
        (id,)
    )
    dados = cursor.fetchall()[0][0]
    conexao.close()
    print('****************************')
    sleep(0.5)
    print(f'***********{dados}***********')
    sleep(0.5)
    print('****************************')
    sleep(0.5)
    return dados


def Saque(id):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT saldo FROM Conta
            WHERE id = ?
        """,
        (id,)
    )
    saldo = cursor.fetchall()[0][0]
    if saldo <= 0:
        print('****************************')
        sleep(0.5)
        print('****SEM*SALDO*SUFICIENTE****')
        sleep(0.5)
        print('****************************')
        return False
    else:
        print('****************************')
        sleep(0.5)
        print('**QUAL*VALOR*DESEJA*SACAR?**')
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        print('****************************')
        sleep(0.5)
        print(f'**********{saldo}**********')
        sleep(0.5)
        print('****************************')
        saque = float(input('R:'))
        os.system("cls")
        if saldo >= saque:
            valor = saldo - saque
            cursor.execute(
                """
                    UPDATE Conta
                    SET saldo = ?
                    WHERE ?;
                """,
                (valor, id)
            )
            conexao.commit()
            conexao.close()
            print('****************************')
            sleep(0.5)
            print('*****SAQUE*BEM*SUCEDIDO*****')
            sleep(0.5)
            print('****************************')

            CriarExtrato('Saque', saque, id)
            return ''


def Deposito(id):
    try:
        conexao = sqlite3.connect("banco.db")
        cursor = conexao.cursor()
        print('****************************')
        sleep(0.5)
        print('QUAL*VALOR*DESEJA*DEPOSITAR?')
        sleep(0.5)
        print('****************************')
        deposito = float(input('R:'))
        cursor.execute(
            """
                SELECT saldo FROM Conta
                WHERE id = ?
            """,
            (id,)
        )

        saldo = cursor.fetchall()[0][0]
        os.system("cls")

        valor = saldo + deposito

        cursor.execute(
        """
            UPDATE Conta
            SET saldo = ?
            WHERE id = ?;
        """,
        (valor, id)
        )
        conexao.commit()
        print('****************************')
        sleep(0.5)
        print('****DEPÓSITO*BEM*SUCEDIDO***')
        sleep(0.5)
        print('****************************')
        return ''
    except ValueError:
        return ErroMensager()


def ConsultarExtrato(id):
    lista_dados = ['ID', 'DATA E HORA', 'TIPO DA TRANSAÇÃO', ]
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()
    cursor.execute(
        """
            SELECT * FROM Extratos
            WHERE conta_id = ?
        """,
        (id,)
    )
    dados = cursor.fetchall()[0]
    for dado in dados:
        if type(dado) == str:
            dado.upper()
        print('****************************')
        sleep(0.5)
        print(f'{dado}')
        sleep(0.5)
        print('****************************')
        sleep(0.5)
    conexao.close()
    return dados


