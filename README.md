# Sistema Bancário

Simulador bancário de terminal feito com Python e SQLite. Crie uma conta fictícia, faça depósitos e saques e consulte o saldo e o histórico de movimentações. Os dados permanecem disponíveis entre execuções.

## Como rodar

Você precisa de Git para clonar o projeto e de Python 3.12 ou superior. O SQLite já vem com o Python, e o projeto usa apenas a biblioteca padrão.

```sh
git clone https://github.com/Kakawm005/sistema-bancario.git
cd sistema-bancario
python main.py
```

Se o comando `python` estiver indisponível, tente `py -3 main.py` no Windows ou `python3 main.py` no macOS e no Linux.

Na primeira execução, o programa cria o arquivo `banco.db` na pasta em que você executou o comando. Use dados fictícios e uma senha exclusiva para esta demonstração.

## Roteiro de demonstração

| Etapa | O que fazer | Resultado esperado |
| --- | --- | --- |
| 1 | Escolha **1. Criar conta**. Informe o nome `Ana Demo`, a senha `demo123`, a conta `1001` e a agência `0001`. | O programa confirma o cadastro. |
| 2 | Escolha **2. Entrar** e informe a conta `1001` e a senha `demo123`. | O menu da conta é exibido. |
| 3 | Escolha **4. Depositar** e informe `100,50`. | O programa confirma o depósito. |
| 4 | Escolha **3. Sacar** e informe `30,25`. | O programa confirma o saque. |
| 5 | Escolha **1. Consultar saldo** e **2. Consultar extrato**. | O saldo é **R$ 70,25** e o extrato mostra as duas movimentações, com a mais recente primeiro. |

Para testar uma operação recusada, tente sacar `100,00` depois da etapa 5. O sistema informa que o saldo é insuficiente e mantém o saldo em **R$ 70,25**.

## Como funciona

- [`main.py`](main.py) inicializa o banco e abre o menu.
- [`db/create_db.py`](db/create_db.py) cria as tabelas de contas e extratos e configura a conexão SQLite.
- [`db/query.py`](db/query.py) implementa cadastro, login e movimentações. As senhas são armazenadas com PBKDF2 e salt individual. Saldo e lançamento de extrato são gravados na mesma transação.
- [`tests/`](tests/) cobre o fluxo de terminal, a persistência, o isolamento entre contas e a validação de operações.

## Testes automatizados

```sh
python -m unittest discover -s tests -v
```

Cada teste usa seu próprio banco temporário. O [workflow de testes](.github/workflows/testes.yml) executa a suíte em Windows e Linux com Python 3.12 e 3.14 a cada push e pull request.
